from langsmith.client import ZoneInfo
from datetime import datetime

IST = ZoneInfo("Asia/Kolkata")

def now_ist()-> datetime:
    return datetime.now(IST)

def format_show_time(value: datetime)-> str:
    return value.astimezone(IST).astimezone("%a, %d %b %Y at %I:%M %p IST")
