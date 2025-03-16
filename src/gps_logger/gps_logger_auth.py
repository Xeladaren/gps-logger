
import argparse
import datetime
import qrcode
import time
import sys
import pathlib

from .server.auth import api_key

args = None

def type_datetime(str):
    try:
        return datetime.datetime.fromisoformat(str).timestamp()
    except:
        raise ValueError()

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--api-keys", "-a", type=api_key.api_keys_type, required=True)
    parser.add_argument("--name", "-n", type=str)
    parser.add_argument("--allow-path", "-p", type=pathlib.Path)
    parser.add_argument("--expire-date", "-d", type=type_datetime)

    global args
    args = parser.parse_args()
    print(args)
    print()

    if args.expire_date and args.expire_date < time.time():
        print("The expire time, can't be on the past.")
        sys.exit(1)

    new_key = args.api_keys.create_key(name=args.name, path=args.allow_path, expire_date=args.expire_date)

    if args.expire_date:
        expire_date = datetime.datetime.fromtimestamp(args.expire_date, datetime.timezone.utc)
    else:
        expire_date = None

    print(f"New API Key : {new_key}")
    if expire_date:
        print(f"Expire Time : {expire_date}")

    qr = qrcode.QRCode()
    qr.add_data(new_key)
    qr.print_ascii()
    
    print(f"(you can't get again this api key)")