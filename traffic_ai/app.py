from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Traffic AI Running"

@app.route("/traffic")
def traffic():
    try:
        with open("traffic_data.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"error": "No data yet"})

if __name__ == "__main__":
    app.run(debug=True)