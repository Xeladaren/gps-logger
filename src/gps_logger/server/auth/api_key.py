
import json
import hashlib
import random
import string
import os.path
import qrcode

def api_keys_type(path):
    return ApiKey(path)

class ApiKey():
    def __init__(self, file_path):

        self.file_path = file_path
        self.last_file_mod = 0.0
        self._reload_data()


    def _save_data(self):

        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def _reload_data(self):
        if os.path.exists(self.file_path):
            if os.path.getmtime(self.file_path) > self.last_file_mod:
                self.last_file_mod = os.path.getmtime(self.file_path)
                with open(self.file_path, "r") as file:
                    self.data = json.load(file)
        else:
            self.data = []

    def create_key(self):

        api_key = ''.join(random.sample(string.ascii_letters+string.digits, 20))
        print(f"New API Key : {api_key}")

        qr = qrcode.QRCode()
        qr.add_data(api_key)
        qr.print_ascii()
        
        print(f"(you can't get again this api key)")

        encoded_api_key = api_key.encode("ascii")
        api_key_hash = hashlib.sha512(encoded_api_key).hexdigest()
        # print(api_key_hash)

        data_object = {'api-key-hash': api_key_hash}

        self.data.append(data_object)
        self._save_data()

    def check_key(self, key):

        if type(key) == str:
            key = key.encode("ascii")
        elif type(key) != bytes:
            raise TypeError("The key is or str or bytes type.")

        self._reload_data()

        key_hash = hashlib.sha512(key).hexdigest()
        # print(f"checked key hash : {key_hash}")

        for api_key in self.data:
            # print(f"\tcheck_to : {api_key['api-key-hash']}")
            if api_key['api-key-hash'] == key_hash:
                return True
        
        return False


