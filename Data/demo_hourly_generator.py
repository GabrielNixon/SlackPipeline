import json
import random
import time
from datetime import datetime, timedelta

def generate_synthetic_hourly_report(timestamp):
    return {
        "timestamp": timestamp.isoformat() + "Z",
        "system": "DemoSystem",
        "type": "hourly",
        "cpu": {
            "utilization_percent": round(85 + random.uniform(-3, 6), 2),
            "queue_days": round(1.8 + random.uniform(-0.4, 0.6), 2)
        },
        "gpu": {
            "utilization_percent": round(88 + random.uniform(-2.5, 5), 2),
            "queue_days": round(4.5 + random.uniform(-1.0, 1.8), 2)
        }
    }

current_time = datetime.utcnow()

while True:
    report = generate_synthetic_hourly_report(current_time)
    with open("demo_hourly_latest.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Generated new hourly report at", current_time.isoformat())
    current_time += timedelta(hours=1)
    time.sleep(3600) 
