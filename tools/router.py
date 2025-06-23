import re
import dateparser
from datetime import datetime, timedelta, timezone
import calendar

KEYWORDS = {
    "cpu": ["cpu", "processor", "core"],
    "gpu": ["gpu", "graphics", "nvidia"],
    "summary": ["summary", "report", "status", "overview"],
    "days_down": ["days down", "under", "lower than", "less than"]
}

def match_keyword(query, category):
    return any(keyword in query.lower() for keyword in KEYWORDS[category])

def parse_month_by_name(query):
    query = query.lower()
    months = list(calendar.month_name)[1:]  # Jan to Dec
    for i, month in enumerate(months):
        if month.lower() in query:
            year = datetime.now().year
            start = datetime(year, i + 1, 1, tzinfo=timezone.utc)
            last_day = calendar.monthrange(year, i + 1)[1]
            end = datetime(year, i + 1, last_day, 23, 59, 59, tzinfo=timezone.utc)
            return start, end
    return None, None

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
    elif "last month" in query:
        now = datetime.now(timezone.utc)
        first_day_this_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        start = datetime(last_day_last_month.year, last_day_last_month.month, 1, tzinfo=timezone.utc)
        end = datetime(last_day_last_month.year, last_day_last_month.month,
                       calendar.monthrange(last_day_last_month.year, last_day_last_month.month)[1],
                       23, 59, 59, tzinfo=timezone.utc)
        return start, end
    elif "between" in query:
        match = re.search(r"between (.+?) and (.+)", query)
        if match:
            start = dateparser.parse(match.group(1), settings={'TIMEZONE': 'UTC'})
            end = dateparser.parse(match.group(2), settings={'TIMEZONE': 'UTC'})
            if start and end:
                return start, end
    else:
        return parse_month_by_name(query)

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

    if params.get("start_date") and params.get("end_date"):
        return task, params
    else:
        return None, {}
