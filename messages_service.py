from flask import Flask, jsonify
from threading import Thread
from kafka import KafkaConsumer
import os
import uuid

app = Flask(__name__)
messages = []

KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092', 'localhost:9093', 'localhost:9094']

def consume_messages():
    consumer = KafkaConsumer(
        'test_topic',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=f'my-group-{uuid.uuid4()}',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )
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

if __name__ == '__main__':
    start_kafka_thread()
    port = int(os.environ.get("PORT", 5004))
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)

