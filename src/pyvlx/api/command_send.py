"""Module for sending commands to API."""
from typing import TYPE_CHECKING

from ..parameter import FunctionalParams, Parameter
from .completable_api_event import CompletableApiEvent
from .frames import (
    CommandSendConfirmationStatus, FrameBase, FrameCommandSendConfirmation,
    FrameCommandSendRequest)
from .session_id import get_new_session_id

if TYPE_CHECKING:
    from pyvlx import PyVLX


class CommandSend(CompletableApiEvent):
    """Class for sending command to API."""

    def __init__(
            self,
            *,
            pyvlx: "PyVLX",
            node_id: int,
            parameter: Parameter,
            functional_parameter: FunctionalParams | None = None,
            active_parameter: int = 0,
            wait_for_completion: bool = True,
            timeout_in_seconds: int = 2,
    ):
        """Initialize CommandSend class."""
        super().__init__(pyvlx=pyvlx, timeout_in_seconds=timeout_in_seconds, wait_for_completion=wait_for_completion)
        self.node_id = node_id
        self.parameter = parameter
        self.active_parameter = active_parameter
        self.functional_parameter = functional_parameter

    def check_confirmation(self, frame: FrameBase) -> bool | None:
        """Check if frame is a CommandSendConfirmation for this session."""
        if isinstance(frame, FrameCommandSendConfirmation) and frame.session_id == self.session_id:
            return frame.status == CommandSendConfirmationStatus.ACCEPTED
        return None

    def request_frame(self) -> FrameCommandSendRequest:
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameCommandSendRequest(
            node_ids=[self.node_id],
            parameter=self.parameter,
            active_parameter=self.active_parameter,
            session_id=self.session_id,
            functional_parameter=self.functional_parameter
        )
