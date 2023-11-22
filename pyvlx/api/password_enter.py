"""Module for handling the login to API."""
from typing import TYPE_CHECKING

from pyvlx.log import PYVLXLOG

from .api_event import ApiEvent
from .frames import (
    FrameBase, FramePasswordEnterConfirmation, FramePasswordEnterRequest,
    PasswordEnterConfirmationStatus)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class PasswordEnter(ApiEvent):
    """Class for handling login to API."""

    def __init__(self, pyvlx: "PyVLX", password: str):
        """Initialize login class."""
        super().__init__(pyvlx=pyvlx)
        self.password = password
        self.success = False

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FramePasswordEnterConfirmation):
            return False
        if frame.status == PasswordEnterConfirmationStatus.FAILED:
            PYVLXLOG.warning(
                'Failed to authenticate with password "%s****"', self.password[:2]
            )
            self.success = False
        if frame.status == PasswordEnterConfirmationStatus.SUCCESSFUL:
            self.success = True
        return True

    def request_frame(self) -> FramePasswordEnterRequest:
        """Construct initiating frame."""
        return FramePasswordEnterRequest(password=self.password)
