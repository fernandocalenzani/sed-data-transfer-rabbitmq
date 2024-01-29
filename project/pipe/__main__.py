import time

import consumer.__main__ as Consumer
import libs.admin.get_clients as Clients
import libs.admin.manager as Manager
import producer.__main__ as Producer
from dotenv import load_dotenv
from libs.utils.logger import CustomLogger

load_dotenv()


if __name__ == "__main__":
    try:
        clients = {}
        log = CustomLogger('admin', 'mimir@manager')

        data = [
            ["Project", "Mimir"],
            ["Version", "0.1.0"],
            ["Company", "Arise Technology"],
            ["License", "12345-6"],
        ]
        headers = ["Info", "Value"]

        log.table(data, headers)

        while True:
            task_manager = Manager.TaskManager()

            clients = Clients.get_clients(clients)

            for client_key, client_value in clients.items():
                if client_value['status'] == 0:
                    services = [(Consumer.start, client_value['params']),
                                (Producer.start, client_value['params'])]

                    for task_function, params in services:
                        task_manager.start_task(task_function, params)

            print(task_manager.get_task_status())

            time.sleep(60)

    except KeyboardInterrupt as k:
        log.critical("the programm was interrupted!")
        pass

    except Exception as e:
        log.error(f"Error: {e}")
