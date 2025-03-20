
from string import Template
import os.path

from .resources import resources
from ...utils import position
from ...utils import dateutils
from ...output.file import raw

def get_page(path, query=None):
    data = raw.get(path)

    if not data:
        return None

    if 'reload' in query:
        auto_reload = int(query['reload'][0])
    else:
        auto_reload = None

    if 'zoom' in query:
        zoom = int(query['zoom'][0])
    else:
        zoom = None
    
    return build_map_page(data, auto_reload=auto_reload, zoom=zoom)
    

def build_map_page(data, auto_reload=None, zoom=None):
    
    res_page = resources.Resource("html/device_map_page.html")

    template_dict = dict()

    template_dict['page_title'] = f"GPS Logger"
    template_dict['page_head'] = ""

    if auto_reload:
        template_dict['page_head'] += f'<meta http-equiv="refresh" content="{int(auto_reload)}">\n'

    if not zoom:
        if 'eda' in data and data['eda'] > 0:
            position.dist_to_zoom(data['eda'])
        else:
            zoom = 14

    template_dict['map_init_script'] = f"<script>build_map(L.latLng({data['lat']}, {data['lon']}), {zoom}, 0);</script>"
    template_dict['widget_zone'] = build_widget_zone(data)

    return res_page.get_template().safe_substitute(template_dict)

def build_widget_zone(data):

    out_str = '<div class="widget-zone">\n'

    out_str += build_widget_position(data)
    out_str += build_widget_aux_nav(data)
    out_str += build_widget_datetime(data)
    out_str += build_targets(data)
    out_str += build_technics(data)

    out_str += '</div>\n'

    return out_str

def build_widget_elem(icon_name, text, text_attrs={}, img_attrs={}):

    text_attrs = text_attrs.copy()
    img_attrs  = img_attrs.copy()

    if 'class' in text_attrs:
        text_attrs['class'].append("widget-text")
    else:
        text_attrs['class'] = ["widget-text"]

    if 'class' in img_attrs:
        img_attrs['class'].append("widget-icon")
    else:
        img_attrs['class'] = ["widget-icon"]
    
    img_attrs['src'] = [os.path.join("/res", icon_name)]

    text_attrs_list = []
    for attr in text_attrs:
        text_attrs_list.append(f'{attr}="' + ' '.join(text_attrs[attr]) + '"')
    text_attrs_str = " ".join(text_attrs_list)

    img_attrs_list = []
    for attr in img_attrs:
        img_attrs_list.append(f'{attr}="' + ' '.join(img_attrs[attr]) + '"')
    img_attrs_str = " ".join(img_attrs_list)

    out_str = f'<img {img_attrs_str}/>\n'
    out_str += f'<span {text_attrs_str}>{text}</span>\n'

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

    geo_link = f"geo:{data['lat']:06},{data['lon']:06}"

    out_str  = f'<a href="{geo_link}">\n'
    out_str += '<div class="widget">\n'

    out_str += build_widget_elem(lat_icon_name, f"{lat_str}")
    out_str += build_widget_elem(lon_icon_name, f"{lon_str}")

    out_str += '</div>\n'
    out_str += '</a>\n'

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
    text = dateutils.get_adaptatif_str(data['timestamp'], data['lat'], data['lon'])
    out_str += build_widget_elem(icon, text)

    icon = "img/widget_track_recording_duration_day.svg"
    text = dateutils.get_delta_str(data['timestamp'])
    out_str += build_widget_elem(icon, text, text_attrs={
        "class": ["date-delta"], 
        "isodate": [f"{dateutils.timestamp_to_iso(data['timestamp'])}"]
    })

    out_str += '</div>\n'

    return out_str

def build_targets(data):

    if not 'eda' in data or data['eda'] == 0.0:
        return ""

    if not 'edfa' in data or data['edfa'] == 0.0:
        return ""

    out_str = ""

    if data['eda'] != data['edfa']:
        out_str += build_target(data, "intermediate")

    out_str += build_target(data, "final")

    return out_str


def build_target(data, type):

    out_str = '<div class="widget">\n'

    if type == "intermediate":
        icon = "img/widget_intermediate_day.svg"
        text = position.dist_human(data['edfa'])
        out_str += build_widget_elem(icon, text)

        icon = "img/widget_intermediate_time_day.svg"
        text = dateutils.get_adaptatif_str(data['etfa'], data['lat'], data['lon'])
        out_str += build_widget_elem(icon, text)

        icon = "img/widget_intermediate_time_to_go_day.svg"
        text = dateutils.get_delta_str(data['etfa'])
        out_str += build_widget_elem(icon, text, text_attrs={
            "class": ["date-delta"], 
            "isodate": [f"{dateutils.timestamp_to_iso(data['etfa'])}"]
        })

    elif type == "final":
        icon = "img/widget_target_day.svg"
        text = position.dist_human(data['eda'])
        out_str += build_widget_elem(icon, text)

        icon = "img/widget_time_to_distance_day.svg"
        text = dateutils.get_adaptatif_str(data['eta'], data['lat'], data['lon'])
        out_str += build_widget_elem(icon, text)

        icon = "img/widget_destination_time_to_go_day.svg"
        text = dateutils.get_delta_str(data['eta'])
        out_str += build_widget_elem(icon, text, text_attrs={
            "class": ["date-delta"], 
            "isodate": [f"{dateutils.timestamp_to_iso(data['eta'])}"]
        })

    out_str += '</div>\n'
    return out_str

def build_technics(data):

    if not 'sat' in data and not 'acc' in data and not 'batt' in data:
        return ""

    out_str = '<div class="widget">\n'

    if 'sat' in data:
        icon = "img/widget_gps_info_day.svg"
        text = f"{int(data['sat'])} sat"
        out_str += build_widget_elem(icon, text)

    if 'acc' in data:
        icon = "img/widget_ruler_circle_day.svg"
        text = f"{int(data['acc'])} m"
        out_str += build_widget_elem(icon, text)

    if 'batt' in data:
        if 'ischarging' in data and data['ischarging']:
            icon = "img/widget_battery_charging_day.svg"
        else:
            icon = "img/widget_battery_day.svg"
        text = f"{int(data['batt'])} %"
        out_str += build_widget_elem(icon, text)

    out_str += '</div>\n'
    return out_str