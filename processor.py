import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

import ssl
import json
import faust
import joblib
import pandas as pd

from config import BOOTSTRAP_SERVER, API_KEY, API_SECRET, RAW_TOPIC, PREDICTIONS_TOPIC

model = joblib.load("model/bike_model.pkl")
print("Bike rental prediction model loaded.")

FEATURE_COLS = [
    "season", "yr", "mnth", "hr", "holiday", "weekday",
    "workingday", "weathersit", "temp", "atemp",
    "hum", "windspeed"
]

ssl_context = ssl.create_default_context()

broker_credentials = faust.SASLCredentials(
    username=API_KEY,
    password=API_SECRET,
    ssl_context=ssl_context,
    mechanism="PLAIN",
)

app = faust.App(
    "bike-predictor",
    broker=f"kafka://{BOOTSTRAP_SERVER}",
    broker_credentials=broker_credentials,
    topic_replication_factor=3,
)

raw_topic = app.topic(RAW_TOPIC)
predictions_topic = app.topic(PREDICTIONS_TOPIC)

@app.agent(raw_topic)
async def predict(records):
    async for record in records:
        try:
            if isinstance(record, bytes):
                record = json.loads(record.decode("utf-8"))
            elif isinstance(record, str):
                record = json.loads(record)

            input_data = pd.DataFrame([{col: record[col] for col in FEATURE_COLS}])
            prediction = model.predict(input_data)[0]

            output = {
                "row_index": record.get("row_index"),
                "hour": record["hr"],
                "actual_count": record["cnt"],
                "predicted_count": round(float(prediction), 2),
            }

            await predictions_topic.send(value=json.dumps(output).encode("utf-8"))

            print(
                f"[PREDICTED] Row {output['row_index']} | "
                f"Hour: {output['hour']} | "
                f"Actual: {output['actual_count']} | "
                f"Predicted: {output['predicted_count']}"
            )

        except Exception as e:
            print(f"[ERROR] {e} — skipping record")

if __name__ == "__main__":
    app.main()