from flask import Flask, jsonify
from threading import Thread
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import consul
import uuid
import time
import os

app = Flask(__name__)
messages = []

consul_client = consul.Consul(host="consul")

def get_members(key):
    data = None
    while data is None:
        index, data = consul_client.kv.get(key)
        time.sleep(5)
    return data['Value'].decode().split(",")

KAFKA_BOOTSTRAP_SERVERS = get_members('kafka/bootstrap_servers')

def register_service(service_name, service_id, service_port):
    """Реєстрація сервісу в Consul."""
    consul_client.agent.service.register(
        service_name,
        service_id=service_id,
        port=service_port,
        tags=["api"],
        check=consul.Check.http(f'http://{service_id}:{service_port}/health', interval="10s")
    )

def get_kafka_consumer():
    consumer = None
    while not consumer:
        try:
            consumer = KafkaConsumer(
                'test_topic',
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                group_id="my-consumer-group",  # Same group id for all instances
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: x.decode('utf-8')
            )
        except NoBrokersAvailable:
            print("Kafka not ready, retrying...")
            time.sleep(5)
    return consumer

def consume_messages():
    print("starting thread")
    consumer = get_kafka_consumer()
    print("consumer created")
    for message in consumer:
        print(f"[Kafka] Отримано повідомлення: {message.value}")
        messages.append(message.value)

@app.route('/message', methods=['GET'])
def get_messages():
    return jsonify(" ".join(messages)), 200

def start_kafka_thread():
    consumer_thread = Thread(target=consume_messages)
    consumer_thread.daemon = True
    consumer_thread.start()

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    start_kafka_thread()
    port = int(os.getenv("PORT", ""))
    service_name = os.getenv("SERVICE_NAME", "")
    register_service("messages_service", service_name, port)
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)

