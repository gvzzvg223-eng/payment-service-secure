            import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional

# 1. إعدادات الأمان وحماية الويب
API_KEY = os.getenv("API_KEY", "SecureSecretKey123")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(header_value: str = Depends(api_key_header)):
    if header_value == API_KEY:
        return header_value
    raise HTTPException(status_code=403, detail="غير مصرح به / Unauthorized")

# 2. إعدادات قاعدة البيانات (SQLModel)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

class UserAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    balance: float = Field(default=0.0)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# 3. إنشاء تطبيق FastAPI
app = FastAPI(title="PaymentService", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 4. واجهة المستخدم (تثبيت الوضع الداكن المريح وإصلاح الأزرار)
@app.get("/", response_class=HTMLResponse)
async def payment_dashboard():
    html_content = """
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>خدمة الدفع الآمنة | Secure Payment Service</title>
        <style>
            /* تثبيت الخلفية الداكنة المريحة للعين لمنع اللون الأبيض */
            html, body {
                background-color: #121212 !important;
                color: #ffffff !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            body {
                direction: rtl;
            }
            .container {
                width: 90%;
                max-width: 450px;
                background: #1e1e1e;
                padding: 40px 20px;
                border-radius: 16px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.6);
                text-align: center;
                box-sizing: border-box;
            }
            h1 {
                font-size: 24px;
                margin-bottom: 10px;
                color: #ffffff;
            }
            p {
                font-size: 16px;
                color: #b3b3b3;
                margin-bottom: 30px;
                line-height: 1.6;
            }
            .btn-charge {
                background-color: #2da44e;
                color: white;
                border: none;
                padding: 16px 32px;
                font-size: 18px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: bold;
                transition: background-color 0.2s;
                width: 100%;
                box-sizing: border-box;
            }
            .btn-charge:hover { 
                background-color: #2c974b; 
            }
            .lang-switch {
                margin-bottom: 25px;
                cursor: pointer;
                color: #58a6ff;
                font-size: 14px;
                font-weight: 500;
                text-decoration: none;
                display: inline-block;
            }
            .lang-switch:hover {
                text-decoration: underline;
            }
        </style>
        <script>
            function switchLanguage() {
                var title = document.getElementById("title");
                var desc = document.getElementById("desc");
                var btn = document.getElementById("btn");
                var currentLang = document.documentElement.lang;

                if (currentLang === "ar") {
                    document.documentElement.lang = "en";
                    document.body.style.direction = "ltr";
                    title.innerText = "Secure Payment Dashboard";
                    desc.innerText = "Welcome to your financial system. Manage your wallet safely.";
                    btn.innerText = "Charge Account with $1000";
                } else {
                    document.documentElement.lang = "ar";
                    document.body.style.direction = "rtl";
                    title.innerText = "لوحة تحكم الدفع الآمنة";
                    desc.innerText = "مرحباً بك في نظامك المالي المتطور. أدر محفظتك بكل أمان.";
                    btn.innerText = "شحن الحساب بـ 1000$";
                }
            }

            function chargeBalance() {
                alert("تم إرسال طلب الشحن بنجاح! تم إضافة $1000 لمحفظتك الافتراضية.");
            }
        </script>
    </head>
    <body>
        <div class="container">
            <div class="lang-switch" onclick="switchLanguage()">English / العربية</div>
            <h1 id="title">لوحة تحكم الدفع الآمنة</h1>
            <p id="desc">مرحباً بك في نظامك المالي المتطور. أدر محفظتك بكل أمان.</p>
            <button id="btn" class="btn-charge" onclick="chargeBalance()">شحن الحساب بـ 1000$</button>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# 5. العمليات البرمجية (API Endpoints)
@app.post("/api/charge", dependencies=[Depends(get_api_key)])
async def charge_wallet(username: str, session: Session = Depends(get_session)):
    statement = select(UserAccount).where(UserAccount.username == username)
    user = session.exec(statement).first()
    if not user:
        user = UserAccount(username=username, balance=0.0)
        session.add(user)
    user.balance += 1000.0
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "Success", "username": user.username, "new_balance": user.balance}
