import cv2
import numpy as np


class BuildVideoResponse:
    def __init__(self, fps, width, height, output) -> None:
        self.n_frames = 0
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(output, self.fourcc, fps, (width, height))

    def append_frames_to_video(self, data):
        frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
        self.out.write(frame)
        self.n_frames += 1

    def get_n_frames(self):
        return self.n_frames

    def release_resources(self):
        self.out.release()
        cv2.destroyAllWindows()
