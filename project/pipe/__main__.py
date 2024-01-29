import asyncio
import os
import random
import time
from multiprocessing import Pool, Process, Queue

import consumer.__main__ as Consumer
import producer.__main__ as Producer
import psutil
from dotenv import load_dotenv
from libs.utils.api_request import ApiRequest
from tabulate import tabulate
from termcolor import colored

load_dotenv()


def task_get_clients(online_clients):
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
                    'data': {
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
                    'data': {
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


def task_start(args):
    core, params = args
    core(params)


def task_pool(params):
    try:
        tasks = [(Consumer.start, params), (Producer.start, params)]

        with Pool() as pool:
            pool.map(task_start, tasks)

    except Exception as e:
        print(f"[MIMIR] Error: {e}")

    except KeyboardInterrupt as k:
        print(f"[MIMIR] the programm was interrupted!")
        pass


"""
pid = psutil.Process()

time_t0 = time.time(),
cpu_t0 = pid.cpu_percent(interval=0.1)
ram_t0 = pid.memory_info().rss / 1024 / 1024
mem_t0 = psutil.virtual_memory().percent
disk_t0 = psutil.disk_usage('/').percent
swap_t0 = psutil.swap_memory().percent
battery_t0 = psutil.sensors_battery().percent if psutil.sensors_battery() else None

print(f"\n\n[MIMIR] Statistics:")

time_tn = time.time(),
cpu_tn = pid.cpu_percent(interval=0.1)
ram_tn = pid.memory_info().rss / 1024 / 1024
mem_tn = psutil.virtual_memory().percent
disk_tn = psutil.disk_usage('/').percent
swap_tn = psutil.swap_memory().percent
battery_tn = psutil.sensors_battery().percent if psutil.sensors_battery() else None

table = [
    ["Start", "End", f"{(time_tn[0] - time_t0[0]):.2f}s"],
    ["CPU", f"{cpu_t0}%", f"{cpu_tn}%"],
    ["RAM (MB)", f"{(ram_t0):.2f} MB", f"{(ram_tn):.2f} MB"],
    ["VM (MB)", f"{(mem_t0):.2f} MB", f"{(mem_tn):.2f} MB"],
    ["Disk (MB)", f"{disk_t0} MB", f"{disk_tn} MB"],
    ["Swap", f"{swap_t0}%", f"{swap_tn}%"],
    ["Battery", f"{battery_t0}%", f"{battery_tn}%"],
]

print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
"""

""" if __name__ == "__main__":
    try:
        asyncio.run(main())

    except Exception as e:
        print(f"[MIMIR] Error: {e}")

 """


async def main():
    tasks = []
    clients = {}

    while True:
        clients = task_get_clients(clients)

        for client_key, client_value in clients.items():
            print(client_key, client_value)

            if client_value['status'] == 0:
                task = asyncio.create_task(task_pool(client_value['data']))

                tasks[client_value['data']['client']['sn']] = {
                    'task': task, 'sn': client_value['data']['client']['sn']}

        await asyncio.gather(*tasks)

        for client in clients:
            task = tasks.get(client[1]['data']['client']['sn'])

            if task['task'].done():
                clients[f"{client[1]['data']['client']['sn']}"]['status'] = 0

        time.sleep(10)


asyncio.run(main())
