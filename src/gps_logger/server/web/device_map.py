
from string import Template

from .resources import resources
from ...utils import osm_frame
from ...utils import position
from ...utils import dateutils
from ...output.file import raw

# 12.97261 77.58064 Bengaluru
# 47.054500 -0.879083 Cholet

def build_test_page():
    # data = {'device': 'voiture', 'timestamp': 1741886502.658, 'lat': 47.055054, 'lon': -0.8797846, 'ele': 76.1137, 'spd': 5.17, 'acc': 3.7900925, 'dir': 217.1, 'eta': 1741886519.658, 'etfa': 1741886519.658, 'eda': 94.0, 'edfa': 94.0}
    # data = {'device': 'voiture', 'timestamp': 1741884253.648, 'lat': 47.067375, 'lon': -0.8536533, 'ele': 128.80542, 'spd': 4.97, 'acc': 3.7900925, 'dir': 188.9, 'eta': 1741885166.648, 'etfa': 1741884599.648, 'eda': 7449.0, 'edfa': 3900.0}
    # data = {'device': 'voiture', 'timestamp': 1741886520.615, 'lat': 47.054596, 'lon': -0.8797171, 'ele': 78.96166, 'spd': 0.73, 'acc': 3.7900925, 'dir': 157.4, 'eta': 0.0, 'etfa': 0.0, 'eda': 0.0, 'edfa': 0.0}
    # data = {'device': 'alexandre.portable', 'timestamp': 1741977485.0, 'lat': 47.05427905, 'lon': -0.87936821, 'ele': 148.4644775390625, 'spd': 0.0, 'acc': 14.892243385314941, 'sat': 45.0, 'batt': 63.0, 'ischarging': True, 'dir': 0.0}

    data = raw.get("/alexandre/all")
    print(data)

    if not data:
        return ""
    
    return build_map_page(data, auto_reload=None)

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
    res_style = resources.Resource("css/device_map_style.css")
    res_page_icon = resources.Resource("img/widget_coordinates_location_day.svg")

    template_dict = dict()

    template_dict['page_title'] = f"GPS Logger"
    template_dict['page_icon_href'] = res_page_icon.get_html_href()
    template_dict['page_head'] = ""

    if auto_reload:
        template_dict['page_head'] += f'<meta http-equiv="refresh" content="{int(auto_reload)}">\n'

    template_dict['page_head'] += resources.get_html_block("style", [
        "css/device_map_style.css"
    ])
    template_dict['page_head'] += resources.get_html_block("script", [
        "js/func_get_human_time.js",
        "js/func_update_date_delta.js"
    ])

    if not zoom:
        if 'eda' in data and data['eda'] > 0:
            zoom = int(data['eda'])
            if zoom < 1000:
                zoom = 1000
            if zoom > 4_000_000:
                zoom = 4_000_000
        else:
            zoom = 10_000

    template_dict['osm_frame_src'] = osm_frame.get_link(data['lat'], data['lon'], zoom=zoom)
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

    img_data = resources.Resource(icon_name).get_html_href()

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
    
    img_attrs['src'] = [img_data]

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