import os

import cv2
import numpy as np
import packages.broker.rabbitmq as Broker
import packages.utils.read_project_config as Reader


def send_producer(payload, __device):
    __data = Reader.read_host('project_config.json')
    __host = __data['hosts']["HOST_RABBITMQ"]["host"]
    __port = __data['hosts']["HOST_RABBITMQ"]["port"]
    __username = os.getenv("RABBIT_PASSWORD")
    __pass = os.getenv("RABBIT_USERNAME")

    rabbitmq = Broker.RabbitMQ(__host, __port, __username, __pass)
    rabbitmq.publish_stream(f"exchange_{__device}", payload, 2, "")


def start_producer():
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    cam = cv2.VideoCapture(0)

    i = 0
    while (i < 10):
        i += 1

        ok, frame = cam.read()

        # pegar do cadastro do cliente:
        __device = os.getenv("DEVICE")

        send_producer(np.array(frame), __device)

        cv2.imshow("video", frame)

        # wait for 'q' in keypress
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # memory clean
    cam.release()
    cv2.destroyAllWindows()

    return
