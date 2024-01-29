async def main():
    tasks = []
    clients = {}

    while True:
        clients = task_get_clients(clients)

        for client_key, client_value in clients.items():
            print(client_key, client_value)

            if client_value['status'] == 0:
                task = asyncio.create_task(task_pool(client_value['data']))

                tasks[client_value['data']['client']['sn']] = {
                    'task': task, 'sn': client_value['data']['client']['sn']}

        await asyncio.gather(*tasks)

        for client in clients:
            task = tasks.get(client[1]['data']['client']['sn'])

            if task['task'].done():
                clients[f"{client[1]['data']['client']['sn']}"]['status'] = 0

        time.sleep(10)
