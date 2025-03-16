
import zoneinfo
import datetime
import qrcode
import io
import base64

from .resources import resources
from ..auth import api_key
from ...utils import args

def get_page(query):

    page_resource      = resources.Resource("html/apikey_create_page.html")
    page_icon_resource = resources.Resource("img/widget_coordinates_location_day.svg")

    template_dict = dict()

    template_dict['page_title'] = f"GPS Logger"
    template_dict['page_icon_href'] = page_icon_resource.get_html_href()
    template_dict['page_head'] = ""

    template_dict['apikey_result_section'] = build_result(query)
    template_dict['apikey_create_script']  = build_script()

    return page_resource.get_template().safe_substitute(template_dict)

def build_result(query):

    if 'create' in query and query['create'][0] == "true":
        print(query)
        api_keys = args.get('api_keys')
        out_str  = "<h1>New key</h1>\n"

        if 'name' in query:
            name = query['name'][0]
            out_str  += f"<p>Name : {name}</p>\n"
        else:
            name = None

        if 'path' in query:
            path = query['path'][0]
            out_str  += f"<p>Path : {path}</p>\n"
        else:
            path = None

        if 'expire' in query and query['expire'][0] == 'on':

            if 'expire-date' in query:
                expire_date = datetime.datetime.fromisoformat(query['expire-date'][0])
            else:
                raise ValueError("need 'expire-date' arg if 'expire' is on.")
            
            if 'timezone' in query:
                timezone_raw = query['timezone'][0]

                if timezone_raw in zoneinfo.available_timezones():
                    timezone = zoneinfo.ZoneInfo(timezone_raw)
                    expire_date = expire_date.replace(tzinfo=timezone)
            
            out_str  += f"<p>Expire : {expire_date}</p>\n"
        else:
            expire_date = None

        if expire_date:
            api_key = api_keys.create_key(name=name, path=path, expire_date=expire_date.timestamp())
        else:
            api_key = api_keys.create_key(name=name, path=path)

        out_str += f'<input type="text" value="{api_key}" readonly/><br />'
        out_str += f'<img width="300" src="{make_qrcode_image(api_key)}" /><br />'
        out_str  += f"<p>(you can't get again this api key)</p>\n"

        return out_str
    else:
        return ""

def build_script():
    script_resource = resources.Resource("js/apikey_create.js")

    out_str  = "<script>\n"
    out_str += script_resource.get_string()
    out_str += "</script>\n"

    return out_str

def make_qrcode_image(data):

    img = qrcode.make(data).get_image()

    img_io = io.BytesIO()
    img.save(img_io, "png")

    img_io.seek(0)
    img_bytes = img_io.read()

    img_b64 = base64.b64encode(img_bytes)

    return f'data:image/png;base64,{img_b64.decode('utf-8')}'
