
import http.server

from ..utils import args
from .gpsrequesthandler import GPSRequestHandler

def start():

    config = args.get('config')

    port = config['server']['port']
    addr = config['server']['listen']

    with http.server.HTTPServer((addr, port), GPSRequestHandler) as httpd:
        print(f"Server start to ({addr}:{port})", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("stop server", flush=True)
            pass