from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():

    conn = sqlite3.connect("alerts.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
    """)

    alerts = cursor.fetchall()

    total_alerts = len(alerts)

    high_alerts = 0
    critical_alerts = 0

    for alert in alerts:

        if alert[3] == "HIGH":
            high_alerts += 1

        elif alert[3] == "CRITICAL":
            critical_alerts += 1

    cursor.execute("""
        SELECT attack_type, COUNT(*)
        FROM alerts
        GROUP BY attack_type
    """)

    attack_stats = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        alerts=alerts,
        total_alerts=total_alerts,
        high_alerts=high_alerts,
        critical_alerts=critical_alerts,
        attack_stats=attack_stats
    )

if __name__ == "__main__":
    app.run(debug=True)