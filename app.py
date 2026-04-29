from flask import Flask, render_template_string, request, session, redirect, url_for, send_file
import requests


TELEGRAM_TOKEN = "8559600899:AAHBgTVCNdED5fetBmnPNs9KOh78rYt5yxo"
CHAT_ID = "8475921354"
import csv
from datetime import datetime
import os


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


app = Flask(__name__)
app.secret_key = "trustwatch_secret_key"
# ================= ALERT STORAGE =================
alert_history = []


# ================= ANALYSIS ENGINE =================
def send_telegram_alert(user, reason):
    url = f"https://api.telegram.org/bot8559600899:AAHBgTVCNdED5fetBmnPNs9KOh78rYt5yxo/sendMessage"


    message = f"""
🚨 HIGH RISK ALERT DETECTED


👤 User: {user['name']}
📍 Location: {user['location']}
💻 Device: {user.get('device','Unknown')}
⚠️ Activity: {user['activity']}
📊 Score: {user['score']}


🧠 AI Analysis:
{reason}


🛠 Suggested Action:
- Reset password
- Block suspicious login
- Verify identity
"""


    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })


def generate_analysis(name, location, device="Unknown", activity="Login"):
    score = 0
    loc = location.lower()


    if loc in ["unknown", "vpn", "foreign", ""]:
        score += 30
    if "failed" in activity.lower():
        score += 40
    if "download" in activity.lower():
        score += 25
    if "large" in activity.lower():
        score += 20


    if len(name) % 2 == 0:
        score += 10


    if score >= 75:
        risk = "High"
    elif score >= 45:
        risk = "Medium"
    else:
        risk = "Low"


    return {
        "name": name,
        "location": location,
        "device": device,
        "activity": activity,
        "score": score,
        "risk": risk,
        "time": datetime.now().strftime("%H:%M:%S")
    }
# ================= HIGH RISK SUMMARY =================
def generate_summary(user):
    reasons = []


    if "failed" in user["activity"].lower():
        reasons.append("multiple failed logins")


    if user["location"].lower() in ["vpn", "unknown", "foreign", "usa", "uk", "dubai", "sri lanka"]:
        reasons.append("suspicious location")


    if "download" in user["activity"].lower():
        reasons.append("unusual data download")


    if not reasons:
        return "General suspicious behavior detected."


    return "Possible threat due to " + ", ".join(reasons) + "."


# ================= THREAT + SOLUTION ENGINE =================
def get_threats_and_solutions(user):
    threats = []
    solutions = []


    if "failed" in user["activity"].lower():
        threats.append("Multiple Failed Login Attempts")
        solutions.append("Enable account lockout policy and multi-factor authentication.")


    if user["location"].lower() in ["vpn", "unknown", "foreign", "usa", "uk", "dubai", "sri lanka"]:
        threats.append("Suspicious Login Location")
        solutions.append("Restrict login from unknown regions and enable geo-blocking.")


    if "download" in user["activity"].lower():
        threats.append("Unusual Data Download Activity")
        solutions.append("Monitor file access and apply data loss prevention policies.")


    if not threats:
        threats.append("General Suspicious Behavior")
        solutions.append("Monitor user activity closely.")


    return threats, solutions


# ================= AI AGENT =================
def ai_soc_agent(question, logs):
    question = question.lower()


    high = [l for l in logs if l["risk"] == "High"]
    medium = [l for l in logs if l["risk"] == "Medium"]


    # Basic intelligence responses
    if "high risk" in question:
        return f"There are {len(high)} high risk users. These users may have suspicious activities like failed logins or unusual locations."


    if "who is risky" in question or "critical" in question:
        return "High risk users: " + ", ".join([l["name"] for l in high]) if high else "No critical users found."


    if "location" in question:
        return "Some users are logging in from unusual locations like VPN/foreign regions which may indicate compromise."


    if "why" in question:
        return "Risk is calculated based on failed logins, suspicious locations, downloads, and abnormal behavior patterns."


    if "safe" in question:
        return "Low risk users are considered safe. Medium risk users should be monitored."


    if "breach" in question:
        return "Possible breach indicators include: multiple failed logins, foreign/VPN access, and large data downloads."


    # Default smart summary
    return f"""
SOC Summary:
- High Risk: {len(high)}
- Medium Risk: {len(medium)}


Advice:
Investigate high-risk users immediately. Monitor medium-risk users for unusual activity.
"""
# ================= PDF GENERATOR =================
def generate_pdf(logs):
    file_path = "TrustWatch_Report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []


    content.append(Paragraph("TrustWatch AI - SOC SECURITY REPORT", styles["Title"]))
    content.append(Spacer(1, 12))


    high = len([l for l in logs if l["risk"] == "High"])
    medium = len([l for l in logs if l["risk"] == "Medium"])
    low = len([l for l in logs if l["risk"] == "Low"])


    content.append(Paragraph(f"High Risk Users: {high}", styles["Normal"]))
    content.append(Paragraph(f"Medium Risk Users: {medium}", styles["Normal"]))
    content.append(Paragraph(f"Low Risk Users: {low}", styles["Normal"]))
    content.append(Spacer(1, 12))


    content.append(Paragraph("CRITICAL USERS", styles["Heading2"]))
    for l in logs:
        if l["risk"] == "High":
            content.append(Paragraph(f"{l['name']} | {l['location']} | {l['activity']} | HIGH RISK", styles["Normal"]))


    content.append(Spacer(1, 12))


    content.append(Paragraph("LOCATION SUMMARY", styles["Heading2"]))
    for l in logs:
        content.append(Paragraph(f"{l['name']} logged in from {l['location']} at {l['time']}", styles["Normal"]))


    doc.build(content)
    return file_path


# ================= HIGH RISK PDF REPORT =================
def generate_high_risk_pdf(logs):
    file_path = "High_Risk_Report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []


    content.append(Paragraph("HIGH RISK SECURITY REPORT", styles["Title"]))
    content.append(Spacer(1, 12))


    for l in logs:
        if l["risk"] == "High":
            threats, solutions = get_threats_and_solutions(l)


            content.append(Paragraph(f"User: {l['name']}", styles["Heading2"]))
            content.append(Paragraph(f"Location: {l['location']}", styles["Normal"]))
            content.append(Paragraph(f"Activity: {l['activity']}", styles["Normal"]))
            content.append(Paragraph(f"Risk Score: {l['score']}", styles["Normal"]))


            content.append(Spacer(1, 8))
            content.append(Paragraph("Threats:", styles["Heading3"]))
            for t in threats:
                content.append(Paragraph(f"- {t}", styles["Normal"]))


            content.append(Spacer(1, 8))
            content.append(Paragraph("Solutions:", styles["Heading3"]))
            for s in solutions:
                content.append(Paragraph(f"- {s}", styles["Normal"]))


            content.append(Spacer(1, 20))


    doc.build(content)
    return file_path


