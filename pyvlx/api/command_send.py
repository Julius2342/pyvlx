"""Module for retrieving scene list from API."""
from typing import TYPE_CHECKING, Any, Optional

from ..exception import PyVLXException
from ..parameter import Parameter
from .api_event import ApiEvent
from .frames import (
    CommandSendConfirmationStatus, FrameBase,
    FrameCommandRemainingTimeNotification, FrameCommandRunStatusNotification,
    FrameCommandSendConfirmation, FrameCommandSendRequest,
    FrameSessionFinishedNotification)
from .session_id import get_new_session_id

if TYPE_CHECKING:
    from pyvlx import PyVLX


class CommandSend(ApiEvent):
    """Class for sending command to API."""

    def __init__(
            self,
            pyvlx: "PyVLX",
            node_id: int,
            parameter: Parameter,
            active_parameter: int = 0,
            wait_for_completion: bool = True,
            timeout_in_seconds: int = 2,
            **functional_parameter: Any
    ):
        """Initialize SceneList class."""
        super().__init__(pyvlx=pyvlx, timeout_in_seconds=timeout_in_seconds)
        self.success = False
        self.node_id = node_id
        self.parameter = parameter
        self.active_parameter = active_parameter
        self.functional_parameter = functional_parameter
        self.wait_for_completion = wait_for_completion
        self.session_id: Optional[int] = None

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if (
                isinstance(frame, FrameCommandSendConfirmation)
                and frame.session_id == self.session_id
        ):
            if frame.status == CommandSendConfirmationStatus.ACCEPTED:
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

    async def send(self) -> None:
        """Send frame to KLF200."""
        await self.do_api_call()
        if not self.success:
            raise PyVLXException("Unable to send command")

    def request_frame(self) -> FrameCommandSendRequest:
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameCommandSendRequest(
            node_ids=[self.node_id],
            parameter=self.parameter,
            active_parameter=self.active_parameter,
            session_id=self.session_id,
            **self.functional_parameter
        )
