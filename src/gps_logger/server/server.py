
import http.server

from ..utils import args
from ..utils import logging
from .gpsrequesthandler import GPSRequestHandler

logger = logging.getLogger(__name__)

def start():

    config = args.get('config')

    port = config['server']['port']
    addr = config['server']['listen']

    with http.server.HTTPServer((addr, port), GPSRequestHandler) as httpd:
        logger.info(f"Server start to ({addr}:{port})")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("stop server")
            pass