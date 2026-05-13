import webbrowser
import threading

from flask import Flask, render_template, request, jsonify
from generator import ALLOWED_LENGTHS, batch_generate, password_info

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", lengths=ALLOWED_LENGTHS)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(force=True)
    length = data.get("length", 16)
    count = data.get("count", 1)

    if length not in ALLOWED_LENGTHS:
        return jsonify({"error": f"Length must be one of {ALLOWED_LENGTHS}"}), 400
    if not (1 <= count <= 50):
        return jsonify({"error": "Count must be 1-50"}), 400

    results = [password_info(pw) for pw in batch_generate(length, count)]
    return jsonify({"passwords": results})


def open_browser():
    webbrowser.open("http://127.0.0.1:8089")


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=8089, debug=False)
