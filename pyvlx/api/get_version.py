"""Module for retrieving firmware version from API."""
from typing import TYPE_CHECKING

from pyvlx.dataobjects import DtoVersion

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGetVersionConfirmation, FrameGetVersionRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class GetVersion(ApiEvent):
    """Class for retrieving firmware version from API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize GetVersion class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.version = DtoVersion()

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetVersionConfirmation):
            return False
        self.version = DtoVersion(frame.software_version, frame.hardware_version,
                                  frame.product_group, frame.product_type)
        self.success = True
        return True

    def request_frame(self) -> FrameGetVersionRequest:
        """Construct initiating frame."""
        return FrameGetVersionRequest()
