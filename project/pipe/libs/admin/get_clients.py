import os

from dotenv import load_dotenv
from libs.utils.api_request import ApiRequest


def get_clients(online_clients):
    load_dotenv()

    clients = {}

    url = f"http://{os.getenv('BACKEND_HOST')}:{os.getenv('BACKEND_PORT')}"
    api = ApiRequest(url)

    res = api.make_request(
        endpoint="api/device/read-all",
    )

    if res.status_code == 200:
        base_clients = res.json()

        for client in base_clients:
            online_client = online_clients.get(client['sn'])

            if online_client is not None:
                clients[client['sn']] = {
                    'status': online_client['status'],
                    'params': {
                        "client": {
                            "ip": client['ip'],
                            "name": client['name'],
                            "port": client['port'],
                            "sn": client['sn'],
                        },
                        "rabbitmq": {
                            "username":  os.getenv("RABBIT_USERNAME"),
                            "password":  os.getenv("RABBIT_PASSWORD"),
                            "host": os.getenv("RABBITMQ_HOST"),
                            "port": os.getenv("RABBITMQ_PORT"),
                            "host_cli": os.getenv("RABBITMQ_CLI_HOST"),
                            "port_cli": os.getenv("RABBITMQ_CLI_PORT"),
                        }
                    }
                }
            else:
                clients[client['sn']] = {
                    'status': 0,
                    'params': {
                        "client": {
                            "ip": client['ip'],
                            "name": client['name'],
                            "port": client['port'],
                            "sn": client['sn'],
                        },
                        "rabbitmq": {
                            "username":  os.getenv("RABBIT_USERNAME"),
                            "password":  os.getenv("RABBIT_PASSWORD"),
                            "host": os.getenv("RABBITMQ_HOST"),
                            "port": os.getenv("RABBITMQ_PORT"),
                            "host_cli": os.getenv("RABBITMQ_CLI_HOST"),
                            "port_cli": os.getenv("RABBITMQ_CLI_PORT"),
                        }
                    }
                }

        return clients
    else:
        return online_clients
