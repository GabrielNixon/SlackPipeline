import dateparser
from datetime import datetime, timedelta
import pandas as pd

def parse_natural_date_range(text: str):
    text = text.lower()
    today = datetime.now()

    if "last month" in text:
        month = today.month - 1 or 12
        year = today.year if today.month != 1 else today.year - 1
        start = datetime(year, month, 1)
        end = datetime(today.year, today.month, 1) - timedelta(days=1)

    elif "this month" in text:
        start = datetime(today.year, today.month, 1)
        end = today

    elif "last week" in text:
        start = today - timedelta(days=today.weekday() + 7)
        end = start + timedelta(days=6)

    elif "this week" in text:
        start = today - timedelta(days=today.weekday())
        end = today

    elif "between" in text and "and" in text:
        parts = text.split("between")[1].split("and")
        start = dateparser.parse(parts[0].strip())
        end = dateparser.parse(parts[1].strip())

    elif "from" in text and "to" in text:
        parts = text.split("from")[1].split("to")
        start = dateparser.parse(parts[0].strip())
        end = dateparser.parse(parts[1].strip())

    elif "for" in text:
        date_text = text.split("for")[1].strip()
        parsed = dateparser.parse(date_text)
        if parsed:
            start = datetime(parsed.year, parsed.month, 1)
            if parsed.month == 12:
                end = datetime(parsed.year + 1, 1, 1) - timedelta(days=1)
            else:
                end = datetime(parsed.year, parsed.month + 1, 1) - timedelta(days=1)
        else:
            start = end = None
    else:
        start = end = None

    if start and end:
        start = pd.to_datetime(start).tz_localize("UTC")
        end = pd.to_datetime(end).tz_localize("UTC")

    return start, end


def simple_router(query: str):
    keywords = ["summary", "report", "cpu", "gpu", "utilization", "queue", "down", "days"]
    if any(word in query.lower() for word in keywords):
        return "slack_summary"
    return None
