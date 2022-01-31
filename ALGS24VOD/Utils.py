import datetime as dt
import json


def load_json(fp):
    with open(fp, "r", encoding="UTF-8") as f:
        return json.load(f)


def timestamp():
    time = dt.datetime.utcnow()
    time += dt.timedelta(hours=8)
    return time.strftime("%Y-%m-%d %H:%M:%S")
