import cv2
import numpy as np
import broker.rabbitmq as Broker


def send_producer(payload):
    rabbitmq = Broker.RabbitMQ()
    rabbitmq.publish_stream("exchange_d_face", payload, 2, "")


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
