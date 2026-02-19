"""Module for setting limitation value."""
from typing import TYPE_CHECKING, Optional

from pyvlx.const import Originator

from ..parameter import (
    IgnorePosition, LimitationTime, LimitationTimeUnlimited, Position)
from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameSetLimitationConfirmation, FrameSetLimitationRequest,
    SetLimitationRequestStatus)
from .session_id import get_new_session_id

if TYPE_CHECKING:
    from pyvlx import PyVLX


class SetLimitation(ApiEvent):
    """Class for setting limitation."""

    # NOTE: Required to always set both limits at the same time.
    # If setting only one limit to a value, the other to Ignore, Default or Current, the gateway will reject the Frame.
    def __init__(self, pyvlx: "PyVLX", node_id: int, limitation_value_min: Position = IgnorePosition(),
                 limitation_value_max: Position = IgnorePosition(), limitation_time: LimitationTime = LimitationTimeUnlimited()):
        """Initialize SetLimitation class."""
        super().__init__(pyvlx=pyvlx)
        self.node_id = node_id
        self.limitation_value_min = limitation_value_min
        self.limitation_value_max = limitation_value_max
        self.success = False
        self.notification_frame: Optional[FrameSetLimitationConfirmation] = None
        self.session_id: Optional[int] = None
        self.originator: Optional[Originator] = None
        self.limitation_time = limitation_time

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameSetLimitationConfirmation):
            if frame.status == SetLimitationRequestStatus.REJECTED:
                self.success = False
            else:
                self.success = True
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
