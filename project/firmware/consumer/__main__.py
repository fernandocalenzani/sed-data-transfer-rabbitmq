import _consumer as Consumer
import libs.checker.check_host as Checker
import libs.utils.read_project_config as Reader


def main():
    Consumer.start_consumer()


if __name__ == "__main__":
    print("[MIMIR] --CONSUMER--")

    __data = Reader.read_host('project_config.json')
    __host = __data['hosts']["HOST_CONSUMER"]["host"]
    __port = __data['hosts']["HOST_CONSUMER"]["port"]
    __attempts = __data['settings']["attempt_recovery"]
    __timeout = __data['settings']["timeout_in_sec"]

    print("[MIMIR] checking dependencies...")

    if Checker.ping(__host, __port, __attempts, __timeout):
        print("[MIMIR] Starting consumer")
        main()
    else:
        print("[MIMIR] broker not found, ending consumer")
