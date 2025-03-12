from flask import Flask, request, jsonify
import time
import requests
import uuid
import random


app = Flask(__name__)

MAX_RETRIES = 10
RETRY_DELAY = 2
LOGGING_SERVICES = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]
MESSAGES_SERVICE_URL = "http://localhost:5004"

def get_available_service():
    """Випадково вибирає logging-service та перевіряє його доступність."""
    random.shuffle(LOGGING_SERVICES)
    for service in LOGGING_SERVICES:
        try:
            response = requests.get(f"{service}/logs", timeout=1)
            if response.status_code == 200:
                return service
        except requests.exceptions.RequestException:
            continue
    return None

@app.route('/post', methods=['POST'])
def post_message():
    data = request.json
    msg = data.get("msg")
    if not msg:
        return jsonify({"error": "Message is required"}), 400
    selected_service = get_available_service()
    if not selected_service:
        return jsonify({"error": "No available logging-service"}), 503
    msg_id = str(uuid.uuid4())
    payload = {"id": msg_id, "msg": msg}
    log_to_service = requests.post(f"{selected_service}/log", json=payload, timeout=5)
    if log_to_service.status_code != 200:
        return jsonify({"error": f"Logging service unreachable after {MAX_RETRIES} retries"}), 50
    return jsonify(payload) 

@app.route('/get', methods=['GET'])
def get_messages():
    selected_service = get_available_service()
    if not selected_service:
        return jsonify({"error": "No available logging-service"}), 503
    log_response = requests.get(f"{selected_service}/logs", timeout=5)
    if log_response.status_code != 200:
        return jsonify({"error": f"Logging service unreachable after {MAX_RETRIES} retries"}), 50
    msg_response = requests.get(f"{MESSAGES_SERVICE_URL}/message", timeout=5)
    if msg_response.status_code != 200:
        return jsonify({"error": f"Logging service unreachable after {MAX_RETRIES} retries"}), 50
    return (log_response.text + " " + msg_response.text + "\n").strip(" \t")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
