import subprocess
import time

import cv2
from libs.utils.logger import CustomLogger


def check_availability_http(command, sn, service, max_attempts=10, wait_time=10):
    attempts = 0
    log = CustomLogger(sn, service)

    while attempts < max_attempts:
        try:
            result = subprocess.run(
                command, shell=True, check=True, capture_output=True, text=True)

            http_status = None
            for line in result.stdout.split('\n'):
                if line.startswith('HTTP/'):
                    http_status = line.split(' ')[1]
                    break

            if http_status == '200':
                return True
        except Exception as e:
            log.error(e)

        time.sleep(wait_time)
        attempts += 1

    return False


def check_availability_rtsp(url):
    try:
        cap = cv2.VideoCapture(url)

        if cap.isOpened():
            return True, cap
        else:
            return False, cap
    except Exception as e:
        return False, cap
