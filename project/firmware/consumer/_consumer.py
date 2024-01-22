import json
import os
import pickle
import random

import cv2
import libs.broker.rabbitmq as Broker
from dotenv import load_dotenv


def callback(ch, method, properties, payload):
    data = pickle.loads(payload)
    processed_image = process_image(data)
    send_response_to_client(processed_image)


def process_image(payload):
    processed_image = cv2.cvtColor(payload, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("processed_image" + str(random.randint(1, 100)) +
                ".jpg", processed_image)

    return cv2.imencode('.jpg', processed_image)[1].tobytes()


def send_response_to_client(payload):
    print("Resposta enviada para o cliente.")


def start_consumer():
    load_dotenv()
    _env_host_dir = os.path.join('/config', 'hosts.json')

    with open(_env_host_dir, 'r') as hosts:
        _data_host = json.load(hosts)

    __host = _data_host["HOST_RABBITMQ"]["host"]
    __port = _data_host["HOST_RABBITMQ"]["port"]
    __username = os.getenv("RABBIT_PASSWORD")
    __pass = os.getenv("RABBIT_USERNAME")

    rabbitmq = Broker.RabbitMQ(__host, __port, __username, __pass)
    rabbitmq.build_broker("exchange_d_face", "queue_d_face", "")
    rabbitmq.start(callback, "queue_d_face")
