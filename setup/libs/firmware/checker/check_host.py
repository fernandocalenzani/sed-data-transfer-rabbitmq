import subprocess
import time

def check_availability_http(command, max_attempts=10, wait_time=10):
    attempts = 0

    while attempts < max_attempts:
        print(
            f"[MIMIR] Attempt {attempts + 1}/{max_attempts} - Verifying host connection")

        try:
            print(command)
            result = subprocess.run(
                command, shell=True, check=True, capture_output=True, text=True)
            print(result)

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

        except Exception as e:
            print(
                f"[MIMIR] The command is not available.\nError: {e}\nWaiting {wait_time}s before next attempt")

        time.sleep(wait_time)
        attempts += 1

    print(f"[MIMIR] host not found, ending")
    return False
