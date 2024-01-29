import time

import libs.checker.check_host as Checker
import producer.producer as Producer
from libs.utils.logger import CustomLogger


def start(params):
    log = CustomLogger(params['client']['sn'], 'mimir@producer')
    log.info(f"Creating new producer")
    log.info(f"ip: {params['client']['ip']}")
    log.info(f"name: {params['client']['name']}")

    command = f"curl -i -u {params['rabbitmq']['username']}:{params['rabbitmq']['password']} http://{params['rabbitmq']['host_cli']}:{params['rabbitmq']['port_cli']}/api/vhosts"

    if Checker.check_availability_http(command, 10, 15):
        time.sleep(2)

        params["client"]["url"] = f"rtsp://{params['client']['ip']}:{params['client']['port']}/video_stream"

        Producer.start_producer(params)

    else:
        log.info(f"broker not found, ending consumer")
