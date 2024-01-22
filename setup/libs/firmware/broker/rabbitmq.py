import pickle

import pika


class RabbitMQ:
    def __init__(self, host, port, username, password) -> None:
        self.__host = host
        self.__port = port
        self.__username = username
        self.__pass = password

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
        print(f"[MIMIR] Listening on RabbitMQ channel")
        print(f" ")

        self.set_queue(queue, callback_message)
        self.__channel.start_consuming()
