
"""Module for set limitation classes."""
from enum import Enum
from typing import Optional

from pyvlx.const import Command, Originator, Priority
from pyvlx.parameter import LimitationTime, Position

from .frame import FrameBase


class FrameSetLimitationRequest(FrameBase):
    """Frame for setting limitation."""

    PAYLOAD_LEN = 31

    def __init__(self,
                 node_ids: Optional[list] = None,
                 session_id: Optional[int] = None,
                 limitation_value_min: Optional[Position] = None,
                 limitation_value_max: Optional[Position] = None,
                 limitation_time: Optional[LimitationTime] = None):
        """Init Frame."""
        super().__init__(Command.GW_SET_LIMITATION_REQ)
        self.session_id = session_id
        self.originator = Originator.USER
        self.priority = Priority.USER_LEVEL_2
        self.node_ids = node_ids

        self.parameter_id = 0  # Main Parameter
        self.limitation_value_min = limitation_value_min
        self.limitation_value_max = limitation_value_max
        self.limitation_time = limitation_time

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        assert self.limitation_value_min is not None
        assert self.limitation_value_max is not None
        assert self.limitation_time is not None
        assert self.node_ids is not None

        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.originator.value])
        ret += bytes([self.priority.value])
        ret += bytes([len(self.node_ids)])  # index array count
        ret += bytes(self.node_ids) + bytes(20 - len(self.node_ids))
        ret += bytes([self.parameter_id])
        ret += bytes(self.limitation_value_min)
        ret += bytes(self.limitation_value_max)
        ret += bytes(self.limitation_time)
        return ret

    def __str__(self) -> str:
        """Return human readable string."""
        return f'<{type(self).__name__} node_ids="{self.node_ids}" ' \
               f'session_id="{self.session_id}" originator="{self.originator}" ' \
               f'limitation_value_min="{self.limitation_value_min}" ' \
               f'limitation_value_max="{self.limitation_value_max}" ' \
               f'limitation_time="{self.limitation_time}" />'


class SetLimitationRequestStatus(Enum):
    """Enum for set limitation request status."""

    REJECTED = 0
    ACCEPTED = 1


class FrameSetLimitationConfirmation(FrameBase):
    """Frame for response for set limitation requests."""

    PAYLOAD_LEN = 3

    def __init__(self, session_id: Optional[int] = None, status: Optional[SetLimitationRequestStatus] = None):
        """Init Frame."""
        super().__init__(Command.GW_SET_LIMITATION_CFM)
        self.session_id = session_id
        self.status = status

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        assert self.status is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.status.value])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.status = SetLimitationRequestStatus(payload[2])

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} session_id="{}" status="{}"/>'.format(
            type(self).__name__, self.session_id, self.status
        )
