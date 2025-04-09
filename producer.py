from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data = {'id': 1, 'message': 'Hello Kafka!'}
producer.send('test-topic', value=data)
producer.flush()
print("Message sent.")
