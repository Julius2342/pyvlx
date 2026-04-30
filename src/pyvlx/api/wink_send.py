"""Module for sending wink request to API."""
from typing import TYPE_CHECKING

from ..const import WinkTime
from .completable_api_event import CompletableApiEvent
from .frames import (
    FrameBase, FrameWinkSendConfirmation, FrameWinkSendNotification,
    FrameWinkSendRequest, WinkSendConfirmationStatus)
from .session_id import get_new_session_id

if TYPE_CHECKING:
    from pyvlx import PyVLX


class WinkSend(CompletableApiEvent):
    """Class for sending wink request to API."""

    def __init__(
            self,
            pyvlx: "PyVLX",
            node_id: int,
            wink_time: WinkTime = WinkTime.BY_MANUFACTURER,
            wait_for_completion: bool = True,
            timeout_in_seconds: int = 5,
    ):
        """Initialize WinkSend class."""
        super().__init__(pyvlx=pyvlx, timeout_in_seconds=timeout_in_seconds, wait_for_completion=wait_for_completion)
        self.node_id = node_id
        self.wink_time = wink_time

    def check_confirmation(self, frame: FrameBase) -> bool | None:
        """Check if frame is a WinkSendConfirmation for this session."""
        if isinstance(frame, FrameWinkSendConfirmation) and frame.session_id == self.session_id:
            return frame.status == WinkSendConfirmationStatus.ACCEPTED
        return None

    def check_completion(self, frame: FrameBase) -> bool:
        """Return True if this frame signals wink completion."""
        return (
            isinstance(frame, FrameWinkSendNotification)
            and frame.session_id == self.session_id
        )

    def request_frame(self) -> FrameWinkSendRequest:
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameWinkSendRequest(
            node_ids=[self.node_id],
            wink_time=self.wink_time,
            session_id=self.session_id,
        )
