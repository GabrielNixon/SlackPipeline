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
    if "last" in query and "day" in query:
        try:
            num = int(re.search(r"last (\d+) day", query).group(1))
            end = datetime.now(timezone.utc)
            start = end - timedelta(days=num)
            return start, end
        except:
            pass
    elif "last week" in query:
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=7)
        return start, end
    elif "between" in query:
        match = re.search(r"between (.+?) and (.+)", query)
        if match:
            start = dateparser.parse(match.group(1), settings={'TIMEZONE': 'UTC'})
            end = dateparser.parse(match.group(2), settings={'TIMEZONE': 'UTC'})
            if start and end:
                return start, end
    else:
        return None, None


def simple_router(query):
    task = "slack_summary"
    params = {}

    start_date, end_date = parse_natural_date_range(query)
    if start_date and end_date:
        params["start_date"] = str(start_date.date())
        params["end_date"] = str(end_date.date())

    for key in ["cpu", "gpu", "summary", "days_down"]:
        if match_keyword(query, key):
            params[key] = True

    if params:
        return task, params
    else:
        return None, {}
