import json
import pandas as pd
from datetime import datetime
from transformers import pipeline

with open("../Data/demo_hourly_5months.json", "r") as f:
    data = json.load(f)

df = pd.json_normalize(data)
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.sort_values("timestamp")

def get_datetime(prompt):
    while True:
        try:
            return pd.to_datetime(input(prompt)).tz_localize("UTC")
        except Exception:
            print("Invalid format. Please use YYYY-MM-DD.")

start_time = get_datetime("Enter start date (YYYY-MM-DD): ")
end_time = get_datetime("Enter end date (YYYY-MM-DD): ")

filtered = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

if filtered.empty:
    print(f"No data found between {start_time.date()} and {end_time.date()}.")
else:
    cpu_avg = filtered["cpu.utilization_percent"].mean()
    gpu_avg = filtered["gpu.utilization_percent"].mean()
    cpu_max_q = filtered["cpu.queue_days"].max()
    gpu_max_q = filtered["gpu.queue_days"].max()
    cpu_min_q = filtered["cpu.queue_days"].min()
    gpu_min_q = filtered["gpu.queue_days"].min()
    cpu_days_below_80 = (filtered["cpu.utilization_percent"] < 80).sum()
    gpu_days_below_80 = (filtered["gpu.utilization_percent"] < 80).sum()
    cpu_q_below_1 = (filtered["cpu.queue_days"] < 1).sum()
    gpu_q_below_1 = (filtered["gpu.queue_days"] < 1).sum()

    if cpu_avg > 90 and gpu_avg > 90:
        utilization_comment = "Both CPU and GPU resources are highly utilized."
    elif cpu_avg > 85 or gpu_avg > 85:
        utilization_comment = "At least one of CPU or GPU is under heavy usage."
    else:
        utilization_comment = "Utilization is moderate."

    if gpu_max_q > cpu_max_q + 2:
        queue_comment = "GPU queue times are significantly higher than CPU."
    elif cpu_max_q > gpu_max_q + 2:
        queue_comment = "CPU queue is relatively more congested."
    else:
        queue_comment = "Queue times are fairly balanced."

    summary = f"""
System Summary: {start_time.date()} to {end_time.date()}

Average CPU Utilization: {cpu_avg:.2f}%
Average GPU Utilization: {gpu_avg:.2f}%

Max CPU Queue Time: {cpu_max_q:.2f} days
Min CPU Queue Time: {cpu_min_q:.2f} days
Max GPU Queue Time: {gpu_max_q:.2f} days
Min GPU Queue Time: {gpu_min_q:.2f} days

Days with CPU Utilization < 80%: {cpu_days_below_80}
Days with GPU Utilization < 80%: {gpu_days_below_80}
Days with CPU Queue < 1 day: {cpu_q_below_1}
Days with GPU Queue < 1 day: {gpu_q_below_1}

Insights:
- {utilization_comment}
- {queue_comment}
"""

    print(summary)

    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=0)
    ai_summary = summarizer(summary.strip(), max_length=100, min_length=30, do_sample=False)[0]["summary_text"]

    print("\nAI Summary:")
    print(ai_summary)
