from flask import Flask, request

app = Flask(__name__)
logs = {}

@app.route('/log', methods=['POST'])
def log_message():
    data = request.json
    msg_id = data["id"]
    if msg_id in logs:
        return "Duplicate message ignored\n", 200
    logs[msg_id] = data["msg"]
    print(f"Logged: {data['msg']}")
    return "Logged", 200

@app.route('/logs', methods=['GET'])
def get_logs():
    return " ".join(logs.values())


if __name__ == '__main__':
    app.run(port=5001, debug=True)
