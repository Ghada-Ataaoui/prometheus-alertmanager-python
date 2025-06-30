# Python Monitoring Application with Prometheus & Alertmanager

A complete monitoring solution demonstrating how to monitor a Python web application using Prometheus for metrics collection and Alertmanager for alerting. The project includes a simple Python HTTP server with Prometheus metrics instrumentation, alerting rules, and a request generator for testing.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Python App     │    │   Prometheus    │    │  Alertmanager   │
│  (Port 8080)    │◄───┤   (Port 9090)   │◄───┤   (Port 9093)   │
│  Metrics: 8000  │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                                              │
         │                                              │
┌─────────────────┐                              ┌─────────────────┐
│ Request         │                              │ Email Alerts    │
│ Generator       │                              │ (Gmail SMTP)    │
└─────────────────┘                              └─────────────────┘
```

## 📋 Features

- **Python Web Application**: Simple HTTP server with custom metrics
- **Prometheus Monitoring**: Collects metrics from the Python app
- **Alerting System**: Automated alerts for high latency and downtime
- **Email Notifications**: Gmail SMTP integration for alert delivery
- **Request Generator**: HTML-based tool for load testing
- **Custom Metrics**: HTTP request counter and latency histogram

## 📊 Monitored Metrics

- `python_http_requests_total`: Counter for total HTTP requests
- `python_request_latency_seconds`: Histogram for request latency tracking

## 🚨 Alert Rules

1. **High Request Latency**: Triggers when average latency > 1 second for 1 minute
2. **Service Down**: Triggers when the Python app is unreachable for 15+ seconds

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- Prometheus server
- Alertmanager
- Gmail account with app password (for email alerts)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ghada-Ataaoui/monitoring-app-python.git
   cd monitoring-app-python
   ```

2. **Install Python dependencies**
   ```bash
   pip install prometheus_client
   ```

3. **Configure Email Alerts** (Optional)
   
   Edit `alertmanager/alertmanager.yml` and update the email configuration:
   ```yaml
   auth_username: "your-email@gmail.com"
   auth_password: "your-app-password"
   from: "your-email@gmail.com"
   to: "recipient@example.com"
   ```

4. **Start the Python Application**
   ```bash
   cd "python app"
   python index.py
   ```
   The app will be available at:
   - HTTP server: http://localhost:8080
   - Metrics endpoint: http://localhost:8000

5. **Start Prometheus**
   ```bash
   cd prometheus
   # Assuming prometheus binary is in your PATH
   prometheus --config.file=prometheus.yml
   ```
   Access Prometheus at: http://localhost:9090

6. **Start Alertmanager**
   ```bash
   cd alertmanager
   # Assuming alertmanager binary is in your PATH
   alertmanager --config.file=alertmanager.yml
   ```
   Access Alertmanager at: http://localhost:9093

### Testing the Setup

1. **Open the Request Generator**
   
   Open `request generator/index.html` in your web browser

2. **Generate Load**
   
   Use the request generator to send multiple requests to the Python app

3. **Monitor Metrics**
   
   Visit Prometheus at http://localhost:9090 and try these queries:
   - Request rate: `irate(python_http_requests_total[5m])`
   - Average latency: `rate(python_request_latency_seconds_sum[5m])/rate(python_request_latency_seconds_count[5m])`

4. **Test Alerts**
   
   Stop the Python app to trigger the "down" alert, or generate high load to trigger latency alerts

## 📁 Project Structure

```
monitoring-app-python/
├── README.md                          # This file
├── .gitignore                         # Git ignore rules
├── alertmanager/
│   └── alertmanager.yml              # Alertmanager configuration
├── prometheus/
│   ├── prometheus.yml                # Prometheus configuration
│   ├── commands.json                 # Useful PromQL queries
│   └── rules/
│       └── python-rules.yml          # Alert rules definition
├── python app/
│   └── index.py                      # Python web application
└── request generator/
    └── index.html                    # Load testing tool
```

## 🔧 Configuration Files

### Prometheus Configuration
- **Scrape Targets**: Python app metrics (localhost:8000), Prometheus self-monitoring, Alertmanager
- **Evaluation Interval**: 15 seconds
- **Alert Rules**: Loaded from `rules/python-rules.yml`

### Alertmanager Configuration
- **Email Integration**: Gmail SMTP
- **Routing**: All alerts sent to admin receiver
- **Timing**: 30s repeat interval, 15s group wait/interval

### Alert Rules
- **HighRequestLatency**: Average latency > 1s for 1+ minutes
- **ServiceDown**: Python app unreachable for 15+ seconds

## 📈 Useful PromQL Queries

The `prometheus/commands.json` file contains pre-defined queries:

```json
{
    "get requests rate" : "irate(python_http_requests_total[5m])",
    "get latency avg" : "rate(python_request_latency_seconds_sum[5m])/rate(python_request_latency_seconds_count[5m])"
}
```

## 🛠️ Customization

### Adding New Metrics
1. Import additional metric types from `prometheus_client`
2. Define metrics in the Python app
3. Instrument your code with the new metrics
4. Update Prometheus queries and alert rules as needed

### Modifying Alert Thresholds
Edit `prometheus/rules/python-rules.yml` to adjust:
- Latency thresholds
- Time windows
- Alert severity levels

### Adding New Alert Channels
Modify `alertmanager/alertmanager.yml` to add:
- Slack notifications
- PagerDuty integration
- Webhook endpoints

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 8080, 8000, 9090, and 9093 are available
2. **Email Alerts Not Working**: Verify Gmail app password and SMTP settings
3. **Metrics Not Appearing**: Check if Python app is exposing metrics on port 8000
4. **Alerts Not Firing**: Verify Prometheus is evaluating rules and can reach Alertmanager

### Logs & Debugging

- Check Prometheus targets at: http://localhost:9090/targets
- View alert status at: http://localhost:9090/alerts
- Monitor Alertmanager at: http://localhost:9093
