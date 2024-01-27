import time
from datetime import datetime

import consumer.consumer as Consumer
import libs.checker.check_host as Checker


def start(params):
    print("[MIMIR] --NEW CONSUMER--")
    print(f"[MIMIR | Consumer] ip: {params['client']['ip']}")
    print(f"[MIMIR | Consumer] ip: {params['client']['name']}")
    print(f"[MIMIR | Consumer] ip: {datetime.now()}")

    command = f"curl -i -u {params['rabbitmq']['username']}:{params['rabbitmq']['password']} http://{params['rabbitmq']['host_cli']}:{params['rabbitmq']['port_cli']}/api/vhosts"

    print("[MIMIR | Consumer] checking dependencies...", end='\r')

    if Checker.check_availability_http(command, 10, 15):
        print("[MIMIR | Consumer] Starting...")

        time.sleep(2)

        Consumer.start_consumer(params)

    else:
        print("[MIMIR | Consumer] broker not found, ending consumer")
