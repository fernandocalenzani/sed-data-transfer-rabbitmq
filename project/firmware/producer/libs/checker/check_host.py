import socket
import time


def ping(host="localhost", port=5672, max_attempts=1000, wait_time=10):
    attempts = 0

    while attempts < max_attempts:
        print(
            f"[MIMIR] Attempt {attempts + 1} of {max_attempts} - Verifying {host}:{port}")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((host, port))
            print(f"[MIMIR] Connected on {host}:{port} successfully")
            return True

        except socket.error:
            print(
                f"[MIMIR] The {host}:{port} is not available. Waiting {wait_time}s before next attempt")
            time.sleep(wait_time)
            attempts += 1
        finally:
            sock.close()

    print(f"[MIMIR] {host}:{port} not found, ending")
    return False
