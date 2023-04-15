import datetime

def round_to_year(d: datetime.datetime):
    return datetime.datetime(d.year, 0, 0, 0, 0, 0, 0)

def round_to_month(d: datetime.datetime):
    return datetime.datetime(d.year, d.month, 0, 0, 0, 0, 0)

def round_to_day(d: datetime.datetime):
    return datetime.datetime(d.year, d.month, d.day, 0, 0, 0, 0)

def round_to_hour(d: datetime.datetime):
    return datetime.datetime(d.year, d.month, d.day, d.hour, 0, 0, 0)

def round_to_sec(d: datetime.datetime):
    return datetime.datetime(d.year, d.month, d.day, d.hour, d.minute, d.second, 0)