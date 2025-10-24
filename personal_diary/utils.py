from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def within_date_range(entry_date, start_date, end_date):
    entry_dt = datetime.strptime(entry_date.split()[0], "%Y-%m-%d")
    return start_date <= entry_dt <= end_date
