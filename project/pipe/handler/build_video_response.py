""" import cv2
import numpy as np
from libs.admin.config import Config


class BuildVideoResponse:
    def __init__(self, output) -> None:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 1
        frame_size = (640, 480)

        self.n_frames = 0
        self.out = cv2.VideoWriter(
            output,
            fourcc,
            fps,
            frame_size
        )

    def append_frames_to_video(self, data):
        self.out.write(data)
        self.n_frames += 1

    def get_n_frames(self):
        return self.n_frames

    def release_resources(self):
        self.out.release()
        cv2.destroyAllWindows()
 """
