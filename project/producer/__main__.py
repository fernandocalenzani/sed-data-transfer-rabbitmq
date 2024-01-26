import os

import _producer as Producer
import packages.checker.check_host as Checker
import packages.utils.read_file as Reader


def main(url):
    Producer.start_producer(url)


if __name__ == "__main__":
    print("[MIMIR] --PRODUCER--")

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
        print("[MIMIR] Starting producer")

        main("rtsp://172.17.0.1:8554/video_stream")

    else:
        print("[MIMIR] host not found, ending producer")
