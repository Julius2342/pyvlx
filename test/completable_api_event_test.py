"""Unit test for completable api event module."""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from pyvlx import PyVLX
from pyvlx.api.completable_api_event import CompletableApiEvent
from pyvlx.api.frames import FrameBase, FrameSessionFinishedNotification
from pyvlx.const import Command


class _TestCompletableApiEvent(CompletableApiEvent):
    """Test helper implementation of CompletableApiEvent."""

    def check_confirmation(self, frame: FrameBase):
        """Return confirmation state from test frame if present."""
        return getattr(frame, "confirmation", None)

    # unused but needs to be implemented to instantiate CompletableApiEvent
    def request_frame(self) -> FrameBase:
        return FrameBase(command=Command.GW_GET_NODE_INFORMATION_REQ)


class TestCompletableApiEvent(IsolatedAsyncioTestCase):
    """Test class for CompletableApiEvent."""

    def setUp(self) -> None:
        """Set up test instance."""
        pyvlx = MagicMock(spec=PyVLX)
        self.event = _TestCompletableApiEvent(pyvlx=pyvlx, wait_for_completion=True)
        self.event.session_id = 42

    def test_check_completion(self) -> None:
        """Test check_completion method."""
        frame = FrameSessionFinishedNotification(session_id=42)
        self.assertTrue(self.event.check_completion(frame))

        frame = FrameSessionFinishedNotification(session_id=41)
        self.assertFalse(self.event.check_completion(frame))

        frame = MagicMock(spec=FrameBase)
        self.assertFalse(self.event.check_completion(frame))

    async def test_handle_frame_confirmation_accepted_no_wait(self) -> None:
        """Test handle_frame on accepted confirmation without completion wait."""
        self.event.wait_for_completion = False
        frame = MagicMock(spec=FrameBase)
        frame.confirmation = True

        self.assertTrue(await self.event.handle_frame(frame))
        self.assertTrue(self.event.success)

    async def test_handle_frame_confirmation_accepted_wait(self) -> None:
        """Test handle_frame on accepted confirmation with completion wait."""
        self.event.wait_for_completion = True
        frame = MagicMock(spec=FrameBase)
        frame.confirmation = True

        self.assertFalse(await self.event.handle_frame(frame))
        self.assertTrue(self.event.success)

    async def test_handle_frame_confirmation_rejected(self) -> None:
        """Test handle_frame on rejected confirmation."""
        self.event.wait_for_completion = True
        frame = MagicMock(spec=FrameBase)
        frame.confirmation = False

        self.assertTrue(await self.event.handle_frame(frame))
        self.assertFalse(self.event.success)

    async def test_handle_frame_completion_notification(self) -> None:
        """Test handle_frame returns completion state for non-confirmation frames."""
        frame = FrameSessionFinishedNotification(session_id=42)
        self.assertTrue(await self.event.handle_frame(frame))

        frame = FrameSessionFinishedNotification(session_id=99)
        self.assertFalse(await self.event.handle_frame(frame))

        frame = MagicMock(spec=FrameBase)
        self.assertFalse(await self.event.handle_frame(frame))
