"""Module for retrieving node information from API."""
from typing import TYPE_CHECKING, List

from pyvlx.log import PYVLXLOG

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGetAllNodesInformationConfirmation,
    FrameGetAllNodesInformationFinishedNotification,
    FrameGetAllNodesInformationNotification,
    FrameGetAllNodesInformationRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class GetAllNodesInformation(ApiEvent):
    """Class for retrieving node information from API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize SceneList class."""
        super().__init__(pyvlx=pyvlx)
        self.number_of_nodes = 0
        self.success = False
        self.notification_frames: List[FrameGetAllNodesInformationNotification] = []

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetAllNodesInformationConfirmation):
            self.number_of_nodes = frame.number_of_nodes
            # We are still waiting for FrameGetAllNodesInformationNotification
            return False
        if isinstance(frame, FrameGetAllNodesInformationNotification):
            self.notification_frames.append(frame)
        if isinstance(frame, FrameGetAllNodesInformationFinishedNotification):
            if self.number_of_nodes != len(self.notification_frames):
                PYVLXLOG.warning(
                    "Number of received scenes does not match expected number"
                )
            self.success = True
            return True
        return False

    def request_frame(self) -> FrameGetAllNodesInformationRequest:
        """Construct initiating frame."""
        return FrameGetAllNodesInformationRequest()
