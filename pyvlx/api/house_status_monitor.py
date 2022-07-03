"""Module for house status monitor."""
from pyvlx.exception import PyVLXException

from .api_event import ApiEvent
from .frames import (
    FrameHouseStatusMonitorDisableConfirmation,
    FrameHouseStatusMonitorDisableRequest,
    FrameHouseStatusMonitorEnableConfirmation,
    FrameHouseStatusMonitorEnableRequest)


class HouseStatusMonitorEnable(ApiEvent):
    """Class for enabling house status monotor."""

    def __init__(self, pyvlx):
        """Initialize HouseStatusMonitorEnable class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameHouseStatusMonitorEnableConfirmation):
            return False
        self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameHouseStatusMonitorEnableRequest()


class HouseStatusMonitorDisable(ApiEvent):
    """Class for disabling house status monotor."""

    def __init__(self, pyvlx):
        """Initialize HouseStatusMonitorEnable class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameHouseStatusMonitorDisableConfirmation):
            return False
        self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameHouseStatusMonitorDisableRequest()
