from system_summary_agent import summarize_from_json

TOOL_REGISTRY = {
    "slack_summary": {
        "function": summarize_from_json,
        "args": ["start_date", "end_date"],
    }
}
