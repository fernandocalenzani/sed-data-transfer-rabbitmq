import base64
import hashlib
import hmac
import time

import requests


def gen_api_key(secret, data):
    timestamp = str(int(time.time()))
    dados = f'{timestamp}:{data}'

    hash_hmac = hmac.new(secret.encode('utf-8'),
                         dados.encode('utf-8'), hashlib.sha256)
    chave_api = base64.urlsafe_b64encode(hash_hmac.digest()).decode('utf-8')

    # Substitua os caracteres "+" e "/" por "-" e "_"
    chave_api = chave_api.replace('+', '-').replace('/', '_')

    return f'{timestamp}.{chave_api}'


api = ApiRequest(
    f"http://localhost:5000")

res = api.make_request("api/device/read-all")
print(res.status_code)
print(res.json())
