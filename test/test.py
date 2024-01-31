import asyncio


async def main():
    loop = asyncio.get_event_loop()

    tasks = [
        loop.create_task(function1()),
        loop.create_task(function2()),
        loop.create_task(function3())
    ]

    # Aguardar a conclusão de todas as tarefas
    resultados = await asyncio.gather(*tasks)

    print("Resultados finais:")
    for resultado in resultados:
        print(resultado)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()


"""
        data = pickle.loads(payload)
        processed_image = process_image(data)

        send_response_to_client(
            processed_image, metadata['method']['exchange'])

def process_image(payload):
    processed_image = cv2.cvtColor(payload, cv2.COLOR_BGR2GRAY)
    return processed_image


def send_response_to_client(payload, exchange):
    try:
        cv2.imwrite("processed_image_" + str(exchange) +
                    "_" + str(datetime.now()) + ".jpg", payload)

        print(f"{datetime.now()} Resposta enviada para o cliente: {exchange}.")

    except Exception as e:
        print(e)
 """
