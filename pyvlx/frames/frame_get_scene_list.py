"""Module for get scene list frame classes."""
from pyvlx.const import Command
from pyvlx.exception import PyVLXException
from pyvlx.string_helper import bytes_to_string, string_to_bytes

from .frame import FrameBase


class FrameGetSceneListRequest(FrameBase):
    """Frame for get scene list request."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_SCENE_LIST_REQ)


class FrameGetSceneListConfirmation(FrameBase):
    """Frame for confirmation for scene list request."""

    PAYLOAD_LEN = 1

    def __init__(self, count_scenes=0):
        """Init Frame."""
        super().__init__(Command.GW_GET_SCENE_LIST_CFM)
        self.count_scenes = count_scenes

    def get_payload(self):
        """Return Payload."""
        return bytes([self.count_scenes])

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.count_scenes = payload[0]

    def __str__(self):
        """Return human readable string."""
        return '<FrameGetSceneListConfirmation count_scenes={}/>'.format(self.count_scenes)


class FrameGetSceneListNotification(FrameBase):
    """Frame for scene list notification."""

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_SCENE_LIST_NTF)
        self.scenes = []
        self.remaining_scenes = 0

    def get_payload(self):
        """Return Payload."""
        ret = bytes([len(self.scenes)])
        for number, name in self.scenes:
            ret += bytes([number])
            ret += string_to_bytes(name, 64)
        ret += bytes([self.remaining_scenes])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        number_of_objects = payload[0]
        self.remaining_scenes = payload[-1]
        predicted_len = number_of_objects * 65 + 2
        if len(payload) != predicted_len:
            raise PyVLXException('scene_list_notification_wrong_length')
        self.scenes = []
        for i in range(number_of_objects):
            scene = payload[(i*65+1):(i*65+66)]
            number = scene[0]
            name = bytes_to_string(scene[1:])
            self.scenes.append((number, name))

    def __str__(self):
        """Return human readable string."""
        return '<FrameGetSceneListNotification scenes={} remaining_scenes={}>'.format(self.scenes, self.remaining_scenes)
