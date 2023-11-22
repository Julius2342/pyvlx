"""Module for setting UTC time within gateway."""
import time
from typing import TYPE_CHECKING

from .api_event import ApiEvent
from .frames import FrameBase, FrameSetUTCConfirmation, FrameSetUTCRequest

if TYPE_CHECKING:
    from pyvlx import PyVLX


class SetUTC(ApiEvent):
    """Class for setting UTC time within gateway."""

    def __init__(self, pyvlx: "PyVLX", timestamp: float = time.time()):
        """Initialize SetUTC class."""
        super().__init__(pyvlx=pyvlx)
        self.timestamp = timestamp
        self.success = False

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameSetUTCConfirmation):
            return False
        self.success = True
        return True

    def request_frame(self) -> FrameSetUTCRequest:
        """Construct initiating frame."""
        timestamp = int(self.timestamp)
        return FrameSetUTCRequest(timestamp=timestamp)
