import json
import random
import time
from datetime import datetime, timedelta
import os

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
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hourly")
os.makedirs(output_dir, exist_ok=True)

while True:
    report = generate_synthetic_hourly_report(current_time)
    filename = f"demo_hourly_{current_time.strftime('%Y%m%dT%H%M%SZ')}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Generated: {filepath}")

    os.system("git add .")
    os.system(f"git commit -m 'Add {filename}'")
    os.system("git push")

    current_time += timedelta(hours=1)
    time.sleep(3600)
