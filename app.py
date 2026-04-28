from flask import Flask, render_template_string, jsonify
from datetime import datetime

app = Flask(__name__)

# Simulated employee activity data for hackathon demo
employee_logs = [
    {
        "name": "Rahul Sharma",
        "login_time": "02:15 AM",
        "location": "Unknown Location",
        "device": "Unrecognized Device",
        "failed_attempts": 5,
        "sensitive_access": True,
        "large_download": True,
        "threat_score": "High",
        "reason": "Late-night login + unknown location + large sensitive file download"
    },
    {
        "name": "Priya Verma",
        "login_time": "09:20 AM",
        "location": "Bangalore Office",
        "device": "Authorized Laptop",
        "failed_attempts": 0,
        "sensitive_access": False,
        "large_download": False,
        "threat_score": "Low",
        "reason": "Normal working behavior detected"
    },
    {
        "name": "Amit Singh",
        "login_time": "11:45 PM",
        "location": "Different Country",
        "device": "Mobile Browser",
        "failed_attempts": 3,
        "sensitive_access": True,
        "large_download": False,
        "threat_score": "Medium",
        "reason": "Impossible travel + unusual confidential file access"
    }
]

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrustWatch AI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            background: #0b1020;
            color: white;
            padding: 20px;
        }

        .header {
            background: #111827;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
        }

        .header h1 {
            font-size: 32px;
            color: #38bdf8;
        }

        .header p {
            margin-top: 8px;
            color: #cbd5e1;
        }

        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .card {
            background: #111827;
            padding: 20px;
            border-radius: 14px;
            box-shadow: 0 0 15px rgba(0,0,0,0.15);
        }

        .card h2 {
            margin-bottom: 15px;
            color: #22c55e;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #374151;
            font-size: 14px;
        }

        th {
            color: #38bdf8;
        }

        .high {
            color: #ef4444;
            font-weight: bold;
        }

        .medium {
            color: #f59e0b;
            font-weight: bold;
        }

        .low {
            color: #22c55e;
            font-weight: bold;
        }

        .alert-box {
            background: #1f2937;
            padding: 15px;
            border-left: 5px solid #ef4444;
            border-radius: 10px;
            margin-top: 10px;
        }
    </style>
</head>
<body>

<div class="header">
    <h1>TrustWatch AI</h1>
    <p>Predictive Insider Threat Detection System for Enterprise Cybersecurity</p>
</div>

<div class="dashboard">
    <div class="card">
        <h2>Admin Security Alerts</h2>
        {% for log in logs %}
            {% if log.threat_score == 'High' %}
                <div class="alert-box">
                    <strong>{{ log.name }}</strong><br>
                    Threat Level: <span class="high">{{ log.threat_score }}</span><br>
                    Reason: {{ log.reason }}
                </div>
            {% endif %}
        {% endfor %}
    </div>

    <div class="card">
        <h2>Employee Activity Logs</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>Login Time</th>
                <th>Location</th>
                <th>Threat</th>
            </tr>
            {% for log in logs %}
            <tr>
                <td>{{ log.name }}</td>
                <td>{{ log.login_time }}</td>
                <td>{{ log.location }}</td>
                <td class="{{ log.threat_score.lower() }}">{{ log.threat_score }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</div>

</body>
</html>
'''


@app.route('/')
def dashboard():
    return render_template_string(HTML_PAGE, logs=employee_logs)


@app.route('/api/logs')
def api_logs():
    return jsonify({
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": employee_logs
    })


if __name__ == '__main__':
    app.run(debug=True)
