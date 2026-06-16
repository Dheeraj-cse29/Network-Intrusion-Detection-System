import sqlite3
from collections import defaultdict

# Track ports accessed by each IP
port_tracker = defaultdict(set)

# Track SYN packets from each IP
syn_tracker = defaultdict(int)


def save_alert(ip, attack_type, severity):

    conn = sqlite3.connect("alerts.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO alerts
        (source_ip, attack_type, severity)
        VALUES (?, ?, ?)
        """,
        (
            ip,
            attack_type,
            severity
        )
    )

    conn.commit()
    conn.close()

    print(f"[{severity}] {attack_type} Detected from {ip}")


def detect_port_scan(ip, port):

    port_tracker[ip].add(port)

    # Detect if an IP accesses many different ports
    if len(port_tracker[ip]) >= 5:

        save_alert(
            ip,
            "Port Scan",
            "HIGH"
        )

        # Reset tracking
        port_tracker[ip].clear()


def detect_syn_flood(ip):

    syn_tracker[ip] += 1

    # Detect excessive SYN packets
    if syn_tracker[ip] >= 20:

        save_alert(
            ip,
            "SYN Flood",
            "CRITICAL"
        )

        # Reset tracking
        syn_tracker[ip] = 0