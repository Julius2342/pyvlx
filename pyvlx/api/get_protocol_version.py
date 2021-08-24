"""Module for retrieving protocol version from API."""

from pyvlx.dataobjects import DtoProtocolVersion

from .api_event import ApiEvent
from .frames import (
    FrameGetProtocolVersionConfirmation, FrameGetProtocolVersionRequest)


class GetProtocolVersion(ApiEvent):
    """Class for retrieving protocol version from API."""

    def __init__(self, pyvlx):
        """Initialize GetProtocolVersion class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.protocolversion = DtoProtocolVersion()

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetProtocolVersionConfirmation):
            return False
        self.protocolversion = DtoProtocolVersion(frame.major_version, frame.minor_version)
        self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetProtocolVersionRequest()

    @property
    def version(self):
        """Return Protocol Version as human readable string."""
        return "{}.{}".format(self.protocolversion.majorversion, self.protocolversion.minorversion)
