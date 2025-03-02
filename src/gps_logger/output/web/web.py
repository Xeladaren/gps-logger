
import urllib.parse
import urllib.request

from ...utils import args

def save(data):
    web_dest_list = args.get('config', ['output', 'web'])

    for web_dest in web_dest_list:
        if 'enable' in web_dest and web_dest['enable']:
            if not 'device-whitelist' in web_dest or data['device'] in web_dest['device-whitelist']:
                send_dest(web_dest, data)
            else:
                print("\tData not send, not in whitelist.")

def send_dest(dest, data):

    if 'data_raw' in dest:
        data_send = dest['data_raw'].format(**data)
    elif 'data_form' in dest:
        out_data_dic = {}

        for elem in dest['data_form']:
            if dest['data_form'][elem] in data:
                out_data_dic[elem] = data[dest['data_form'][elem]]

        data_send = urllib.parse.urlencode(out_data_dic)


    if not 'method' in dest or dest['method'] == "GET":

        url = dest['url']
        url = f"{url}?{data_send}"

        request = urllib.request.Request(url, data=None, method="GET")

    elif 'method' in dest and dest['method'] == "POST":
        
        url = dest['url']
        data_encoded = data_send.encode("UTF-8")

        request = urllib.request.Request(url, data=data_encoded, method="POST")
        request.add_header("Content-Length", str(len(data_encoded)))
        request.add_header("Content-Type", "application/x-www-form-urlencoded")

    response = urllib.request.urlopen(request)
    print(f"\tData send: {response.status}")
