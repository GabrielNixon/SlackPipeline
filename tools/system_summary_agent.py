import json
import pandas as pd
from datetime import datetime
from transformers import pipeline

with open("../Data/demo_hourly_5months.json", "r") as f:
    data = json.load(f)

df = pd.json_normalize(data)
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.sort_values("timestamp")

def summarize_from_json(start_date, end_date, fields=None):
    start_time = pd.to_datetime(start_date).tz_localize("UTC")
    end_time = pd.to_datetime(end_date).tz_localize("UTC")
    filtered = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

    if filtered.empty:
        return f"No data found between {start_date} and {end_date}."

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

    utilization_comment = (
        "Both CPU and GPU resources are highly utilized."
        if cpu_avg > 90 and gpu_avg > 90 else
        "At least one of CPU or GPU is under heavy usage."
        if cpu_avg > 85 or gpu_avg > 85 else
        "Utilization is moderate."
    )

    queue_comment = (
        "GPU queue times are significantly higher than CPU."
        if gpu_max_q > cpu_max_q + 2 else
        "CPU queue is relatively more congested."
        if cpu_max_q > gpu_max_q + 2 else
        "Queue times are fairly balanced."
    )

    output = f"System Summary: {start_date} to {end_date}\n\n"

    if not fields or "cpu" in fields or "summary" in fields:
        output += f"Average CPU Utilization: {cpu_avg:.2f}%\n"
        output += f"Max CPU Queue Time: {cpu_max_q:.2f} days\n"
        output += f"Min CPU Queue Time: {cpu_min_q:.2f} days\n"
        output += f"Days with CPU Utilization < 80%: {cpu_days_below_80}\n"
        output += f"Days with CPU Queue < 1 day: {cpu_q_below_1}\n"

    if not fields or "gpu" in fields or "summary" in fields:
        output += f"Average GPU Utilization: {gpu_avg:.2f}%\n"
        output += f"Max GPU Queue Time: {gpu_max_q:.2f} days\n"
        output += f"Min GPU Queue Time: {gpu_min_q:.2f} days\n"
        output += f"Days with GPU Utilization < 80%: {gpu_days_below_80}\n"
        output += f"Days with GPU Queue < 1 day: {gpu_q_below_1}\n"

    output += f"\nInsights:\n- {utilization_comment}\n- {queue_comment}"

    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=0)
    ai_summary = summarizer(output.strip(), max_length=100, min_length=30, do_sample=False)[0]["summary_text"]

    output += f"\n\nAI Summary:\n{ai_summary}"

    return output
