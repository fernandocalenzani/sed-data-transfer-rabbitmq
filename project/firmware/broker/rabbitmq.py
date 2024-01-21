import json
import os
import pickle

import pika
from dotenv import load_dotenv


class RabbitMQ:
    def __init__(self) -> None:
        load_dotenv()

        _env_host_dir = os.path.join("/firmware", 'libs', 'shared', 'hosts.json')

        with open(_env_host_dir, 'r') as hosts:
            _data_host = json.load(hosts)

        self.__host = _data_host["HOST_RABBITMQ"]["host"]
        self.__port = _data_host["HOST_RABBITMQ"]["port"]
        self.__username = os.getenv("RABBIT_PASSWORD")
        self.__pass = os.getenv("RABBIT_USERNAME")

        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_params = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username, password=self.__pass)
        )

        channel = pika.BlockingConnection(connection_params).channel()

        return channel

    def build_broker(self, exchange_name, queue_name, routing_key):
        self.__channel.exchange_declare(exchange=exchange_name,
                                        exchange_type='direct'
                                        )

        self.__channel.queue_declare(queue=queue_name, durable=True)

        self.__channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    def set_queue(self, queue, callback_message):
        self.__channel.queue_declare(
            queue=queue,
            durable=True
        )

        return self.__channel.basic_consume(queue=queue, auto_ack=True,
                                            on_message_callback=callback_message)

    def publish_stream(self, exchange, body, mode, routing_key):
        self.__channel.basic_publish(exchange=exchange,
                                     routing_key=routing_key,
                                     body=self.frame_to_bytes(body),
                                     properties=pika.BasicProperties(
                                         delivery_mode=mode)
                                     )

    def frame_to_bytes(self, frame):
        return pickle.dumps(frame)

    def bytes_to_frame(self, frame_bytes):
        return pickle.loads(frame_bytes)

    def start(self, callback_message, queue):
        print(f"Listening on RabbitMQ channel")
        self.set_queue(queue, callback_message)
        self.__channel.start_consuming()
