from flask import Flask, request
import hazelcast
import os
import signal
import subprocess

HAZELCAST_PATH = "/home/compicraft/hazelcast/hazelcast-5.5.0/bin/hz"
app = Flask(__name__)

hz_client = None
hz_process = None
logs = None

def start_node():
    """Start the Hazelcast node process if not already running."""
    global hz_process
    if hz_process is None:
        hz_process = subprocess.Popen([HAZELCAST_PATH, "start"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Hazelcast node started.")

def stop_node():
    """Stop the Hazelcast node process."""
    global hz_process
    if hz_process:
        os.kill(hz_process.pid, signal.SIGTERM)
        print("Hazelcast node stopped.")
        hz_process = None

def init_hazelcast():
    """Initialize the Hazelcast client only if it's not already running."""
    global hz_client, logs
    if hz_client is None or not hz_client.lifecycle.is_running():
        start_node()
        hz_client = hazelcast.HazelcastClient(cluster_members=[])
        logs = hz_client.get_map("logs").blocking()
        print(f"Hazelcast client initialized in worker {os.getpid()}")

@app.route('/log', methods=['POST'])
def log_message():
    """Log a message into Hazelcast."""
    data = request.json
    logs.put(data["id"], data["msg"])
    print(f"Logged: {data['msg']}")
    return "Logged", 200

@app.route('/logs', methods=['GET'])
def get_logs():
    """Retrieve all logs from Hazelcast."""
    all_logs = dict(logs.entry_set())
    return " ".join(all_logs.values())

with app.app_context():
    init_hazelcast() 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="127.0.0.1", port=port, debug=True)
