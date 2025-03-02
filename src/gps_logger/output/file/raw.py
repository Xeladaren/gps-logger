
import os.path

from ...utils import file
from ...utils import args

def save(path, data):

    if args.get('config', ['output', 'file', 'raw', 'save']):
        save_dir = file.get_save_dir(path, data)
        save_file = file.get_file_name(data, ext="raw")
        save_path = os.path.join(save_dir, save_file)

        data = _make_saved_data(data)

        print(f"\tSave path raw = {save_path}", flush=True)
        print(f"\tSave data raw = {data}", flush=True)

        os.makedirs(save_dir, exist_ok=True)

        with open(save_path, "a") as raw_file:
            raw_file.write(f"{data}\n")

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

