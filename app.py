from flask import Flask
import socket
import os
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests")

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return {
        "service": "task-api",
        "host": socket.gethostname(),
        "version": os.getenv("VERSION", "v1")
    }

@app.route("/metrics")
def metrics():
    return generate_latest()

app.run(host="0.0.0.0", port=5000)
