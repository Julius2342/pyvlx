"""Module for retrieving scene list from API."""
from pyvlx.frame_get_scene_list import FrameGetSceneListRequest, FrameGetSceneListConfirmation, FrameGetSceneListNotification
from pyvlx.api_event import ApiEvent


class SceneList(ApiEvent):
    """Class for retrieving scene list from API."""

    def __init__(self, connection):
        """Initialize SceneList class."""
        super().__init__(connection)
        self.success = False
        self.count_scenes = None
        self.scenes = []

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetSceneListConfirmation):
            self.count_scenes = frame.count_scenes
            # We are still waiting for FrameGetSceneListNotification(s)
            return False
        if isinstance(frame, FrameGetSceneListNotification):
            self.scenes.extend(frame.scenes)
            if frame.remaining_scenes != 0:
                # We are still waiting for FrameGetSceneListConfirmation(s)
                return False
            if self.count_scenes != len(self.scenes):
                print("Warning: number of received scenes does not match expected number")
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetSceneListRequest()
