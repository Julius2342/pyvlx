"""Module for sending command to gw."""
import struct
from datetime import datetime

from pyvlx.const import Command

from .frame import FrameBase


class FrameSetUTCConfirmation(FrameBase):
    """Frame for confirmation for setting UTC time."""

    PAYLOAD_LEN = 0

    def __init__(self) -> None:
        """Init Frame."""
        super().__init__(Command.GW_SET_UTC_CFM)


class FrameSetUTCRequest(FrameBase):
    """Frame for command for setting UTC time."""

    PAYLOAD_LEN = 4

    def __init__(self, timestamp: float = 0):
        """Init Frame."""
        super().__init__(Command.GW_SET_UTC_REQ)
        self.timestamp = timestamp

    @property
    def timestamp_formatted(self) -> str:
        """Return time as human readable string."""
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def get_payload(self) -> bytes:
        """Return Payload."""
        return struct.pack(">I", self.timestamp)

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.timestamp = struct.unpack(">I", payload[0:4])[0]

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} time="{}"/>'.format(type(self).__name__, self.timestamp_formatted)
