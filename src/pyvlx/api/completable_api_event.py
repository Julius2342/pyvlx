"""Base class for completable API calls with confirmation + completion pattern."""
from typing import TYPE_CHECKING, Optional

from ..exception import PyVLXException
from .api_event import ApiEvent
from .frames import FrameBase, FrameSessionFinishedNotification

if TYPE_CHECKING:
    from pyvlx import PyVLX


class CompletableApiEvent(ApiEvent):
    """Base class for completable API calls.

    Completable API calls follow a common pattern, they are used for API calls that
    send a request frame and then expect a confirmation frame (accepted/rejected).

    While the device is performing the action (e.g. window close, which takes time),
    incoming FrameCommandRunStatusNotification and FrameCommandRemainingTimeNotification
    frames can be received, they are ignored.

    If wait_for_completion is True, the API call normally waits until a
    session finished notification is received, usually indicating the action
    is completed on the device side. However, ApiEvent.do_api_call() will
    also stop waiting when the timeout expires, in which case the call ends
    without having seen a completion notification.

    If wait_for_completion is False, the API call is considered complete right
    after receiving the confirmation frame. In this case, any frames received
    after the confirmation frame are ignored.

    The flow is:
    1. Send a request frame with a session ID (sending is handled by the base class,
       subclasses just need to implement request_frame() including the session ID in the frame)
    2. Receive a confirmation frame (accepted or rejected)
    3. Optionally wait for a completion frame signaling the end of the session
       (e.g. FrameSessionFinishedNotification) until the timeout is reached.

    Subclasses implement check_confirmation() to identify their specific
    confirmation frame type. The default check_completion() handles the
    standard FrameSessionFinishedNotification; override if needed.

    The ``success`` attribute reflects whether an accepted confirmation frame was
    received within the timeout. Completion notifications do not change the
    ``success`` value; they only influence how long the call waits when
    ``wait_for_completion`` is True. If the command is rejected or no accepted
    confirmation is received before the timeout, ``success`` is False and
    send() will raise PyVLXException. If an accepted confirmation is received,
    ``success`` remains True even if no completion notification is seen before
    the timeout.
    """

    def __init__(self, pyvlx: "PyVLX", timeout_in_seconds: int = 10, wait_for_completion: bool = True):
        """Initialize CompletableApiEvent."""
        super().__init__(pyvlx=pyvlx, timeout_in_seconds=timeout_in_seconds)
        self.wait_for_completion = wait_for_completion
        self.session_id: Optional[int] = None

    def check_confirmation(self, frame: FrameBase) -> Optional[bool]:
        """Check if frame is a confirmation for this session.

        Returns True if accepted, False if rejected, None if not a matching confirmation frame.
        """
        raise NotImplementedError("Subclasses must implement check_confirmation()")

    def check_completion(self, frame: FrameBase) -> bool:
        """Return True if this frame signals session completion."""
        return (
            isinstance(frame, FrameSessionFinishedNotification)
            and frame.session_id == self.session_id
        )

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming frame. Return True if this frame completes the API call."""
        confirmation = self.check_confirmation(frame)
        if confirmation is not None:
            self.success = confirmation
            if not confirmation:
                return True  # Rejected means done, no point waiting
            return not self.wait_for_completion
        return self.check_completion(frame)

    async def send(self) -> None:
        """Send request, wait for confirmation and (optionally) completion, and raise if no accepted confirmation is received."""
        await self.do_api_call()
        if not self.success:
            raise PyVLXException(f"{type(self).__name__} send with session ID {self.session_id} failed")
