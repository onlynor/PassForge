import os
import sys
import webbrowser
import threading
import socket
import time

import pystray
from PIL import Image
from flask import Flask, render_template, request, jsonify
from generator import ALLOWED_LENGTHS, batch_generate, batch_generate_jwt, password_info, JWT_DEFAULT_LENGTH

PORT = 18080
URL = f"http://127.0.0.1:{PORT}"


def resource_path(relative_path):
    """Get path to resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/config", methods=["GET"])
def api_config():
    return jsonify({
        "allowedLengths": list(ALLOWED_LENGTHS),
        "jwtDefaultLength": JWT_DEFAULT_LENGTH,
        "maxLength": 128,
        "maxCount": 500
    })


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}

    try:
        count = int(data.get("count", 1))
    except (TypeError, ValueError):
        return jsonify({"error": "Count must be an integer"}), 400

    if not (1 <= count <= 500):
        return jsonify({"error": "Count must be 1-500"}), 400

    password_type = data.get("type", "standard")
    is_jwt = password_type == "jwt"

    if is_jwt:
        length = int(data.get("length", JWT_DEFAULT_LENGTH))
        if length < 16:
            return jsonify({"error": "JWT password length must be at least 16"}), 400
        results = [password_info(pw, is_jwt=True) for pw in batch_generate_jwt(count, length)]
    else:
        length = int(data.get("length", 16))
        if length not in ALLOWED_LENGTHS:
            return jsonify({"error": f"Length must be one of {ALLOWED_LENGTHS}"}), 400
        results = [password_info(pw) for pw in batch_generate(length, count)]

    return jsonify({"passwords": results})


@app.route("/api/shutdown", methods=["POST"])
def shutdown():
    """Exit the application"""
    os._exit(0)


def open_browser():
    webbrowser.open(URL)


def run_flask():
    app.run(host="127.0.0.1", port=PORT, debug=False)


def wait_for_server(timeout=10.0, interval=0.1):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_port_in_use(PORT):
            return True
        time.sleep(interval)
    return False


def show_error(message: str):
    print(f"Error: {message}")


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def create_tray_icon():
    icon_path = resource_path("logo/passforge.png")
    image = Image.open(icon_path)
    image = image.resize((64, 64), Image.LANCZOS)

    def on_open(icon, item):
        open_browser()

    def on_exit(icon, item):
        icon.stop()
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem("打开界面", on_open, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("退出", on_exit),
    )

    return pystray.Icon("PassForge", image, "PassForge", menu)


if __name__ == "__main__":
    if is_port_in_use(PORT):
        show_error(f"Port {PORT} is already in use. Please close the other program and try again.")
        raise SystemExit(1)

    try:
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        if wait_for_server():
            open_browser()
            print(f"PassForge running at {URL}")
            icon = create_tray_icon()
            icon.run()
        else:
            show_error(f"Failed to start PassForge at {URL}")
            raise SystemExit(1)
    except KeyboardInterrupt:
        print("\nPassForge stopped.")
