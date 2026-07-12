import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PaymentService_Global", 
    version="3.0",
    docs_url="/dev-testing",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PaymentService_Global", "version": "3.0"}

@app.get("/", response_class=HTMLResponse)
async def payment_dashboard():
    # تم إصلاح السلسلة النصية وإزالة أي تعارض في العلامات المسببة للانهيار
    html_content = """<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوابة الدفع العالمية الآمنة</title>
    <style>
        html, body {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        body { direction: rtl; padding: 20px; box-sizing: border-box; }
        .container {
            width: 100%;
            max-width: 420px;
            background-color: #161b22 !important;
            padding: 30px 20px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            text-align: center;
            box-sizing: border-box;
            border: 1px solid #30363d;
        }
        h1 { font-size: 22px; margin-bottom: 8px; color: #ffffff !important; }
        p { font-size: 14px; color: #8b949e !important; margin-bottom: 25px; line-height: 1.5; }
        .section-title {
            font-size: 14px;
            color: #58a6ff;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 20px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .btn-charge {
            background-color: #238636 !important;
            color: #ffffff !important;
            border: none;
            padding: 14px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
            box-sizing: border-box;
            transition: 0.2s;
        }
        .btn-charge:hover { background-color: #2ea043 !important; }
        .premium-box {
            background-color: #21262d;
            border: 1px dashed #30363d;
            border-radius: 10px;
            padding: 15px;
            margin-top: 25px;
            text-align: center;
        }
        .price-tag {
            font-size: 24px;
            color: #58a6ff;
            font-weight: bold;
            margin: 10px 0;
        }
        .btn-subscribe {
            background-color: #1f6feb !important;
            color: white !important;
            border: none;
            padding: 12px;
            font-size: 15px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
            transition: 0.2s;
        }
        .btn-subscribe:hover { background-color: #388bfd !important; }
        .lang-container {
            margin-bottom: 25px;
            display: flex;
            justify-content: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .lang-btn {
            background: #21262d;
            border: 1px solid #30363d;
            color: #c9d1d9;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
        }
        .lang-btn:hover { background: #30363d; color: #58a6ff; }
    </style>
    <script>
        const translations = {
            ar: {
                dir: "rtl",
                title: "بوابة الدفع العالمية الآمنة",
                desc: "أدوات برمجية مؤتمتة بالكامل للمطورين وأصحاب المتاجر حول العالم.",
                sec1: "⚡ فحص تجريبي مجاني",
                btn: "شحن محفظة افتراضية بـ 1000$",
                sec2: "💰 رخصة الاستخدام التجاري",
                p_desc: "احصل على صلاحية الربط الكاملة لموقعك أو متجرك الحقيقي.",
                p_price: "$5 / شهرياً",
                p_btn: "اشترك تلقائياً ($5 / شهرياً)",
                alert_charge: "تمت محاكاة العملية بنجاح! تم إضافة $1000 للحساب التجريبي.",
                alert_sub: "سيتم توجيهك الآن إلى بوابة الدفع الآمنة لتفعيل حسابك تلقائياً!"
            },
            en: {
                dir: "ltr",
                title: "Global Secure Payment Engine",
                desc: "Automated backend tools for developers and stores worldwide.",
                sec1: "⚡ Free Sandbox Test",
                btn: "Simulate $1000 Wallet Charge",
                sec2: "💰 Commercial Licensing",
                p_desc: "Get full API access for your commercial website or app.",
                p_price: "$5 / Monthly",
                p_btn: "Subscribe Automatically ($5 / mo)",
                alert_charge: "Simulation successful! $1000 added to demo account.",
                alert_sub: "Smart System: Redirecting to secure portal to activate your subscription!"
            }
        };

        let currentLang = "ar";

        function changeLanguage(lang) {
            currentLang = lang;
            const data = translations[lang];
            document.body.dir = data.dir;
            document.getElementById("main-title").innerText = data.title;
            document.getElementById("main-desc").innerText = data.desc;
            document.getElementById("sec1-title").innerText = data.sec1;
            document.getElementById("btn-charge").innerText = data.btn;
            document.getElementById("sec2-title").innerText = data.sec2;
            document.getElementById("premium-desc").innerText = data.p_desc;
            document.getElementById("price-tag").innerText = data.p_price;
            document.getElementById("btn-subscribe").innerText = data.p_btn;
        }

        function handleCharge() {
            alert(translations[currentLang].alert_charge);
        }

        function handleSubscribe() {
            alert(translations[currentLang].alert_sub);
        }
    </script>
</head>
<body>
    <div class="container">
        <div class="lang-container">
            <button class="lang-btn" onclick="changeLanguage('ar')">العربية 🇸🇦</button>
            <button class="lang-btn" onclick="changeLanguage('en')">English 🇬🇧</button>
        </div>
        <h1 id="main-title">بوابة الدفع العالمية الآمنة</h1>
        <p id="main-desc">أدوات برمجية مؤتمتة بالكامل للمطورين وأصحاب المتاجر حول العالم.</p>
        <div class="section-title" id="sec1-title">⚡ فحص تجريبي مجاني</div>
        <button class="btn-charge" id="btn-charge" onclick="handleCharge()">شحن محفظة افتراضية بـ 1000$</button>
        <div class="premium-box">
            <div class="section-title" style="margin-top:0;" id="sec2-title">💰 رخصة الاستخدام التجاري</div>
            <div id="premium-desc">احصل على صلاحية الربط الكاملة لموقعك أو متجرك الحقيقي.</div>
            <div class="price-tag" id="price-tag">$5 / شهرياً</div>
            <button class="btn-subscribe" id="btn-subscribe" onclick="handleSubscribe()">اشترك تلقائياً ($5 / شهرياً)</button>
        </div>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html_content)
