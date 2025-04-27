from flask import Flask, request
import hazelcast
import os
import consul
import time
app = Flask(__name__)

hz_client = None
logs = None

consul_client = consul.Consul(host="consul")

def get_members(key):
    data = None
    while data is None:
        index, data = consul_client.kv.get(key)
        time.sleep(5)
    return data['Value'].decode().split(",")

cluster_members = get_members('hazelcast/cluster_members')

def register_service(service_name, service_id, service_port):
    """Реєстрація сервісу в Consul."""
    consul_client.agent.service.register(
        service_name,
        service_id=service_id,
        port=service_port,
        tags=["api"],
        check=consul.Check.http(f'http://{service_id}:{service_port}/health', interval="1s")
    )

def init_hazelcast():
    """Initialize the Hazelcast client only if it's not already running."""
    global hz_client, logs
    if hz_client is None:
        print("connecting to hazelcast")
        hz_client = hazelcast.HazelcastClient(cluster_members=cluster_members)
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

@app.route('/health')
def health_check():
    return "OK", 200

with app.app_context():
    init_hazelcast()

if __name__ == "__main__":
    port = int(os.getenv("PORT", ""))
    service_name = os.getenv("SERVICE_NAME", "")
    port = int(os.environ.get("PORT", 5001))
    register_service("logging_service", service_name, port)
    # init_hazelcast()
    app.run(host="0.0.0.0", port=port, debug=True)
