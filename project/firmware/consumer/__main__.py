import _consumer as Consumer
import libs.checker.check_host as Checker
import libs.utils.read_project_config as Reader


def main():
    Consumer.start_consumer()


if __name__ == "__main__":
    print("[MIMIR] STARTING CONSUMER")

    __data = Reader.read_host('host.json')

    __host = __data["HOST_CONSUMER"]["host"]
    __port = __data["HOST_CONSUMER"]["port"]
    print("[MIMIR] checking dependencies...")
    if Checker.ping(__host, __port, 1000, 15):

        main()
    else:
        print("[MIMIR] broker not found, ending consumer")
