import os
import sys
import time

import cv2
import libs.broker.rabbitmq as Broker
from libs.utils.logger import CustomLogger


def publish(params, frame):
    try:
        rabbitmq = Broker.RabbitMQ(
            params['rabbitmq']['host'],
            params['rabbitmq']['port'],
            params['rabbitmq']['username'],
            params['rabbitmq']['password']
        )

        rabbitmq.publish_stream(
            f"exchange_{params['client']['sn']}", frame, 2, "")

    except Exception as e:
        log = CustomLogger(params['client']['sn'], 'producer')
        log.error(e)


def start_producer(params):
    cam = cv2.VideoCapture(params['client']['url'])

    while True:
        try:
            ok, frame = cam.read()

            if ok:
                publish(params, frame)
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
