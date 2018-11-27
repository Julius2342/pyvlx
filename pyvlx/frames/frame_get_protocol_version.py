"""Module for get version frame classes."""
from pyvlx.const import Command

from .frame import FrameBase


class FrameGetProtocolVersionRequest(FrameBase):
    """Frame for requesting protocol version."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_PROTOCOL_VERSION_REQ)


class FrameGetProtocolVersionConfirmation(FrameBase):
    """Frame for response for get protocol version requests."""

    PAYLOAD_LEN = 4

    def __init__(self, major_version=0, minor_version=0):
        """Init Frame."""
        super().__init__(Command.GW_GET_PROTOCOL_VERSION_CFM)
        self.major_version = major_version
        self.minor_version = minor_version

    @property
    def version(self):
        """Return formatted protocol version."""
        return "{}.{}".format(self.major_version, self.minor_version)

    def get_payload(self):
        """Return Payload."""
        return bytes(
            [self.major_version >> 8 & 255, self.major_version & 255,
             self.minor_version >> 8 & 255, self.minor_version & 255])

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.major_version = payload[0] * 256 + payload[1]
        self.minor_version = payload[2] * 256 + payload[3]

    def __str__(self):
        """Return human readable string."""
        return '<FrameGetProtocolVersionConfirmation version="{}"/>'.format(self.version)
