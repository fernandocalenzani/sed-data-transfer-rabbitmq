import broker.rabbitmq as Broker
import cv2
import numpy as np
from libs.utils.logger import CustomLogger

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
cam = cv2.VideoCapture(0)

i = 0
while (i < 10):
    i += 1

    ok, frame = cam.read()

    send_producer(np.array(frame))

    cv2.imshow("video", frame)

    # wait for 'q' in keypress
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# memory clean
cam.release()
cv2.destroyAllWindows()
