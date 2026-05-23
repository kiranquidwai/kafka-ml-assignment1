# Real-Time Streaming with Apache Kafka

## Assignment 1

In this project, I have used Apache Kafka, Confluent Cloud, Faust, and Python for real-time streaming. For which I have used bike rental data as live Kafka events, also performed machine learning predictions in real time, then published the predicted results to an output topic.

---

# Dataset:

## Bike Sharing Dataset

Link:
https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset

File used:

```text
hour.csv
```

This dataset has hourly bike rental records, also the weather and seasonal information.

### Features Used

* season
* yr
* mnth
* hr
* holiday
* weekday
* workingday
* weathersit
* temp
* atemp
* hum
* windspeed

### Target Variable

```text
cnt
```

Here I have used machine learning to predict the hourly bike rental count.

---

# Streams Library Used

## Python + Faust (`faust-streaming`)

This project uses the Faust Streams API with the `@app.agent` decorator.

The Faust processor:

1. Used live events from the Kafka `raw-data` topic
2. Loaded a pre-trained machine learning model
3. Predicted bike rental demand in real time
4. Sent prediction results to the Kafka `predictions` topic

---

# Machine Learning Model Performance

## Model

* Algorithm: Random Forest Regressor
* Task Type: Regression
* Training Split: 80% training / 20% testing
* Model File: `model/bike_model.pkl`

## Performance Metrics

* MAE: 24.90
* RMSE: 42.07
* R² Score: 0.9441

The model was trained offline in:

```text
train_model.py
```

and loaded inside the Faust stream processor during real-time execution.

---

# Project Structure

```text
kafka-ml-assignment/
├── data/
│   └── hour.csv
├── model/
│   └── bike_model.pkl
│   └── train_model.py    # trains ML model offline
├── producer.py           # streams dataset rows to raw-data topic
├── processor.py          # Faust Streams processor and ML inference
├── consumer.py           # reads predictions topic and prints results
├── config.py             # loads Kafka configuration
├── requirements.txt
└── README.md
```

---

# Kafka Topics

| Topic       | Purpose                            |
| ----------- | ---------------------------------- |
| raw-data    | Receives streamed bike rental rows |
| predictions | Stores ML prediction results       |

---

# Setup Steps

## 1. Create Virtual Environment

```bash
python -m venv venv
```

## 2. Activate Virtual Environment

Windows:

```bash
.\venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Create `.env` File

Create a `.env` file in the project root directory:

```env
KAFKA_BOOTSTRAP_SERVERS= bootstrap_server
KAFKA_API_KEY= API_key
KAFKA_API_SECRET= API_secret
```

## 5. Download Dataset

Download the Bike Sharing Dataset from UCI and place:

```text
hour.csv
```

inside:

```text
data/
```

## Train the ML Model

```bash
python train_model.py
```

This generates:

```text
model/bike_model.pkl
```

---

# How to Run Each Component

Open three separate terminals.

Activate the virtual environment in each terminal before running commands.

---

## Terminal 1 — Start Faust Streams Processor

```bash
faust -A processor worker -l info
```

Wait until the worker is ready before continuing.

---

## Terminal 2 — Start Consumer

```bash
python consumer.py
```

The consumer listens to the `predictions` topic and prints prediction results in real time.

---

## Terminal 3 — Start Producer

```bash
python producer.py
```

The producer streams dataset rows one by one into the Kafka `raw-data` topic at approximately one row per second.

---

# Expected Output

## Producer Output

```text
[SENT] Row 0 | Hour: 0.0 | Actual: 16.0
[SENT] Row 1 | Hour: 1.0 | Actual: 40.0
```

## Processor Output

```text
[PREDICTED] Row 0 | Hour: 0.0 | Actual: 16.0 | Predicted: 24.56
[PREDICTED] Row 1 | Hour: 1.0 | Actual: 40.0 | Predicted: 34.94
```

## Consumer Output

```text
[OUTPUT] Row 0 | Hour: 0.0 | Actual: 16.0 | Predicted: 24.56
[OUTPUT] Row 1 | Hour: 1.0 | Actual: 40.0 | Predicted: 34.94
```

---

# Real-Time Pipeline Architecture

```text
Bike Sharing Dataset
        ↓
producer.py
        ↓
Kafka Topic: raw-data
        ↓
Faust Streams Processor
        ↓
Machine Learning Prediction
        ↓
Kafka Topic: predictions
        ↓
consumer.py
```

---

# Video Demo

Demo video link: https://1drv.ms/v/c/bf0d7750d7656aae/IQAZP69SBvYmRqpoJXFQDDPiAROcm3zbI-39g4EetgZgrHQ?e=495sCX

---

# Dependencies

* faust-streaming
* aiokafka
* kafka-python
* confluent-kafka
* pandas
* scikit-learn
* joblib
* python-dotenv
* certifi
