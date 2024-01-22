import _producer as Producer
import libs.checker.check_host as Checker
import libs.utils.read_project_config as Reader


def main():
    Producer.start_producer()


if __name__ == "__main__":
    print("[MIMIR] --PRODUCER--")

    __data = Reader.read_host('project_config.json')
    __host = __data['hosts']["HOST_PRODUCER"]["host"]
    __port = __data['hosts']["HOST_PRODUCER"]["port"]
    __attempts = __data['settings']["attempt_recovery"]
    __timeout = __data['settings']["timeout_in_sec"]

    print("[MIMIR] checking dependencies...")

    if Checker.ping(__host, __port, __attempts, __timeout):
        print("[MIMIR] Starting producer")
        main()
    else:
        print("[MIMIR] host not found, ending producer")
