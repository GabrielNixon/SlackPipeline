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

    if "last" in query and "day" in query:
        try:
            num = int(re.search(r"last (\d+) day", query).group(1))
            end = now
            start = end - timedelta(days=num)
            return start, end
        except:
            pass

    if "last week" in query:
        end = now
        start = end - timedelta(days=7)
        return start, end

    match = re.search(r"between (.+?) and (.+)", query)
    if match:
        start = dateparser.parse(match.group(1), settings={'TIMEZONE': 'UTC'})
        end = dateparser.parse(match.group(2), settings={'TIMEZONE': 'UTC'})
        if start and end:
            return start, end

    match = re.search(r"(first|second|last) (\d+)? ?week[s]? of ([a-z]+ ?\d{0,4})", query)
    if match:
        part = match.group(1)
        num_weeks = int(match.group(2)) if match.group(2) else 1
        month_str = match.group(3).strip()
        ref_date = dateparser.parse(f"1 {month_str}", settings={'TIMEZONE': 'UTC'})
        if ref_date:
            if part == "first":
                start = ref_date
                end = start + timedelta(weeks=num_weeks)
                return start, end
            elif part == "second":
                start = ref_date + timedelta(weeks=1)
                end = start + timedelta(weeks=num_weeks)
                return start, end
            elif part == "last":
                next_month = ref_date.replace(day=28) + timedelta(days=4)
                last_day = next_month - timedelta(days=next_month.day)
                end = datetime.combine(last_day, datetime.min.time(), tzinfo=timezone.utc)
                start = end - timedelta(weeks=num_weeks)
                return start, end

    month_match = re.search(r"(january|february|march|april|may|june|july|august|september|october|november|december)( \d{4})?", query)
    if month_match:
        month_str = month_match.group(0)
        start = dateparser.parse(f"1 {month_str}", settings={'TIMEZONE': 'UTC'})
        if start:
            next_month = start.replace(day=28) + timedelta(days=4)
            end = next_month - timedelta(days=next_month.day)
            return start, end

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
