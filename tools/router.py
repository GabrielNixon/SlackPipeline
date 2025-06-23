import re
import dateparser
from datetime import datetime, timedelta

def parse_natural_date_range(text):
    if "last week" in text.lower():
        today = datetime.now()
        start = today - timedelta(days=7)
        end = today
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

    match = re.search(r"(?:from|between)?\s*(\w+\s*\d{4})", text)
    if match:
        try:
            start = dateparser.parse(match.group(1))
            if start:
                end = start.replace(day=28) + timedelta(days=4)
                end = end - timedelta(days=end.day)
                return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
        except:
            pass

    dates = dateparser.search.search_dates(text)
    if dates and len(dates) >= 1:
        start = dates[0][1]
        end = dates[1][1] if len(dates) > 1 else start
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

    return None, None

def simple_router(query):
    fields = []
    if "cpu" in query.lower():
        fields.append("cpu")
    if "gpu" in query.lower():
        fields.append("gpu")
    if "summary" in query.lower() or "report" in query.lower():
        fields.append("summary")
    if "down" in query.lower() or "less than" in query.lower():
        fields.append("low_days")

    start, end = parse_natural_date_range(query)
    return {
        "tool": "slack_summary",
        "args": {
            "start_date": start,
            "end_date": end,
            "fields": fields
        }
    }
