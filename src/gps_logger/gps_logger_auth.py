
import argparse
from .server.auth import api_key

args = None
    
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--api-keys", "-a", type=api_key.api_keys_type, required=True)
    parser.add_argument("--name", "-n", type=str)

    global args
    args = parser.parse_args()

    args.api_keys.create_key(name=args.name)