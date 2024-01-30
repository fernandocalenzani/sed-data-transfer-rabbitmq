import pickle
from datetime import datetime

import cv2
import numpy as np
from libs.utils.logger import CustomLogger


def callback(ch, method, properties, payload):
    metadata = {
        'ch': {},
        'method': {},
        'properties': {},
        'data': payload
    }

    metadata['ch']['channel_number'] = ch.channel_number
    metadata['ch']['connection'] = ch.connection
    metadata['ch']['is_open'] = ch.is_open
    metadata['method']['consumer_tag'] = method.consumer_tag
    metadata['method']['delivery_tag'] = method.delivery_tag
    metadata['method']['exchange'] = method.exchange
    metadata['method']['redelivered'] = method.redelivered
    metadata['method']['routing_key'] = method.routing_key
    metadata['properties']['delivery_mode'] = properties.delivery_mode

    data = pickle.loads(payload)
    processed_image = process_image(data)

    send_response_to_client(processed_image, metadata['method']['exchange'])


def process_image(payload):
    processed_image = cv2.cvtColor(payload, cv2.COLOR_BGR2GRAY)
    """     cv2.imwrite("processed_image" + str(random.randint(1, 10)) +
                    ".jpg", processed_image)
    """
    return cv2.imencode('.jpg', processed_image)[1].tobytes()


def send_response_to_client(payload, exchange):
    try:
        log.info(f"{datetime.now()} Resposta enviada para o cliente: {exchange}.")

    except Exception as e:
        log.error(f"Erro ao exibir imagem: {e}")
