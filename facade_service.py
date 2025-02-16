from flask import Flask, request, jsonify
import time
import requests
import uuid

app = Flask(__name__)

MAX_RETRIES = 10
RETRY_DELAY = 2
LOGGING_SERVICE_URL = "http://localhost:5001"
MESSAGES_SERVICE_URL = "http://localhost:5002"

@app.route('/post', methods=['POST'])
def post_message():
    data = request.json
    msg = data.get("msg")
    if not msg:
        return jsonify({"error": "Message is required"}), 400
    msg_id = str(uuid.uuid4())
    payload = {"id": msg_id, "msg": msg}
    log_to_service = lambda : requests.post(f"{LOGGING_SERVICE_URL}/log", json=payload, timeout=5)
    check, _ = send_request(log_to_service)
    if check is False:
        return jsonify({"error": f"Logging service unreachable after {MAX_RETRIES} retries"}), 50
    return jsonify(payload) 

@app.route('/get', methods=['GET'])
def get_messages():
    log_response = lambda : requests.get(f"{LOGGING_SERVICE_URL}/logs", timeout=5)
    check_log, text_log = send_request(log_response)
    if check_log is False:
        return jsonify({"error": f"Logging service unreachable after {MAX_RETRIES} retries"}), 50
    msg_response = lambda : requests.get(f"{MESSAGES_SERVICE_URL}/message", timeout=5)
    check_msg, text_msg = send_request(msg_response)
    if check_msg is False:
        return jsonify({"error": f"Logging service unreachable after {MAX_RETRIES} retries"}), 50
    return (text_log + " " + text_msg + "\n").strip(" \t")

def send_request(request_func):
    for attempt in range(MAX_RETRIES):
        try:
            response = request_func()
            if response.status_code == 200:
                return True, response.text
        except requests.exceptions.RequestException:
            if attempt < MAX_RETRIES - 1:
                print("Failed to establish connection, retrying...")
                time.sleep(RETRY_DELAY)
            else:
                return False, response.text


if __name__ == '__main__':
    app.run(port=5000, debug=True)
