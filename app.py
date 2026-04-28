from flask import Flask, render_template_string, request
import csv

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrustWatch AI</title>

    <style>
        body {
            background: #0b1020;
            color: white;
            font-family: Arial, sans-serif;
            padding: 20px;
            margin: 0;
        }

        .header, .card {
            background: #111827;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
        }

        h1 {
            color: #38bdf8;
            margin: 0 0 8px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }

        .stat {
            background: #111827;
            border-radius: 14px;
            padding: 18px;
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

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            padding: 10px;
            border-bottom: 1px solid #333;
            text-align: left;
        }

        button {
            padding: 10px 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }

        input[type="file"] {
            margin-top: 10px;
        }
    </style>
</head>
<body>

<div class="header">
    <h1>TrustWatch AI</h1>
    <p>Predictive Insider Threat Detection System</p>
</div>

<div class="grid">
    <div class="stat">
        <h3>Monitoring</h3>
        <p>24/7 Active</p>
    </div>

    <div class="stat">
        <h3>Threat Engine</h3>
        <p>Live Detection</p>
    </div>

    <div class="stat">
        <h3>Security Alerts</h3>
        <p>Real-Time</p>
    </div>

    <div class="stat">
        <h3>Status</h3>
        <p>Protected</p>
    </div>
</div>

<div class="card">
    <h2>Upload Employee Activity File</h2>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <br><br>
        <button type="submit">Analyze File</button>
    </form>
</div>

{% if logs %}
<div class="card">
    <h2>Analysis Result</h2>

    <table>
        <tr>
            <th>Name</th>
            <th>Threat Score</th>
            <th>Risk Level</th>
            <th>Reason</th>
            <th>AI Recommendation</th>
        </tr>

        {% for log in logs %}
        <tr>
            <td>{{ log["name"] }}</td>
            <td>{{ log["score"] }}%</td>
            <td class="{{ log['risk'].lower() }}">
                {{ log["risk"] }}
            </td>
            <td>{{ log["reason"] }}</td>
            <td>{{ log["recommendation"] }}</td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endif %}

</body>
</html>
"""


def generate_analysis(name):
    score = 0
    reasons = []

    # Late Night Login Detection
    if len(name) % 2 == 0:
        score += 20
        reasons.append("Late night login detected")

    # Unknown Device Detection
    if len(name) % 3 == 0:
        score += 20
        reasons.append("Unknown device detected")

    # Sensitive File Access Detection
    if len(name) % 5 == 0:
        score += 25
        reasons.append("Sensitive file access detected")

    # Large File Download Detection
    if len(name) % 4 == 0:
        score += 20
        reasons.append("Large confidential file download")

    # Failed Login Attempts
    if len(name) % 7 == 0:
        score += 15
        reasons.append("Multiple failed login attempts")

    # Impossible Travel Detection
    if len(name) % 6 == 0:
        score += 20
        reasons.append("Impossible travel pattern detected")

    if score >= 75:
        risk = "High"
    elif score >= 45:
        risk = "Medium"
    else:
        risk = "Low"

    if not reasons:
        reasons.append("Normal employee behavior")

    reason = ", ".join(reasons)

    if risk == "High":
        recommendation = "Temporarily block account and alert admin"
    elif risk == "Medium":
        recommendation = "Require additional verification"
    else:
        recommendation = "Monitor user activity"

    return {
        "name": name,
        "score": score,
        "risk": risk,
        "reason": reason,
        "recommendation": recommendation
    }


@app.route("/", methods=["GET", "POST"])
def home():
    logs = []

    if request.method == "POST":
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename:
            content = uploaded_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(content)

            for row in reader:
                name = row.get("name", "").strip()

                if name:
                    logs.append(generate_analysis(name))

    return render_template_string(
        HTML_PAGE,
        logs=logs
    )


if __name__ == "__main__":
    app.run(debug=True)
