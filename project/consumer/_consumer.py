import os

import packages.broker.rabbitmq as Broker
import packages.utils.read_file as Reader
from callback import callback

def start_consumer():
    __data = Reader.read_host(
        f'{os.path.dirname(os.path.abspath(__file__))}/config/project_config.json')

    __host = __data['hosts']["HOST_RABBITMQ"]["host"]
    __port = __data['hosts']["HOST_RABBITMQ"]["port"]
    __username = os.getenv("RABBIT_PASSWORD")
    __pass = os.getenv("RABBIT_USERNAME")

    # pegar do cadastro do cliente:
    __device = os.getenv("DEVICE")

    rabbitmq = Broker.RabbitMQ(__host, __port, __username, __pass)
    rabbitmq.build_broker(f"exchange_{__device}", f"queue_{__device}", "")
    rabbitmq.start(callback, f"queue_{__device}")
