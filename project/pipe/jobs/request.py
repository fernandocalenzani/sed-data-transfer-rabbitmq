import os

import requests


def receive_request():
    url = f"http://{os.getenv('BACKEND_HOST')}:{os.getenv('BACKEND_PORT')}/api/clients"

    headers = {'Authorization': f'Bearer {os.getenv("BACKEND_SECRET_KEY")}'}

    response = requests.get(url, headers=headers)

    return response.data


def gen_jwt():

    return
