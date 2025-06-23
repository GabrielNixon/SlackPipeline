import re
import dateparser
from datetime import datetime, timedelta, timezone

KEYWORDS = {
    "cpu": ["cpu", "processor", "core"],
    "gpu": ["gpu", "graphics", "nvidia"],
    "summary": ["summary", "report", "status", "overview"],
    "days_down": ["days down", "under", "lower than", "less than"]
}

def match_keyword(query, category):
    return any(keyword in query.lower() for keyword in KEYWORDS[category])

def parse_natural_date_range(query):
    query = query.lower()
    now = datetime.now(timezone.utc)

    if "last week" in query:
        end = now
        start = now - timedelta(days=7)
        return start, end

    match = re.search(r"last (\d+) day", query)
    if match:
        num = int(match.group(1))
        end = now
        start = end - timedelta(days=num)
        return start, end

    match = re.search(r"between (.+?) and (.+)", query)
    if match:
        start = dateparser.parse(match.group(1), settings={'TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True})
        end = dateparser.parse(match.group(2), settings={'TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True})
        if start and end:
            return start, end

    # Check for single month/year like "March 2025"
    match = re.search(r"([a-zA-Z]+\s+\d{4})", query)
    if match:
        dt = dateparser.parse(match.group(1), settings={'TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True})
        if dt:
            start = datetime(dt.year, dt.month, 1, tzinfo=timezone.utc)
            if dt.month == 12:
                end = datetime(dt.year + 1, 1, 1, tzinfo=timezone.utc) - timedelta(seconds=1)
            else:
                end = datetime(dt.year, dt.month + 1, 1, tzinfo=timezone.utc) - timedelta(seconds=1)
            return start, end

    return None, None

def simple_router(query):
    task = "slack_summary"
    params = {}

    start_date, end_date = parse_natural_date_range(query)
    if start_date and end_date:
        params["start_date"] = str(start_date.date())
        params["end_date"] = str(end_date.date())

    for key in KEYWORDS.keys():
        if match_keyword(query, key):
            params[key] = True

    if params:
        return task, params
    else:
        return None, {}
