
from pathlib import Path
import os.path
import base64
import magic
from string import Template

class Resource():

    def __init__(self, path):

        parent_dir = Path(__file__).parent
        self.path = os.path.join(parent_dir, path)
        self.mime = magic.from_file(self.path, mime=True)


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
