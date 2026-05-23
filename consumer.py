import json
from confluent_kafka import Consumer
from config import BOOTSTRAP_SERVER, API_KEY, API_SECRET, PREDICTIONS_TOPIC

consumer_config = {
    "bootstrap.servers": BOOTSTRAP_SERVER,
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": API_KEY,
    "sasl.password": API_SECRET,
    "group.id": "bike-output-consumer",
    "auto.offset.reset": "latest",
}

consumer = Consumer(consumer_config)
consumer.subscribe([PREDICTIONS_TOPIC])

print("Waiting for predictions...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        result = json.loads(msg.value().decode("utf-8"))

        print(
            f"[OUTPUT] Row {result['row_index']} | "
            f"Hour: {result['hour']} | "
            f"Actual: {result['actual_count']} | "
            f"Predicted: {result['predicted_count']}"
        )

except KeyboardInterrupt:
    print("Consumer stopped.")

finally:
    consumer.close()