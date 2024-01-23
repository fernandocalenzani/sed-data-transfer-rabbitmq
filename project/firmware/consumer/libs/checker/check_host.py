import subprocess
import time

import pika
from requests.exceptions import RequestException


def check_availability_http(command, max_attempts=10, wait_time=10):
    attempts = 0

    while attempts < max_attempts:
        print(
            f"[MIMIR] Attempt {attempts + 1}/{max_attempts} - Verifying command curl")

        try:
            result = subprocess.run(
                command, shell=True, check=True, capture_output=True, text=True)

            http_status = None
            for line in result.stdout.split('\n'):
                if line.startswith('HTTP/'):
                    http_status = line.split(' ')[1]
                    break

            if http_status == '200':
                print(
                    f"[MIMIR] Connected Successfully")
                return True
            else:
                print(
                    f"[MIMIR] The command is not available.\nError: {result.stderr}\nWaiting {wait_time}s before next attempt")

        except RequestException as e:
            print(
                f"[MIMIR] The command is not available.\nError: {e}\nWaiting {wait_time}s before next attempt")

        time.sleep(wait_time)
        attempts += 1

    print(f"[MIMIR] host not found, ending")
    return False


def check_availability_rabbitmq(
    host,
    port,
    username,
    password,
    max_attempts=10,
    wait_time=10
):

    attempts = 0

    while attempts < max_attempts:
        print(
            f"[MIMIR] Attempt {attempts + 1}/{max_attempts} - Verifying command curl")

        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters("179.21.0.1", "4000"))
            connection.close()
            print(
                f"[MIMIR] Connected Successfully")

            return True

        except RequestException as e:
            print(
                f"[MIMIR] The command is not available.\nError: {e}\nWaiting {wait_time}s before next attempt")

        time.sleep(wait_time)
        attempts += 1

    print(f"[MIMIR] host not found, ending")
    return False
