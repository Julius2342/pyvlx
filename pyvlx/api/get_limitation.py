"""Module for retrieving limitation value from API."""

from ..const import LimitationType
from ..parameter import Position
from .api_event import ApiEvent
from .frames import (
    FrameGetLimitationStatus, FrameGetLimitationStatusConfirmation,
    FrameGetLimitationStatusNotification)
from .session_id import get_new_session_id


class GetLimitation(ApiEvent):
    """Class for retrieving gateway state from API."""

    def __init__(self, pyvlx, node_id, limitation_type=LimitationType.MIN_LIMITATION):
        """Initialize SceneList class."""
        super().__init__(pyvlx=pyvlx)
        self.node_id = node_id
        self.limitation_type = limitation_type
        self.success = False
        self.notification_frame = None
        self.session_id = None
        self.min_value_raw = None
        self.max_value_raw = None
        self.originator = None
        self.limit_time = None

    @property
    def max_value(self):
        return Position.to_percent(self.max_value_raw)

    @property
    def min_value(self):
        return Position.to_percent(self.min_value_raw)

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetLimitationStatusConfirmation):
            return False  # Wait for Notification Frame
        if isinstance(frame, FrameGetLimitationStatusNotification):
            if frame.session_id == self.session_id:
                self.success = True
                self.min_value_raw = frame.min_value
                self.max_value_raw = frame.max_value
                self.originator = frame.limit_originator
                self.limit_time = frame.limit_time
                self.notification_frame = frame
                return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameGetLimitationStatus(node_ids=[self.node_id], session_id=self.session_id,
                                        limitation_type=self.limitation_type)
