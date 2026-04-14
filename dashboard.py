from flask import Flask, jsonify, render_template
import random
import os

app = Flask(__name__)

# Dummy traffic data
junctions = [
    {"name": "Junction 1", "lat": 13.0827, "lon": 80.2707},
    {"name": "Junction 2", "lat": 13.0847, "lon": 80.2727},
    {"name": "Junction 3", "lat": 13.0800, "lon": 80.2750},
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    for j in junctions:
        j["traffic"] = random.randint(10, 100)
        j["status"] = "red" if j["traffic"] > 60 else "green"
    return jsonify(junctions)

@app.route("/metrics")
def metrics():
    return jsonify({
        "total_junctions": len(junctions),
        "avg_traffic": random.randint(30, 80),
        "status": "AI Active"
    })

# IMPORTANT FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
