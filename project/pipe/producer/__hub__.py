import time

import libs.checker.check_host as Checker
import producer.publisher as Producer
from libs.utils.logger import CustomLogger


def start(metadata):
    params = metadata['params']

    log = CustomLogger(params['client']['sn'], 'producer')
    log.warn(f"Creating new producer")
    log.warn(f"ip: {params['client']['ip']}")
    log.warn(f"name: {params['client']['name']}")

    command = f"curl -i -u {params['rabbitmq']['username']}:{params['rabbitmq']['password']} http://{params['rabbitmq']['host_cli']}:{params['rabbitmq']['port_cli']}/api/vhosts"

    if Checker.check_availability_http(
        command=command,
        sn=params['client']['sn'],
        service='consumer',
        max_attempts=10,
        wait_time=10,
    ):
        time.sleep(2)

        params["client"]["url"] = f"rtsp://{params['client']['ip']}:{params['client']['port']}/video_stream"

        Producer.handler(metadata)

    else:
        log.error(f"broker not found, ending consumer")
