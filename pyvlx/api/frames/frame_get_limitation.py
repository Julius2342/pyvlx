
"""Module for get local time classes."""
from typing import List, Optional

from pyvlx.const import Command, LimitationType, Originator, Priority

from .frame import FrameBase


class FrameGetLimitationStatus(FrameBase):
    """Frame for requesting limitation status."""

    PAYLOAD_LEN = 25

    def __init__(self,
                 node_ids: Optional[List[int]] = None,
                 session_id: Optional[int] = None,
                 limitation_type: LimitationType = LimitationType.MIN_LIMITATION):
        """Init Frame."""
        super().__init__(Command.GW_GET_LIMITATION_STATUS_REQ)
        self.session_id = session_id
        self.originator = Originator.USER
        self.priority = Priority.USER_LEVEL_2
        self.node_ids = node_ids if node_ids is not None else []

        self.parameter_id = 0  # Main Parameter
        self.limitations_type = limitation_type

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([len(self.node_ids)])  # index array count
        ret += bytes(self.node_ids) + bytes(20 - len(self.node_ids))
        ret += bytes([self.parameter_id])
        ret += bytes([self.limitations_type.value])
        return ret

    def __str__(self) -> str:
        """Return human readable string."""
        return f'<{type(self).__name__} node_ids="{self.node_ids}" ' \
               f'session_id="{self.session_id}" originator="{self.originator}" />'


class FrameGetLimitationStatusConfirmation(FrameBase):
    """Frame for response for get limitation requests."""

    PAYLOAD_LEN = 3

    def __init__(self, session_id: Optional[int] = None, data: Optional[int] = None):
        """Init Frame."""
        super().__init__(Command.GW_GET_LIMITATION_STATUS_CFM)
        self.session_id = session_id
        self.data = data

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        assert self.data is not None
        ret += bytes([self.data])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.data = payload[2]

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} session_id="{}" status="{}"/>'.format(
            type(self).__name__, self.session_id, self.data
        )


class FrameGetLimitationStatusNotification(FrameBase):
    """Frame for notification of note information request."""

    PAYLOAD_LEN = 10

    def __init__(self) -> None:
        """Init Frame."""
        super().__init__(Command.GW_LIMITATION_STATUS_NTF)
        self.session_id: Optional[int] = None
        self.node_id = 0
        self.parameter_id = 0
        self.min_value: Optional[bytes] = None
        self.max_value: Optional[bytes] = None
        self.limit_originator: Optional[Originator] = None
        self.limit_time: Optional[int] = None

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        assert self.min_value is not None
        assert self.max_value is not None
        assert self.limit_originator is not None
        assert self.limit_time is not None
        payload = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        payload += bytes([self.node_id])
        payload += bytes([self.parameter_id])
        payload += self.min_value
        payload += self.max_value
        payload += bytes([self.limit_originator.value])
        payload += bytes([self.limit_time])
        return payload

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.node_id = payload[2]
        self.parameter_id = payload[3]
        self.min_value = payload[4:5]
        self.max_value = payload[6:7]
        self.limit_originator = Originator(payload[8])
        self.limit_time = payload[9]

    def __str__(self) -> str:
        """Return human readable string."""
        return (
            '<{} node_id="{}" session_id="{}" min_value="{!r}" '
            'max_value="{!r}" originator="{}" limit_time="{}"/>'.format(
                type(self).__name__, self.node_id, self.session_id,
                self.min_value, self.max_value, self.limit_originator,
                self.limit_time
            )
        )
