"""Module for retrieving limitation value from API."""

from ..parameter import IgnorePosition, Position
from .api_event import ApiEvent
from .frames import (
    FrameGetLimitationStatusNotification, FrameSetLimitationConfirmation,
    FrameSetLimitationRequest, SetLimitationRequestStatus)
from .session_id import get_new_session_id


class SetLimitation(ApiEvent):
    """Class for setting limitation."""

    # NOTE: Required to always set both limits at the same time.
    # If setting only one limit to a value, the other to Ignore, Default or Current, the gateway will reject the Frame.
    def __init__(self, pyvlx, node_id, limitation_value_min=IgnorePosition(), limitation_value_max=IgnorePosition(), limitation_time=0x01):
        """Initialize SceneList class."""
        super().__init__(pyvlx=pyvlx)
        self.node_id = node_id
        self.limitation_value_min = limitation_value_min
        self.limitation_value_max = limitation_value_max
        self.success = False
        self.notification_frame = None
        self.session_id = None
        self.min_value_raw = None
        self.max_value_raw = None
        self.originator = None
        self.limitation_time = limitation_time

    @property
    def max_value(self):
        """Return max value."""
        return Position.to_percent(self.max_value_raw)

    @property
    def min_value(self):
        """Return min value."""
        return Position.to_percent(self.min_value_raw)

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameSetLimitationConfirmation):
            if frame.status == SetLimitationRequestStatus.REJECTED:
                self.success = False
                return True  # Stop if request is cancelled
            return False  # Wait for Notification Frame
        if isinstance(frame, FrameGetLimitationStatusNotification):
            if frame.session_id == self.session_id:
                self.success = True
                self.min_value_raw = frame.min_value
                self.max_value_raw = frame.max_value
                self.originator = frame.limit_originator
                self.limitation_time = frame.limit_time
                self.notification_frame = frame
                return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameSetLimitationRequest(
            node_ids=[self.node_id], session_id=self.session_id,
            limitation_value_min=self.limitation_value_min, limitation_value_max=self.limitation_value_max,
            limitation_time=self.limitation_time)
