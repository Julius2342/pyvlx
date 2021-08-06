"""Module for handling the FactoryDefault to API."""
from pyvlx.log import PYVLXLOG

from .api_event import ApiEvent
from .frames import (
    FrameGatewayFactoryDefaultConfirmation, FrameGatewayFactoryDefaultRequest)


class FactoryDefault(ApiEvent):
    """Class for handling Factory reset API."""

    def __init__(self, pyvlx):
        """Initialize facotry default class."""
        super().__init__(pyvlx=pyvlx)
        self.pyvlx = pyvlx
        self.success = False

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGatewayFactoryDefaultConfirmation):
            PYVLXLOG.warning("KLF200 is factory resetting")
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGatewayFactoryDefaultRequest()
