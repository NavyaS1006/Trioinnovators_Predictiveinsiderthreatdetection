#  TrustWatch AI - Predictive Insider Threat Detection System

TrustWatch AI is a **cybersecurity SOC-style web application** built for hackathons that detects and predicts insider threats inside an organization using user activity logs.

It simulates a real-world Security Operations Center (SOC) dashboard with analytics, threat scoring, location anomaly detection, admin alerts, and automated report generation.

---

##  Features

###  1. Insider Threat Detection
- Analyzes user login activity from uploaded CSV files
- Assigns **Threat Scores (0–100)**
- Categorizes users into:
  -  Low Risk
  -  Medium Risk
  -  High Risk

---

###  2. Graph Dashboard (Chart.js)
- Pie Chart → Risk distribution (Low/Medium/High)
- Bar Chart → Employee threat scores
- Line Chart → Threat trend over time

---

###  3. Admin SOC Dashboard
-  Critical Alerts (High-risk users)
-  Breach Detection (suspicious activity patterns)
-  File Access Monitoring (sensitive activity logs)

---

###  4. Location Warning System
-  Impossible Travel Detection (e.g., India → Sri Lanka in short time)
-  Login Location Tracking (all user login origins)
- Detects VPN / Foreign / Unknown logins

---

###  5. Automated PDF Report Generation
- Generates SOC-style security report
- Includes:
  - Risk summary
  - Critical users list
  - Location activity logs
- Downloadable from dashboard (bottom-right button)

---

###  6. CSV File Upload System
Upload structured logs in format:

```csv
name,location,activity
Rahul Sharma,Bangalore,Login
Priya Verma,India,File Access
Akhil Kumar,VPN,Failed Login Attempts
