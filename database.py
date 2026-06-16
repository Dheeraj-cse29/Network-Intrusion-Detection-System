import sqlite3

conn = sqlite3.connect("alerts.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE alerts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_ip TEXT,
    attack_type TEXT,
    severity TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")