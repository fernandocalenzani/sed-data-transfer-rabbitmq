import _producer as Producer
import libs.checker.check_host as Checker


def main():
    Producer.start_producer()


if __name__ == "__main__":
    print("[MIMIR] STARTING PRODUCER")

    print("[MIMIR] checking dependencies...")
    if Checker.ping("localhost", ):
        print("[MIMIR] Starting producer")

        main()
    else:
        print("[MIMIR] host not found, ending producer")
