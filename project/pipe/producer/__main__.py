import time
from datetime import datetime

import libs.checker.check_host as Checker
import producer.producer as Producer


def start(params):
    print(f"[MIMIR | Producer] --NEW PRODUCER--")
    print(f"[MIMIR | Producer] ip: {params['client']['ip']}")
    print(f"[MIMIR | Producer] ip: {params['client']['name']}")
    print(f"[MIMIR | Producer] ip: {datetime.now()}")

    command = f"curl -i -u {params['rabbitmq']['username']}:{params['rabbitmq']['password']} http://{params['rabbitmq']['host_cli']}:{params['rabbitmq']['port_cli']}/api/vhosts"

    print("[MIMIR | Producer] checking dependencies...")

    if Checker.check_availability_http(command, 10, 15):
        print("\n\n[MIMIR | Producer] Starting produce service")

        time.sleep(2)

        params["client"]["url"] = f"rtsp://{params['client']['ip']}:{params['client']['port']}/video_stream"

        Producer.start_producer(params)

    else:
        print("[MIMIR | Producer] host not found, ending producer")
