
import http.server
import urllib.parse
import re

from ..output import output
from ..utils  import args
from .web     import device_map
from .web     import web
from .web.resources import resources

class GPSRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            self.send_response_page(http.HTTPStatus.OK)

        elif self.path == "/coffee":
            self.send_response_page(http.HTTPStatus.IM_A_TEAPOT)

        elif self.path.startswith("/res/"):
            res = None
            try:
                url_parse = urllib.parse.urlparse(self.path)
                res_path = url_parse.path.removeprefix("/res/")
                res = resources.Resource(res_path)
            except Exception as e:
                print(type(e), e)
                self.send_response_page(http.HTTPStatus.NOT_FOUND)
            else:
                print(res.get_mime())
                self.send_response(http.HTTPStatus.OK)
                self.send_header("Content-type", res.get_mime())
                self.send_header("Cache-Control", "max-age=3600")
                self.end_headers()
                self.wfile.write(res.get_bytes()) # src/gps_logger/server/web/resources/res/img/widget_battery_day.svg

        elif self.path.startswith("/api/"):
            try:
                self.check_api_auth()
            except PermissionError:
                self.send_response_page(http.HTTPStatus.UNAUTHORIZED)
            else:
                url_parse = urllib.parse.urlparse(self.path)
                data = urllib.parse.parse_qs(url_parse.query)
                api_path = url_parse.path.removeprefix("/api/")

                self.save_data(api_path, data)
        elif self.path.startswith("/web/"):
            try:
                self.check_api_auth()
            except PermissionError:
                self.send_response_page(http.HTTPStatus.UNAUTHORIZED)
            else:
                url_parse = urllib.parse.urlparse(self.path)
                query = urllib.parse.parse_qs(url_parse.query)
                api_path = url_parse.path.removeprefix("/web/")

                self.get_web_page(api_path, query)
        else:
            self.send_response_page(http.HTTPStatus.NOT_FOUND)

    def do_POST(self):
        
        if self.path.startswith("/api/"):
            if "content-length" in self.headers:
                content_len = int(self.headers["content-length"])
            else:
                self.send_response_page(http.HTTPStatus.LENGTH_REQUIRED)
                return

            try:
                self.check_api_auth()
            except PermissionError:
                self.send_response_page(http.HTTPStatus.UNAUTHORIZED)

            else:
                url_parse = urllib.parse.urlparse(self.path)

                raw_data = self.rfile.read(content_len).decode("utf-8")
                data = urllib.parse.parse_qs(raw_data)
                api_path = url_parse.path.removeprefix("/api/")

                self.save_data(api_path, data)
        else:
            self.send_response_page(http.HTTPStatus.NOT_FOUND)

    def check_api_auth(self):

        api_keys = args.get('api_keys')

        if "Api-Key" in self.headers:
            api_key = self.headers["Api-Key"]
        else:
            key_match = re.search(r"^/\w+/([0-9a-zA-Z]+)/", self.path)
            if key_match:
                api_key = key_match[1]
            else:
                raise PermissionError

        self.path = self.path.replace(f"{api_key}/", "")

        api_check, api_name = api_keys.check_key(api_key, self.path)
        if api_check:
            if api_name:
                print(f"Api key {api_name} validate.")
            else:
                print(f"Anonimous Api key validate.")
            return None
        else:
            raise PermissionError

    def get_web_page(self, path, query):

        try:
            page_data = web.get_web_page(path, query=query)
        except Exception as e:
            print(e)
            self.send_response_page(http.HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            if page_data:
                self.send_response(http.HTTPStatus.OK)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(page_data.encode("utf-8"))
            else:
                self.send_response_page(http.HTTPStatus.NOT_FOUND)

    def save_data(self, path, data):

        try:
            output.save(path, data)
        except ValueError as e:
            print(f"Save Error: {type(e)}: {e}", flush=True)
            self.send_response_page(http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            print(f"Save Error: {type(e)}: {e}", flush=True)
            self.send_response_page(http.HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            self.send_response_page(http.HTTPStatus.CREATED)

    def send_response_page(self, code, message=None):

        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head>", "utf-8"))
        self.wfile.write(bytes(f"<title>GPS Logger - {code} {code.phrase}</title>", "utf-8"))
        self.wfile.write(bytes("<link rel=\"icon\" href=\"/res/img/icon.svg\">", "utf-8"))
        self.wfile.write(bytes("</head>", "utf-8"))
        self.wfile.write(bytes(f"<h1>{code}: {code.phrase}</h1>", "utf-8"))
        self.wfile.write(bytes(f"<h2>{code.description}</h2>", "utf-8"))
        if message:
            self.wfile.write(bytes(f"<p>{message}</p>", "utf-8"))
        self.wfile.write(bytes(f'<img src="https://http.cat/{code}.jpg"/>', "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def send_response(self, code, message=None):

        print(f"{self.command} {self.path} {code} {message}", flush=True)
        self.send_response_only(code, message)
