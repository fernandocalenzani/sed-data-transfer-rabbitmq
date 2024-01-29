import multiprocessing

from tabulate import tabulate
import psutil


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def __task_wrapper(self, task_function, params):
        try:
            task_function(params)
        except Exception as e:
            print(f"Error in task: {e}")

    def manager__update_task(self, clients):

        for client_key, client_value in clients.items():
            if client_key not in self.tasks:
                self.tasks[client_key] = {
                    'process': None,
                    'status': 0,
                    'params': client_value,
                }

        for sn, task in self.tasks.items():
            if task["process"] is not None and task["process"].is_alive():
                self.tasks[sn]["status"] = 1
            else:
                self.tasks[sn]["status"] = 0

        return self.tasks

    def manager__get_task(self):
        return self.tasks

    def manager__monitoring_task(self):
        headers = ["SN", "Status", "PID", "IP", "Name", "CPU (%)", "RAM (MB)"]
        rows = []

        for sn, task_info in self.tasks.items():
            status = task_info["status"]
            pid = task_info["process"].pid
            ip = task_info["params"]["client"]["ip"]
            name = task_info["params"]["client"]["name"]

            try:
                process_info = psutil.Process(pid)
                cpu_percent = 1000*process_info.cpu_percent(interval=0.1)
                ram_usage = process_info.memory_info().rss / (1024 * 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                cpu_percent = "N/A"
                ram_usage = "N/A"

            rows.append([sn, status, pid, ip, name,
                        f"{cpu_percent:.2f}", f"{ram_usage:.2f}"])

        table = tabulate(rows, headers, tablefmt="fancy_grid")
        print('- - - | Tasks | - - -')
        print(table)
        print('\n\n')
        print('- - - | Logs | - - -')
        print('\n')

    def perform_action__start_task(self, task_function, params):
        process = multiprocessing.Process(
            target=self.__task_wrapper, args=(task_function, params))
        process.start()

        self.tasks[params['client']['sn']]['process'] = process

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
            print(f"Task with sn {sn} not found")

    def perform_action__stop_all_task(self):
        for sn, task_info in self.tasks.items():
            task = task_info["process"]
            task.terminate()
            task.join()
