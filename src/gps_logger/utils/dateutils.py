

import datetime
import timezonefinder
import zoneinfo
import time


def from_timestamp_pos(timestamp, lat, lon):

    tzfinder = timezonefinder.TimezoneFinder()
    tz = tzfinder.timezone_at(lat=lat, lng=lon)
    tzinfo = zoneinfo.ZoneInfo(tz)

    return datetime.datetime.fromtimestamp(timestamp, tz=tzinfo)

def get_adaptatif_str(timestamp, lat, lon):
    time = from_timestamp_pos(timestamp, lat, lon)
    now  = datetime.datetime.now(time.tzinfo)

    if time.date() == now.date():
        return time.strftime("%H:%M:%S %Z")
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S %Z")

def delta_format(delta_sec, hour="h", min="min", sec="s", day="day"):

    second = int(delta_sec)

    day = second

def timestamp_to_iso(timestamp, timespec='seconds'):
    tz = datetime.timezone.utc
    date = datetime.datetime.fromtimestamp(timestamp, tz=tz)
    return date.isoformat(timespec='seconds')

def get_delta_str(timestamp):

    delta = timestamp - time.time()

    if delta > 0:
        out_str = "dans"
    else:
        out_str = "il y a"

    delta = abs(delta)

    day = int(delta / (3600 * 24))

    if day > 1:
        out_str += f" {day} jours"
    elif day > 0:
        out_str += f" {day} jours"

    delta -= (day * 3600 * 24)

    hour = int(delta / 3600)

    if hour > 0:
        out_str += f" {hour}h"

    delta -= (hour * 3600)

    min = int(delta / 60)

    if min > 0:
        out_str += f" {min}min"

    delta -= (min * 60)
    out_str += f" {int(delta)}s"

    return out_str
    
