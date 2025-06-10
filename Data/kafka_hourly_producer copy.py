import json
import pandas as pd
from datetime import datetime

# === Load JSON Data ===
with open("Data/demo_hourly_5months.json", "r") as f:
    data = json.load(f)

# === Normalize & Preprocess ===
df = pd.json_normalize(data)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# === Prompt User for Time Range ===
def get_datetime(prompt):
    while True:
        try:
            return pd.to_datetime(input(prompt))
        except Exception:
            print("Invalid format. Please use YYYY-MM-DD.")

start_time = get_datetime("Enter start date (YYYY-MM-DD): ")
end_time = get_datetime("Enter end date (YYYY-MM-DD): ")

# === Filter for Time Range ===
filtered = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

if filtered.empty:
    print(f"\n No data found between {start_time.date()} and {end_time.date()}.")
else:
    # === Compute Summary Stats ===
    cpu_avg = filtered["cpu.utilization"].mean()
    gpu_avg = filtered["gpu.utilization"].mean()
    cpu_max_queue = filtered["cpu.queue_days"].max()
    gpu_max_queue = filtered["gpu.queue_days"].max()

    # === Create Summary ===
    summary = f"""
System Summary from {start_time.date()} to {end_time.date()}:

Average CPU Utilization: {cpu_avg:.2f}%
Average GPU Utilization: {gpu_avg:.2f}%

Max CPU Queue Time: {cpu_max_queue:.2f} days
Max GPU Queue Time: {gpu_max_queue:.2f} days

Insight: The system remained heavily utilized throughout the period, with queue times occasionally spiking, especially on the GPU side.
"""
    print(summary)
