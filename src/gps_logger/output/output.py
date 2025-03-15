
import re
import datetime

from ..utils import args

from .file import raw
from .file import gpx
from .web  import web

def save(path, data):

    data = _compute_data(data)

    if not "device" in data:
        data['device'] = path.removeprefix("/").replace("/", ".")

    if not 'lat' in data or not 'lon' in data:
        raise ValueError("Data need 'lat' and 'lon' data, for latitude and longitude.")

    print("Output data:", flush=True)
    print(f"\tPath = {path}", flush=True)
    print(f"\tData = {data}", flush=True)

    raw.save(path, data)
    gpx.save(path, data)
    web.save(data)

def _compute_data(data):
    out_data = {}
    config = args.get('config')

    if 'output' in config and 'args-convert' in config['output']:
        convert_table = args.get('config')['output']['args-convert']
    else:
        convert_table = None

    for elem in data:
        key = elem
        value = data[key]

        if convert_table and key in convert_table:
            key = convert_table[key]

        if type(value) == list:
            value = "".join(value)

        if type(value) == str and (("timestamp" in key) or ("eta" in key) or ("etfa" in key)):
            if len(value) > 10:
                value = value[:10] + "." + value[10:]

        if type(value) == str and value.lower() in ["true", "false"]:
            value = bool(value)

        if type(value) == str and re.match(r"^[+-]?\d+\.?\d*$", value):
            value = float(value)
            pass

        if type(value) == str and key in ['time', 'timeoffset']:
            value = value.replace("Z", "+00:00") # fix for 3.9 python
            value = datetime.datetime.fromisoformat(value)

        out_data[key] = value

    if not "time" in out_data:
        if 'timestamp' in out_data:
            out_data['time'] = datetime.datetime.fromtimestamp(out_data['timestamp'], tz=datetime.timezone.utc)
        else:
            out_data['time'] = datetime.datetime.now(datetime.timezone.utc)
    
    if not "timestamp" in out_data:
        out_data['timestamp'] = out_data['time'].timestamp()

    return out_data