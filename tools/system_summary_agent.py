import json
import pandas as pd
from datetime import datetime
from transformers import pipeline

def summarize_from_json(start_date, end_date, cpu=False, gpu=False, summary=False, days_down=False):
    with open("../Data/demo_hourly_5months.json", "r") as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp")

    start = pd.to_datetime(start_date).tz_localize("UTC")
    end = pd.to_datetime(end_date).tz_localize("UTC")
    filtered = df[(df["timestamp"] >= start) & (df["timestamp"] <= end)]

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

    output = f"\nSystem Summary: {start.date()} to {end.date()}\n"

    if cpu:
        output += f"\nAverage CPU Utilization: {cpu_avg:.2f}%\n"
        output += f"CPU Queue Time: min {cpu_min_q:.2f} to max {cpu_max_q:.2f} days\n"
        output += f"Days with CPU Utilization < 80%: {cpu_days_below_80}\n"
        output += f"Days with CPU Queue < 1 day: {cpu_q_below_1}\n"

    if gpu:
        output += f"\nAverage GPU Utilization: {gpu_avg:.2f}%\n"
        output += f"GPU Queue Time: min {gpu_min_q:.2f} to max {gpu_max_q:.2f} days\n"
        output += f"Days with GPU Utilization < 80%: {gpu_days_below_80}\n"
        output += f"Days with GPU Queue < 1 day: {gpu_q_below_1}\n"

    if days_down:
        output += f"\nUnderload Days:\n"
        output += f"CPU Util < 80%: {cpu_days_below_80} days\n"
        output += f"GPU Util < 80%: {gpu_days_below_80} days\n"
        output += f"CPU Queue < 1 day: {cpu_q_below_1} days\n"
        output += f"GPU Queue < 1 day: {gpu_q_below_1} days\n"

    if summary or (not cpu and not gpu and not days_down):
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

        output += "\nInsights:\n"
        output += f"- {utilization_comment}\n"
        output += f"- {queue_comment}\n"

    return output.strip()
