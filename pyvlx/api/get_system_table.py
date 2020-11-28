"""Module for retrieving scene list from API."""
from .api_event import ApiEvent
from .frames import (FrameGetSystemTableDataRequest,
                     FrameGetSystemTableDataConfirmation, FrameGetSystemTableDataNotification)


class GetSystemTable(ApiEvent):
    """Class for retrieving system Table from API."""

    def __init__(self, pyvlx):
        """Initialize GetSystemTable class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.systemtableentries = []

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetSystemTableDataConfirmation):
            # We are still waiting for FrameGetSystemTableDataNotification(s)
            # If there is no system table at all, this one will have to timeout
            return False

        if isinstance(frame, FrameGetSystemTableDataNotification):
            self.systemtableentries.append(frame.systemtableobjects)
            if frame.remainingnumberofentry != 0:
                # We are still waiting for FrameGetSystemTableDataNotification(s)
                return False
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetSystemTableDataRequest()
