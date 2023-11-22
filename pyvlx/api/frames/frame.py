"""Module for Frames."""
import struct

from pyvlx.const import Command
from pyvlx.exception import PyVLXException

from .frame_helper import calc_crc


class FrameBase:
    """Class for Base Frame."""

    def __init__(self, command: Command):
        """Initialize Base Frame."""
        self.command = command

    def __bytes__(self) -> bytes:
        """Get raw bytes of Frame."""
        payload = self.get_payload()
        self.validate_payload_len(payload)
        return self.build_frame(self.command, payload)

    def validate_payload_len(self, payload: bytes) -> None:
        """Validate payload len."""
        if not hasattr(self, "PAYLOAD_LEN"):
            # No fixed payload len, e.g. within FrameGetSceneListNotification
            return
        # pylint: disable=no-member
        if len(payload) != self.PAYLOAD_LEN:
            raise PyVLXException(
                "Invalid payload len",
                expected_len=self.PAYLOAD_LEN,
                current_len=len(payload),
                frame_type=type(self).__name__,
            )

    def get_payload(self) -> bytes:
        """Return Payload."""
        return b""

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""

    def __str__(self) -> str:
        """Return human readable string."""
        return "<{}/>".format(type(self).__name__)

    @staticmethod
    def build_frame(command: Command, payload: bytes) -> bytes:
        """Build raw bytes from command and payload."""
        packet_length = 2 + len(payload) + 1
        ret = struct.pack("BB", 0, packet_length)
        ret += struct.pack(">H", command.value)
        ret += payload
        ret += struct.pack("B", calc_crc(ret))
        return ret
