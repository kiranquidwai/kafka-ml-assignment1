import json
import time
import pandas as pd
from confluent_kafka import Producer
from config import BOOTSTRAP_SERVER, API_KEY, API_SECRET, RAW_TOPIC

producer_config = {
    "bootstrap.servers": BOOTSTRAP_SERVER,
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": API_KEY,
    "sasl.password": API_SECRET,
}

producer = Producer(producer_config)

df = pd.read_csv("data/hour.csv")

features = [
    "season", "yr", "mnth", "hr", "holiday", "weekday",
    "workingday", "weathersit", "temp", "atemp", "hum", "windspeed", "cnt"
]

for index, row in df[features].iterrows():
    event = row.to_dict()
    event["row_index"] = int(index)

    producer.produce(
        RAW_TOPIC,
        key=str(event["row_index"]),
        value=json.dumps(event),
    )

    producer.flush()

    print(f"[SENT] Row {event['row_index']} | Hour: {event['hr']} | Actual: {event['cnt']}")
    time.sleep(1)