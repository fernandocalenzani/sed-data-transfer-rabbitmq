import logging

from tabulate import tabulate


class CustomLogger:
    def __init__(self, client_id, service_name):
        self.logger = logging.getLogger(f"{service_name}_{client_id}")
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def table(self, data, headers):
        print('- - - | ADMIN | - - -')
        formatted_data = [[f"[{self.logger.name}]", *row] for row in data]
        table = tabulate(formatted_data, headers, tablefmt="fancy_grid")
        self.logger.info(f"\n{table}")
        print('\n')
