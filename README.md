GuardianX
GuardianX is a Flask-based real-time Cybersecurity Monitoring Dashboard that displays simulated security logs in a structured table format. It consists of a backend server that receives log data via HTTP POST requests and stores it temporarily in memory. A separate Python script (simulate_logs.py) simulates network events by sending logs to the server every few seconds. Each log contains a timestamp, IP address, message, and severity level. The frontend, built with HTML, CSS, and JavaScript, fetches the latest logs from the server using periodic AJAX requests and displays them in a table labeled Time, IP Address, and Severity. The dashboard dynamically updates without needing a page refresh, giving users a near real-time view of potential threats. The architecture is modular, allowing for future enhancements such as persistent storage, authentication, or graphical visualizations. This project is ideal for learning log ingestion, live data rendering, and creating an interactive web-based monitoring tool.
________________________________________
🚀 Getting Started
These instructions will help you run the project locally.
________________________________________
📦 Prerequisites
•	Python 3.8 or higher
•	pip (Python package manager)
________________________________________
🛠️ Installation Steps
1.	Clone the repository
2.	git clone https://github.com/Manan-78581/guardianx.git
cd guardianx
Create and activate a virtual environment
