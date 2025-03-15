
from . import device_map

def get_web_page(path, query=None):
    page_data = device_map.get_page(path, query=query)

    return page_data