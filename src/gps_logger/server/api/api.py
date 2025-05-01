
import json

from ...output import output
from ...output.file import raw

def post(path, data):
    output.save(path, data)

def get(path):
    data = raw.get(path)

    data_json = json.dumps(data)

    return data_json