# GuardianX 🛡️

**GuardianX** is a Flask-based real-time Cybersecurity Monitoring Dashboard that displays simulated security logs in a structured and interactive table format. This project helps visualize potential threats as they occur, using simulated log data sent from a Python script.

---

## 🔍 Features

- Real-time log monitoring  
- Structured log display: **Time**, **IP Address**, **Severity**  
- AJAX-powered live updates (no page refresh required)  
- Modular backend using Flask  
- Easy to extend for persistence, authentication, or analytics  

---

## 🚀 Getting Started

These instructions will help you set up and run the project locally.

---

## 📦 Prerequisites

Make sure you have:

- Python 3.8 or higher  
- `pip` (Python package manager)  

---

## 🛠️ Installation Steps

### 1. Clone the repository

```bash
git clone https://github.com/Manan-78581/guardianx.git
cd guardianx
```

### 2. Create and activate a virtual environment

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install required packages

```bash
pip install flask requests flask_socketio python-dotenv
```

### 4. Run the Flask server

```bash
python app.py
```

### 5. In a new terminal window, run the log simulator

```bash
python simulate_logs.py
```

---

## 📂 Project Structure

```
guardianx/
│
├── static/             # CSS and JavaScript files
│   ├── styles.css
│   └── script.js
│
├── templates/          # HTML templates
│   └── index.html
│
├── app.py              # Main Flask backend
├── simulate_logs.py    # Simulated log generator
├── README.md           # Project documentation
```

---

## 🧑‍💻 Author

**Manan**  
GitHub: [@Manan-78581](https://github.com/Manan-78581)

---

## ❤️ Support

If you found this project helpful, feel free to **star ⭐** the repository or contribute via pull requests.
