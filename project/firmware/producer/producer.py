import cv2
import numpy as np
import json
import os
from dotenv import load_dotenv
import libs.broker.rabbitmq as Broker

def send_producer(payload):

    load_dotenv()
    _env_host_dir = os.path.join("/firmware", 'config', 'hosts.json')

    with open(_env_host_dir, 'r') as hosts:
        _data_host = json.load(hosts)

    __host = _data_host["HOST_RABBITMQ"]["host"]
    __port = _data_host["HOST_RABBITMQ"]["port"]
    __username = os.getenv("RABBIT_PASSWORD")
    __pass = os.getenv("RABBIT_USERNAME")

    rabbitmq = Broker.RabbitMQ(__host, __port, __username, __pass)
    rabbitmq.publish_stream("exchange_d_face", payload, 2, "")


def start_producer():
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    cam = cv2.VideoCapture(0)

    i = 0
    while (i < 10):
        i += 1

        ok, frame = cam.read()

        send_producer(np.array(frame))

        cv2.imshow("video", frame)

        # wait for 'q' in keypress
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # memory clean
    cam.release()
    cv2.destroyAllWindows()

    return
