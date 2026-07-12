import uuid
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel, Field, Session, create_engine, select
from pydantic import BaseModel

# ==========================================
# 1. DOMAIN LAYER & DATABASE SETUP
# ==========================================
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
# Note: connect_args={"check_same_thread": False} is needed for SQLite in FastAPI
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=False)

class Payment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: float
    state: str = Field(default="pending") # States: pending, settled, failed, refunded
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LedgerAccount(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    balance: float = Field(default=0.0)

# ==========================================
# 2. LIFESPAN & APPLICATION INIT
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables automatically on startup
    SQLModel.metadata.create_all(engine)
    yield
    # Cleanup resources if needed

app = FastAPI(title="PaymentService API", version="1.0.4", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 3. SECURITY & DEPENDENCIES
# ==========================================
API_KEY_NAME = "X-API-Key"
API_KEY = "SecureSecretKey123"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )

def get_session():
    with Session(engine) as session:
        yield session

# ==========================================
# 4. API SCHEMAS
# ==========================================
class AuthorizeRequest(BaseModel):
    account_id: uuid.UUID
    amount: float

class RefundRequest(BaseModel):
    payment_id: uuid.UUID

# ==========================================
# 5. INFRASTRUCTURE & CORE ENDPOINTS
# ==========================================

@app.post("/ledger/setup", tags=["Infrastructure"])
def setup_ledger(session: Session = Depends(get_session)):
    """Seed endpoint: Creates a test LedgerAccount with a pre-funded balance of 1000.0."""
    account = LedgerAccount(balance=1000.0)
    session.add(account)
    session.commit()
    session.refresh(account)
    return {
        "message": "Ledger account created successfully", 
        "account_id": account.id, 
        "balance": account.balance
    }

@app.post("/payments/authorize", tags=["Core"])
def authorize_payment(
    req: AuthorizeRequest, 
    session: Session = Depends(get_session),
    api_key: str = Depends(get_api_key)
):
    """Authorizes a payment by deducting the amount from the ledger account."""
    account = session.get(LedgerAccount, req.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    if account.balance < req.amount:
        payment = Payment(amount=req.amount, state="failed")
        session.add(payment)
        session.commit()
        raise HTTPException(status_code=400, detail="Insufficient funds")

    account.balance -= req.amount
    payment = Payment(amount=req.amount, state="settled")
    session.add(account)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    
    return {"message": "Payment authorized successfully", "payment_id": payment.id, "state": payment.state}

@app.post("/payments/refund", tags=["Core"])
def refund_payment(
    req: RefundRequest, 
    session: Session = Depends(get_session),
    api_key: str = Depends(get_api_key)
):
    """Refunds a payment and restores the ledger balance."""
    payment = session.get(Payment, req.payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
        
    if payment.state != "settled":
        raise HTTPException(status_code=400, detail=f"Cannot refund a payment in state: {payment.state}")

    # For simplicity in this architecture, we refund the first available ledger account.
    account = session.exec(select(LedgerAccount)).first()
    if not account:
        raise HTTPException(status_code=500, detail="No ledger account available for refund")

    account.balance += payment.amount
    payment.state = "refunded"
    session.add(account)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    
    return {"message": "Payment refunded successfully", "payment_id": payment.id, "state": payment.state, "new_balance": account.balance}


# ==========================================
# 6. GLOBAL UI LOCALIZATION & THEME ENGINE
# ==========================================
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def serve_dashboard():
    """Serves the App Builder UI merging backend control with frontend visualizations."""
    return """
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PaymentService | App Builder</title>
        <style>
            :root {
                --bg-color: #F8FAFC;
                --text-color: #1E293B;
                --card-bg: #FFFFFF;
                --border-color: #E2E8F0;
                --primary: #3B82F6;
                --primary-hover: #2563EB;
                --success: #10B981;
                --terminal-bg: #0F172A;
                --terminal-text: #34D399;
            }
            .dark {
                --bg-color: #0F172A;
                --text-color: #F1F5F9;
                --card-bg: #1E293B;
                --border-color: #334155;
                --terminal-bg: #000000;
            }
            body {
                background-color: var(--bg-color);
                color: var(--text-color);
                font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;
                margin: 0;
                padding: 0;
                transition: background-color 0.3s, color 0.3s;
            }
            .nav {
                display: flex; justify-content: space-between; align-items: center;
                padding: 1rem 2rem; border-bottom: 1px solid var(--border-color);
                background: var(--card-bg);
            }
            .nav h1 { margin: 0; font-size: 1.25rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
            .btn-group { display: flex; gap: 0.5rem; }
            button {
                background: var(--bg-color); color: var(--text-color);
                border: 1px solid var(--border-color); padding: 0.5rem 1rem;
                border-radius: 0.5rem; cursor: pointer; font-weight: 600;
                transition: all 0.2s;
            }
            button:hover { background: var(--border-color); }
            button.primary { background: var(--primary); color: white; border-color: var(--primary); }
            button.primary:hover { background: var(--primary-hover); }
            
            .container { padding: 2rem; max-width: 1000px; margin: 0 auto; display: grid; gap: 1.5rem; }
            .card {
                background: var(--card-bg); border: 1px solid var(--border-color);
                border-radius: 1rem; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .card h3 { margin-top: 0; font-size: 0.875rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.1em; }
            .terminal {
                background: var(--terminal-bg); color: var(--terminal-text);
                padding: 1rem; border-radius: 0.5rem; font-family: monospace; font-size: 0.875rem;
                height: 250px; overflow-y: auto; margin-top: 1rem;
            }
            .status-dot {
                display: inline-block; width: 8px; height: 8px;
                background-color: var(--success); border-radius: 50%;
                margin-inline-end: 0.5rem;
            }
        </style>
    </head>
    <body>
        <div class="nav">
            <h1 id="title"><span class="status-dot"></span>PaymentService API</h1>
            <div class="btn-group">
                <button onclick="toggleTheme()" id="themeBtn">Dark Mode</button>
                <button onclick="toggleLang()" id="langBtn">عربي</button>
            </div>
        </div>
        
        <div class="container">
            <div class="card">
                <h3 id="panelTitle">Infrastructure Controls</h3>
                <p id="panelDesc" style="font-size: 0.875rem; margin-bottom: 1.5rem; opacity: 0.8;">
                    Initialize the database and spawn a pre-funded test ledger account for authorization testing.
                </p>
                <button class="primary" onclick="setupLedger()" id="setupBtn">Setup Test Ledger</button>
                
                <div class="terminal" id="consoleOutput">
                    > FastAPI server mounted on port 8000.
                    > SQLite Database connected.
                    > SQLModel Lifetime tables verified.
                    > Waiting for infrastructure setup...
                </div>
            </div>
        </div>

        <script>
            let isDark = false;
            let lang = 'en';

            const dictionary = {
                en: {
                    title: "PaymentService API",
                    themeBtn: "Dark Mode",
                    langBtn: "عربي",
                    panelTitle: "Infrastructure Controls",
                    panelDesc: "Initialize the database and spawn a pre-funded test ledger account for authorization testing.",
                    setupBtn: "Setup Test Ledger",
                    consoleInit: "> FastAPI server mounted.\\n> SQLite Database connected.\\n> Waiting for infrastructure setup..."
                },
                ar: {
                    title: "واجهة برمجة تطبيقات خدمة الدفع",
                    themeBtn: "الوضع الداكن",
                    langBtn: "English",
                    panelTitle: "ضوابط البنية التحتية",
                    panelDesc: "قم بتهيئة قاعدة البيانات وإنشاء حساب دفتر أستاذ اختباري مسبق التمويل لاختبار التفويض.",
                    setupBtn: "إعداد دفتر الأستاذ الاختباري",
                    consoleInit: "> خادم FastAPI يعمل.\\n> قاعدة بيانات SQLite متصلة.\\n> في انتظار إعداد البنية التحتية..."
                }
            };

            function updateUI() {
                const isAr = lang === 'ar';
                document.documentElement.dir = isAr ? 'rtl' : 'ltr';
                
                document.getElementById('title').innerHTML = `<span class="status-dot"></span>${dictionary[lang].title}`;
                document.getElementById('themeBtn').innerText = dictionary[lang].themeBtn;
                document.getElementById('langBtn').innerText = dictionary[lang].langBtn;
                document.getElementById('panelTitle').innerText = dictionary[lang].panelTitle;
                document.getElementById('panelDesc').innerText = dictionary[lang].panelDesc;
                document.getElementById('setupBtn').innerText = dictionary[lang].setupBtn;
            }

            function toggleTheme() {
                isDark = !isDark;
                if (isDark) document.body.classList.add('dark');
                else document.body.classList.remove('dark');
                document.getElementById('themeBtn').innerText = isDark ? 
                    (lang === 'ar' ? 'الوضع الفاتح' : 'Light Mode') : 
                    (lang === 'ar' ? 'الوضع الداكن' : 'Dark Mode');
            }

            function toggleLang() {
                lang = lang === 'en' ? 'ar' : 'en';
                updateUI();
                logToConsole(dictionary[lang].consoleInit, true);
            }

            function logToConsole(msg, clear = false) {
                const terminal = document.getElementById('consoleOutput');
                if (clear) terminal.innerText = msg;
                else terminal.innerText += "\\n" + msg;
                terminal.scrollTop = terminal.scrollHeight;
            }

            async function setupLedger() {
                try {
                    const res = await fetch('/ledger/setup', { method: 'POST' });
                    const data = await res.json();
                    
                    if (res.ok) {
                        const successMsg = lang === 'ar' 
                            ? `> نجاح الإعداد!\\n> المعرف: ${data.account_id}\\n> الرصيد: ${data.balance}`
                            : `> Setup Successful!\\n> ID: ${data.account_id}\\n> Balance: ${data.balance}`;
                        logToConsole(successMsg);
                    } else {
                        logToConsole(lang === 'ar' ? '> خطأ في الإعداد.' : '> Error during setup.');
                    }
                } catch (e) {
                    logToConsole(lang === 'ar' ? '> فشل الاتصال بالخادم.' : '> Failed to connect to server.');
                }
            }

            // Initialization
            updateUI();
        </script>
    </body>
    </html>
    """
