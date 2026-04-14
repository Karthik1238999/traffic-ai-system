from flask import Flask, jsonify
import json
import os

app = Flask(__name__)


# ------------------------------
# SAFE JSON READER
# ------------------------------
def read_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}


# ------------------------------
# HOME ROUTE (NO TEMPLATE ERROR)
# ------------------------------
@app.route("/")
def home():
    return """
    <h1>🚦 Traffic AI System is LIVE</h1>
    <p>Deployment Successful on Render</p>
    <ul>
        <li>/data → Traffic Data</li>
        <li>/metrics → System Metrics</li>
        <li>/top → Top Congested Junctions</li>
    </ul>
    """


# ------------------------------
# TRAFFIC DATA API
# ------------------------------
@app.route("/data")
def get_data():
    data = read_json("traffic_data.json")
    return jsonify(data)


# ------------------------------
# METRICS API
# ------------------------------
@app.route("/metrics")
def get_metrics():
    metrics = read_json("metrics.json")

    return jsonify({
        "steps": metrics.get("steps", 0),
        "total_delay": metrics.get("total_delay", 0)
    })


# ------------------------------
# TOP CONGESTED API
# ------------------------------
@app.route("/top")
def top_congested():
    data = read_json("traffic_data.json")

    sorted_data = sorted(
        data.items(),
        key=lambda x: x[1].get("current", 0),
        reverse=True
    )

    top5 = dict(sorted_data[:5])
    return jsonify(top5)


# ------------------------------
# RUN SERVER (RENDER COMPATIBLE)
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
