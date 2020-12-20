"""Module for local time firmware version from API."""
from pyvlx.dataobjects import DtoLocalTime

from .api_event import ApiEvent
from .frames import FrameGetLocalTimeConfirmation, FrameGetLocalTimeRequest


class GetLocalTime(ApiEvent):
    """Class for retrieving firmware version from API."""

    def __init__(self, pyvlx):
        """Initialize GetLocalTime class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.localtime = DtoLocalTime()

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetLocalTimeConfirmation):
            return False
        self.localtime = frame.localtime
        self.success = True

        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetLocalTimeRequest()
