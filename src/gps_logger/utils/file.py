
import os.path
import re

from . import args

def get_file_name(data, ext=None, device=True):

    time_str = data['time'].strftime("%Y-%m-%d")
    out_str = ""

    if ext:
        out_str = f"{time_str}.{ext}"
    else:
        out_str = f"{time_str}"

    if device:
        out_str = f"{data['device']}_" + out_str

    return out_str

def get_save_dir(path, data):
    config = args.get('config')
    dir_save = args.get('dir_save')

    rel_path = path.removeprefix("/")

    dir_save = os.path.join(dir_save, rel_path)

    if 'output' in config and 'file' in config['output'] and 'date-subdir' in config['output']['file']:
        if config['output']['file']['date-subdir']:
            dir_save = os.path.join(dir_save, f"{data['time'].year:04d}", f"{data['time'].month:02d}")

    return dir_save

def get_last_file(path):

    dir_save = args.get('dir_save')
    path = path.removeprefix("/")
    path = os.path.join(dir_save, path)

    if os.path.isdir(path):
        last_year  = 0
        last_mount = 0
        last_day   = 0

        year_path = ""
        mount_path = ""
        file_name = ""

        for elem in os.listdir(path):

            if re.match(r"\d{4}", elem):
                year = int(elem)
                if year > last_year:
                    last_year = year
                    year_path = elem
        
        if last_year == 0:
            return None
        else:
            path = os.path.join(path, year_path)

        for elem in os.listdir(path):

            if re.match(r"\d{2}", elem):
                mount = int(elem)
                if mount > last_mount:
                    last_mount = mount
                    mount_path = elem


        if last_mount == 0:
            return None
        else:
            path = os.path.join(path, mount_path)

        for elem in os.listdir(path):
            file_match = re.match(fr"{year_path}-{mount_path}-(\d\d).raw", elem)
            if file_match:
                day = int(file_match[1])
                if day > last_day:
                    last_day = day
                    file_path = elem

        if last_day == 0:
            return None
        else:
            path = os.path.join(path, file_path)

        return path


    else:
        return None