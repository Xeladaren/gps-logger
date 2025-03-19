
import os.path

from ...utils import file
from ...utils import args
from ...utils import logging

logger = logging.getLogger(__name__)

def save(path, data):

    if args.get('config', ['output', 'file', 'raw', 'save']):
        save_dir = file.get_save_dir(path, data)
        save_file = file.get_file_name(data, ext="raw", device=False)
        save_path = os.path.join(save_dir, save_file)

        data = _make_saved_data(data)

        logger.info(f"Save raw file: {save_path}")
        logger.debug(f"Save raw data: {data}")

        os.makedirs(save_dir, exist_ok=True)

        with open(save_path, "a") as raw_file:
            raw_file.write(f"{data}\n")

def get(path):

    path_dir    = os.path.dirname(path)
    path_device = os.path.basename(path) 
    merge_delay = args.get("config", ['server', 'web', 'device-map', 'merge-delay'])

    last_file = file.get_last_file(path_dir)

    timestamp = None
    data_out = {}

    if last_file:

        raw_file  = open(last_file, "r")
        lines = raw_file.readlines()
        lines.reverse()
        for line in lines:

            data = eval(line)

            if 'timestamp' in data:
                if timestamp != None:
                    time_diff = timestamp - data['timestamp']

                    if merge_delay and time_diff > merge_delay:
                        break
                    elif time_diff < 0:
                        for elem in data:
                            data_out[elem] = data[elem]
                        timestamp = data['timestamp']
                else:
                    for elem in data:
                        data_out[elem] = data[elem]
                    timestamp = data['timestamp']

            if path_device == "all" or 'device' in data and data['device'] == path_device:
                for elem in data:
                    if not elem in data_out:
                        data_out[elem] = data[elem]
            else:
                break
        
        raw_file.close()

        if data_out != {}:
            return data_out
        else:
            return None
    else:
        return None

def _make_saved_data(data):
    saved_values = args.get('config', ['output', 'file', 'raw', 'saved_values'])
    
    if saved_values:
        out_data = {}
    
        for saved_value in saved_values:
            if saved_value in data:
                out_data[saved_value] = data[saved_value]
        return out_data
    else:
        return data

