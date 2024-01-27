import os
import time
from multiprocessing import Pool

import consumer.__main__ as Consumer
import matplotlib.pyplot as plt
import producer.__main__ as Producer
import psutil
from dotenv import load_dotenv

load_dotenv()

params = {
    "client": {
        "ip": "172.22.0.1",
        "name": "arise_technology",
        "port": "8554",
        "sn": "2024MIMIR1"
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


def start(args):
    core, params = args
    core(params)


if __name__ == "__main__":
    try:
        start_time = time.time()

        tasks = [(Consumer.start, params), (Producer.start, params)]

        pid = psutil.Process()

        cpu_before = pid.cpu_percent(interval=0.1)
        mem_before = pid.memory_info().rss / 1024 / 1024

        with Pool() as pool:
            pool.map(start, tasks)

    except Exception as e:
        print(f"[MIMIR] Error: {e}")

    except KeyboardInterrupt as k:
        print(f"[MIMIR] the programm was interrupted!")
        pass

    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        cpu_after = pid.cpu_percent(interval=0.1)
        mem_after = pid.memory_info().rss / 1024 / 1024

        print(f"Uso de CPU antes: {cpu_before}% | Depois: {cpu_after}%")
        print(
            f"Uso de Memória antes: {mem_before} MB | Depois: {mem_after} MB")
        print(
            f"A função levou {execution_time:.2f} segundos para ser concluída.")
