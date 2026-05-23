import os
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").strip()
API_KEY = os.getenv("KAFKA_API_KEY", "").strip()
API_SECRET = os.getenv("KAFKA_API_SECRET", "").strip()

RAW_TOPIC = "raw-data"
PREDICTIONS_TOPIC = "predictions"