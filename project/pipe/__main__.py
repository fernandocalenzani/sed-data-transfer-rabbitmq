import os
import time
from multiprocessing import Pool

import consumer.__main__ as Consumer
import matplotlib.pyplot as plt
import producer.__main__ as Producer
import psutil
from dotenv import load_dotenv
from tabulate import tabulate

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
        pid = psutil.Process()

        time_t0 = time.time(),
        cpu_t0 = pid.cpu_percent(interval=0.1)
        ram_t0 = pid.memory_info().rss / 1024 / 1024
        mem__t0 = psutil.virtual_memory().percent
        disk_t0 = psutil.disk_usage('/').percent
        swap_t0 = psutil.swap_memory().percent
        battery_t0 = psutil.sensors_battery().percent if psutil.sensors_battery() else None

        tasks = [(Consumer.start, params), (Producer.start, params)]

        with Pool() as pool:
            pool.map(start, tasks)

    except Exception as e:
        print(f"[MIMIR] Error: {e}")

    except KeyboardInterrupt as k:
        print(f"[MIMIR] the programm was interrupted!")
        pass

    finally:
        print(f"\n\n[MIMIR] Statistics:")

        time_tn = time.time(),
        cpu_tn = pid.cpu_percent(interval=0.1)
        ram_tn = pid.memory_info().rss / 1024 / 1024
        mem__tn = psutil.virtual_memory().percent
        disk_tn = psutil.disk_usage('/').percent
        swap_tn = psutil.swap_memory().percent
        battery_tn = psutil.sensors_battery().percent if psutil.sensors_battery() else None

        table = [
            ["Start", "End", f"{(time_tn[0] - time_t0[0]):.2f}s"],
            ["CPU", f"{cpu_t0}%", f"{cpu_tn}%"],
            ["RAM (MB)", f"{(ram_t0):.2f} MB", f"{(ram_tn):.2f} MB"],
            ["Disk (MB)", f"{disk_t0} MB", f"{disk_tn} MB"],
            ["Swap", f"{swap_t0}%", f"{swap_tn}%"],
            ["Battery", f"{battery_t0}%", f"{battery_tn}%"],
        ]

        print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