# ================= HOME PAGE =================
HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>TrustWatch AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
    --bg:#04070d;
    --bg-2:#07111f;
    --panel:rgba(7,16,28,0.78);
    --panel-solid:#0a1422;
    --panel-2:rgba(13,24,40,0.9);
    --line:rgba(72, 196, 255, 0.14);
    --line-strong:rgba(54, 208, 255, 0.38);
    --text:#d9f3ff;
    --muted:#7ea0b8;
    --cyan:#31d7ff;
    --cyan-2:#7ef9ff;
    --green:#22c55e;
    --red:#ff4d6d;
    --yellow:#facc15;
    --violet:#6d5efc;
    --shadow:0 0 0 1px rgba(49,215,255,0.06), 0 12px 40px rgba(0,0,0,0.45), 0 0 28px rgba(49,215,255,0.08);
    --radius:18px;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
    margin:0;
    font-family:'Inter', Arial, sans-serif;
    background:
        radial-gradient(circle at top right, rgba(49,215,255,0.10), transparent 24%),
        radial-gradient(circle at bottom left, rgba(109,94,252,0.10), transparent 20%),
        linear-gradient(135deg, #03060b 0%, #06101c 55%, #03060b 100%);
    color:var(--text);
    min-height:100vh;
    overflow-x:hidden;
}
body::before{
    content:"";
    position:fixed;
    inset:0;
    background-image:
        linear-gradient(rgba(60,120,180,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(60,120,180,0.08) 1px, transparent 1px);
    background-size:48px 48px;
    mask-image:linear-gradient(to bottom, rgba(255,255,255,0.55), rgba(255,255,255,0.18));
    pointer-events:none;
}
body::after{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    background:
        linear-gradient(transparent 0%, rgba(0,255,255,0.02) 50%, transparent 100%);
    animation:scan 8s linear infinite;
}
@keyframes scan{
    0%{transform:translateY(-100%);}
    100%{transform:translateY(100%);}
}
a{text-decoration:none;}
.header{
    position:sticky;
    top:0;
    z-index:10;
    backdrop-filter:blur(14px);
    background:rgba(3,8,14,0.72);
    border-bottom:1px solid var(--line);
    padding:18px 28px;
}
.header-row{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:16px;
    flex-wrap:wrap;
}
.brand{
    display:flex;
    align-items:center;
    gap:14px;
}
.logo{
    width:46px;
    height:46px;
    border-radius:14px;
    display:grid;
    place-items:center;
    background:
        radial-gradient(circle at 30% 30%, rgba(126,249,255,0.45), rgba(49,215,255,0.12) 42%, rgba(49,215,255,0.04) 70%),
        rgba(8,18,30,0.95);
    border:1px solid rgba(126,249,255,0.22);
    box-shadow:0 0 24px rgba(49,215,255,0.15);
    font-size:20px;
}
.brand h1{
    margin:0;
    font-family:'Orbitron', sans-serif;
    font-size:clamp(1.2rem, 2vw, 1.8rem);
    letter-spacing:1px;
}
.brand p{
    margin:4px 0 0 0;
    color:var(--muted);
    font-size:13px;
}
.status-strip{
    display:flex;
    gap:10px;
    flex-wrap:wrap;
}
.pill{
    padding:8px 12px;
    border:1px solid var(--line);
    border-radius:999px;
    background:rgba(10,22,36,0.7);
    color:var(--muted);
    font-size:12px;
    letter-spacing:.4px;
}
.pill b{color:var(--cyan-2);}
.container{
    width:min(1180px, calc(100% - 32px));
    margin:28px auto 120px;
}
.hero{
    display:grid;
    grid-template-columns:1.35fr .85fr;
    gap:20px;
    margin-bottom:22px;
}
.panel{
    background:var(--panel);
    border:1px solid var(--line);
    border-radius:var(--radius);
    box-shadow:var(--shadow);
    backdrop-filter:blur(10px);
}
.hero-main{
    padding:28px;
    position:relative;
    overflow:hidden;
}
.hero-main::before{
    content:"";
    position:absolute;
    inset:auto -40px -60px auto;
    width:220px;
    height:220px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(49,215,255,0.18), transparent 62%);
}
.eyebrow{
    display:inline-flex;
    align-items:center;
    gap:8px;
    color:var(--cyan-2);
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:1.6px;
    margin-bottom:14px;
}
.hero-main h2{
    margin:0 0 10px 0;
    font-family:'Orbitron', sans-serif;
    font-size:clamp(1.8rem, 4vw, 3rem);
    line-height:1.1;
}
.hero-main p{
    margin:0;
    color:var(--muted);
    max-width:60ch;
    line-height:1.7;
}
.hero-stats{
    margin-top:22px;
    display:grid;
    grid-template-columns:repeat(3, 1fr);
    gap:14px;
}
.stat{
    padding:16px;
    border-radius:16px;
    border:1px solid rgba(49,215,255,0.10);
    background:linear-gradient(180deg, rgba(10,24,40,0.8), rgba(7,15,25,0.72));
}
.stat .label{
    color:var(--muted);
    font-size:12px;
    margin-bottom:8px;
    text-transform:uppercase;
    letter-spacing:1px;
}
.stat .value{
    font-size:1.4rem;
    font-weight:700;
    color:var(--text);
}
.side-panel{
    padding:24px;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
}
.side-panel h3{
    margin:0 0 8px 0;
    font-family:'Orbitron', sans-serif;
    font-size:1rem;
}
.side-panel p{
    margin:0;
    color:var(--muted);
    line-height:1.6;
}
.live-box{
    margin-top:18px;
    padding:16px;
    border-radius:16px;
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(126,249,255,0.14);
}
.live-dot{
    width:10px;
    height:10px;
    border-radius:50%;
    background:#22c55e;
    box-shadow:0 0 12px #22c55e;
    display:inline-block;
    margin-right:8px;
}
.grid{
    display:grid;
    grid-template-columns:1.05fr .95fr;
    gap:20px;
}
.card{
    background:var(--panel);
    border:1px solid var(--line);
    padding:24px;
    border-radius:var(--radius);
    margin-bottom:18px;
    box-shadow:var(--shadow);
    backdrop-filter:blur(10px);
    position:relative;
    overflow:hidden;
}
.card::after{
    content:"";
    position:absolute;
    inset:0;
    border-radius:inherit;
    padding:1px;
    background:linear-gradient(135deg, rgba(126,249,255,0.20), transparent 30%, transparent 70%, rgba(109,94,252,0.18));
    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
    -webkit-mask-composite:xor;
            mask-composite:exclude;
    pointer-events:none;
}
.card h3{
    margin:0 0 14px 0;
    font-family:'Orbitron', sans-serif;
    font-size:1rem;
    letter-spacing:.6px;
}
.card p{
    color:var(--muted);
    line-height:1.65;
}
.upload-box{
    display:grid;
    gap:16px;
}
input[type="file"]{
    width:100%;
    padding:16px;
    border-radius:14px;
    border:1px dashed rgba(126,249,255,0.32);
    background:rgba(2,10,18,0.65);
    color:var(--muted);
}
button{
    background:linear-gradient(135deg, rgba(10,28,44,0.95), rgba(6,18,28,0.95));
    color:var(--cyan-2);
    border:1px solid rgba(49,215,255,0.24);
    padding:12px 16px;
    border-radius:12px;
    cursor:pointer;
    font-weight:600;
    letter-spacing:.3px;
    transition:.25s ease;
    box-shadow:0 0 0 rgba(0,0,0,0);
}
button:hover{
    transform:translateY(-1px);
    background:linear-gradient(135deg, rgba(18,62,88,0.95), rgba(10,28,44,0.95));
    color:white;
    box-shadow:0 10px 24px rgba(49,215,255,0.12);
}
.dashboard-grid{
    display:grid;
    grid-template-columns:repeat(2, minmax(0, 1fr));
    gap:14px;
}
.dashboard-link button{
    width:100%;
    min-height:78px;
    text-align:left;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:10px;
    padding:16px 18px;
}
.dashboard-link span{
    display:block;
}
.dashboard-link .small{
    color:var(--muted);
    font-size:12px;
    margin-top:4px;
    font-weight:400;
}
.success{color:#22c55e;font-weight:700;}
.error{color:#ff6b81;font-weight:700;}
.red{color:#ff4d6d;}
.green{color:#22c55e;}
.yellow{color:#facc15;}
.blue{color:#31d7ff;}
.float-left,
.float-right{
    position:fixed;
    bottom:20px;
    z-index:999;
}
.float-left{left:20px;}
.float-right{right:20px; display:flex; gap:12px; flex-wrap:wrap; justify-content:flex-end;}
.fab-danger{
    background:linear-gradient(135deg, rgba(126,14,32,0.96), rgba(62,8,17,0.96));
    color:white;
    border:1px solid rgba(255,77,109,0.35);
    border-radius:999px;
    padding:14px 18px;
    box-shadow:0 10px 30px rgba(255,77,109,0.18);
}
.fab-danger:hover{
    background:linear-gradient(135deg, rgba(180,22,51,0.96), rgba(88,12,24,0.96));
}
.log-presence{
    margin-top:14px;
    display:flex;
    align-items:center;
    gap:10px;
    color:var(--muted);
    font-size:14px;
}
.empty-note{
    margin-top:10px;
    color:var(--muted);
}
@media (max-width: 980px){
    .hero,.grid{grid-template-columns:1fr;}
}
@media (max-width: 700px){
    .hero-stats,.dashboard-grid{grid-template-columns:1fr;}
    .container{width:min(100% - 20px, 1180px);}
    .header{padding:16px;}
    .hero-main,.side-panel,.card{padding:18px;}
    .float-right{left:20px; right:20px; bottom:84px; justify-content:stretch;}
    .float-right a{flex:1;}
    .float-right button{width:100%;}
}
</style>
</head>
<body>


<div class="header">
    <div class="header-row">
        <div class="brand">
            <div class="logo">🛡</div>
            <div>
                <h1>TrustWatch AI SOC Platform</h1>
                <p>Cyber defense command center • Live threat visibility • Intelligent response</p>
            </div>
        </div>
        <div class="status-strip">
            <div class="pill"><b>MODE</b> • ACTIVE MONITORING</div>
            <div class="pill"><b>GRID</b> • SECURE NETWORK</div>
            <div class="pill"><b>STATUS</b> • LIVE UI</div>
        </div>
    </div>
</div>


<div class="container">

    <section class="hero">
        <div class="panel hero-main">
            <div class="eyebrow">● Cybersecurity Intelligence Layer</div>
            <h2>Creative SOC interface with high-visibility threat control.</h2>
            <p>Upload your log data, enter the control grid, and open dashboards only when you choose. Nothing sensitive appears automatically until the related dashboard is clicked.</p>

            <div class="hero-stats">
                <div class="stat">
                    <div class="label">Threat State</div>
                    <div class="value">{% if logs %}Armed{% else %}Standby{% endif %}</div>
                </div>
                <div class="stat">
                    <div class="label">Dataset</div>
                    <div class="value">{% if logs %}{{ logs|length }} Logs{% else %}0 Logs{% endif %}</div>
                </div>
                <div class="stat">
                    <div class="label">Total Risk</div>
                    <div class="value">
                        {% if logs %}
                            {% set ns = namespace(total=0) %}
                            {% for log in logs %}
                                {% set ns.total = ns.total + log.score %}
                            {% endfor %}
                            {{ ns.total }}
                        {% else %}
                            0
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>

        <div class="panel side-panel">
            <div>
                <h3>Live Defense Feed</h3>
                <p>This interface is redesigned to feel like a modern security operations center, with layered glass panels, glowing controls, and modular command cards.</p>
                <div class="live-box">
                    <div><span class="live-dot"></span><strong>Realtime Status:</strong> visual system online</div>
                    <p style="margin-top:10px;">All dashboard data remains closed until the operator explicitly opens the corresponding module.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="grid">
        <div>
            <div class="card">
                <h3>Upload Threat Log CSV</h3>
                <form method="POST" enctype="multipart/form-data" class="upload-box">
                    <input type="file" name="file" required>
                    <button type="submit">Analyze Security Log</button>
                </form>

                {% if message %}
                <p class="{{ msg_type }}" style="margin-top:14px;">{{ message }}</p>
                {% endif %}

                <div class="log-presence">
                    <span class="live-dot" style="background:{% if logs %}#22c55e{% else %}#facc15{% endif %}; box-shadow:0 0 12px {% if logs %}#22c55e{% else %}#facc15{% endif %};"></span>
                    {% if logs %}
                    <span>Log intelligence loaded and ready for dashboard access.</span>
                    {% else %}
                    <span>No uploaded security intelligence yet.</span>
                    {% endif %}
                </div>
            </div>
        </div>

        <div>
            <div class="card">
                <h3>Mission Brief</h3>
                <p>Access modules only when required. This keeps the interface cleaner, reduces cognitive overload, and ensures no dashboard information is shown before operator interaction.</p>
            </div>
        </div>
    </section>

    <div class="card">
        <h3>🛡 SOC Control Panel</h3>
        <p style="margin-bottom:16px;">Open a module to reveal its live dashboard. No panel preloads visible analytics or data until clicked.</p>

        <div class="dashboard-grid">
            <a class="dashboard-link" href="/graphs">
                <button>
                    <span>
                        📊 Threat Analytics
                        <span class="small">Charts and security trend intelligence</span>
                    </span>
                    <span>↗</span>
                </button>
            </a>

            <a class="dashboard-link" href="/admin">
                <button>
                    <span>
                        🚨 Security Monitoring
                        <span class="small">Critical, breach, and file access panels</span>
                    </span>
                    <span>↗</span>
                </button>
            </a>

            <a class="dashboard-link" href="/location-warning">
                <button>
                    <span>
                        📍 Geo Intelligence
                        <span class="small">Suspicious region and location activity</span>
                    </span>
                    <span>↗</span>
                </button>
            </a>

            <a class="dashboard-link" href="/high-risk-dashboard">
                <button>
                    <span>
                        🔥 High Risk Users
                        <span class="small">Critical users with attack summaries</span>
                    </span>
                    <span>↗</span>
                </button>
            </a>

            <a class="dashboard-link" href="/ai-agent">
                <button>
                    <span>
                        🧠 AI Assistant
                        <span class="small">Ask about threats, users, and anomalies</span>
                    </span>
                    <span>↗</span>
                </button>
            </a>
        </div>

        {% if not logs %}
        <p class="empty-note">Dashboards are available, but their insights will remain empty until a CSV log is uploaded.</p>
        {% endif %}
    </div>
</div>


<a href="/reset" class="float-left" onclick="return confirm('Are you sure you want to reset all data?')">
    <button class="fab-danger">🔄 Reset All Data</button>
</a>


{% if logs %}
<div class="float-right">
    <a href="/download-report">
        <button class="fab-danger">📄 Download Report</button>
    </a>

    <a href="/download-high-risk-report">
        <button class="fab-danger"
        onmouseover="this.style.filter='brightness(1.08)'"
        onmouseout="this.style.filter='brightness(1)'">
        🚨 High Risk Report
        </button>
    </a>
</div>
{% endif %}


</body>
</html>
"""


# ================= GRAPHS =================
GRAPH_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Graphs</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
    --bg:#04070d;
    --panel:rgba(7,16,28,0.82);
    --line:rgba(72,196,255,.16);
    --line-strong:rgba(72,196,255,.32);
    --text:#d9f3ff;
    --muted:#87a7bd;
    --cyan:#31d7ff;
    --green:#22c55e;
    --red:#ff4d6d;
    --yellow:#facc15;
    --shadow:0 0 0 1px rgba(49,215,255,0.06), 0 12px 40px rgba(0,0,0,0.45), 0 0 30px rgba(49,215,255,0.08);
}
*{box-sizing:border-box;}
body{
    margin:0;
    font-family:'Inter', sans-serif;
    color:var(--text);
    background:
        radial-gradient(circle at top right, rgba(49,215,255,0.10), transparent 24%),
        linear-gradient(135deg, #03060b 0%, #06101c 55%, #03060b 100%);
    min-height:100vh;
}
body::before{
    content:"";
    position:fixed;
    inset:0;
    background-image:
        linear-gradient(rgba(60,120,180,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(60,120,180,0.08) 1px, transparent 1px);
    background-size:48px 48px;
    pointer-events:none;
}
.header{
    position:sticky;
    top:0;
    z-index:10;
    padding:18px 24px;
    background:rgba(4,8,14,.72);
    backdrop-filter:blur(14px);
    border-bottom:1px solid var(--line);
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:12px;
    flex-wrap:wrap;
}
.header h1{
    margin:0;
    font-family:'Orbitron', sans-serif;
    font-size:clamp(1.15rem, 3vw, 1.7rem);
}
.back{
    color:var(--cyan);
    border:1px solid var(--line);
    padding:10px 14px;
    border-radius:12px;
    background:rgba(9,20,34,.72);
}
.container{
    width:min(1120px, calc(100% - 32px));
    margin:26px auto 40px;
}
.control-card,.chart-card,.info-card{
    background:var(--panel);
    border:1px solid var(--line);
    border-radius:18px;
    padding:22px;
    box-shadow:var(--shadow);
    backdrop-filter:blur(10px);
    margin-bottom:18px;
}
.control-card h3,.chart-card h2,.info-card h3{
    margin:0 0 12px 0;
    font-family:'Orbitron', sans-serif;
}
.control-card p,.info-card p{
    margin:0 0 16px 0;
    color:var(--muted);
    line-height:1.65;
}
.tab-row{
    display:flex;
    gap:12px;
    flex-wrap:wrap;
}
button{
    background:linear-gradient(135deg, rgba(10,28,44,0.95), rgba(6,18,28,0.95));
    color:var(--cyan);
    border:1px solid rgba(49,215,255,0.24);
    padding:12px 16px;
    border-radius:12px;
    cursor:pointer;
    font-weight:600;
    transition:.25s ease;
}
button:hover, button.active{
    color:white;
    background:linear-gradient(135deg, rgba(18,62,88,0.95), rgba(10,28,44,0.95));
    box-shadow:0 10px 24px rgba(49,215,255,0.12);
}
.hidden{
    display:none !important;
}
.canvas-wrap{
    min-height:380px;
    position:relative;
}
.placeholder{
    min-height:260px;
    display:grid;
    place-items:center;
    text-align:center;
    border:1px dashed rgba(49,215,255,0.22);
    border-radius:16px;
    color:var(--muted);
    background:rgba(2,10,18,0.45);
    padding:24px;
}
.legend{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
    margin-top:16px;
}
.legend-box{
    padding:14px;
    border-radius:14px;
    border:1px solid var(--line);
    background:rgba(255,255,255,0.02);
}
.legend-box span{
    display:block;
    font-size:12px;
    color:var(--muted);
    margin-bottom:6px;
}
.legend-box b{
    font-size:1.05rem;
}
@media (max-width:700px){
    .legend{grid-template-columns:1fr;}
    .container{width:min(100% - 20px, 1120px);}
}
</style>
</head>
<body>


<div class="header">
    <h1>Graph Dashboard</h1>
    <a href="/" class="back">← Back to Control Panel</a>
</div>


<div class="container">

    <div class="control-card">
        <h3>Threat Analytics Console</h3>
        <p>Charts are intentionally hidden on first load. Click a chart type below to reveal the selected intelligence view.</p>

        <div class="tab-row">
            <button onclick="showChart('pie', this)">Pie</button>
            <button onclick="showChart('bar', this)">Bar</button>
            <button onclick="showChart('line', this)">Timeline</button>
        </div>
    </div>

    <div class="chart-card">
        {% if not logs %}
        <div class="placeholder">
            <div>
                <h2 style="margin-top:0;">📡 Threat Intelligence Overview</h2>
                <p>No data available. Please upload a CSV file.</p>
            </div>
        </div>
        {% else %}
        <h2>📡 Threat Intelligence Overview</h2>
        <div id="chartPlaceholder" class="placeholder">
            <div>
                <p style="margin:0;">No chart is displayed yet.</p>
                <p style="margin:8px 0 0 0;">Select Pie, Bar, or Timeline to view analytics.</p>
            </div>
        </div>
        <div id="chartWrap" class="canvas-wrap hidden">
            <canvas id="chart"></canvas>
        </div>
        {% endif %}
    </div>

</div>


<script>
const logs = {{ logs|tojson }} || [];
let chart;

function destroyChart(){
    if(chart){ chart.destroy(); }
}

function clearActiveButtons(){
    document.querySelectorAll('.tab-row button').forEach(btn => btn.classList.remove('active'));
}

function showChart(type, el){
    if(logs.length === 0) return;

    clearActiveButtons();
    if(el){ el.classList.add('active'); }

    document.getElementById('chartPlaceholder').classList.add('hidden');
    document.getElementById('chartWrap').classList.remove('hidden');

    destroyChart();
    const ctx = document.getElementById('chart');

    if(type === 'pie'){
        let h=0,m=0,l=0;
        logs.forEach(x=>{
            if(x.risk==='High') h++;
            else if(x.risk==='Medium') m++;
            else l++;
        });

        chart = new Chart(ctx,{
            type:'pie',
            data:{
                labels:['High','Medium','Low'],
                datasets:[{
                    data:[h,m,l],
                    backgroundColor:['#ff4d6d','#facc15','#22c55e'],
                    borderColor:['#101826','#101826','#101826'],
                    borderWidth:2
                }]
            },
            options:{
                plugins:{
                    legend:{labels:{color:'#d9f3ff'}}
                }
            }
        });
    }

    if(type === 'bar'){
        chart = new Chart(ctx,{
            type:'bar',
            data:{
                labels:logs.map(x=>x.name),
                datasets:[{
                    label:'Threat Score',
                    data:logs.map(x=>x.score),
                    backgroundColor:'#31d7ff',
                    borderRadius:8
                }]
            },
            options:{
                scales:{
                    x:{ticks:{color:'#d9f3ff'}, grid:{color:'rgba(255,255,255,0.06)'}},
                    y:{ticks:{color:'#d9f3ff'}, grid:{color:'rgba(255,255,255,0.06)'}}
                },
                plugins:{
                    legend:{labels:{color:'#d9f3ff'}}
                }
            }
        });
    }

    if(type === 'line'){
        chart = new Chart(ctx,{
            type:'line',
            data:{
                labels:logs.map(x=>x.time),
                datasets:[{
                    label:'Threat Trend',
                    data:logs.map(x=>x.score),
                    borderColor:'#ff4d6d',
                    backgroundColor:'rgba(255,77,109,0.15)',
                    fill:true,
                    tension:0.35,
                    pointBackgroundColor:'#31d7ff',
                    pointBorderColor:'#31d7ff'
                }]
            },
            options:{
                scales:{
                    x:{ticks:{color:'#d9f3ff'}, grid:{color:'rgba(255,255,255,0.06)'}},
                    y:{ticks:{color:'#d9f3ff'}, grid:{color:'rgba(255,255,255,0.06)'}}
                },
                plugins:{
                    legend:{labels:{color:'#d9f3ff'}}
                }
            }
        });
    }
}
</script>


</body>
</html>
"""


# ================= ADMIN =================
ADMIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Admin SOC</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
    --panel:rgba(7,16,28,0.82);
    --line:rgba(72,196,255,.16);
    --text:#d9f3ff;
    --muted:#87a7bd;
    --cyan:#31d7ff;
    --red:#ff4d6d;
    --yellow:#facc15;
    --shadow:0 0 0 1px rgba(49,215,255,0.06), 0 12px 40px rgba(0,0,0,0.45), 0 0 30px rgba(49,215,255,0.08);
}
*{box-sizing:border-box;}
body{
    margin:0;
    font-family:'Inter',sans-serif;
    color:var(--text);
    background:
        radial-gradient(circle at top right, rgba(49,215,255,0.10), transparent 24%),
        linear-gradient(135deg, #03060b 0%, #06101c 55%, #03060b 100%);
    min-height:100vh;
}
body::before{
    content:"";
    position:fixed;
    inset:0;
    background-image:
        linear-gradient(rgba(60,120,180,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(60,120,180,0.08) 1px, transparent 1px);
    background-size:48px 48px;
    pointer-events:none;
}
.header{
    position:sticky; top:0; z-index:10;
    padding:18px 24px;
    background:rgba(4,8,14,.72);
    backdrop-filter:blur(14px);
    border-bottom:1px solid var(--line);
    display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;
}
.header h1{margin:0;font-family:'Orbitron',sans-serif;font-size:clamp(1.15rem, 3vw, 1.7rem);}
.back{color:var(--cyan);border:1px solid var(--line);padding:10px 14px;border-radius:12px;background:rgba(9,20,34,.72);text-decoration:none;}
.container{width:min(1120px, calc(100% - 32px));margin:26px auto 40px;}
.card{
    background:var(--panel);
    border:1px solid var(--line);
    border-radius:18px;
    padding:22px;
    box-shadow:var(--shadow);
    backdrop-filter:blur(10px);
    margin-bottom:18px;
}
.card h3{margin:0 0 12px 0;font-family:'Orbitron',sans-serif;}
.card p{color:var(--muted);line-height:1.65;}
.controls{display:flex;gap:12px;flex-wrap:wrap;}
button{
    background:linear-gradient(135deg, rgba(10,28,44,0.95), rgba(6,18,28,0.95));
    color:var(--cyan);
    border:1px solid rgba(49,215,255,0.24);
    padding:12px 16px;
    border-radius:12px;
    cursor:pointer;
    font-weight:600;
    transition:.25s ease;
}
button:hover,button.active{
    color:white;
    background:linear-gradient(135deg, rgba(18,62,88,0.95), rgba(10,28,44,0.95));
    box-shadow:0 10px 24px rgba(49,215,255,0.12);
}
.section{
    display:none;
}
.section.active{
    display:block;
}
.data-line{
    padding:12px 14px;
    border:1px solid rgba(72,196,255,.10);
    border-radius:12px;
    background:rgba(255,255,255,0.02);
    margin-bottom:10px;
    color:#d9f3ff;
}
.empty{
    border:1px dashed rgba(49,215,255,0.22);
    border-radius:16px;
    padding:28px;
    text-align:center;
    color:var(--muted);
    background:rgba(2,10,18,0.45);
}
@media (max-width:700px){
    .container{width:min(100% - 20px, 1120px);}
}
</style>
</head>
<body>


<div class="header">
    <h1>Admin SOC Dashboard</h1>
    <a href="/" class="back">← Back to Control Panel</a>
</div>


<div class="container">

    {% if not critical and not breach and not file_access %}
    <div class="card">
        <div class="empty">No data available. Upload a file to view SOC insights.</div>
    </div>
    {% else %}
    <div class="card">
        <h3>Security Monitoring Modules</h3>
        <p>All admin dashboard sections are hidden by default. Click a module to reveal its data.</p>
        <div class="controls">
            <button onclick="show('c', this)">Critical</button>
            <button onclick="show('b', this)">Breach</button>
            <button onclick="show('f', this)">File Access</button>
        </div>
    </div>

    <div id="c" class="card section">
        <h3>Critical Alerts</h3>
        {% for l in critical %}
        <div class="data-line">{{l.name}} | {{l.location}} | {{l.activity}} | {{l.risk}}</div>
        {% endfor %}
    </div>

    <div id="b" class="card section">
        <h3>Breach Detection</h3>
        {% for l in breach %}
        <div class="data-line">{{l.name}} | Possible breach activity | {{l.risk}}</div>
        {% endfor %}
    </div>

    <div id="f" class="card section">
        <h3>File Access Logs</h3>
        {% for l in file_access %}
        <div class="data-line">{{l.name}} | {{l.activity}} | {{l.risk}}</div>
        {% endfor %}
    </div>
    {% endif %}

</div>


<script>
function show(id, el){
    document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
    document.querySelectorAll('.controls button').forEach(b=>b.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    if(el){ el.classList.add('active'); }
}
</script>


</body>
</html>
"""


# ================= LOCATION =================
LOCATION_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Location Warning</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
    --panel:rgba(7,16,28,0.82);
    --line:rgba(72,196,255,.16);
    --text:#d9f3ff;
    --muted:#87a7bd;
    --cyan:#31d7ff;
    --red:#ff4d6d;
    --shadow:0 0 0 1px rgba(49,215,255,0.06), 0 12px 40px rgba(0,0,0,0.45), 0 0 30px rgba(49,215,255,0.08);
}
*{box-sizing:border-box;}
body{
    margin:0;
    font-family:'Inter',sans-serif;
    color:var(--text);
    background:
        radial-gradient(circle at top right, rgba(49,215,255,0.10), transparent 24%),
        linear-gradient(135deg, #03060b 0%, #06101c 55%, #03060b 100%);
    min-height:100vh;
}
body::before{
    content:"";
    position:fixed;
    inset:0;
    background-image:
        linear-gradient(rgba(60,120,180,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(60,120,180,0.08) 1px, transparent 1px);
    background-size:48px 48px;
    pointer-events:none;
}
.header{
    position:sticky; top:0; z-index:10;
    padding:18px 24px;
    background:rgba(4,8,14,.72);
    backdrop-filter:blur(14px);
    border-bottom:1px solid var(--line);
    display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;
}
.header h1{margin:0;font-family:'Orbitron',sans-serif;font-size:clamp(1.15rem, 3vw, 1.7rem);}
.back{color:var(--cyan);border:1px solid var(--line);padding:10px 14px;border-radius:12px;background:rgba(9,20,34,.72);text-decoration:none;}
.container{width:min(1120px, calc(100% - 32px));margin:26px auto 40px;}
.card{
    background:var(--panel);
    border:1px solid var(--line);
    border-radius:18px;
    padding:22px;
    box-shadow:var(--shadow);
    backdrop-filter:blur(10px);
    margin-bottom:18px;
}
.card h3{margin:0 0 12px 0;font-family:'Orbitron',sans-serif;}
.card p{color:var(--muted);line-height:1.65;}
.controls{display:flex;gap:12px;flex-wrap:wrap;}
button{
    background:linear-gradient(135deg, rgba(10,28,44,0.95), rgba(6,18,28,0.95));
    color:var(--cyan);
    border:1px solid rgba(49,215,255,0.24);
    padding:12px 16px;
    border-radius:12px;
    cursor:pointer;
    font-weight:600;
    transition:.25s ease;
}
button:hover,button.active{
    color:white;
    background:linear-gradient(135deg, rgba(18,62,88,0.95), rgba(10,28,44,0.95));
    box-shadow:0 10px 24px rgba(49,215,255,0.12);
}
.section{display:none;}
.section.active{display:block;}
.data-line{
    padding:12px 14px;
    border:1px solid rgba(72,196,255,.10);
    border-radius:12px;
    background:rgba(255,255,255,0.02);
    margin-bottom:10px;
}
.red{color:#ff4d6d;}
.blue{color:#31d7ff;}
.empty{
    border:1px dashed rgba(49,215,255,0.22);
    border-radius:16px;
    padding:28px;
    text-align:center;
    color:var(--muted);
    background:rgba(2,10,18,0.45);
}
@media (max-width:700px){
    .container{width:min(100% - 20px, 1120px);}
}
</style>
</head>
<body>


<div class="header">
    <h1>🌍 Geo Threat Intelligence</h1>
    <a href="/" class="back">← Back to Control Panel</a>
</div>


<div class="container">

    {% if not logs %}
    <div class="card">
        <div class="empty">No location data available. Upload logs first.</div>
    </div>
    {% else %}
    <div class="card">
        <h3>Geo Modules</h3>
        <p>No geo information is shown initially. Choose a panel to reveal location intelligence.</p>
        <div class="controls">
            <button onclick="show('i', this)">Impossible Travel</button>
            <button onclick="show('l', this)">Login Locations</button>
        </div>
    </div>

    <div id="i" class="card section">
        <h3>Impossible Travel</h3>
        {% for l in logs %}
        {% if l.location.lower() in ['foreign','usa','uk','dubai','sri lanka','vpn','unknown'] %}
        <div class="data-line red">{{l.name}} | {{l.location}} | {{l.time}}</div>
        {% endif %}
        {% endfor %}
    </div>

    <div id="l" class="card section">
        <h3>Login Locations</h3>
        {% for l in logs %}
        <div class="data-line blue">{{l.name}} | {{l.location}} | {{l.time}} | {{l.risk}}</div>
        {% endfor %}
    </div>
    {% endif %}

</div>


<script>
function show(id, el){
    document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
    document.querySelectorAll('.controls button').forEach(b=>b.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    if(el){ el.classList.add('active'); }
}
</script>


</body>
</html>
"""
# ================= HIGH RISK DASHBOARD =================
HIGH_RISK_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>High Risk Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
    --panel:rgba(7,16,28,0.82);
    --line:rgba(72,196,255,.16);
    --text:#d9f3ff;
    --muted:#87a7bd;
    --cyan:#31d7ff;
    --red:#ff4d6d;
    --yellow:#facc15;
    --shadow:0 0 0 1px rgba(49,215,255,0.06), 0 12px 40px rgba(0,0,0,0.45), 0 0 30px rgba(49,215,255,0.08);
}
*{box-sizing:border-box;}
body{
    margin:0;
    font-family:'Inter',sans-serif;
    color:var(--text);
    background:
        radial-gradient(circle at top right, rgba(255,77,109,0.10), transparent 24%),
        linear-gradient(135deg, #03060b 0%, #06101c 55%, #03060b 100%);
    min-height:100vh;
}
body::before{
    content:"";
    position:fixed;
    inset:0;
    background-image:
        linear-gradient(rgba(60,120,180,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(60,120,180,0.08) 1px, transparent 1px);
    background-size:48px 48px;
    pointer-events:none;
}
.header{
    position:sticky; top:0; z-index:10;
    padding:18px 24px;
    background:rgba(4,8,14,.72);
    backdrop-filter:blur(14px);
    border-bottom:1px solid var(--line);
    display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;
}
.header h1{margin:0;font-family:'Orbitron',sans-serif;font-size:clamp(1.15rem, 3vw, 1.7rem);}
.back{color:var(--cyan);border:1px solid var(--line);padding:10px 14px;border-radius:12px;background:rgba(9,20,34,.72);text-decoration:none;}
.container{width:min(1120px, calc(100% - 32px));margin:26px auto 40px;}
.card{
    background:var(--panel);
    border:1px solid rgba(255,77,109,0.16);
    border-radius:18px;
    padding:22px;
    box-shadow:0 0 0 1px rgba(255,77,109,0.08), 0 12px 40px rgba(0,0,0,0.45), 0 0 30px rgba(255,77,109,0.10);
    backdrop-filter:blur(10px);
    margin-bottom:18px;
}
.card h2,.card h3{margin:0 0 12px 0;font-family:'Orbitron',sans-serif;}
.red{color:#ff4d6d;}
.summary,.score{color:#d9f3ff;}
.empty{
    border:1px dashed rgba(255,77,109,0.25);
    border-radius:16px;
    padding:28px;
    text-align:center;
    color:var(--muted);
    background:rgba(20,8,12,0.45);
}
.badge{
    display:inline-flex;
    align-items:center;
    gap:8px;
    padding:8px 12px;
    border-radius:999px;
    background:rgba(255,77,109,0.12);
    border:1px solid rgba(255,77,109,0.20);
    color:#ff9aae;
    font-size:12px;
    margin-bottom:14px;
}
</style>
</head>
<body>


<div class="header">
    <h1>🚨 High Risk Users Dashboard</h1>
    <a href="/" class="back">← Back to Control Panel</a>
</div>


<div class="container">


{% if users and users|length > 0 %}
{% for u in users %}
<div class="card critical">
    <div class="badge">THREAT LEVEL • CRITICAL</div>
    <h2 class="red">{{u.name}}</h2>
    <p class="red"><b>⚠ CRITICAL USER</b></p>

    <p><b>Location:</b> {{u.location}}</p>
    <p><b>Activity:</b> {{u.activity}}</p>
    <p class="score">Risk Score: {{u.score}}</p>

    <p class="summary"><b>Summary:</b> {{u.summary}}</p>
</div>
{% endfor %}
{% else %}
<div class="empty">No high risk users found.</div>
{% endif %}


</div>


</body>
</html>
"""
# ================= ALERT DASHBOARD =================
ALERT_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Alert Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
    --panel:rgba(7,16,28,0.82);
    --line:rgba(72,196,255,.16);
    --text:#d9f3ff;
    --muted:#87a7bd;
    --cyan:#31d7ff;
    --green:#22c55e;
    --red:#ff4d6d;
    --shadow:0 0 0 1px rgba(49,215,255,0.06), 0 12px 40px rgba(0,0,0,0.45), 0 0 30px rgba(49,215,255,0.08);
}
*{box-sizing:border-box;}
body{
    margin:0;
    font-family:'Inter',sans-serif;
    color:var(--text);
    background:
        radial-gradient(circle at top right, rgba(49,215,255,0.10), transparent 24%),
        linear-gradient(135deg, #03060b 0%, #06101c 55%, #03060b 100%);
    min-height:100vh;
}
.header{padding:20px 24px;background:rgba(4,8,14,.72);border-bottom:1px solid var(--line);backdrop-filter:blur(14px);}
.header h1{margin:0;font-family:'Orbitron',sans-serif;}
.container{width:min(1000px, calc(100% - 32px));margin:24px auto;}
.card{
    background:var(--panel);
    border:1px solid var(--line);
    border-radius:18px;
    padding:22px;
    box-shadow:var(--shadow);
    margin-bottom:18px;
}
input{
    padding:12px 14px;
    width:min(100%, 420px);
    border-radius:12px;
    border:1px solid rgba(49,215,255,0.18);
    background:rgba(2,10,18,0.7);
    color:var(--text);
}
button{
    padding:12px 16px;
    background:linear-gradient(135deg, rgba(10,28,44,0.95), rgba(6,18,28,0.95));
    border:1px solid rgba(49,215,255,0.24);
    border-radius:12px;
    color:var(--cyan);
    cursor:pointer;
    margin-left:10px;
}
.green{color:#22c55e;}
.red{color:#ff4d6d;}
</style>
</head>
<body>


<div class="header">
<h1>📩 Alert System Dashboard</h1>
</div>


<div class="container">


<div class="card">
<h3>Send Manual Alert</h3>
<form method="POST">
<input type="text" name="phone" placeholder="Enter number (+91...)" required>
<button type="submit">Send Alert</button>
</form>


{% if message %}
<p class="{{status}}">{{message}}</p>
{% endif %}
</div>


<div class="card">
<h3>Alert History</h3>
{% for a in alerts %}
<p>{{a.time}} | {{a.number}} | Sent</p>
{% endfor %}
</div>


</div>


</body>
</html>
"""
# ================= AI PAGE =================
AI_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>AI SOC Assistant</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
    --panel:rgba(7,16,28,0.82);
    --line:rgba(72,196,255,.16);
    --text:#d9f3ff;
    --muted:#87a7bd;
    --cyan:#31d7ff;
    --shadow:0 0 0 1px rgba(49,215,255,0.06), 0 12px 40px rgba(0,0,0,0.45), 0 0 30px rgba(49,215,255,0.08);
}
*{box-sizing:border-box;}
body{
    margin:0;
    font-family:'Inter', Arial, sans-serif;
    background:
        radial-gradient(circle at top right, rgba(49,215,255,0.10), transparent 24%),
        linear-gradient(135deg, #03060b 0%, #06101c 55%, #03060b 100%);
    color:var(--text);
    min-height:100vh;
}
body::before{
    content:"";
    position:fixed;
    inset:0;
    background-image:
        linear-gradient(rgba(60,120,180,0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(60,120,180,0.08) 1px, transparent 1px);
    background-size:48px 48px;
    pointer-events:none;
}
.header{
    padding:18px 24px;
    background:rgba(4,8,14,.72);
    border-bottom:1px solid var(--line);
    backdrop-filter:blur(14px);
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:12px;
    flex-wrap:wrap;
}
.header h1{
    margin:0;
    font-family:'Orbitron', sans-serif;
    font-size:clamp(1.15rem, 3vw, 1.7rem);
}
.back{
    color:var(--cyan);
    border:1px solid var(--line);
    padding:10px 14px;
    border-radius:12px;
    background:rgba(9,20,34,.72);
    text-decoration:none;
}
.container{
    width:min(980px, calc(100% - 32px));
    margin:26px auto 40px;
}
.card{
    background:var(--panel);
    border:1px solid var(--line);
    padding:24px;
    border-radius:18px;
    box-shadow:var(--shadow);
    backdrop-filter:blur(10px);
    margin-bottom:18px;
}
form{
    display:flex;
    gap:12px;
    flex-wrap:wrap;
}
input[type="text"]{
    flex:1;
    min-width:240px;
    padding:14px 16px;
    border-radius:14px;
    border:1px solid rgba(49,215,255,0.18);
    background:rgba(2,10,18,0.7);
    color:var(--text);
}
button{
    background:linear-gradient(135deg, rgba(10,28,44,0.95), rgba(6,18,28,0.95));
    color:var(--cyan);
    border:1px solid rgba(49,215,255,0.24);
    padding:12px 18px;
    border-radius:12px;
    cursor:pointer;
    font-weight:600;
}
button:hover{
    color:white;
    background:linear-gradient(135deg, rgba(18,62,88,0.95), rgba(10,28,44,0.95));
}
.chat{
    margin-top:18px;
    display:grid;
    gap:12px;
}
.msg{
    padding:16px;
    border-radius:14px;
    line-height:1.65;
}
.user{
    background:rgba(49,215,255,0.09);
    border:1px solid rgba(49,215,255,0.16);
}
.ai{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
}
</style>
</head>
<body>


<div class="header">
    <h1>🧠 SOC Intelligence Assistant</h1>
    <a href="/" class="back">← Back to Control Panel</a>
</div>


<div class="container">


<div class="card">
<form method="POST">
<input type="text" name="question" placeholder="Ask about security threats..." required>
<button type="submit">Ask</button>
</form>


<div class="chat">
{% if question %}
<div class="msg user"><b>You:</b> {{question}}</div>
<div class="msg ai"><b>AI:</b> {{answer}}</div>
{% endif %}
</div>


</div>


</div>


</body>
</html>
"""
# ================= ROUTES =================
@app.route("/", methods=["GET","POST"])
def home():


    session.setdefault("uploaded", False)


    message=""
    msg_type=""


    logs = session.get("logs", [])


    if request.method=="POST":
        file=request.files.get("file")


        try:
            if not file or file.filename=="":
                raise Exception("No file selected")


            logs=[]
            data=file.read().decode("utf-8", errors="ignore").splitlines()
            reader=csv.DictReader(data)


            for row in reader:
                name=row.get("name","").strip()
                location=row.get("location","Unknown").strip()
                activity=row.get("activity","Login").strip()
                if name:
                    result = generate_analysis(name, location, activity=activity)
                    logs.append(result)


    # 🚨 HIGH RISK ALERT LOGIC (FIXED)
                if result["risk"] == "High":
                    reason = ""


                    if "vpn" in result["location"].lower():
                        reason += "Suspicious VPN location detected. "


                    if "failed" in result["activity"].lower():
                        reason += "Multiple failed login attempts. "


                    if result["score"] > 80:
                        reason += "High anomaly score detected. "


                    send_telegram_alert(result, reason)
            session["logs"]=logs
            session["uploaded"] = True
            message=f"Upload successful ({len(logs)})"
            msg_type="success"


        except Exception as e:
            message=str(e)
            msg_type="error"


    return render_template_string(HOME_PAGE,
                                  message=message,
                                  msg_type=msg_type,
                                  logs=session.get("logs"))


@app.route("/graphs")
def graphs():
    logs = session.get("logs", []) if session.get("uploaded") else []
    return render_template_string(GRAPH_PAGE, logs=logs)


@app.route("/location-warning")
def location_warning():
    logs = session.get("logs", []) if session.get("uploaded") else []
    return render_template_string(LOCATION_PAGE, logs=logs)


@app.route("/admin")
def admin():
    logs = session.get("logs", []) if session.get("uploaded") else []


    return render_template_string(ADMIN_PAGE,
        critical=[l for l in logs if l["risk"]=="High"],
        breach=[l for l in logs if l["risk"]=="High"],
        file_access=[l for l in logs if l["risk"] in ["High","Medium"]]
    )


@app.route("/download-report")
def download_report():
    logs=session.get("logs",[])
    if not logs:
        return redirect(url_for("home"))


    file_path = generate_pdf(logs)
    return send_file(file_path, as_attachment=True)


@app.route("/download-high-risk-report")
def download_high_risk_report():


    # ❌ Block access if no upload happened
    if not session.get("uploaded"):
        return redirect(url_for("home"))


    logs = session.get("logs", [])


    # ❌ Block if no logs exist
    if not logs:
        return redirect(url_for("home"))


    # Filter only high risk users
    high_risk_logs = [l for l in logs if l["risk"] == "High"]


    # ❌ If no high risk users
    if len(high_risk_logs) == 0:
        return redirect(url_for("home"))


    file_path = generate_high_risk_pdf(high_risk_logs)
    return send_file(file_path, as_attachment=True)


@app.route("/high-risk-dashboard")
def high_risk_dashboard():


    # ❌ Block if no upload happened
    if not session.get("uploaded"):
        return render_template_string(HIGH_RISK_PAGE, users=[])


    logs = session.get("logs", [])


    # Filter high risk users only
    high_users = []


    for l in logs:
        if l["risk"] == "High":
            l["summary"] = generate_summary(l)
            high_users.append(l)


    return render_template_string(HIGH_RISK_PAGE, users=high_users)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))


@app.route("/ai-agent", methods=["GET","POST"])
def ai_agent():
    logs = session.get("logs", [])
    answer = ""
    question = ""


    if request.method == "POST":
        question = request.form.get("question")
        answer = ai_soc_agent(question, logs)


    return render_template_string(AI_PAGE, question=question, answer=answer)


# ================= RUN =================
if __name__=="__main__":
    app.run(debug=True)

