
from . import device_map
from . import apikey_create

def get_web_page(path, query=None):

    if path.startswith("create-apikey"):
        page_data = apikey_create.get_page(query)
    else:
        page_data = device_map.get_page(path, query=query)

    return page_data