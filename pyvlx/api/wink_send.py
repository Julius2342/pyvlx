"""Module for sending wink request to API."""
from typing import TYPE_CHECKING, Optional

from ..const import WinkTime
from ..exception import PyVLXException
from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameWinkSendConfirmation, FrameWinkSendNotification,
    FrameWinkSendRequest, WinkSendConfirmationStatus)
from .session_id import get_new_session_id

if TYPE_CHECKING:
    from pyvlx import PyVLX


class WinkSend(ApiEvent):
    """Class for sending wink request to API."""

    def __init__(
            self,
            pyvlx: "PyVLX",
            node_id: int,
            wink_time: WinkTime = WinkTime.BY_MANUFACTURER,
            wait_for_completion: bool = True,
            timeout_in_seconds: Optional[int] = None,
    ):
        """Initialize WinkSend class."""
        if timeout_in_seconds is None:
            timeout_in_seconds = 5
        super().__init__(pyvlx=pyvlx, timeout_in_seconds=timeout_in_seconds)
        self.success = False
        self.node_id = node_id
        self.wink_time = wink_time
        self.wait_for_completion = wait_for_completion
        self.session_id: Optional[int] = None

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if (
                isinstance(frame, FrameWinkSendConfirmation)
                and frame.session_id == self.session_id
        ):
            if frame.status == WinkSendConfirmationStatus.ACCEPTED:
                self.success = True
                return not self.wait_for_completion
            if frame.status == WinkSendConfirmationStatus.REJECTED:
                self.success = False
                return True
        if (
                isinstance(frame, FrameWinkSendNotification)
                and frame.session_id == self.session_id
        ):
            return True
        return False

    async def wink(self) -> None:
        """Send frame to KLF200."""
        await self.do_api_call()
        if not self.success:
            raise PyVLXException("Unable to send wink command")

    def request_frame(self) -> FrameWinkSendRequest:
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameWinkSendRequest(
            node_ids=[self.node_id],
            wink_time=self.wink_time,
            session_id=self.session_id,
        )
