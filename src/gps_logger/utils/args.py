
import argparse
import json

from ..server.auth import api_key
from . import logging

_args = None

def _json_type(file_path):
    
    with open(file_path, "r") as file:
        json_data = json.load(file)

    return json_data

def parse():

    global _args

    if _args == None:

        parser = argparse.ArgumentParser()

        parser.add_argument("--config", "-c", type=_json_type, required=True)
        parser.add_argument("--api-keys", "-a", type=api_key.api_keys_type, required=True)
        parser.add_argument("--dir-save", "-d", default="./gps_log")
        parser.add_argument("--log-level", "-l", default="INFO", type=logging.log_type)

        _args = parser.parse_args()

def get(arg_name=None, sub_args=[]):
    if _args == None:
        parse()

    if arg_name:
        arg_val = vars(_args)

        if arg_name in arg_val:
            arg_val = arg_val[arg_name]

        for sub_arg in sub_args:
            if sub_arg in arg_val:
                arg_val = arg_val[sub_arg]
            else:
                return None

        return arg_val
    else:
        return _args
