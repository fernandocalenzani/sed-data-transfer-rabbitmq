import os
import time

import consumer.__main__ as Consumer
import libs.admin.api_backend as ApiBackend
import libs.admin.manager as Manager
import producer.__main__ as Producer
from dotenv import load_dotenv
from libs.utils.logger import CustomLogger

load_dotenv()


if __name__ == "__main__":
    try:
        clients = {}
        tasks = {}
        update_interval = 5
        data = [
            ["Project", "Mimir"],
            ["Version", "0.1.0"],
            ["Company", "Arise Technology"],
            ["Setting", f"update each {update_interval}s"],
            ["License", "12345-6"],
        ]
        headers = ["Info", "Value"]

        os.system('clear')

        log = CustomLogger('admin', 'manager')

        log.introduction(data, headers)

        task_manager = Manager.TaskManager()
        task_manager.perform_action__stop_all_task()

        while True:

            clients = ApiBackend.get_clients(clients)

            tasks = task_manager.manager__update_task(clients)

            for sn, task_info in tasks.items():

                if task_info['status'] == 0 or task_info['status'] == None:
                    services = [(Consumer.start, task_info['params']),
                                (Producer.start, task_info['params'])]

                    for function, params in services:
                        task_manager.perform_action__start_task(
                            function, params)

                time.sleep(5)

            os.system('clear')

            log.table(data, headers)
            task_manager.manager__monitoring_task()

            time.sleep(update_interval)

    except KeyboardInterrupt as k:
        log.critical("the programm was interrupted!")
        pass

    except Exception as e:
        log.error(f"Error: {e}")
