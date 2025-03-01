#!/usr/bin/env python3

import http.server
import urllib.parse
import urllib.request
import datetime
import os
import os.path
import xml.dom.minidom

class GPSRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        url_parse = urllib.parse.urlparse(self.path)
        data = urllib.parse.parse_qs(url_parse.query)

        try:
            device = url_parse.path.removeprefix("/").replace("/", ".")
            save_raw(device, data)
            save_gpx(device, data)
            send_to_homeass(device, data)
        except Exception as e:
            print(f"Save Error: {type(e)}: {e}")
            self.send_response(500)
            self.send_header("Content-type", "none")
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "none")
            self.end_headers()

    def do_POST(self):
        if "content-length" in self.headers:
            content_len = int(self.headers["content-length"])
        else:
            self.send_response(411)
            self.send_header("Content-type", "none")
            self.end_headers()
            return

        url_parse = urllib.parse.urlparse(self.path)

        raw_data = self.rfile.read(content_len).decode("utf-8")
        data = urllib.parse.parse_qs(raw_data)

        try:
            device = url_parse.path.removeprefix("/").replace("/", ".")
            save_raw(device, data)
            save_gpx(device, data)
            send_to_homeass(device, data)
        except Exception as e:
            print(f"Save Error: {type(e)}: {e}")
            self.send_response(500)
            self.send_header("Content-type", "none")
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "none")
            self.end_headers()

def get_time(data):

    if 'time' in data:
        time = datetime.datetime.fromisoformat(data['time'][0])
    elif 'timestamp' in data:
        if len(data['timestamp'][0]) <= 10:
            timestamp = int(data['timestamp'][0])
        else:
            timestamp = data['timestamp'][0]
            timestamp = timestamp[:10] + "." + timestamp[10:]
            timestamp = float(timestamp)
            time = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    else:
        time = datetime.datetime.now(datetime.timezone.utc)

    if not 'time' in data:
        data['time'] = [time.isoformat().replace("+00:00", "Z")]
        print(data['time'])

    return time

def save_raw(path, data):

    time = get_time(data)
    path = path.removeprefix("/")

    save_dir = os.path.join(".", "gpx_save", path, f"{time.year:04d}", f"{time.month:02d}")
    save_file = os.path.join(save_dir, time.strftime("%Y-%m-%d.raw"))

    os.makedirs(save_dir, exist_ok=True)

    with open(save_file, "a") as file:
        file.write(f"{data}\n")
    print(f"Update file {save_file} done.")

def save_gpx(path, data):

    time = get_time(data)
    path = path.removeprefix("/")

    save_dir = os.path.join(".", "gpx_save", path, f"{time.year:04d}", f"{time.month:02d}")
    save_file = os.path.join(save_dir, time.strftime("%Y-%m-%d.gpx"))

    if os.path.exists(save_file):
        update_new_gpx(save_file, data)
        print(f"Update file {save_file} done.")
    else:
        os.makedirs(save_dir, exist_ok=True)
        create_new_gpx(save_file, data)
        print(f"Create file {save_file} done.")

def update_new_gpx(save_file, data):

    xmlRoot = xml.dom.minidom.parse(save_file)
    trkseg_list = xmlRoot.getElementsByTagName('trkseg')

    if trkseg_list:
        trkseg = trkseg_list[-1]
        add_gpx_trkpt(xmlRoot, trkseg, data)

        with open(save_file, "w") as file:
            xmlRoot.writexml(file, standalone="yes", encoding="UTF-8")

def create_new_gpx(save_file, data):
    xmlRoot = xml.dom.minidom.Document()

    gpxRoot = xmlRoot.createElement('gpx')

    #version="1.1" creator="OsmAnd+ 4.2.7" xmlns="http://www.topografix.com/GPX/1/1" xmlns:osmand="https://osmand.net" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd
    gpxRoot.setAttribute('version', '1.1')
    gpxRoot.setAttribute('xmlns', 'http://www.topografix.com/GPX/1/1')

    xmlRoot.appendChild(gpxRoot)

    metadatas = xmlRoot.createElement('metadata')
    gpxRoot.appendChild(metadatas)

    trk = xmlRoot.createElement('trk')
    gpxRoot.appendChild(trk)

    trkseg = xmlRoot.createElement('trkseg')
    trk.appendChild(trkseg)

    date = xmlRoot.createElement('date')
    dateValue = xmlRoot.createTextNode(data['time'][0])
    date.appendChild(dateValue)
    metadatas.appendChild(date)
    
    add_gpx_trkpt(xmlRoot, trkseg, data)

    with open(save_file, "w") as file:
        xmlRoot.writexml(file, standalone="yes", encoding="UTF-8")

def add_gpx_trkpt(xmlRoot, parent, data):

    data = data.copy()

    trkpt = xmlRoot.createElement('trkpt')

    trkpt.setAttribute("lat", data['lat'][0])
    data.pop("lat")

    trkpt.setAttribute("lon", data['lon'][0])
    data.pop("lon")

    value_convert = {
        "alt": "ele"
    }

    for gpx_value in ["alt", "time", "sat", "hdop", "vdop", "pdop"]:
        if gpx_value in data:
            if gpx_value in value_convert:
                xml_node = xmlRoot.createElement(value_convert[gpx_value])
            else:
                xml_node = xmlRoot.createElement(gpx_value)
            nodeValue = xmlRoot.createTextNode(data[gpx_value][0])
            xml_node.appendChild(nodeValue)
            trkpt.appendChild(xml_node)
            data.pop(gpx_value)

    if len(data) > 0:
        ext_node = xmlRoot.createElement("extensions")
        for elem in data:
            xml_node = xmlRoot.createElement(f"{elem}")
            nodeValue = xmlRoot.createTextNode(data[elem][0])
            xml_node.appendChild(nodeValue)
            ext_node.appendChild(xml_node)
        trkpt.appendChild(ext_node)

    parent.appendChild(trkpt)

def send_to_homeass(device, data):

    print(data)

    out_data_dic = {}

    out_data_dic['device'] = device

    if not 'lat' in data or not 'lon' in data:
        raise ValueError("need latitude and longitude value (lat=0.00, lon=0.00)")

    out_data_dic['latitude'] = data['lat'][0]
    out_data_dic['longitude'] = data['lon'][0]

    if 'acc' in data:
        out_data_dic['accuracy'] = data['acc'][0]

    if 'batt' in data:
        out_data_dic['battery'] = data['batt'][0]

    if 'spd' in data:
        out_data_dic['speed'] = data['spd'][0]

    if 'dir' in data:
        out_data_dic['direction'] = data['dir'][0]
    
    if 'alt' in data:
        out_data_dic['altitude'] = data['alt'][0]

    if 'prov' in data:
        out_data_dic['provider'] = data['prov'][0]

    # latitude=%LAT&longitude=%LON&device=%SER&accuracy=%ACC&battery=%BATT&speed=%SPD&direction=%DIR&altitude=%ALT&provider=%PROV&activity=%ACT
    send_data = urllib.parse.urlencode(out_data_dic).encode("UTF-8")
    # f"latitude={data['lat'][0]}&longitude={data['lon'][0]}&device={device}"
    print(send_data)

    webhook = ""
    url = f"https://home.basque.tf/api/webhook/{webhook}"

    request = urllib.request.Request(url, data=send_data, method="POST")
    request.add_header("Content-Length", str(len(send_data)))
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    print(request)
    print(request.headers)

    response = urllib.request.urlopen(request)
    print(response)

def main():

    PORT = 8080

    with http.server.HTTPServer(("", PORT), GPSRequestHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


if __name__ == "__main__":
    main()