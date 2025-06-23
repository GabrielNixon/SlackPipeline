from datetime import datetime
import json
import pandas as pd
from transformers import pipeline

def summarize_slack_data(start_date: str, end_date: str) -> str:
    with open("Data/demo_hourly_5months.json", "r") as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp")

    start_time = pd.to_datetime(start_date).tz_localize("UTC")
    end_time = pd.to_datetime(end_date).tz_localize("UTC")
    filtered = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

    if filtered.empty:
        return f"No data between {start_date} and {end_date}"

    cpu_avg = filtered["cpu.utilization_percent"].mean()
    gpu_avg = filtered["gpu.utilization_percent"].mean()
    cpu_max_q = filtered["cpu.queue_days"].max()
    gpu_max_q = filtered["gpu.queue_days"].max()
    cpu_min_q = filtered["cpu.queue_days"].min()
    gpu_min_q = filtered["gpu.queue_days"].min()
    cpu_days_low_util = (filtered["cpu.utilization_percent"] < 50).sum()
    gpu_days_low_util = (filtered["gpu.utilization_percent"] < 50).sum()

    if cpu_avg > 90 and gpu_avg > 90:
        utilization_comment = "Both CPU and GPU resources are heavily loaded."
    elif cpu_avg > 85 or gpu_avg > 85:
        utilization_comment = "At least one of CPU or GPU is under heavy usage."
    else:
        utilization_comment = "Utilization levels are moderate."

    if gpu_max_q > cpu_max_q + 2:
        queue_comment = "GPU queue delays are notably higher."
    elif cpu_max_q > gpu_max_q + 2:
        queue_comment = "CPU queue is more congested."
    else:
        queue_comment = "Queue delays are balanced."

    report = f"""
System Summary: {start_date} to {end_date}

Average CPU Utilization: {cpu_avg:.2f}%
Average GPU Utilization: {gpu_avg:.2f}%

Max CPU Queue Time: {cpu_max_q:.2f} days
Min CPU Queue Time: {cpu_min_q:.2f} days
Max GPU Queue Time: {gpu_max_q:.2f} days
Min GPU Queue Time: {gpu_min_q:.2f} days

Days CPU <50%: {cpu_days_low_util} | GPU <50%: {gpu_days_low_util}

Insights:
- {utilization_comment}
- {queue_comment}
""".strip()

    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device="mps")
    short = summarizer(report, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]

    return f"{report}\n\nAI Summary:\n{short}"
