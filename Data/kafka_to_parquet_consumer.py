import json
import os
import pandas as pd
from datetime import datetime
from kafka import KafkaConsumer

PARQUET_DIR = "parquet_output"
os.makedirs(PARQUET_DIR, exist_ok=True)

consumer = KafkaConsumer(
    'demo-hourly',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

batch = []

def save_batch_to_parquet(batch):
    df = pd.DataFrame(batch)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filepath = os.path.join(PARQUET_DIR, f"demo_kafka_{ts}.parquet")
    df.to_parquet(filepath, index=False)
    print(f"[Parquet] Saved {len(batch)} rows to {filepath}")

for message in consumer:
    data = message.value
    print(f"[Kafka Consumer] Received: {data}")
    batch.append(data)

    if len(batch) >= 10:
        save_batch_to_parquet(batch)
        batch = []
