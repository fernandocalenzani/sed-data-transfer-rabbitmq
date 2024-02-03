import os
import time

import libs.admin.api_backend as ApiBackend
import libs.admin.manager as Manager
import producer.__hub__ as Producer
from consumer.__hub__ import Consumer
from dotenv import load_dotenv
from libs.admin.config import Config
from libs.utils.logger import CustomLogger

load_dotenv()


if __name__ == "__main__":
    try:
        os.system('clear')

        clients = {}
        tasks = {}

        log = CustomLogger('admin', 'manager')
        task_manager = Manager.TaskManager()
        config = Config()

        data, headers = config.get_project_info()
        update_interval = config.get_update_interval()

        log.introduction(data, headers)

        task_manager.perform_action__stop_all_task()

        while True:
            clients = ApiBackend.get_clients(clients)

            tasks = task_manager.manager__update_task(clients)

            for sn, task_info in tasks.items():

                if task_info['status'] == 0 or task_info['status'] == None:
                    pool = task_manager.perform_action_generate_pool(
                        consumer_func=Consumer.start,
                        producer_func=Producer.start,
                        task_info=task_info
                    )

                    for function, params in pool:
                        task_manager.perform_action__start_task(
                            function, params)

                time.sleep(5)

            # os.system('clear')

            log.introduction(data, headers)
            task_manager.manager__monitoring_task()

            time.sleep(update_interval)

    except KeyboardInterrupt as k:
        log.critical("the programm was interrupted!")
        pass

    except Exception as e:
        log.error(e)
