import asyncio
import pickle
import time
from datetime import datetime

import cv2
from libs.utils.logger import CustomLogger


class Callbacks:
    def __init__(self):
        log = CustomLogger('callbacks', 'manager')
        self.log = log
        self.loop = asyncio.get_event_loop()

        # self.builder_video = BuildVideoResponse('data/video')

    def get_callback_by_service(self, service):
        try:
            if (service == "CAM"):
                return self.__callback_queue_cam

            elif (service == "D_FACE"):
                return self.__callback_queue_d_face

            elif (service == "R_ACTION"):
                return self.__callback_queue_r_action

            elif (service == "R_EMOTION"):
                return self.__callback_queue_r_emotion

            elif (service == "R_FACE"):
                return self.__callback_queue_r_face

            elif (service == "T_OBJECT"):
                return self.__callback_queue_t_object

            else:
                raise ValueError("Service is not available")

        except ValueError as e:
            self.log.error(e)

    def __metadata(self, ch, method, properties, payload):
        try:
            metadata = {
                'ch': {},
                'method': {},
                'properties': {},
                'frame': pickle.loads(payload)
            }

            metadata['ch']['channel_number'] = ch.channel_number
            metadata['ch']['connection'] = ch.connection
            metadata['ch']['is_open'] = ch.is_open
            metadata['method']['consumer_tag'] = method.consumer_tag
            metadata['method']['delivery_tag'] = method.delivery_tag
            metadata['method']['exchange'] = method.exchange
            metadata['method']['redelivered'] = method.redelivered
            metadata['method']['routing_key'] = method.routing_key
            metadata['properties']['delivery_mode'] = properties.delivery_mode

            return metadata
        except Exception as e:
            self.log.error(e)

    def __controller(self, ch, method, properties, payload):

        task_d_face = self.loop.create_task(self.__callback_queue_d_face(
            ch, method, properties, payload))

        task_r_action = self.loop.create_task(self.__callback_queue_r_action(
            ch, method, properties, payload))

        task_r_emotion = self.loop.create_task(self.__callback_queue_r_emotion(
            ch, method, properties, payload))

        task_r_face = self.loop.create_task(self.__callback_queue_r_face(
            ch, method, properties, payload))

        task_t_object = self.loop.create_task(self.__callback_queue_t_object(
            ch, method, properties, payload))

        resultados = self.loop.run_until_complete(
            asyncio.gather(
                task_d_face,
                task_r_action,
                task_r_emotion,
                task_r_face,
                task_t_object
            ))

        return resultados

    def __callback_queue_cam(self, ch, method, properties, payload):
        try:
            metadata = self.__metadata(ch, method, properties, payload)

            self.__controller(
                ch, method, properties, metadata)

        except Exception as e:
            self.log.error(e)

    async def __callback_queue_d_face(self, ch, method, properties, payload):
        try:
            cv2.imwrite(
                f'data/d_face_{str(datetime.now())}.jpg', payload['frame'])

        except Exception as e:
            self.log.error(e)

    async def __callback_queue_r_action(self, ch, method, properties, payload):
        try:
            cv2.imwrite(
                f'data/r_action_{str(datetime.now())}.jpg', payload['frame'])

        except Exception as e:
            self.log.error(e)

    async def __callback_queue_r_emotion(self, ch, method, properties, payload):
        try:
            cv2.imwrite(
                f'data/r_emotion_{str(datetime.now())}.jpg', payload['frame'])

        except Exception as e:
            self.log.error(e)

    async def __callback_queue_r_face(self, ch, method, properties, payload):
        try:
            cv2.imwrite(
                f'data/r_face_{str(datetime.now())}.jpg', payload['frame'])

        except Exception as e:
            self.log.error(e)

    async def __callback_queue_t_object(self, ch, method, properties, payload):
        try:
            cv2.imwrite(
                f'data/t_object_{str(datetime.now())}.jpg', payload['frame'])
        except Exception as e:
            self.log.error(e)
