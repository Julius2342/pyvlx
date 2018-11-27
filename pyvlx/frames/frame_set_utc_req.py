"""Module for sending command to gw."""
import struct
from datetime import datetime

from pyvlx.const import Command

from .frame import FrameBase


class FrameSetUTCRequest(FrameBase):
    """Frame for sending command to gw."""

    PAYLOAD_LEN = 4

    def __init__(self, timestamp=0):
        """Init Frame."""
        super().__init__(Command.GW_SET_UTC_REQ)
        self.timestamp = timestamp

    @property
    def timestamp_formatted(self):
        """Return time as human readable string."""
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def get_payload(self):
        """Return Payload."""
        return struct.pack(">I", self.timestamp)

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.timestamp = struct.unpack(">I", payload[0:4])[0]

    def __str__(self):
        """Return human readable string."""
        return '<FrameSetUTCRequest time="{}"/>'.format(self.timestamp_formatted)
