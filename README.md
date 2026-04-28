#  TrustWatch AI – SOC Security Monitoring System

## Overview

**TrustWatch AI** is a Security Operations Center (SOC) simulation platform that analyzes user activity logs, detects suspicious behavior, and provides intelligent insights using rule-based AI.

The system helps identify potential security breaches such as:

* Unauthorized access
* Suspicious login locations
* Failed login attempts
* Abnormal user activities

---

## Features

###  Log Analysis Engine

* Upload CSV files containing user activity logs
* Automatically processes and evaluates risk levels

### Risk Detection

* Classifies users into:

  * Low Risk
  * Medium Risk
  * High Risk

### Interactive Dashboards

* Graph visualizations (Pie, Bar, Timeline)
* Admin SOC dashboard
* Location-based anomaly detection

###  AI SOC Assistant

* Answers user queries about threats
* Explains risk levels and breach reasons
* Provides security insights

### Report Generation

* Generates downloadable PDF reports
* Includes summaries and critical user analysis

---

## How It Works

The system assigns a **risk score** based on:

* Suspicious locations (VPN, foreign, unknown)
* Failed login attempts
* Large data downloads
* Unusual activity patterns

Based on the score:

* **High Risk** → Immediate attention required
* **Medium Risk** → Monitor closely
* **Low Risk** → Safe

---

## Project Structure

```id="structure"
app.py              # Main Flask application
templates           # Embedded HTML (render_template_string)
static              # (Optional for future UI enhancements)
TrustWatch_Report.pdf # Generated reports
```

---

##  Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Visualization:** Chart.js
* **PDF Reports:** ReportLab
* **Data Handling:** CSV

---

##  Installation

### 1. Clone the repository

```bash id="clone"
git clone https://github.com/your-username/trustwatch-ai.git
cd trustwatch-ai
```

### 2. Create virtual environment

```bash id="venv"
python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash id="install"
pip install flask reportlab
```

---

## Running the App

```bash id="run"
python app.py
```

Open in browser:

```id="url"
http://127.0.0.1:5000/
```

---

##  CSV Format

Upload a CSV file with the following structure:

```csv id="csv"
name,location,activity
Ravi,India,Login
Amit,USA,Failed Login
John,VPN,Large Download
```

---

##  Example Use Cases

* Detect suspicious login attempts
* Identify compromised user accounts
* Monitor user behavior in enterprise systems
* Simulate SOC operations for learning

---

##  Future Enhancements

* Real-time alert system
* Machine Learning-based anomaly detection
* Database integration (SQLite/PostgreSQL)
* User authentication system
* Advanced analytics dashboard

---

##  Author

Developed as a cybersecurity and AI project to simulate real-world SOC operations.

---

##  License

This project is for educational and demonstration purposes.
