from flask import Flask, request, jsonify
import requests
import uuid
import consul
import random
from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.errors import NoBrokersAvailable
import time

app = Flask(__name__)

consul_client = consul.Consul(host="consul")


def get_members(key):
    data = None
    while data is None:
        index, data = consul_client.kv.get(key)
        time.sleep(5)
    return data['Value'].decode().split(",")

KAFKA_BOOTSTRAP_SERVERS = get_members('kafka/bootstrap_servers')


def get_kafka_producer():
    producer = None
    while not producer:
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        except NoBrokersAvailable:
            print("Kafka not ready, retrying...")
            time.sleep(5)
    return producer

producer = get_kafka_producer()



def register_service(service_name, service_id, service_port):
    """Реєстрація сервісу в Consul."""
    consul_client.agent.service.register(
        service_name,
        service_id=service_id,
        port=service_port,
        tags=["api"],
        check=consul.Check.http(f'http://facade_service:{service_port}/health', interval="1s")
    )

def get_service_links_by_name(service_name):
    services = consul_client.health.service(service_name)
    return services

@app.route('/post', methods=['POST'])
def post_message():
    print("POST")
    data = request.json
    msg = data.get("msg")
    if not msg:
        return jsonify({"error": "Message is required"}), 400
    selected_service = random.choice(get_service_links_by_name("logging_service"))
    if not selected_service:
        return jsonify({"error": "No available logging-service"}), 503
    msg_id = str(uuid.uuid4())
    payload = {"id": msg_id, "msg": msg}
    log_to_service = requests.post(f"{selected_service}/log", json=payload, timeout=5)
    if log_to_service.status_code != 200:
        return jsonify({"error": f"Logging service unreachable"}), 50
    future = producer.send('test_topic', msg.encode('utf-8'))
    try:
        record_metadata = future.get(timeout=10)  # Wait for the result with a timeout
        print(f"Message sent to topic {record_metadata.topic}, partition {record_metadata.partition}, offset {record_metadata.offset}")
    except KafkaError as e:
        print(f"Error while sending message: {e}")
    return jsonify(payload) 

@app.route('/get', methods=['GET'])
def get_messages():
    selected_service = random.choice(get_service_links_by_name("logging_service"))
    if not selected_service:
        return jsonify({"error": "No available logging-service"}), 503

    selected_message_service = random.choice(get_service_links_by_name("messages_service"))
    if not selected_message_service:
        return jsonify({"error": "No available logging-service"}), 503

    log_response = requests.get(f"{selected_service}/logs", timeout=5)
    if log_response.status_code != 200:
        return jsonify({"error": f"Logging service unreachable"}), 50
    
    msg_response = requests.get(f"{selected_message_service}/message", timeout=5)
    if msg_response.status_code != 200:
        return jsonify({"error": f"Message service unreachable"}), 50
    
    return (log_response.text + " " + msg_response.text + "\n").strip(" \t")

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    register_service("facade_service", "facade_service", 5000)
    app.run(host = "0.0.0.0", port=5000, debug=True)
