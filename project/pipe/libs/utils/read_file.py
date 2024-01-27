import json

from dotenv import load_dotenv


def read_host(path):
    load_dotenv()
    with open(path, 'r') as file:
        data = json.load(file)
    return data
