from datetime import datetime

from tabulate import tabulate


class CustomLogger:
    def __init__(self, client_id, service_name):
        self.client_id = client_id
        self.service_name = service_name

    def introduction(self, data, headers):
        print('\n' + '- - - - - - | MIMIR | - - - - - -')
        formatted_data = [
            [f"[{self.service_name}@{self.client_id}]", *row] for row in data]
        table = tabulate(formatted_data, headers, tablefmt="fancy_grid")
        print(table + '\n')

    def debug(self, message):
        print(f"{self.get_prefix()} -DEBUG- {message}")

    def info(self, message):
        print(f"{self.get_prefix()} -INFO- {message}")

    def warn(self, message):
        print(f"{self.get_prefix()} -WARNING- {message}")

    def error(self, message):
        print(f"{self.get_prefix()} -ERROR- {message}")

    def critical(self, message):
        print(f"{self.get_prefix()} -CRITICAL- {message}")

    def graph(self, message):
        print(f"\n{message}\n")

    def get_prefix(self):
        return f"{self.get_timestamp()} [{self.service_name}@{self.client_id}]"

    def get_timestamp(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
