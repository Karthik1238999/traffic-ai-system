from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/data')
def data():
    try:
        with open("traffic_data.json") as f:
            traffic = json.load(f)

        with open("metrics.json") as f:
            metrics = json.load(f)

        with open("positions.json") as f:
            positions = json.load(f)

        return jsonify({
            "traffic": traffic,
            "metrics": metrics,
            "positions": positions
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, port=5001)