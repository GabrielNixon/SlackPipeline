from system_summary_agent import summarize_from_json

TOOL_REGISTRY = {
    "slack_summary": {
        "function": summarize_from_json,
        "description": "Summarizes system metrics from Slack JSON logs between given start and end date.",
        "args": ["start_date", "end_date"]
    }
}
