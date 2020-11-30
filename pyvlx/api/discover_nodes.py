"""Module for discovering of Nodes from API."""
from .api_event import ApiEvent
from .frames import (
    FrameDiscoverNodesRequest, FrameDiscoverNodesConfirmation)


class DiscoverNodes(ApiEvent):
    """Class for starting Node Discovery from API."""

    def __init__(self, pyvlx):
        """Initialize DiscoverNodes class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameDiscoverNodesConfirmation):
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameDiscoverNodesRequest()
