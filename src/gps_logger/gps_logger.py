
import argparse
import json

from .utils import args
from .server import server

def main():
    args.parse()
    server.start()
