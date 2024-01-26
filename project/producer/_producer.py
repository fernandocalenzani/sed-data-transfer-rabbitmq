import os
import sys
import time

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

    __device = os.getenv("DEVICE")

    while True:
        try:
            ok, frame = cam.read()

            if ok:
                send_producer(np.array(frame), __device)
            else:
                cam.release()
                cv2.destroyAllWindows()
                time.sleep(5)
                cam = cv2.VideoCapture(__url)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except cv2.error as e:
            sys.stdout = open(os.devnull, 'w')
            print(f"Erro OpenCV: {e}")
            sys.stdout = sys.__stdout__
