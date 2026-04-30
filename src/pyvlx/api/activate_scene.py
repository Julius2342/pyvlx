"""Module for activating scenes via API."""
from typing import TYPE_CHECKING

from .completable_api_event import CompletableApiEvent
from .frames import (
    ActivateSceneConfirmationStatus, FrameActivateSceneConfirmation,
    FrameActivateSceneRequest, FrameBase)
from .session_id import get_new_session_id

if TYPE_CHECKING:
    from pyvlx import PyVLX


class ActivateScene(CompletableApiEvent):
    """Class for activating scene via API."""

    def __init__(
            self, pyvlx: "PyVLX", scene_id: int, wait_for_completion: bool = True, timeout_in_seconds: int = 60
    ):
        """Initialize ActivateScene class."""
        super().__init__(pyvlx=pyvlx, timeout_in_seconds=timeout_in_seconds, wait_for_completion=wait_for_completion)
        self.scene_id = scene_id

    def check_confirmation(self, frame: FrameBase) -> bool | None:
        """Check if frame is an ActivateSceneConfirmation for this session."""
        if isinstance(frame, FrameActivateSceneConfirmation) and frame.session_id == self.session_id:
            return frame.status == ActivateSceneConfirmationStatus.ACCEPTED
        return None

    def request_frame(self) -> FrameActivateSceneRequest:
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameActivateSceneRequest(
            scene_id=self.scene_id, session_id=self.session_id
        )
