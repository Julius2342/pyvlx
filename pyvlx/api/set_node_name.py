"""Module for changing a node name."""
from typing import TYPE_CHECKING

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameSetNodeNameConfirmation, FrameSetNodeNameRequest,
    SetNodeNameConfirmationStatus)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class SetNodeName(ApiEvent):
    """Class for changing the name of a node via API."""

    def __init__(self, pyvlx: "PyVLX", node_id: int, name: str):
        """Initialize class."""
        super().__init__(pyvlx=pyvlx)
        self.node_id = node_id
        self.name = name
        self.success = False

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameSetNodeNameConfirmation):
            return False
        self.success = frame.status == SetNodeNameConfirmationStatus.OK
        return True

    def request_frame(self) -> FrameSetNodeNameRequest:
        """Construct initiating frame."""
        return FrameSetNodeNameRequest(node_id=self.node_id, name=self.name)
