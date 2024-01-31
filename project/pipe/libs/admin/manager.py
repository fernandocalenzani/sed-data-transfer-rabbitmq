import multiprocessing

import psutil
from handler.callbacks import Callbacks
from libs.utils.logger import CustomLogger
from tabulate import tabulate


class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.config = {
            "services": ["CAM", "D_FACE", "R_ACTION",
                         "R_EMOTION", "R_FACE", "T_OBJECT"
                         ]
        }
        self.log = CustomLogger('manager', 'admin')

    def __task_wrapper(self, task_function, params):
        try:
            task_function(params)
        except Exception as e:
            self.log.error(e)

    def manager__get_config(self):
        return self.config

    def manager__get_task(self):
        return self.tasks

    def manager__update_task(self, clients):

        for client_key, client_value in clients.items():
            if client_key not in self.tasks:
                self.tasks[client_key] = {
                    'process': None,
                    'status': 0,
                    'params': client_value,
                    'errors': 0,
                }

        for sn, task in self.tasks.items():
            if task["process"] is not None and task["process"].is_alive():
                self.tasks[sn]["status"] = 1
            else:
                self.tasks[sn]["status"] = 0

        return self.tasks

    def manager__update_error(self, sn):
        self.tasks[sn]["status"] = 1

        return self.tasks

    def manager__get_task(self):
        return self.tasks

    def manager__monitoring_task(self):
        headers = ["SN", "Status", "PID", "IP",
                   "Name", "CPU (%)", "RAM (MB)", "Error"]
        rows = []
        total_errors = 0

        for sn, task_info in self.tasks.items():
            status = task_info["status"]
            pid = task_info["process"].pid
            ip = task_info["params"]["client"]["ip"]
            name = task_info["params"]["client"]["name"]

            try:
                process_info = psutil.Process(pid)
                cpu_percent = process_info.cpu_percent(interval=0.1)
                ram_usage = process_info.memory_info().rss / (1024 * 1024)
                error = 0

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                cpu_percent = "N/A"
                ram_usage = "N/A"
                error = 1
                total_errors += 1

            rows.append([sn, status, pid, ip, name,
                        f"{cpu_percent:.2f}", f"{ram_usage:.2f}", error])

        total_ram = sum(float(row[6]) for row in rows if row[6] != "N/A")
        total_processes = len(rows)
        total_cpu = sum(float(row[5]) for row in rows if row[5] != "N/A")

        rows.append(["Total", total_processes, "-", "-", "-",
                    f"{total_cpu:.2f}", f"{total_ram:.2f}", total_errors])

        table = tabulate(rows, headers, tablefmt="fancy_grid")
        self.log.graph('- - - - - - | Tasks | - - - - - -')
        self.log.graph(table)
        self.log.graph('- - - - - - | Logs | - - - - - -')

    def perform_action__start_task(self, task_function, metadata):
        process = multiprocessing.Process(
            target=self.__task_wrapper, args=(task_function, metadata))
        process.start()

        self.tasks[metadata['params']['client']['sn']]['process'] = process

    def perform_action__stop_task(self, sn):
        if sn in self.tasks:

            task_info = self.tasks[sn]
            task = task_info["process"]

            if task.is_alive():
                task.terminate()
                task.join()
                task_info["status"] = "stopped"
            else:
                task_info["status"] = "done"
        else:
            self.log.warn(f"Task with sn {sn} not found")

    def perform_action__stop_all_task(self):
        if self.tasks.items() is not None:
            for sn, task_info in self.tasks.items():
                task = task_info["process"]
                task.terminate()
                task.join()

    def perform_action_generate_pool(self, consumer_func, producer_func, task_info):
        services = task_info['params']['client']['services']

        callbacks = Callbacks()

        pool = [
            (producer_func, {
                "params": task_info['params'],
                "service": services[0],
                "callback": callbacks.get_callback_by_service("CAM")
            })
        ]

        for i in range(0, len(services)):
            metadata = {
                "params": task_info['params'],
                "service": services[i],
                "callback": callbacks.get_callback_by_service(services[i])
            }

            pool.append((consumer_func, metadata))

        return pool
