import base64
import hashlib
import hmac
import os
import time

import requests
from dotenv import load_dotenv


def gen_api_key():
    load_dotenv()

    data = os.getenv('BACKEND_SECRET_DATA')
    secret = os.getenv('BACKEND_SECRET_KEY')

    timestamp = str(int(time.time()))
    dados = f'{timestamp}:{data}'

    hash_hmac = hmac.new(secret.encode('utf-8'),
                         dados.encode('utf-8'), hashlib.sha256)
    chave_api = base64.urlsafe_b64encode(
        hash_hmac.digest()).decode('utf-8')

    chave_api = chave_api.replace('+', '-').replace('/', '_')

    return f'{timestamp}.{chave_api}'


class ApiRequest:
    def __init__(self, base_url):
        self.base_url = base_url
        self.secret = gen_api_key()

        self.headers = {
            "Authorization": f"Bearer {self.secret}",
            "Content-Type": "application/json",
        }

    def make_request(self, endpoint, method="GET", data=None):
        url = f"{self.base_url}/{endpoint}"

        if method.upper() == "GET":
            response = requests.get(url, headers=self.headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=self.headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=self.headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=self.headers)
        else:
            raise ValueError(f"Error: {method}")

        return response
