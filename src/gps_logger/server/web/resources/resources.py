
from pathlib import Path
import os.path
import base64
import magic
from string import Template

class Resource():

    def __init__(self, path):

        path = path.replace("..", "")

        parent_dir = Path(__file__).parent
        res_dir = os.path.join(parent_dir, "res")
        res_path = os.path.join(res_dir, path)

        abs_path = os.path.normpath(os.path.realpath(res_path))
        abs_dir  = os.path.normpath(os.path.realpath(res_dir))+"/"
        
        if not (abs_dir in abs_path):
            raise PermissionError

        if not os.path.exists(res_path):
            raise FileNotFoundError

        self.path = res_path
        self.mime = magic.from_file(self.path, mime=True)

        if self.mime == "text/plain":
            if self.path.endswith(".css"):
                self.mime = "text/css"
            elif self.path.endswith(".js"):
                self.mime = "text/javascript"

    def get_mime(self):
        return self.mime

    def get_bytes(self):

        resource = open(self.path, "rb")
        resource_data = resource.read()
        resource.close()

        return resource_data

    def get_string(self, encoding="utf-8"):
        return self.get_bytes().decode(encoding)

    def get_template(self):
        return Template(self.get_string())

    def get_b64(self):

        raw_data = self.get_bytes()
        return base64.b64encode(raw_data)

    def get_html_href(self, encoding="utf-8"):

        b64 = self.get_b64()

        return f"data:{self.mime};base64,{b64.decode(encoding)}"


def get_html_block(balise, file_list, encoding="utf-8"):

    out_str = f"<{balise}>\n"

    for file_path in file_list:
        resource = Resource(file_path)
        out_str += resource.get_string(encoding=encoding)

    out_str += f"</{balise}>\n"

    return out_str
