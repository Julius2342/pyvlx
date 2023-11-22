"""Module for retrieving limitation value from API."""

from typing import TYPE_CHECKING, Optional

from ..const import LimitationType, Originator
from ..parameter import Position
from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGetLimitationStatus, FrameGetLimitationStatusConfirmation,
    FrameGetLimitationStatusNotification)
from .session_id import get_new_session_id

if TYPE_CHECKING:
    from pyvlx import PyVLX


class GetLimitation(ApiEvent):
    """Class for retrieving gateway state from API."""

    def __init__(self, pyvlx: "PyVLX", node_id: int, limitation_type: LimitationType = LimitationType.MIN_LIMITATION):
        """Initialize SceneList class."""
        super().__init__(pyvlx=pyvlx)
        self.node_id = node_id
        self.limitation_type = limitation_type
        self.success = False
        self.notification_frame: Optional[FrameGetLimitationStatusNotification] = None
        self.session_id: Optional[int] = None
        self.min_value_raw: Optional[bytes] = None
        self.max_value_raw: Optional[bytes] = None
        self.originator: Optional[Originator] = None
        self.limit_time: Optional[int] = None

    @property
    def max_value(self) -> int:
        """Return max value."""
        assert self.max_value_raw is not None
        return Position.to_percent(self.max_value_raw)

    @property
    def min_value(self) -> int:
        """Return min value."""
        assert self.min_value_raw is not None
        return Position.to_percent(self.min_value_raw)

    async def handle_frame(self, frame: FrameBase) -> bool:
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

    def request_frame(self) -> FrameGetLimitationStatus:
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameGetLimitationStatus(node_ids=[self.node_id], session_id=self.session_id,
                                        limitation_type=self.limitation_type)
