"""Module for handling the Reboot to API."""
from typing import TYPE_CHECKING

from pyvlx.log import PYVLXLOG

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGatewayRebootConfirmation, FrameGatewayRebootRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class Reboot(ApiEvent):
    """Class for handling Reboot to API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize Reboot class."""
        super().__init__(pyvlx=pyvlx)
        self.pyvlx = pyvlx
        self.success = False

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGatewayRebootConfirmation):
            PYVLXLOG.warning("KLF200 is rebooting")
            self.success = True
            return True
        return False

    def request_frame(self) -> FrameGatewayRebootRequest:
        """Construct initiating frame."""
        return FrameGatewayRebootRequest()
