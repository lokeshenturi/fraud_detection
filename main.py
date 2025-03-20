from flask import Flask, render_template, send_from_directory
import webbrowser
import threading
import subprocess
import os
import time
import socket

app = Flask(__name__)

# ✅ Define correct file paths for app1.py and app2.py
FRAUD_APP_PATH = r"C:\Users\lokil\OneDrive\Desktop\project\Fraud\MAIN PROJECT\app1.py"
REVIEW_APP_PATH = r"C:\Users\lokil\OneDrive\Desktop\project\Fake-Review-detection-using-ML-main\app2.py"

# ✅ Define ports for both apps
FRAUD_DETECTION_PORT = 5003
FAKE_REVIEW_PORT = 5002

# ✅ Function to check if a port is open (ensures app started)
def wait_for_port(port, timeout=60):
    """Wait until a given port is open, indicating the app is running."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return True  # Port is open (app running)
        time.sleep(2)
    return False  # Timeout reached (app failed to start)

# ✅ Function to start the Fraud Detection App
def start_fraud_detection():
    if os.path.exists(FRAUD_APP_PATH):
        print("🚀 Starting Fraud Detection App...")
        with open("fraud_output.log", "w") as out, open("fraud_error.log", "w") as err:
            process = subprocess.Popen(
                ["python", FRAUD_APP_PATH],
                shell=True,
                cwd=os.path.dirname(FRAUD_APP_PATH),
                stdout=out,
                stderr=err,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

        # ✅ Wait until the app starts successfully
        if wait_for_port(FRAUD_DETECTION_PORT):
            print(f"✅ Fraud Detection running on port {FRAUD_DETECTION_PORT}")
        else:
            print(f"❌ Fraud Detection failed to start. Check fraud_error.log")
    else:
        print(f"❌ Error: Fraud Detection App not found at {FRAUD_APP_PATH}")

# ✅ Function to start the Fake Review Detection App
def start_fake_review():
    if os.path.exists(REVIEW_APP_PATH):
        print("🚀 Starting Fake Review Detection App...")
        with open("review_output.log", "w") as out, open("review_error.log", "w") as err:
            subprocess.Popen(
                ["python", REVIEW_APP_PATH],
                shell=True,
                cwd=os.path.dirname(REVIEW_APP_PATH),
                stdout=out,
                stderr=err,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

        # ✅ Wait until the app starts successfully
        if wait_for_port(FAKE_REVIEW_PORT):
            print(f"✅ Fake Review Detection running on port {FAKE_REVIEW_PORT}")
        else:
            print(f"❌ Fake Review Detection failed to start. Check review_error.log")
    else:
        print(f"❌ Error: Fake Review App not found at {REVIEW_APP_PATH}")

# ✅ Route to serve the favicon (Prevents 404 errors)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# ✅ Main Home Route
@app.route("/")
def home():
    return render_template("main.html", 
        fraud_url=f"http://127.0.0.1:{FRAUD_DETECTION_PORT}/",
        review_url=f"http://127.0.0.1:{FAKE_REVIEW_PORT}/"
    )

# ✅ Function to open the browser automatically in Google Chrome
def open_browser():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Default Chrome path
    url = "http://127.0.0.1:5000/"

    if os.path.exists(chrome_path):  
        subprocess.Popen([chrome_path, url], shell=True)  # Open Chrome with URL
    else:
        print("❌ Google Chrome not found. Opening in default browser instead.")
        webbrowser.open_new(url)  # Fallback to default browser

if __name__ == "__main__":
    threading.Timer(1.25, open_browser).start()  # Open browser after delay

    # ✅ Start both Flask apps in separate threads
    fraud_thread = threading.Thread(target=start_fraud_detection, daemon=True)
    review_thread = threading.Thread(target=start_fake_review, daemon=True)

    fraud_thread.start()
    review_thread.start()

    # ✅ Run the main Flask app
    app.run(host="127.0.0.1", port=5000, debug=False)
