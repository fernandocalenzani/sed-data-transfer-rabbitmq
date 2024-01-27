import libs.broker.rabbitmq as Broker
from consumer.callback import callback


def start_consumer(params):
    try:
        rabbitmq = Broker.RabbitMQ(
            params['rabbitmq']['host'],
            params['rabbitmq']['port'],
            params['rabbitmq']['username'],
            params['rabbitmq']['password']
        )

        rabbitmq.build_broker(
            f"exchange_{params['client']['sn']}",
            f"queue_{params['client']['sn']}",
            ""
        )

        rabbitmq.start(callback, f"queue_{params['client']['sn']}")

    except Exception as e:
        print(e)
