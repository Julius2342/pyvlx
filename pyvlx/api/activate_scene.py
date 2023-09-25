"""Module for retrieving scene list from API."""
from typing import TYPE_CHECKING, Optional

from .api_event import ApiEvent
from .frames import (
    ActivateSceneConfirmationStatus, FrameActivateSceneConfirmation,
    FrameActivateSceneRequest, FrameBase,
    FrameCommandRemainingTimeNotification, FrameCommandRunStatusNotification,
    FrameSessionFinishedNotification)
from .session_id import get_new_session_id

if TYPE_CHECKING:
    from pyvlx import PyVLX


class ActivateScene(ApiEvent):
    """Class for activating scene via API."""

    def __init__(
            self, pyvlx: "PyVLX", scene_id: int, wait_for_completion: bool = True, timeout_in_seconds: int = 60
    ):
        """Initialize SceneList class."""
        super().__init__(pyvlx=pyvlx, timeout_in_seconds=timeout_in_seconds)
        self.success = False
        self.scene_id = scene_id
        self.wait_for_completion = wait_for_completion
        self.session_id: Optional[int] = None

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if (
                isinstance(frame, FrameActivateSceneConfirmation)
                and frame.session_id == self.session_id
        ):
            if frame.status == ActivateSceneConfirmationStatus.ACCEPTED:
                self.success = True
            return not self.wait_for_completion
        if (
                isinstance(frame, FrameCommandRemainingTimeNotification)
                and frame.session_id == self.session_id
        ):
            # Ignoring FrameCommandRemainingTimeNotification
            return False
        if (
                isinstance(frame, FrameCommandRunStatusNotification)
                and frame.session_id == self.session_id
        ):
            # At the moment I don't reall understand what the FrameCommandRunStatusNotification is good for.
            # Ignoring these packets for now
            return False
        if (
                isinstance(frame, FrameSessionFinishedNotification)
                and frame.session_id == self.session_id
        ):
            return True
        return False

    def request_frame(self) -> FrameActivateSceneRequest:
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameActivateSceneRequest(
            scene_id=self.scene_id, session_id=self.session_id
        )
