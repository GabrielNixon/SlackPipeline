import json
import pandas as pd
from datetime import datetime

# === Load JSON Data ===
with open("demo_hourly_5months.json", "r") as f:
    data = json.load(f)

# === Normalize Nested Fields ===
df = pd.json_normalize(data)
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.sort_values("timestamp")

# === Prompt User for Time Range ===
def get_datetime(prompt):
    while True:
        try:
            return pd.to_datetime(input(prompt)).tz_localize("UTC")
        except Exception:
            print("Invalid format. Please use YYYY-MM-DD.")

start_time = get_datetime("Enter start date (YYYY-MM-DD): ")
end_time = get_datetime("Enter end date (YYYY-MM-DD): ")

# === Filter by Time Range ===
filtered = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

if filtered.empty:
    print(f"\n No data found between {start_time.date()} and {end_time.date()}.")
else:
    # === Compute Stats ===
    cpu_avg = filtered["cpu.utilization_percent"].mean()
    gpu_avg = filtered["gpu.utilization_percent"].mean()
    cpu_max_q = filtered["cpu.queue_days"].max()
    gpu_max_q = filtered["gpu.queue_days"].max()


# === Generate Contextual Insight ===
if cpu_avg > 90 and gpu_avg > 90:
    utilization_comment = "Both CPU and GPU resources seem to be nearing full capacity."
elif cpu_avg > 85 or gpu_avg > 85:
    utilization_comment = "At least one resource is showing signs of heavy usage."
else:
    utilization_comment = "Utilization levels appear moderate."

if gpu_max_q > cpu_max_q + 2:
    queue_comment = "The GPU job queue appears to experience longer delays compared to CPU."
elif cpu_max_q > gpu_max_q + 2:
    queue_comment = "The CPU job queue has been relatively more congested in this period."
else:
    queue_comment = "Queue delays are relatively balanced between CPU and GPU."

# === Build Final Summary ===
summary = f"""
System Summary from {start_time.date()} to {end_time.date()}:

Average CPU Utilization: {cpu_avg:.2f}%
Average GPU Utilization: {gpu_avg:.2f}%

Max CPU Queue Time: {cpu_max_q:.2f} days
Max GPU Queue Time: {gpu_max_q:.2f} days

Insight:
- {utilization_comment}
- {queue_comment}
"""

print(summary)
