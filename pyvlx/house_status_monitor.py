"""Module for house status monitor."""
from .api_event import ApiEvent
from .exception import PyVLXException
from .frames import (
    FrameHouseStatusMonitorDisableConfirmation,
    FrameHouseStatusMonitorDisableRequest,
    FrameHouseStatusMonitorEnableConfirmation,
    FrameHouseStatusMonitorEnableRequest)


class HouseStatusMonitorEnable(ApiEvent):
    """Class for enabling house status monotor."""

    def __init__(self, pyvlx):
        """Initialize login class."""
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
        """Initialize login class."""
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


async def house_status_monitor_enable(pyvlx):
    """Enable house status monitor."""
    status_monitor_enable = HouseStatusMonitorEnable(pyvlx=pyvlx)
    await status_monitor_enable.do_api_call()
    if not status_monitor_enable.success:
        raise PyVLXException("Unable enable house status monitor.")


async def house_status_monitor_disable(pyvlx):
    """Disable house status monitor."""
    status_monitor_disable = HouseStatusMonitorDisable(pyvlx=pyvlx)
    await status_monitor_disable.do_api_call()
    if not status_monitor_disable.success:
        raise PyVLXException("Unable disable house status monitor.")
