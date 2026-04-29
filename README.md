TrustWatch AI SOC Platform
TrustWatch AI SOC Platform is a Flask-based cybersecurity dashboard for analyzing uploaded log files, identifying risky user activity, and presenting threat insights through interactive dashboards. The project is designed to help surface suspicious login behavior, unusual locations, failed logins, and download-related risk indicators in a simple web interface.

Features
Upload CSV log files for threat analysis and risk scoring.
​

View overall security insights from the homepage, including Total Risk based on uploaded logs.

Open dashboards only when clicked, so no dashboard data appears by default.

Analyze threat trends using chart-based dashboards.

Review admin monitoring sections such as critical alerts, breach indicators, and file access activity.

Inspect suspicious login locations and impossible-travel style location warnings.

View high-risk users with summaries and risk scores.

Download generated PDF security reports.

Ask questions through the AI SOC assistant for quick security summaries.

Tech Stack
Python

Flask

HTML, CSS, JavaScript

Chart.js

ReportLab

Requests

Project Structure
bash
.
├── app.py
├── TrustWatch_Report.pdf
├── High_Risk_Report.pdf
└── README.md
How It Works
The application accepts uploaded CSV logs, processes each row, calculates a risk score, and classifies entries into Low, Medium, or High risk. README files usually explain the project overview, setup steps, and usage so repository visitors can quickly understand how to run the software and what it does.

Risk calculation is based on simple indicators such as suspicious locations, failed logins, download activity, and other abnormal behavior patterns inferred from the log content. The interface is organized as a central control panel with separate dashboards for graphs, monitoring, geo intelligence, high-risk users, and AI-assisted analysis.

Installation
Clone the repository:

bash
git clone https://github.com/your-username/trustwatch-ai-soc-platform.git
cd trustwatch-ai-soc-platform
Create and activate a virtual environment:

bash
python -m venv venv
On Windows
bash
venv\Scripts\activate
On macOS/Linux
bash
source venv/bin/activate
Install dependencies:

bash
pip install flask requests reportlab
Run the application:

bash
python app.py
Open the local server in your browser:

bash
http://127.0.0.1:5000/
Expected CSV Format
Upload a CSV file containing user log data. A simple example format is shown below.

text
name,location,device,activity
Alice,India,Laptop,Login Success
Bob,VPN,Mobile,Failed Login
Charlie,USA,Desktop,Large Download
Available Dashboards
Dashboard	Purpose
Dashboard	Purpose
Homepage	Upload logs and view high-level summary including Total Risk
Graph Dashboard	View pie, bar, and line charts for threat analysis
Admin SOC Dashboard	View critical alerts, breach indicators, and file access logs
Geo Threat Intelligence	Review suspicious locations and login geography
High Risk Users Dashboard	Inspect high-risk users with summaries
AI Assistant	Ask questions about the uploaded logs
Notes
Dashboard content is hidden by default and only appears after clicking the relevant section.

The homepage box has been updated from Dashboard to Total Risk.

PDF reports are generated from analyzed logs.

Telegram alert integration is included in the code for high-risk alert notifications.

Future Improvements
Database support for persistent log storage

User authentication and role-based access

Better risk scoring models

Real-time websocket-based alert streaming

More advanced visual analytics

Disclaimer
This project is intended for educational, academic, and prototype SOC monitoring use. It should be reviewed and secured further before being used in a real production security environment
