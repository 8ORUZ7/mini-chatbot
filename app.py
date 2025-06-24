from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Handles CORS for all routes

# Your Google Apps Script Web App endpoint
APPS_SCRIPT_ENDPOINT = "https://script.google.com/macros/s/AKfycbzICKJZzRUzLu_VgR-N3ccbjZVq7NMU_tfkv4NnXpSunkARdLSesttJ3RskZvKLw5KX/exec"

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("msg")
    try:
        # Forward to Google Apps Script (which calls Gemini)
        response = requests.post(
            APPS_SCRIPT_ENDPOINT,
            json={ "msg": user_msg },
            timeout=30
        )
        response.raise_for_status()
        # Expecting JSON: { "reply": "..." }
        data = response.json()
        reply = data.get("reply", "No reply received.")
        return jsonify({ "reply": reply })
    except Exception as e:
        # Catch all errors: network, JSON, etc.
        return jsonify({ "reply": f"⚠️ Server Error: {str(e)}" }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)