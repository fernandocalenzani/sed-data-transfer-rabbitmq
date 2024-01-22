import _producer as Producer
import libs.checker.check_host as Checker
import libs.utils.read_project_config as Reader


def main():
    Producer.start_producer()


if __name__ == "__main__":
    print("[MIMIR] STARTING PRODUCER")
    __data = Reader.read_host('host.json')

    __host = __data["HOST_PRODUCER"]["host"]
    __port = __data["HOST_PRODUCER"]["port"]
    print("[MIMIR] checking dependencies...")
    if Checker.ping(__host, __port, 1000, 15):
        print("[MIMIR] Starting producer")

        main()
    else:
        print("[MIMIR] host not found, ending producer")
