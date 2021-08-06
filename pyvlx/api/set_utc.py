"""Module for setting UTC time within gateway."""
import time

from .api_event import ApiEvent
from .frames import FrameSetUTCConfirmation, FrameSetUTCRequest


class SetUTC(ApiEvent):
    """Class for setting UTC time within gateway."""

    def __init__(self, pyvlx, timestamp=time.time()):
        """Initialize SetUTC class."""
        super().__init__(pyvlx=pyvlx)
        self.timestamp = timestamp
        self.success = False

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameSetUTCConfirmation):
            return False
        self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        timestamp = int(self.timestamp)
        return FrameSetUTCRequest(timestamp=timestamp)
