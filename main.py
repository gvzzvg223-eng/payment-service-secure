import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

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

# ✅ تحسين: إضافة مسار للتحقق من صحة الخدمة (Health Check)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PaymentService_Global", "version": "3.0"}

@app.get("/", response_class=HTMLResponse)
async def payment_dashboard():
    html_content = """
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>بوابة الدفع العالمية الآمنة | Global Secure Payment Gateway</title>
        <style>
            /* خلفية داكنة إجبارية وعميقة مريحة جداً لعين المطورين */
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
                max-width: 480px;
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

            /* صندوق اختيار اللغات العالمية */
            .lang-container {
                margin-bottom: 20px;
                display: flex;
                justify-content: center;
                gap: 10px;
                flex-wrap: wrap;
            }
            .lang-btn {
                background: #21262d;
                border: 1px solid #30363d;
                color: #58a6ff;
                padding: 5px 10px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 12px;
            }
            .lang-btn:hover { background: #30363d; }
        </style>
        <script>
            // قاموس اللغات العالمية لتغيير النصوص فورياً وبذكاء
            const translations = {
                ar: {
                    dir: "rtl",
                    title: "بوابة الدفع العالمية الآمنة",
                    desc: "أدوات برمجية مؤتمتة بالكامل للمطورين وأصحاب المتاجر حول العالم.",
                    sec1: "⚡ فحص تجريبي مجاني",
                    btn: "شحن محفظة افتراضية بـ 1000$",
                    sec2: "💰 رخصة الاستخدام التجاري",
                    p_desc: "احصل على صلاحية الربط الكاملة لموقعك أو متجرك الحقيقي.",
                    p_btn: "اشترك تلقائياً (5$ / شهرياً)",
                    alert_charge: "تمت محاكاة العملية بنجاح! تم إنشاء مفتاح تشفير مالي وإضافة \$1000 للحساب التجريبي.",
                    alert_sub: "نظام ذكي: سيتم توجيهك الآن إلى بوابة الدفع الآمنة لاستلام اشتراكك وتفعيل حسابك تلقائياً دون تدخل بشري!"
                },
                en: {
                    dir: "ltr",
                    title: "Global Secure Payment Engine",
                    desc: "Automated backend tools for developers and stores worldwide.",
                    sec1: "⚡ Free Sandbox Test",
                    btn: "Simulate \$1000 Wallet Charge",
                    sec2: "💰 Commercial Licensing",
                    p_desc: "Get full API access for your commercial website or app.",
                    p_btn: "Subscribe Automatically (\$5/mo)",
                    alert_charge: "Simulation successful! Financial crypto-key generated and \$1000 added to demo account.",
                    alert_sub: "Smart System: Redirecting to secure portal to activate your subscription automatically!"
                },
                es: {
                    dir: "ltr",
                    title: "Pasarela de Pago Segura Global",
                    desc: "Herramientas automatizadas para desarrolladores y tiendas del mundo.",
                    sec1: "⚡ Prueba Gratuita de Sandbox",
                    btn: "Simular Carga de Billetera de \$1000",
                    sec2: "💰 Licencia Comercial",
                    p_desc: "Obtenga acceso completo a la API para su sitio web comercial.",
                    p_btn: "Suscribirse Automáticamente (\$5/mes)",
                    alert_charge: "¡Simulación exitosa! Llave criptográfica generada y \$1000 añadidos.",
                    alert_sub: "Sistema Inteligente: ¡Redirigiendo para activar su suscripción automáticamente!"
                },
                fr: {
                    dir: "ltr",
                    title: "Passerelle de Paiement Sécurisée Globale",
                    desc: "Outils backend automatisés pour les développeurs et boutiques du monde.",
                    sec1: "⚡ Test Sandbox Gratuit",
                    btn: "Simuler un Chargement de Portefeuille de 1000$",
                    sec2: "💰 Licence Commerciale",
                    p_desc: "Obtenez un accès API complet pour votre site web commercial.",
                    p_btn: "S'abonner Automatiquement (5$/mois)",
                    alert_charge: "Simulation réussie ! Clé crypto générée et 1000$ ajoutés au compte démo.",
                    alert_sub: "Système Intelligent : Redirection pour activer votre abonnement automatiquement !"
                }
            };

            let currentLang = "ar";

            function changeLanguage(lang) {
                currentLang = lang;
                const data = translations[lang];
                
                document.documentElement.lang = lang;
                document.body.style.direction = data.dir;
                
                document.getElementById("title").innerText = data.title;
                document.getElementById("desc").innerText = data.desc;
                document.getElementById("sec1").innerText = data.sec1;
                document.getElementById("btn").innerText = data.btn;
                document.getElementById("sec2").innerText = data.sec2;
                document.getElementById("p_desc").innerText = data.p_desc;
                document.getElementById("p_btn").innerText = data.p_btn;
            }

            function chargeBalance() {
                alert(translations[currentLang].alert_charge);
            }

            function triggerSubscription() {
                alert(translations[currentLang].alert_sub);
            }
        </script>
    </head>
    <body>
        <div class="container">
            <!-- أزرار اختيار اللغات العالمية -->
            <div class="lang-container">
                <button class="lang-btn" onclick="changeLanguage('ar')">العربية 🇸🇦</button>
                <button class="lang-btn" onclick="changeLanguage('en')">English 🇺🇸</button>
                <button class="lang-btn" onclick="changeLanguage('es')">Español 🇪🇸</button>
                <button class="lang-btn" onclick="changeLanguage('fr')">Français 🇫🇷</button>
            </div>
            
            <h1 id="title">بوابة الدفع العالمية الآمنة</h1>
            <p id="desc">أدوات برمجية مؤتمتة بالكامل للمطورين وأصحاب المتاجر حول العالم.</p>
            
            <div class="section-title" id="sec1">⚡ فحص تجريبي مجاني</div>
            <button id="btn" class="btn-charge" onclick="chargeBalance()">شحن محفظة افتراضية بـ 1000$</button>
            
            <div class="premium-box">
                <div class="section-title" id="sec2" style="margin-top:0; color:#ff7b72;">💰 رخصة الاستخدام التجاري</div>
                <p id="p_desc" style="margin-bottom:10px; font-size:13px;">احصل على صلاحية الربط الكاملة لموقعك أو متجرك الحقيقي.</p>
                <div class="price-tag">\$5 <span style="font-size:14px; color:#8b949e;">/ شهرياً</span></div>
                <button id="p_btn" class="btn-subscribe" onclick="triggerSubscription()">اشترك تلقائياً (5$ / شهرياً)</button>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
