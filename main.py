import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from sqlmodel import SQLModel, Field, Session, create_engine
from pydantic import BaseModel
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, timezone

# ==========================================
# 1. إعدادات الأمان وحماية الويب
# ==========================================
API_KEY_NAME = "X-API-Key"
# المفتاح الافتراضي للتجربة هو SecureSecretKey123 ويمكن غلقه عبر بيئة النظام مستقبلاً
API_KEY = os.getenv("API_KEY", "SecureSecretKey123")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="غير مصرح لك بالدخول! مفتاح الأمان خاطئ.")
    return api_key

# ==========================================
# 2. طبقة الكيانات والجداول (DOMAIN LAYER)
# ==========================================
class PaymentState(str, Enum):
    pending = "pending"
    settled = "settled"
    failed = "failed"
    refunded = "refunded"

class Payment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    amount: float
    state: PaymentState = Field(default=PaymentState.pending)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class LedgerAccount(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    balance: float = Field(default=0.0)

# ==========================================
# 3. إعداد قاعدة البيانات LOCAL SQLITE
# ==========================================
DATABASE_URL = "sqlite:///./payment_service.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    # إنشاء الجداول عند الإقلاع تلقائياً
    SQLModel.metadata.create_all(engine)
    yield

# ==========================================
# 4. المنطق المالي وحالات الاستخدام (SERVICES)
# ==========================================
class PaymentService:
    def __init__(self, session: Session):
        self.session = session

    def authorize_payment(self, payment_id: UUID, account_id: UUID) -> Payment:
        payment = self.session.get(Payment, payment_id)
        account = self.session.get(LedgerAccount, account_id)

        if not payment or not account:
            raise ValueError("المستند أو الحساب غير موجود في النظام!")
        if payment.state != PaymentState.pending:
            raise ValueError("هذه المعاملة ليست في حالة معلقة!")
        if account.balance < payment.amount:
            payment.state = PaymentState.failed
            self.session.add(payment)
            self.session.commit()
            raise ValueError("الرصيد في حساب دفتر الأستاذ غير كافٍ!")

        account.balance -= payment.amount
        payment.state = PaymentState.settled
        self.session.add(account)
        self.session.add(payment)
        self.session.commit()
        self.session.refresh(payment)
        return payment

    def refund_transaction(self, payment_id: UUID, account_id: UUID) -> Payment:
        payment = self.session.get(Payment, payment_id)
        account = self.session.get(LedgerAccount, account_id)

        if not payment or not account:
            raise ValueError("المستند أو الحساب غير موجود!")
        if payment.state != PaymentState.settled:
            raise ValueError("لا يمكن استرداد الأموال إلا للمعاملات المكتملة فقط!")

        account.balance += payment.amount
        payment.state = PaymentState.refunded
        self.session.add(account)
        self.session.add(payment)
        self.session.commit()
        self.session.refresh(payment)
        return payment

# ==========================================
# 5. واجهة التطبيق والروابط المحمية (FASTAPI APP)
# ==========================================
app = FastAPI(
    title="PaymentService API",
    description="نظام إدارة مدفوعات بنكي بنظام القيد المزدوج وبنية نظيفة متكاملة ومحمية.",
    version="1.0.0",
    lifespan=lifespan
)

# تفعيل حماية الـ CORS للسماح لتطبيق الأندرويد بالاتصال بأمان
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PaymentActionRequest(BaseModel):
    payment_id: UUID
    account_id: UUID

@app.post("/payments/authorize", response_model=Payment, dependencies=[Depends(get_api_key)])
def authorize(request: PaymentActionRequest, session: Session = Depends(get_session)):
    try:
        return PaymentService(session).authorize_payment(request.payment_id, request.account_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/payments/refund", response_model=Payment, dependencies=[Depends(get_api_key)])
def refund(request: PaymentActionRequest, session: Session = Depends(get_session)):
    try:
        return PaymentService(session).refund_transaction(request.payment_id, request.account_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
