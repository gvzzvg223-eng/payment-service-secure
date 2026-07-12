                import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# إنشاء التطبيق السريع لـ Railway
app = FastAPI(
    title="PaymentService", 
    version="1.0",
    docs_url="/dev-testing",  # قمنا بنقل صفحة المطورين البيضاء بعيداً حتى لا تضايق عينك
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# الواجهة الرئيسية الملونة بالكامل بالوضع الداكن المريح للعين
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
            /* إجبار المتصفح على عرض اللون الداكن المريح للعين ومنع اللون الأبيض تماماً */
            html, body {
                background-color: #121212 !important;
                color: #ffffff !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                height: 100vh;
                width: 100vw;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }
            body {
                direction: rtl;
            }
            .container {
                width: 90%;
                max-width: 420px;
                background-color: #1e1e1e !important;
                padding: 40px 20px;
                border-radius: 16px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.6);
                text-align: center;
                box-sizing: border-box;
                border: 1px solid #2d2d2d;
            }
            h1 {
                font-size: 24px;
                margin-bottom: 12px;
                color: #ffffff !important;
            }
            p {
                font-size: 15px;
                color: #b3b3b3 !important;
                margin-bottom: 30px;
                line-height: 1.6;
            }
            .btn-charge {
                background-color: #2da44e !important;
                color: #ffffff !important;
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
                background-color: #2c974b !important; 
            }
            .lang-switch {
                margin-bottom: 25px;
                cursor: pointer;
                color: #58a6ff !important;
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
