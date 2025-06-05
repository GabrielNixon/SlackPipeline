import json
import time
import random
from datetime import datetime, timezone
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_report():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu_utilization": round(random.uniform(88, 98), 2),
        "cpu_queue_days": round(random.uniform(1.5, 4.5), 2),
        "gpu_utilization": round(random.uniform(90, 99), 2),
        "gpu_queue_days": round(random.uniform(5.0, 9.0), 2)
    }

if __name__ == "__main__":
    while True:
        report = generate_report()
        print(f"[Kafka Producer] Sent: {report}")
        producer.send("demo-hourly", value=report)
        time.sleep(3600)
