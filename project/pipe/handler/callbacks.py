from handler.build_video_response import BuildVideoResponse
from libs.utils.logger import CustomLogger


class Callbacks:
    def __init__(self):
        log = CustomLogger('callbacks', 'manager')
        self.log = log
        self.builder_video = BuildVideoResponse(
            1, 640, 480, 'video.avi')

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
                'data': payload
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

    def __callback_queue_cam(self, ch, method, properties, payload):
        try:
            metadata = self.__metadata(ch, method, properties, payload)

            if (self.builder_video.get_n_frames() >= 400):
                self.builder_video.release_resources()
            else:
                self.builder_video.append_frames_to_video(payload)

        except Exception as e:
            self.log.error(e)

    def __callback_queue_d_face(self, ch, method, properties, payload):
        try:
            metadata = self.__metadata(ch, method, properties, payload)
            print("callback_queue_d_face")
        except Exception as e:
            self.log.error(e)

    def __callback_queue_r_action(self, ch, method, properties, payload):
        try:
            metadata = self.__metadata(ch, method, properties, payload)
            print("callback_queue_r_action")
        except Exception as e:
            self.log.error(e)

    def __callback_queue_r_emotion(self, ch, method, properties, payload):
        try:
            metadata = self.__metadata(ch, method, properties, payload)
            print("callback_queue_r_emotion")
        except Exception as e:
            self.log.error(e)

    def __callback_queue_r_face(self, ch, method, properties, payload):
        try:
            metadata = self.__metadata(ch, method, properties, payload)
            print("callback_queue_r_face")
        except Exception as e:
            self.log.error(e)

    def __callback_queue_t_object(self, ch, method, properties, payload):
        try:
            metadata = self.__metadata(ch, method, properties, payload)
            print("callback_queue_t_object")
        except Exception as e:
            self.log.error(e)
