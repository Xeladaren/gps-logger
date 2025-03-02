
import os.path
import xml.dom.minidom
import datetime

from ...utils import file
from ...utils import args

valid_gpx_wpt_child = [
    "ele", 
    "time", 
    "magvar", 
    "geoidheight", 
    "name", 
    "cmt", 
    "desc", 
    "src", 
    "sat", 
    "ageofdgpsdata", 
    "dgpsid", 
    "link",
    "sym",
    "type",
    "hdop",
    "vdop", 
    "pdop"
]

def save(path, data):

    if args.get('config', ['output', 'file', 'gpx', 'save']):
        save_dir = file.get_save_dir(path, data)
        save_file = file.get_file_name(data, ext="gpx")
        save_path = os.path.join(save_dir, save_file)

        if os.path.exists(save_path):
            update_gpx(save_path, data)
            print(f"\tUpdate path gpx = {save_path}", flush=True)
        else:
            os.makedirs(save_dir, exist_ok=True)
            create_new_gpx(save_path, data)
            print(f"\tCreate path gpx = {save_path}", flush=True)

def save_xml_file(file_path, xml_root):

    with open(file_path, "w") as file:
        xml_root.writexml(file, standalone="yes", encoding="UTF-8")

def update_gpx(save_file, data):

    xml_root = xml.dom.minidom.parse(save_file)
    trkseg_list = xml_root.getElementsByTagName('trkseg')

    if trkseg_list:
        trkseg = trkseg_list[-1]
        add_gpx_trkpt(xml_root, trkseg, data)

    save_xml_file(save_file, xml_root)


def create_new_gpx(save_file, data):

    xml_root = xml.dom.minidom.Document()
    gpx_root = xml_root.createElement('gpx')

    #version="1.1" creator="OsmAnd+ 4.2.7" xmlns="http://www.topografix.com/GPX/1/1" xmlns:osmand="https://osmand.net" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd
    gpx_root.setAttribute('version', '1.1')
    gpx_root.setAttribute('xmlns', 'http://www.topografix.com/GPX/1/1')

    xml_root.appendChild(gpx_root)

    metadatas = xml_root.createElement('metadata')
    gpx_root.appendChild(metadatas)

    trk = xml_root.createElement('trk')
    gpx_root.appendChild(trk)

    trkseg = xml_root.createElement('trkseg')
    trk.appendChild(trkseg)

    name = xml_root.createElement('name')
    name_value = xml_root.createTextNode(str(data['device']))
    name.appendChild(name_value)
    metadatas.appendChild(name)

    create_date = datetime.datetime.now(datetime.timezone.utc)
    date = xml_root.createElement('time')
    date_value = xml_root.createTextNode(str(create_date))
    date.appendChild(date_value)
    metadatas.appendChild(date)
    
    add_gpx_trkpt(xml_root, trkseg, data)

    save_xml_file(save_file, xml_root)

def add_gpx_trkpt(xml_root, parent, data):

    data = data.copy()

    trkpt = xml_root.createElement('trkpt')

    trkpt.setAttribute("lat", str(data['lat']))
    data.pop("lat")

    trkpt.setAttribute("lon", str(data['lon']))
    data.pop("lon")

    for key in valid_gpx_wpt_child:
        if key in data:
            gpx_value = data[key]

            if key == "time":
                gpx_value = str(gpx_value).replace("+00:00", "Z")
            else:
                gpx_value = str(gpx_value)

            xml_node = xml_root.createElement(key)
            node_value = xml_root.createTextNode(gpx_value)
            xml_node.appendChild(node_value)
            trkpt.appendChild(xml_node)
            data.pop(key)

    if len(data) > 0:
        ext_node = xml_root.createElement("extensions")
        saved_extensions = args.get('config', ['output', 'file', 'gpx', 'saved_extensions'])

        for elem in data:

            if saved_extensions == None or elem in saved_extensions:
                xml_node = xml_root.createElement(f"{elem}")
                node_value = xml_root.createTextNode(str(data[elem]))
                xml_node.appendChild(node_value)
                ext_node.appendChild(xml_node)

        trkpt.appendChild(ext_node)

    parent.appendChild(trkpt)