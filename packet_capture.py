from scapy.all import *
from detector import detect_port_scan
from detector import detect_syn_flood

def capture(packet):

    if packet.haslayer(IP) and packet.haslayer(TCP):

        source_ip = packet[IP].src

        destination_port = packet[TCP].dport

        print(
            f"{source_ip} -> {destination_port}"
        )

        # Port Scan Detection
        detect_port_scan(
            source_ip,
            destination_port
        )

        # SYN Flood Detection
        if packet[TCP].flags == "S":

            detect_syn_flood(
                source_ip
            )

sniff(
    prn=capture,
    store=False
)