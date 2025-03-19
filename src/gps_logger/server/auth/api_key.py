
import json
import hashlib
import random
import string
import os.path
import time
import datetime
import pathlib

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

    def create_key(self, name=None, path=None, expire_date=None):

        api_key = ''.join(random.sample(string.ascii_letters+string.digits, 20))

        encoded_api_key = api_key.encode("ascii")
        api_key_hash = hashlib.sha512(encoded_api_key).hexdigest()

        data_object = {'hash': api_key_hash}
        if name:
            data_object['name'] = name

        if path:
            data_object['path'] = str(path)

        if expire_date:
            data_object['expire-date'] = expire_date

        self.data.append(data_object)
        self._save_data()

        return api_key

    def check_key(self, key, path=None):

        if type(key) == str:
            key = key.encode("ascii")
        elif type(key) != bytes:
            raise TypeError("The key is or str or bytes type.")

        self._reload_data()

        key_hash = hashlib.sha512(key).hexdigest()

        for api_key in self.data:
            if api_key['hash'] == key_hash:

                if path and 'path' in api_key:
                    if not path.startswith(api_key['path']):
                        return (False, None)

                if 'expire-date' in api_key:
                    timestamp_expire = api_key['expire-date']
                    timestamp_now = time.time()

                    if timestamp_expire < timestamp_now:
                        return (False, None)

                if api_key['name']:
                    return (True, api_key['name'])
                else:
                    return (True, None)
        
        return (False, None)


