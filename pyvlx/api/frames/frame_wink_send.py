"""Module for sending wink request."""
from enum import Enum
from typing import List, Optional

from pyvlx.const import Command, Originator, Priority, WinkTime
from pyvlx.exception import PyVLXException

from .frame import FrameBase


class FrameWinkSendRequest(FrameBase):
    """Frame for sending wink request."""

    PAYLOAD_LEN = 27

    def __init__(
            self,
            node_ids: Optional[List[int]] = None,
            wink_time: WinkTime = WinkTime.BY_MANUFACTURER,
            session_id: Optional[int] = None,
            originator: Originator = Originator.USER,
            priority: Priority = Priority.USER_LEVEL_2,
    ):
        """Init Frame."""
        super().__init__(Command.GW_WINK_SEND_REQ)
        self.node_ids = node_ids if node_ids is not None else []
        self.wink_time = wink_time
        self.session_id = session_id
        self.originator = originator
        self.priority = priority

    def get_payload(self) -> bytes:
        """Return Payload."""
        if len(self.node_ids) > 20:
            raise PyVLXException("wink_send_request_wrong_node_length")
        assert self.session_id is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.originator.value])
        ret += bytes([self.priority.value])
        ret += bytes([1])  # WinkState: 1 = Enable wink
        ret += bytes([self.wink_time.value])

        # Nodes array: Number of nodes + node array + padding
        ret += bytes([len(self.node_ids)])  # index array count
        ret += bytes(self.node_ids) + bytes(20 - len(self.node_ids))
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.originator = Originator(payload[2])
        self.priority = Priority(payload[3])
        # payload[4] is WinkState (always enable for this frame currently)
        self.wink_time = WinkTime(payload[5])

        len_node_ids = payload[6]
        if len_node_ids > 20:
            raise PyVLXException("wink_send_request_wrong_node_length")
        self.node_ids = []
        for i in range(len_node_ids):
            self.node_ids.append(payload[7 + i])

    def __str__(self) -> str:
        """Return human readable string."""
        return (
            '<{} node_ids="{}" wink_time="{}" '
            'session_id="{}" originator="{}"/>'.format(
                type(self).__name__, self.node_ids, self.wink_time,
                self.session_id, self.originator,
            )
        )


class WinkSendConfirmationStatus(Enum):
    """Enum class for status of wink send confirmation."""

    REJECTED = 0
    ACCEPTED = 1


class FrameWinkSendConfirmation(FrameBase):
    """Frame for confirmation of wink send frame."""

    PAYLOAD_LEN = 3

    def __init__(self, session_id: Optional[int] = None, status: Optional[WinkSendConfirmationStatus] = None):
        """Init Frame."""
        super().__init__(Command.GW_WINK_SEND_CFM)
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
        self.status = WinkSendConfirmationStatus(payload[2])

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} session_id="{}" status="{}"/>'.format(
            type(self).__name__, self.session_id, self.status
        )


class FrameWinkSendNotification(FrameBase):
    """Frame for notification of wink send frame."""

    PAYLOAD_LEN = 2

    def __init__(self, session_id: Optional[int] = None):
        """Init Frame."""
        super().__init__(Command.GW_WINK_SEND_NTF)
        self.session_id = session_id

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} session_id="{}"/>'.format(
            type(self).__name__, self.session_id
        )
