import os

import cv2
import numpy as np
import packages.broker.rabbitmq as Broker
import packages.utils.read_file as Reader


def send_producer(payload, __device):
    __data = Reader.read_host(
        f'{os.path.dirname(os.path.abspath(__file__))}/config/project_config.json')

    __host = __data['hosts']["HOST_RABBITMQ"]["host"]
    __port = __data['hosts']["HOST_RABBITMQ"]["port"]
    __username = os.getenv("RABBIT_PASSWORD")
    __pass = os.getenv("RABBIT_USERNAME")

    rabbitmq = Broker.RabbitMQ(__host, __port, __username, __pass)

    rabbitmq.publish_stream(f"exchange_{__device}", payload, 2, "")


def start_producer(__url):

    cam = cv2.VideoCapture(__url)

    while True:
        ok, frame = cam.read()

        print(cam)

        if not ok:
            print(ok)
            break

        else:
            # pegar do cadastro do cliente:
            __device = os.getenv("DEVICE")
            send_producer(np.array(frame), __device)
