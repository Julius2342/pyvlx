"""Module for sending command to gw."""
from enum import Enum
from typing import Optional

from pyvlx.const import Command, Originator, Priority, Velocity

from .frame import FrameBase


class FrameActivateSceneRequest(FrameBase):
    """Frame for sending command to gw."""

    PAYLOAD_LEN = 6

    def __init__(
            self,
            scene_id: Optional[int] = None,
            session_id: Optional[int] = None,
            originator: Originator = Originator.USER,
            velocity: Velocity = Velocity.DEFAULT,
    ):
        """Init Frame."""
        super().__init__(Command.GW_ACTIVATE_SCENE_REQ)
        self.scene_id = scene_id
        self.session_id = session_id
        self.originator = originator
        self.priority = Priority.USER_LEVEL_2
        self.velocity = velocity

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        assert self.scene_id is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.originator.value])
        ret += bytes([self.priority.value])
        ret += bytes([self.scene_id])
        ret += bytes([self.velocity.value])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.originator = Originator(payload[2])
        self.priority = Priority(payload[3])
        self.scene_id = payload[4]
        self.velocity = Velocity(payload[5])

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} scene_id="{}" session_id="{}" originator="{}" velocity="{}"/>'.format(
            type(self).__name__, self.scene_id, self.session_id, self.originator, self.velocity
        )


class ActivateSceneConfirmationStatus(Enum):
    """Enum class for status of command send confirmation."""

    ACCEPTED = 0
    ERROR_INVALID_PARAMETER = 1
    ERROR_REQUEST_REJECTED = 2


class FrameActivateSceneConfirmation(FrameBase):
    """Frame for confirmation of command send frame."""

    PAYLOAD_LEN = 3

    def __init__(self, session_id: Optional[int] = None, status: Optional[ActivateSceneConfirmationStatus] = None):
        """Init Frame."""
        super().__init__(Command.GW_ACTIVATE_SCENE_CFM)
        self.session_id = session_id
        self.status = status

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.status is not None
        assert self.session_id is not None
        ret = bytes([self.status.value])
        ret += bytes([self.session_id >> 8 & 255, self.session_id & 255])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.status = ActivateSceneConfirmationStatus(payload[0])
        self.session_id = payload[1] * 256 + payload[2]

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} session_id="{}" status="{}"/>'.format(
            type(self).__name__, self.session_id, self.status
        )
