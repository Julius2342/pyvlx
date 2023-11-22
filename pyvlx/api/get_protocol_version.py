"""Module for retrieving protocol version from API."""

from typing import TYPE_CHECKING

from pyvlx.dataobjects import DtoProtocolVersion

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGetProtocolVersionConfirmation,
    FrameGetProtocolVersionRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class GetProtocolVersion(ApiEvent):
    """Class for retrieving protocol version from API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize GetProtocolVersion class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.protocolversion = DtoProtocolVersion()

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetProtocolVersionConfirmation):
            return False
        self.protocolversion = DtoProtocolVersion(frame.major_version, frame.minor_version)
        self.success = True
        return True

    def request_frame(self) -> FrameGetProtocolVersionRequest:
        """Construct initiating frame."""
        return FrameGetProtocolVersionRequest()

    @property
    def version(self) -> str:
        """Return Protocol Version as human readable string."""
        return "{}.{}".format(self.protocolversion.majorversion, self.protocolversion.minorversion)
