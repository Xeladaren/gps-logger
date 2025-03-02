
import os.path

from . import args

def get_file_name(data, ext=None):

    time_str = data['time'].strftime("%Y-%m-%d")

    if ext:
        return f"{data['device']}_{time_str}.{ext}"
    else:
        return f"{data['device']}_{time_str}"

def get_save_dir(path, data):
    config = args.get('config')
    dir_save = args.get('dir_save')

    rel_path = path.removeprefix("/")

    dir_save = os.path.join(dir_save, rel_path)

    if 'output' in config and 'file' in config['output'] and 'date-subdir' in config['output']['file']:
        if config['output']['file']['date-subdir']:
            dir_save = os.path.join(dir_save, f"{data['time'].year:04d}", f"{data['time'].month:02d}")

    return dir_save