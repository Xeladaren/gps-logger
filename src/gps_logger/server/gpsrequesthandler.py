
import http.server
import urllib.parse

from ..output import output

class GPSRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>GPS Logger</title></head>", "utf-8"))
            self.wfile.write(bytes("<h1>GPS Logger</h1>", "utf-8"))
            self.wfile.write(bytes("<h2>Server OK</h2>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        elif self.path.startswith("/api/"):
            url_parse = urllib.parse.urlparse(self.path)
            data = urllib.parse.parse_qs(url_parse.query)
            api_path = url_parse.path.removeprefix("/api/")

            self.save_data(api_path, data)
        else:
            self.send_response(http.HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/html")
            self.end_headers()

    def do_POST(self):
        
        if self.path.startswith("/api/"):
            if "content-length" in self.headers:
                content_len = int(self.headers["content-length"])
            else:
                self.send_response(http.HTTPStatus.LENGTH_REQUIRED)
                self.send_header("Content-type", "none")
                self.end_headers()
                return

            url_parse = urllib.parse.urlparse(self.path)

            raw_data = self.rfile.read(content_len).decode("utf-8")
            data = urllib.parse.parse_qs(raw_data)
            api_path = url_parse.path.removeprefix("/api/")

            self.save_data(api_path, data)
        else:
            self.send_response(http.HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "text/html")
            self.end_headers()

    def save_data(self, path, data):

        try:
            output.save(path, data)
        except ValueError as e:
            print(f"Save Error: {type(e)}: {e}", flush=True)
            self.send_response(http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            print(f"Save Error: {type(e)}: {e}", flush=True)
            self.send_response(http.HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            self.send_response(http.HTTPStatus.OK)

        self.send_header("Content-type", "none")
        self.end_headers()
