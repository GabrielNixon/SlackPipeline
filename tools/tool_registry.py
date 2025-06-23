from system_summary_agent import summarize_from_json

def filter_args(func, args_dict):
    allowed = func.__code__.co_varnames[:func.__code__.co_argcount]
    return {k: v for k, v in args_dict.items() if k in allowed}

TOOL_REGISTRY = {
    "slack_summary": {
        "function": lambda **kwargs: summarize_from_json(**filter_args(summarize_from_json, kwargs)),
        "args": ["start_date", "end_date"]
    }
}
