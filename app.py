import os
import threading
import time
import random
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import requests
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)

# Load Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# Warn if API key is missing
if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY environment variable not set. AI detection will fail.")

alerts = []
logs = []  # Store all logs here
logging_active = False  # Control flag for log simulation

# --- RULE-BASED ENGINE ---
def check_rules(log):
    reasons = []
    message = log.get("message", "").lower()
    ip = log.get("ip", "")
    user = log.get("user", "")
    time = log.get("time", "")
    location = log.get("location", "")

    if "failed login" in message:
        reasons.append("Too many failed logins")

    blacklisted_ips = ["192.168.1.100", "10.0.0.200"]
    if ip in blacklisted_ips:
        reasons.append("Login from blacklisted IP")

    if "login" in message and time:
        try:
            hour = int(time.split(":")[0])
            if hour < 9 or hour > 18:
                reasons.append("Login outside working hours")
        except ValueError:
            pass

    if "login" in message and "previous_location" in log:
        if location != log["previous_location"]:
            reasons.append("Login from unusual location")

    if any(word in message for word in ["malware", "trojan", "ransomware", "exploit"]):
        reasons.append("Suspicious keyword detected")

    if any(port in message for port in ["port 22", "port 3389"]):
        reasons.append("Access to restricted port")

    if "outbound traffic spike" in message:
        reasons.append("Unusual outbound traffic")

    if "port scan detected" in message:
        reasons.append("Port scanning behavior")

    if "ip spoofing" in message:
        reasons.append("Possible IP spoofing attempt")

    if "sensitive file access" in message:
        reasons.append("Unusual file access")

    if "disabled user" in user:
        reasons.append("Disabled user attempted login")

    if any(cmd in message for cmd in ["rm -rf", "powershell", "wget"]):
        reasons.append("Malicious command detected")

    if "login success" in message and log.get("prev_failures", 0) > 3:
        reasons.append("Suspicious login after multiple failures")

    if "large file download" in message:
        reasons.append("Unusual download activity")

    if "system file access" in message and log.get("user_role") != "admin":
        reasons.append("Non-admin accessed system files")

    if "connection to threat domain" in message:
        reasons.append("Connected to known threat domain")

    if log.get("recent_alerts", 0) > 5:
        reasons.append("Multiple alerts from same machine")

    if any(tool in message for tool in ["netstat", "taskmgr", "ps aux"]):
        reasons.append("Excessive admin tool usage")

    if "config access" in message and log.get("user_role") != "admin":
        reasons.append("Unauthorized config file access")

    if "user privilege changed" in message:
        reasons.append("Privilege escalation attempt")

    return reasons

# --- GROQ AI DETECTION ---
def ai_check_with_groq(log_message):
    if not GROQ_API_KEY:
        print("Error: No Groq API key provided.")
        return "error"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a security analyst. Analyze the following log message and classify it as 'suspicious' or 'normal'."},
            {"role": "user", "content": log_message}
        ],
        "max_tokens": 50
    }

    try:
        response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        prediction = result["choices"][0]["message"]["content"].lower()
        if "suspicious" in prediction:
            return "suspicious"
        return "normal"
    except Exception as e:
        print(f"Groq API Error: {e}")
        return "error"

# --- POST /log API ---
@app.route('/log', methods=['POST'])
def receive_log():
    try:
        log = request.json
        if not log or "message" not in log:
            return jsonify({"status": "error", "message": "Invalid log format"}), 400

        logs.append(log)
        message = log.get("message", "")
        reasons = check_rules(log)

        ai_result = ai_check_with_groq(message)
        if ai_result == "suspicious":
            reasons.append("AI detected suspicious activity")

        if reasons:
            alert = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip": log.get("ip", "unknown"),
                "reason": ", ".join(reasons),
                "message": message
            }
            alerts.append(alert)
            return jsonify({"status": "alert raised", "alert": alert}), 200
        else:
            return jsonify({"status": "log normal"}), 200

    except Exception as e:
        print(f"Error processing log: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- GET /alerts API ---
@app.route('/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alerts)

# --- View all received logs ---
@app.route('/logs', methods=['GET'])
def view_logs():
    return render_template('index.html', logs=logs, alerts=None)

# --- Main Dashboard ---
@app.route('/')
def dashboard():
    return render_template('index.html', logs=logs, alerts=alerts)


# --- Socket.IO Handlers ---
@socketio.on('start_logs')
def handle_start():
    global logging_active
    logging_active = True
    print("Log capturing started")

@socketio.on('stop_logs')
def handle_stop():
    global logging_active
    logging_active = False
    print("Log capturing stopped")

def simulate_logs():
    global logging_active
    while True:
        if logging_active:
            log_type = random.choice(['safe', 'alert'])
            message = "Safe log" if log_type == 'safe' else "Alert log"
            socketio.emit('log_message', {'type': log_type, 'message': message})
        time.sleep(10)

def start_simulation():
    thread = threading.Thread(target=simulate_logs)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    start_simulation()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)