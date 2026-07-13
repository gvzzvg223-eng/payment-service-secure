from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="نظام إدارة الرصيد والاشتراكات")

# 🔒 تفعيل الـ CORS لفتح الاتصال بأمان مع موقع React الخاص بك
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# 💾 قاعدة بيانات مؤقتة لتجربة شحن الرصيد والاشتراك
USER_DATABASE = {
    "balance": 0.0,
    "is_premium": False
}

class RechargeRequest(BaseModel):
    amount: float

class SubscribeRequest(BaseModel):
    plan: str

# 1️⃣ مسار جلب الرصيد
@app.get("/balance")
async def get_balance():
    return {"balance": USER_DATABASE["balance"]}

# 2️⃣ مسار الشحن التجريبي
@app.post("/recharge")
async def recharge_balance(request: RechargeRequest):
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="مبلغ الشحن يجب أن يكون أكبر من صفر")
    USER_DATABASE["balance"] += request.amount
    return {"message": "تم الشحن بنجاح", "balance": USER_DATABASE["balance"]}

# 3️⃣ مسار تفعيل الاشتراك
@app.post("/subscribe")
async def subscribe_plan(request: SubscribeRequest):
    cost = 50.0  # تكلفة الاشتراك المميز
    if USER_DATABASE["balance"] < cost:
        raise HTTPException(status_code=400, detail=f"رصيدك غير كافٍ، الاشتراك يتطلب {cost} ﷼")
    USER_DATABASE["balance"] -= cost
    USER_DATABASE["is_premium"] = True
    return {"message": "تم تفعيل الاشتراك بنجاح", "balance": USER_DATABASE["balance"]}
