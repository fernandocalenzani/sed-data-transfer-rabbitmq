import libs.broker.rabbitmq as Broker
from libs.utils.logger import CustomLogger


def start(metadata):
    try:
        params = metadata["params"]
        service = metadata["service"]
        callback = metadata["callback"]

        rabbitmq = Broker.RabbitMQ(
            params['rabbitmq']['host'],
            params['rabbitmq']['port'],
            params['rabbitmq']['username'],
            params['rabbitmq']['password']
        )

        queue = f"queue_{service}_{params['client']['sn']}"

        rabbitmq.build_broker(
            f"exchange_{params['client']['sn']}",
            queue,
            queue
        )

        rabbitmq.start(queue, callback)

    except Exception as e:
        log = CustomLogger(params['client']['sn'], 'consumer')
        log.error(e)
