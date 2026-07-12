import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# 1. إنشاء تطبيق FastAPI مبسط وسريع جداً لـ Railway
app = FastAPI(title="PaymentService", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. واجهة المستخدم المثبتة بالوضع الداكن لحماية العين
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
            /* خلفية داكنة إجبارية ومريحة للعين تمنع الشاشة البيضاء نهائياً */
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
