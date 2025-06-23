from tools.slack_summary.tool import summarize_slack_data

TOOL_REGISTRY = {
    "slack_summary": {
        "function": summarize_slack_data,
        "description": "Summarizes system stats from synthetic Slack data between two dates.",
        "args": ["start_date", "end_date"]
    }
}
