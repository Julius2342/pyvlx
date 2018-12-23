"""Module for setting UTC time within gateway."""
import time

from .api_event import ApiEvent
from .exception import PyVLXException
from .frames import FrameSetUTCConfirmation, FrameSetUTCRequest


class SetUTC(ApiEvent):
    """Class for setting UTC time within gateway."""

    def __init__(self, pyvlx):
        """Initialize login class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameSetUTCConfirmation):
            return False
        self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        timestamp = int(time.time())
        return FrameSetUTCRequest(timestamp=timestamp)


async def set_utc(pyvlx):
    """Enable house status monitor."""
    setutc = SetUTC(pyvlx=pyvlx)
    await setutc.do_api_call()
    if not setutc.success:
        raise PyVLXException("Unable to set utc.")
