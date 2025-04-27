import requests
import time
import random
from datetime import datetime

log_messages = [
    "User admin failed login from 192.168.1.10",
    "Firewall detected possible trojan on port 443",
    "User john logged in successfully",
    "Multiple failed login attempts detected",
    "Possible malware detected in file upload",
    "Phishing email attempt blocked",
    "Suspicious activity from IP 172.16.0.5",
    "Normal network activity",
    "System rebooted",
    "Unauthorized access to database"
]

ips = [
    "192.168.1.10",
    "10.0.0.5",
    "172.16.0.5",
    "192.168.0.7"
]

severities = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

while True:
    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": random.choice(ips),
        "message": random.choice(log_messages),
        "severity": random.choice(severities)
    }

    response = requests.post("http://127.0.0.1:5000/log", json=log_data)
    print("Sent log:", log_data)
    print("Response:", response.json())

    time.sleep(2)
