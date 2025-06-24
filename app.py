from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) 

APPS_SCRIPT_ENDPOINT = "https://script.google.com/macros/s/AKfycbx_X1xsemDfdnS1dFuPup7cCFch-t5I62gkv-kQfxsPMPxOMNzzgoVmfbeMDNK-NNzx/exec"

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("msg")
    try:

        response = requests.post(
            APPS_SCRIPT_ENDPOINT,
            json={ "msg": user_msg },
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        reply = data.get("reply", "No reply received.")
        return jsonify({ "reply": reply })
    except Exception as e:

        return jsonify({ "reply": f"⚠️ Server Error: {str(e)}" }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
