import os

import cv2
import libs.broker.rabbitmq as Broker
import libs.utils.read_env as Reader
import numpy as np


def send_producer(payload):
    __data = Reader.read_host('host.json')

    __host = __data["HOST_RABBITMQ"]["host"]
    __port = __data["HOST_RABBITMQ"]["port"]
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
