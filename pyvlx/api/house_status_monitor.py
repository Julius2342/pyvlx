"""Module for house status monitor."""
from typing import TYPE_CHECKING

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameHouseStatusMonitorDisableConfirmation,
    FrameHouseStatusMonitorDisableRequest,
    FrameHouseStatusMonitorEnableConfirmation,
    FrameHouseStatusMonitorEnableRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class HouseStatusMonitorEnable(ApiEvent):
    """Class for enabling house status monotor."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize HouseStatusMonitorEnable class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameHouseStatusMonitorEnableConfirmation):
            return False
        self.success = True
        return True

    def request_frame(self) -> FrameHouseStatusMonitorEnableRequest:
        """Construct initiating frame."""
        return FrameHouseStatusMonitorEnableRequest()


class HouseStatusMonitorDisable(ApiEvent):
    """Class for disabling house status monotor."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize HouseStatusMonitorEnable class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameHouseStatusMonitorDisableConfirmation):
            return False
        self.success = True
        return True

    def request_frame(self) -> FrameHouseStatusMonitorDisableRequest:
        """Construct initiating frame."""
        return FrameHouseStatusMonitorDisableRequest()
