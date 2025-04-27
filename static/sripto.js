const socket = io(); // Initialize Socket.io connection
const logsTable = document.getElementById("logs-table");
const alertList = document.getElementById("alert-list");
const logCount = document.getElementById("log-count");
const alertCount = document.getElementById("alert-count");

let autoRefresh = true;

// WebSocket log display handler
socket.on('log_message', function(data) {
    const logBox = document.getElementById("log-display");
    const logDiv = document.createElement("div");

    if (data.type === 'alert') {
        logDiv.innerHTML = `🟥 ${data.message} <span class="badge">AI detected</span>`;
        logDiv.style.color = "red";
    } else {
        logDiv.innerHTML = `🟩 ${data.message}`;
        logDiv.style.color = "green";
    }

    logBox.appendChild(logDiv);
});

// WebSocket control functions
function startLogs() {
    socket.emit('start_logs');
}

function stopLogs() {
    socket.emit('stop_logs');
}

// Chart initialization function
async function initChart() {
  const response = await fetch("/analytics");
  const data = await response.json();
  const labels = Object.keys(data);
  const values = Object.values(data);

  const ctx = document.getElementById("logChart").getContext("2d");
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Logs per 10 seconds',
        data: values,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
        tension: 0.2
      }]
    },
    options: {
      scales: {
        x: { title: { display: true, text: 'Time' } },
        y: { 
          title: { display: true, text: 'Logs' },
          beginAtZero: true 
        }
      }
    }
  });
}

// Initialize chart
let chart;
initChart().then(createdChart => chart = createdChart);

// SSE Client
const logContainer = document.getElementById("log-container");
if (!!window.EventSource) {
  const source = new EventSource("/stream");
  source.onmessage = function(event) {
    const log = JSON.parse(event.data);
    const div = document.createElement("div");
    div.className = "log-entry";
    div.textContent = `[${log.timestamp || 'Unknown'}] ${log.message || 'No message'}`;
    logContainer.prepend(div);
  };
} else {
  logContainer.innerHTML = "<p>Sorry, your browser does not support Server-Sent Events.</p>";
}

// Original code continues unchanged below
// Tracking logs per 10s
let logsBuffer = [];

function fetchLogs() {
  fetch("/alerts")
    .then((res) => res.json())
    .then((data) => {
      renderLogs(data.logs);
      renderAlerts(data.alerts);
      logsBuffer.push(...data.logs);
    });
}

function renderLogs(logs) {
  logsTable.innerHTML = "";
  logs.forEach((log) => {
    const row = document.createElement("tr");
    row.className = log.alert ? "alert" : "safe";
    row.innerHTML = `
      <td>${log.time}</td>
      <td>${log.ip}</td>
      <td>${log.severity} ${log.ai_detected ? "🧠" : ""}</td>
    `;
    logsTable.appendChild(row);
  });
  logCount.textContent = `${logs.length} logs`;
}

function renderAlerts(alerts) {
  alertList.innerHTML = "";
  alerts.forEach((alert) => {
    const li = document.createElement("li");
    li.textContent = `⏰ ${alert.time} — ${alert.reason || "Alert"} (${
      alert.ip
    })`;
    alertList.appendChild(li);
  });
  alertCount.textContent = `${alerts.length} alerts`;
}

// Every 3s fetch logs
setInterval(() => {
  if (autoRefresh) fetchLogs();
}, 3000);

// Every 10s update chart
setInterval(() => {
  const now = new Date().toLocaleTimeString();
  const logCountInLast10s = logsBuffer.length;
  logsBuffer = []; // reset buffer

  labels.push(now);
  data.push(logCountInLast10s);

  if (labels.length > 10) {
    labels.shift();
    data.shift();
  }

  chart.update();
}, 10000);

document.getElementById("auto-refresh-toggle").addEventListener("click", () => {
  autoRefresh = !autoRefresh;
});

document.getElementById("export-btn").addEventListener("click", () => {
  window.location.href = "/export";
});

fetchLogs();