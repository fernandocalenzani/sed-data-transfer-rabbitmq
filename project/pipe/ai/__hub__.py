import libs.admin.manager as Manager
import numpy as np
import torch
from ultralytics import YOLO


class Predictions():
    def __init__(self):
        task_manager = Manager.TaskManager()
        self.params = task_manager.manager__get_config()

        self.conf = 0.5

        self.model_d_object = YOLO("ai/yolov8n.pt")

    def d_object(self, frame, classes=[]):
        if classes:
            results = self.model_d_object.predict(
                np.array(frame), classes=classes, conf=self.conf)
        else:
            results = self.model_d_object.predict(
                frame, conf=self.conf)

        return results

    def d_face(self, frame, classes=[]):

        return []

    def r_action(self, frame, classes=[]):

        return []

    def r_emotion(self, frame, classes=[]):

        return []

    def r_face(self, frame, classes=[]):

        return []

    def t_object(self, frame, classes=[]):

        return []
