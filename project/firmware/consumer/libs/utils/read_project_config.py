import json
import os

from dotenv import load_dotenv


def read_host(to_read):
    load_dotenv()
    _dir = os.path.join(os.getcwd(), 'config', to_read)

    with open(_dir, 'r') as hosts:
        data = json.load(hosts)

    return data
