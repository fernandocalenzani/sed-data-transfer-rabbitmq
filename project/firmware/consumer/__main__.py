import _consumer as Consumer
import libs.checker.check_host as Checker


def main():
    Consumer.start_consumer()


if __name__ == "__main__":
    print("[MIMIR] STARTING CONSUMER")

    print("[MIMIR] checking dependencies...")
    if Checker.ping("localhost"):
        print("[MIMIR] Starting consumer")

        main()
    else:
        print("[MIMIR] broker not found, ending consumer")
