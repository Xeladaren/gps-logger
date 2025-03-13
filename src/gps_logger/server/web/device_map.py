
from string import Template

from .resources import resources
from ...utils import osm_frame
from ...utils import position
from ...utils import datetime

# 12.97261 77.58064 Bengaluru
# 47.054500 -0.879083 Cholet

def build_test_page():
    data = {
        'device': 'voiture', 
        'timestamp': 1741886502.658, 
        'lat': 47.055054, 
        'lon': -0.8797846, 
        'ele': 76.1137, 
        'spd': 5.17, 
        'acc': 3.7900925, 'dir': 217.1, 
        'eta': 1741886519658.0, 
        'etfa': 1741886519658.0, 
        'eda': 94.0, 
        'edfa': 94.0
    }


    return build_map_page(data)

def build_map_page(data):
    
    res_page = resources.Resource("html/device_map_page.html")
    res_style = resources.Resource("css/device_map_style.css")
    res_page_icon = resources.Resource("img/widget_coordinates_location_day.svg")

    template_dict = dict()

    template_dict['page_title'] = f"GPS Logger"
    template_dict['page_icon_href'] = res_page_icon.get_html_href()

    template_dict['page_head'] = f"""
    <style>
    {res_style.get_string()}
    </style>
    """

    template_dict['osm_frame_src'] = osm_frame.get_link(data['lat'], data['lon'])
    template_dict['widget_zone'] = build_widget_zone(data)

    return res_page.get_template().safe_substitute(template_dict)

def build_widget_zone(data):

    out_str = '<div class="widget-zone">\n'

    out_str += build_widget_position(data)
    out_str += build_widget_aux_nav(data)
    out_str += build_widget_datetime(data)

    out_str += '</div>\n'

    return out_str

def build_widget_elem(icon_name, text):

    img_data = resources.Resource(icon_name).get_html_href()

    out_str = f'<img class="widget-icon" src="{img_data}"/>\n'
    out_str += f'<span class="widget-text">{text}</span>\n'

    return out_str

def build_widget_position(data):

    if data['lat'] >= 0:
        lat_icon_name = "img/widget_coordinates_latitude_north_day.svg"
    else:
        lat_icon_name = "img/widget_coordinates_latitude_south_day.svg"

    if data['lon'] >= 0:
        lon_icon_name = "img/widget_coordinates_longitude_east_day.svg"
    else:
        lon_icon_name = "img/widget_coordinates_longitude_west_day.svg"

    lat_str = position.pos_to_str_dms(data['lat'], "NS")
    lon_str = position.pos_to_str_dms(data['lon'], "EW")

    out_str = '<div class="widget">\n'

    out_str += build_widget_elem(lat_icon_name, f"{lat_str}")
    out_str += build_widget_elem(lon_icon_name, f"{lon_str}")

    out_str += '</div>\n'

    return out_str

def build_widget_aux_nav(data):

    is_empty = True
    out_str = '<div class="widget">\n'
    
    if 'ele' in data:
        icon = "img/widget_altitude_day.svg"
        text = f"{int(data['ele'])} m"
        out_str += build_widget_elem(icon, text)
        is_empty = False

    if 'dir' in data:
        icon = "img/widget_bearing_day.svg"
        text = f"{int(data['dir'])}&deg;"
        out_str += build_widget_elem(icon, text)
        is_empty = False

    if 'spd' in data:
        icon = "img/widget_speed_day.svg"
        text = f"{int(data['spd'] * 3.6)} km/h"
        out_str += build_widget_elem(icon, text)
        is_empty = False

    out_str += '</div>\n'

    if is_empty:
        return ""
    else:
        return out_str

def build_widget_datetime(data):

    if not 'timestamp' in data:
        return ""

    out_str = '<div class="widget">\n'

    icon = "img/widget_time_day.svg"
    text = datetime.get_adaptatif_str(data['timestamp'], data['lat'], data['lon'])
    out_str += build_widget_elem(icon, text)

    icon = "img/widget_track_recording_duration_day.svg"
    text = datetime.get_delta_str(data['timestamp'])
    out_str += build_widget_elem(icon, text)

    out_str += '</div>\n'

    return out_str