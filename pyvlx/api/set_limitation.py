"""Module for retrieving limitation value from API."""

from ..parameter import IgnorePosition, LimitationTimeUnlimited, Position
from .api_event import ApiEvent
from .frames import (
    FrameSetLimitationConfirmation, FrameSetLimitationRequest,
    SetLimitationRequestStatus)
from .session_id import get_new_session_id


class SetLimitation(ApiEvent):
    """Class for setting limitation."""

    # NOTE: Required to always set both limits at the same time.
    # If setting only one limit to a value, the other to Ignore, Default or Current, the gateway will reject the Frame.
    def __init__(self, pyvlx, node_id, limitation_value_min=IgnorePosition(),
                 limitation_value_max=IgnorePosition(), limitation_time=LimitationTimeUnlimited()):
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
            else:
                self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameSetLimitationRequest(
            node_ids=[self.node_id], session_id=self.session_id,
            limitation_value_min=self.limitation_value_min, limitation_value_max=self.limitation_value_max,
            limitation_time=self.limitation_time)
