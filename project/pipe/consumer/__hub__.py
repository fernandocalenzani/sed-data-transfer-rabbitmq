import time

import consumer.queues as Consumer
import libs.checker.check_host as Checker
from libs.utils.logger import CustomLogger


def start(metadata):
    params = metadata['params']

    log = CustomLogger(params['client']['sn'], 'consumer')
    log.info(f"Creating new consumer")
    log.info(f"ip: {params['client']['ip']}")
    log.info(f"name: {params['client']['name']}")

    command = f"curl -i -u {params['rabbitmq']['username']}:{params['rabbitmq']['password']} http://{params['rabbitmq']['host_cli']}:{params['rabbitmq']['port_cli']}/api/vhosts"

    if Checker.check_availability_http(
        command=command,
        sn=params['client']['sn'],
        service='consumer',
        max_attempts=10,
        wait_time=10,
    ):

        time.sleep(2)
        Consumer.start(metadata)

    else:
        log.error(f"broker not found, ending consumer")
