from flask import Flask, jsonify, request, g
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)
import time

app = Flask(__name__)

# Total HTTP requests
REQUEST_COUNT = Counter(
    "flask_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

# HTTP request latency
REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

# Track request start time
@app.before_request
def before_request():
    g.start_time = time.time()


# Collect metrics after every request
@app.after_request
def after_request(response):

    if request.path != "/metrics":

        latency = time.time() - g.start_time

        endpoint = request.endpoint or "unknown"

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(latency)

    return response


@app.route("/")
def home():
    return jsonify({
        "message": "Flask Monitoring Application",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/api/success")
def success():
    time.sleep(0.2)

    return jsonify({
        "message": "API request successful"
    }), 200


@app.route("/api/error")
def error():
    return jsonify({
        "error": "Simulated API error"
    }), 500


# Prometheus metrics endpoint
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )