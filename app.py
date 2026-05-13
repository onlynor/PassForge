import os
import webbrowser
import threading
import socket
import time

from flask import Flask, render_template, request, jsonify
from generator import ALLOWED_LENGTHS, batch_generate, password_info

PORT = 18080
URL = f"http://127.0.0.1:{PORT}"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", lengths=ALLOWED_LENGTHS)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}

    try:
        length = int(data.get("length", 16))
        count = int(data.get("count", 1))
    except (TypeError, ValueError):
        return jsonify({"error": "Length and count must be integers"}), 400

    if length not in ALLOWED_LENGTHS:
        return jsonify({"error": f"Length must be one of {ALLOWED_LENGTHS}"}), 400
    if not (1 <= count <= 50):
        return jsonify({"error": "Count must be 1-50"}), 400

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
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("WeakPass", message)
        root.destroy()
    except Exception:
        print(message)


def run_control_window():
    """Small tkinter window as control panel"""
    import tkinter as tk

    root = tk.Tk()
    root.title("WeakPass")
    root.geometry("280x120")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    # Center on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - 280) // 2
    y = (root.winfo_screenheight() - 120) // 2
    root.geometry(f"280x120+{x}+{y}")

    frame = tk.Frame(root, padx=20, pady=15)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="WeakPass 运行中", font=("Microsoft YaHei", 12, "bold")).pack()
    tk.Label(frame, text=f"端口: {PORT}", fg="gray").pack(pady=(2, 10))

    btn_frame = tk.Frame(frame)
    btn_frame.pack(fill="x")

    tk.Button(
        btn_frame, text="打开界面", width=10,
        command=lambda: webbrowser.open(URL)
    ).pack(side="left", padx=(0, 10))

    tk.Button(
        btn_frame, text="退出", width=10,
        command=lambda: os._exit(0)
    ).pack(side="right")

    root.mainloop()


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


if __name__ == "__main__":
    if is_port_in_use(PORT):
        show_error(f"Port {PORT} is already in use.\nPlease close the other program and try again.")
        raise SystemExit(1)

    try:
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        if wait_for_server():
            open_browser()
        else:
            show_error(f"Failed to start WeakPass at {URL}")
            raise SystemExit(1)
        run_control_window()
    except Exception:
        print(f"WeakPass running at {URL}")
        print("Press Ctrl+C to stop")
        try:
            run_flask()
        except KeyboardInterrupt:
            pass
