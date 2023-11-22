"""Module for handling the FactoryDefault to API."""
from typing import TYPE_CHECKING

from pyvlx.log import PYVLXLOG

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGatewayFactoryDefaultConfirmation,
    FrameGatewayFactoryDefaultRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class FactoryDefault(ApiEvent):
    """Class for handling Factory reset API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize facotry default class."""
        super().__init__(pyvlx=pyvlx)
        self.pyvlx = pyvlx
        self.success = False

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGatewayFactoryDefaultConfirmation):
            PYVLXLOG.warning("KLF200 is factory resetting")
            self.success = True
            return True
        return False

    def request_frame(self) -> FrameGatewayFactoryDefaultRequest:
        """Construct initiating frame."""
        return FrameGatewayFactoryDefaultRequest()
