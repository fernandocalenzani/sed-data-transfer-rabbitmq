import pickle
import random

import cv2
import broker.rabbitmq as Broker


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


def test_start_consumer():
    rabbitmq = Broker.RabbitMQ()
    rabbitmq.build_broker("exchange_d_face", "queue_d_face", "")
    rabbitmq.start(callback, "queue_d_face")


test_start_consumer()
