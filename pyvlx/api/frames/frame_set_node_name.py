"""Module for requesting change of node name."""
from enum import Enum
from typing import Optional

from pyvlx.const import Command
from pyvlx.string_helper import bytes_to_string, string_to_bytes

from .frame import FrameBase


class FrameSetNodeNameRequest(FrameBase):
    """Frame for requesting node name change."""

    PAYLOAD_LEN = 65

    def __init__(self, node_id: int = 0, name: Optional[str] = None):
        """Init Frame."""
        super().__init__(Command.GW_SET_NODE_NAME_REQ)
        self.node_id = node_id
        self.name = name

    def get_payload(self) -> bytes:
        """Return Payload."""
        ret = bytes([self.node_id])
        assert self.name is not None
        ret += string_to_bytes(self.name, 64)
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.node_id = payload[0]
        self.name = bytes_to_string(payload[1:65])

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} node_id="{}" name="{}"/>'.format(
            type(self).__name__, self.node_id, self.name
        )


class SetNodeNameConfirmationStatus(Enum):
    """Enum class for status of password enter confirmation."""

    OK = 0
    ERROR_REQUEST_REJECTED = 1
    ERROR_INVALID_SYSTEM_TABLE_INDEX = 2


class FrameSetNodeNameConfirmation(FrameBase):
    """Frame for confirmation for set node name."""

    PAYLOAD_LEN = 2

    def __init__(self, status: SetNodeNameConfirmationStatus = SetNodeNameConfirmationStatus.OK, node_id: int = 0):
        """Init Frame."""
        super().__init__(Command.GW_SET_NODE_NAME_CFM)
        self.status = status
        self.node_id = node_id

    def get_payload(self) -> bytes:
        """Return Payload."""
        return bytes([self.status.value, self.node_id])

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.status = SetNodeNameConfirmationStatus(payload[0])
        self.node_id = payload[1]

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} node_id="{}" status="{}"/>'.format(
            type(self).__name__, self.node_id, self.status
        )
