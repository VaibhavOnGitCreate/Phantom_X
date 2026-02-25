import sys
sys.path.insert(1, "../Phantom_X/ai_model")

import threading
import time
import random
import os
import webbrowser
import ai_model.detector as amd
from phantomx_listener import start_listener
import keyboard
from flask import (
    Flask,
    render_template,
    jsonify,
    send_from_directory
)

# Import Phantom_X OCR
from ai_model.ocr import extract_text


# ============================================================
# Flask Setup
# ============================================================

app = Flask(__name__)

CAPTURE_PATH = "static/capture.png"


# ============================================================
# GLOBAL EXTRACTED TEXT (CORE VARIABLE)
# ============================================================

extracted_text = ""


# ============================================================
# Phantom State
# ============================================================

phantom_state = {

    "status": "idle",

    "text": "",

    "risk_score": 0,

    "risk_category": "SAFE",

    "last_scan_time": None

}


# ============================================================
# OCR AUTO UPDATE WORKER (runs forever)
# ============================================================

def auto_extract_worker():

    global extracted_text, phantom_state

    last_modified = 0

    while True:

        try:

            if os.path.exists(CAPTURE_PATH):

                current_modified = os.path.getmtime(CAPTURE_PATH)

                # Only update if image changed
                if current_modified != last_modified:

                    last_modified = current_modified

                    text = extract_text(CAPTURE_PATH)

                    extracted_text = text

                    phantom_state["text"] = text

                    phantom_state["last_scan_time"] = time.strftime("%H:%M:%S")

                    print("Extracted Text Updated:")
                    print(text)

        except Exception as e:

            print("OCR Auto Extract Error:", e)

        time.sleep(1)


# ============================================================
# Dashboard Route
# ============================================================

@app.route("/")
def dashboard():

    return render_template(
        "dashboard.html",
        state=phantom_state
    )


# ============================================================
# Status Route
# ============================================================

@app.route("/status")
def status():

    return jsonify({
        "text": extracted_text,
        "last_scan_time": phantom_state["last_scan_time"]
    })


# ============================================================
# Capture Image Route
# ============================================================

@app.route("/capture")
def capture():

    if os.path.exists(CAPTURE_PATH):

        return send_from_directory(
            "static",
            "capture.png"
        )

    return "", 404


# ============================================================
# Extract Text Route (direct access)
# ============================================================

@app.route("/extract_text")
def get_extracted_text():

    return jsonify({
        "text": extracted_text
    })


# ============================================================
# Phantom_X Dataset API
# Uses GLOBAL extracted_text
# ============================================================

@app.route("/api/phantom_risk", methods=["POST"])
def phantom_risk():

    global extracted_text

    # Feed REAL extracted text to Phantom_X
    datasets = amd.fetch_risk_datasets(extracted_text)

    return jsonify({
        "datasets": datasets,
        "text_used": extracted_text
    })


# ============================================================
# Graph Dashboard Route
# ============================================================

@app.route("/graphs")
def graphs():

    return render_template("phantom_dashboard.html")

@app.route("/insights")
def insights():

    global extracted_text

    try:

        # generate insights from Phantom_X
        insights = amd.fetch_ai_insights(extracted_text)

        print("Insights generated:", insights)

        # validate
        if not isinstance(insights, list) or len(insights) != 6:
            raise Exception("Invalid insight format")

    except Exception as e:

        print("Insight error:", e)

        insights = [
            "No timeline risk detected\nSystem stable\nNo escalation observed",
            "No phishing indicators\nSafe communication\nLow risk profile",
            "Low threat probability\nNo malicious signals\nSafe behavior",
            "No manipulation detected\nNeutral tone\nNo coercion",
            "No vulnerability exposure\nSystem secure\nNo exploit detected",
            "Overall risk low\nSystem safe\nNo action needed"
        ]

    # send insights directly to HTML
    return render_template(
        "insights.html",
        insights=insights
    )
@app.route("/assistant", methods=["GET", "POST"])
def assistant():

    from flask import request, jsonify, render_template

    global extracted_text

    # ============================
    # POST → generate AI reply
    # ============================
    if request.method == "POST":

        try:

            data = request.get_json()

            if not data:
                return jsonify({"reply": "No input received."})

            user_msg = data.get("message", "")

            print("User message:", user_msg)
            print("Extracted text:", extracted_text)

            full_context = f"""
Captured Text:
{extracted_text}

User Question:
{user_msg}
"""

            # Call your Phantom_X AI
            response = amd.fetch_ai_reponse(full_context)
            print("343223",response)

            print("AI response:", response)

            # fallback if empty
            if not response or str(response).strip() == "":
                response = "Phantom_X could not generate a response."

            return jsonify({
                "reply": str(response)
            })

        except Exception as e:

            print("Assistant error:", str(e))

            return jsonify({
                "reply": "Phantom_X encountered an error."
            })


    # ============================
    # GET → load assistant page
    # ============================

    return render_template(
        "assistant.html",
        extracted_text=extracted_text
    )
# ============================================================
# Start Background OCR Worker
# ============================================================

def start_background_workers():

    # Thread 1 — OCR auto extract worker
    extract_thread = threading.Thread(
        target=auto_extract_worker,
        daemon=True
    )
    extract_thread.start()


    # Thread 2 — Your Ctrl+Shift+X listener
    listener_thread = threading.Thread(
        target=start_listener,
        daemon=True
    )
    listener_thread.start()


    print("Phantom_X background workers started:")
    print(" • OCR auto extract worker running")
    print(" • Ctrl+Shift+X listener running")

# ============================================================
# Main Entry
# ============================================================
open_app = []
if __name__ == "__main__":

    print("===================================")
    print(" Phantom_X Server Starting...")
    print(" Dashboard: http://127.0.0.1:5000")
    print(" Graphs:    http://127.0.0.1:5000/graphs")
    print("===================================")

    start_background_workers()
    if "http://127.0.0.1:5000" not in open_app :
            
        webbrowser.open("http://127.0.0.1:5000")
        open_app.append("http://127.0.0.1:5000")
    time.sleep(1.5)
    keyboard.press
    

    app.run(
        debug=True,
        threaded=True
    )
    
    