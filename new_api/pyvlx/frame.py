"""Module for Frames."""
import struct
from .frame_helper import calc_crc


class FrameBase:
    """Class for Base Frame."""

    def __init__(self, command):
        """Initialize Base Frame."""
        self.command = command

    def __bytes__(self):
        """Get raw bytes of Frame."""
        return self.build_frame(self.command, self.get_payload())

    def get_payload(self):
        """Return Payload."""
        raise NotImplementedError()

    def from_payload(self, payload):
        """Init frame from binary data."""
        raise NotImplementedError()

    def __str__(self):
        """Return human readable string."""
        raise NotImplementedError()

    @staticmethod
    def build_frame(command, payload):
        """Build raw bytes from command and payload."""
        packet_length = 2 + len(payload) + 1
        ret = struct.pack("BB", 0, packet_length)
        ret += struct.pack(">H", command.value)
        ret += payload
        ret += struct.pack("B", calc_crc(ret))
        return ret
