"""Module for retrieving scene list from API."""
from .api_event import ApiEvent
from .frames import (
    FrameGetSceneListConfirmation, FrameGetSceneListNotification,
    FrameGetSceneListRequest)
from .log import PYVLXLOG


class GetSceneList(ApiEvent):
    """Class for retrieving scene list from API."""

    def __init__(self, pyvlx):
        """Initialize SceneList class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.count_scenes = None
        self.scenes = []

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetSceneListConfirmation):
            self.count_scenes = frame.count_scenes
            if self.count_scenes == 0:
                self.success = True
                return True
            # We are still waiting for FrameGetSceneListNotification(s)
            return False
        if isinstance(frame, FrameGetSceneListNotification):
            self.scenes.extend(frame.scenes)
            if frame.remaining_scenes != 0:
                # We are still waiting for FrameGetSceneListConfirmation(s)
                return False
            if self.count_scenes != len(self.scenes):
                PYVLXLOG.warning("Warning: number of received scenes does not match expected number")
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetSceneListRequest()
