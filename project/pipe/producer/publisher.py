import os
import sys
import time

import cv2
import libs.broker.rabbitmq as Broker
from libs.utils.logger import CustomLogger


def publish(metadata, frame):
    try:
        params = metadata["params"]

        rabbitmq = Broker.RabbitMQ(
            params['rabbitmq']['host'],
            params['rabbitmq']['port'],
            params['rabbitmq']['username'],
            params['rabbitmq']['password']
        )

        queue = f"queue_D_FACE_{params['client']['sn']}"

        rabbitmq.publish_stream(
            f"exchange_{params['client']['sn']}", frame, 2, queue)

    except Exception as e:
        log = CustomLogger(params['client']['sn'], 'producer')
        log.error(e)


def handler(metadata):
    params = metadata['params']

    cam = cv2.VideoCapture(params['client']['url'])

    while True:
        try:
            ok, frame = cam.read()

            if ok:
                publish(metadata, frame)
            else:
                cam.release()
                cv2.destroyAllWindows()
                time.sleep(5)
                cam = cv2.VideoCapture(params['client']['url'])

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except cv2.error as e:
            log = CustomLogger(params['client']['sn'], 'producer')
            log.critical(e)

            sys.stdout = open(os.devnull, 'w')
            sys.stdout = sys.__stdout__
