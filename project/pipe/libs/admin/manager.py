import multiprocessing

from tabulate import tabulate


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def start_task(self, task_function, params):
        sn = params['client']['sn']

        process = multiprocessing.Process(
            target=self.__task_wrapper, args=(task_function, params))

        process.start()

        self.tasks[sn] = {
            "process": process,
            "status": "running"
        }

    def __task_wrapper(self, task_function, params):
        try:
            task_function(params)
        except Exception as e:
            print(f"Error in task: {e}")

    def stop_task(self, sn):
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

    def stop_all_tasks(self):
        for sn, task_info in self.tasks.items():
            task = task_info["process"]
            task.terminate()
            task.join()

    def get_task_status(self):
        status_table = [(f"Task {sn}", task_info["status"])
                        for sn, task_info in self.tasks.items()]
        return tabulate(status_table, headers=["Task", "Status"], tablefmt="fancy_grid")
