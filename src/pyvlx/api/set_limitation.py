"""Module for setting limitation value."""
from typing import TYPE_CHECKING

from ..const import LimitationTime
from ..parameter import IgnorePosition, Position
from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGetLimitationStatusNotification,
    FrameSessionFinishedNotification, FrameSetLimitationConfirmation,
    FrameSetLimitationRequest, SetLimitationRequestStatus)
from .session_id import get_new_session_id

if TYPE_CHECKING:
    from pyvlx import PyVLX


class SetLimitation(ApiEvent):
    """Class for setting limitation."""

    # NOTE: Required to always set both limits at the same time.
    # If setting only one limit to a value, the other to Ignore, Default or Current, the gateway will reject the Frame.
    def __init__(self, pyvlx: "PyVLX", node_id: int, limitation_value_min: Position = IgnorePosition(),
                 limitation_value_max: Position = IgnorePosition(), limitation_time: LimitationTime = LimitationTime.UNLIMITED):
        """Initialize SetLimitation class."""
        super().__init__(pyvlx=pyvlx)
        self.node_id = node_id
        self.limitation_value_min = limitation_value_min
        self.limitation_value_max = limitation_value_max
        self.success = False
        self.session_id: int | None = None
        self.limitation_time = limitation_time

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if hasattr(frame, "session_id") and frame.session_id != self.session_id:
            # This frame has a session id, but it doesn't match the one of this API call, so ignore it.
            return False
        if isinstance(frame, FrameSetLimitationConfirmation) and frame.status == SetLimitationRequestStatus.REJECTED:
            # The request was rejected, so success is False. There is also no point in waiting
            # for a completion notification, since the command was not accepted, so we can consider
            # the API call complete at this point and return True to stop waiting for further frames.
            self.success = False
            return True
        if isinstance(frame, FrameGetLimitationStatusNotification):
            # received a notification frame with the new limitation values, so we can consider
            # the API call successful and complete at this point. (see Spec section 10.5.4)
            self.success = True
            return True
        if isinstance(frame, FrameSessionFinishedNotification):
            # The session finished without us having seen a notification frame with the new limitation values, so
            # we consider the API call complete at this point.
            # Success remains False, since we never received the notification frame with the new values.
            # We've most likely seen a FrameCommandRunStatusNotification in between the confirmation and
            # the session finished notification, which indicates that the command was not accepted by the device.
            return True
        return False

    def request_frame(self) -> FrameSetLimitationRequest:
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameSetLimitationRequest(
            node_ids=[self.node_id], session_id=self.session_id,
            limitation_value_min=self.limitation_value_min,
            limitation_value_max=self.limitation_value_max,
            limitation_time=self.limitation_time)
