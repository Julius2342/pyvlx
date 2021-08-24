"""Module for get local time classes."""
from pyvlx.const import Command
from pyvlx.dataobjects import DtoLocalTime

from .frame import FrameBase


class FrameGetLocalTimeRequest(FrameBase):
    """Frame for requesting local time."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_LOCAL_TIME_REQ)


class FrameGetLocalTimeConfirmation(FrameBase):
    """Frame for response for get local time requests."""

    PAYLOAD_LEN = 15

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_LOCAL_TIME_CFM)
        self.time = DtoLocalTime()

    def get_payload(self):
        """Return Payload."""
        return self.time.to_payload()

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.time.from_payload(payload)

    def __str__(self):
        """Return human readable string."""
        return '<{0}>{1}</{0}>'.format(type(self).__name__, self.time)
