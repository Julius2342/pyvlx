"""Module for local time firmware version from API."""
from typing import TYPE_CHECKING

from pyvlx.dataobjects import DtoLocalTime

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGetLocalTimeConfirmation, FrameGetLocalTimeRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class GetLocalTime(ApiEvent):
    """Class for retrieving firmware version from API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize GetLocalTime class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.localtime = DtoLocalTime()

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetLocalTimeConfirmation):
            return False
        self.localtime = frame.time
        self.success = True

        return True

    def request_frame(self) -> FrameGetLocalTimeRequest:
        """Construct initiating frame."""
        return FrameGetLocalTimeRequest()
