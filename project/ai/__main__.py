import os

import _consumer as Consumer
import packages.checker.check_host as Checker
import packages.utils.read_file as Reader


def main():
    print("ai project started")


if __name__ == "__main__":
    print("[MIMIR] --AI--")

    __data = Reader.read_host(
        f'{os.path.dirname(os.path.abspath(__file__))}/config/project_config.json')

    __host = __data['hosts']["HOST_RABBITMQ_CLI"]["host"]
    __port = __data['hosts']["HOST_RABBITMQ_CLI"]["port"]
    __attempts = __data['settings']["attempt_recovery"]
    __timeout = __data['settings']["timeout_in_sec"]
    __username = os.getenv("RABBIT_PASSWORD")
    __pass = os.getenv("RABBIT_USERNAME")
    command = f"curl -i -u {__username}:{__pass} http://{__host}:{__port}/api/vhosts"

    print("[MIMIR] checking dependencies...")

    if Checker.check_availability_http(command, __attempts, __timeout):
        print("[MIMIR] Starting consumer")
        main()
    else:
        print("[MIMIR] broker not found, ending consumer")
