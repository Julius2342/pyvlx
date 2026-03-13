"""Unit test for wink send."""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from pyvlx import PyVLX
from pyvlx.api.frames import (
    FrameCommandRunStatusNotification, FrameWinkSendConfirmation,
    FrameWinkSendNotification, WinkSendConfirmationStatus)
from pyvlx.api.wink_send import WinkSend


class TestWinkSend(IsolatedAsyncioTestCase):
    """Test class for WinkSend."""

    async def test_handle_frame_confirmation(self) -> None:
        """Test handle_frame with confirmation frame."""
        pyvlx = MagicMock(spec=PyVLX)
        wink_send = WinkSend(pyvlx=pyvlx, node_id=1, wait_for_completion=False)
        wink_send.session_id = 42

        frame = FrameWinkSendConfirmation(
            session_id=42, status=WinkSendConfirmationStatus.ACCEPTED
        )
        self.assertTrue(await wink_send.handle_frame(frame))
        self.assertTrue(wink_send.success)

    async def test_handle_frame_confirmation_rejected(self) -> None:
        """Test handle_frame with rejected confirmation frame."""
        pyvlx = MagicMock(spec=PyVLX)
        wink_send = WinkSend(pyvlx=pyvlx, node_id=1, wait_for_completion=False)
        wink_send.session_id = 42

        frame = FrameWinkSendConfirmation(
            session_id=42, status=WinkSendConfirmationStatus.REJECTED
        )
        self.assertTrue(await wink_send.handle_frame(frame))
        self.assertFalse(wink_send.success)

    async def test_handle_frame_run_status_notification(self) -> None:
        """Test handle_frame with run status notification frame."""
        pyvlx = MagicMock(spec=PyVLX)
        wink_send = WinkSend(pyvlx=pyvlx, node_id=1, wait_for_completion=True)
        wink_send.session_id = 42

        frame = FrameCommandRunStatusNotification(
            session_id=42,
            status_id=1,
            index_id=1,
            node_parameter=1,
            parameter_value=1,
            run_status=MagicMock(),
            status_reply=MagicMock(),
        )
        self.assertFalse(await wink_send.handle_frame(frame))

    async def test_handle_frame_notification(self) -> None:
        """Test handle_frame with notification frame."""
        pyvlx = MagicMock(spec=PyVLX)
        wink_send = WinkSend(pyvlx=pyvlx, node_id=1, wait_for_completion=True)
        wink_send.session_id = 42

        frame = FrameWinkSendNotification(session_id=42)
        self.assertTrue(await wink_send.handle_frame(frame))

    @patch("pyvlx.api.ApiEvent.do_api_call", new_callable=AsyncMock)
    async def test_wink_with_explicit_timeout(self, do_api_call: AsyncMock) -> None:
        """Test wink preserves explicitly provided timeout_in_seconds."""
        pyvlx = MagicMock(spec=PyVLX)
        wink_send = WinkSend(pyvlx=pyvlx, node_id=1, timeout_in_seconds=11)
        self.assertEqual(wink_send.timeout_in_seconds, 11)

        wink_send.success = True
        await wink_send.wink()
        do_api_call.assert_awaited_once()

    @patch("pyvlx.api.ApiEvent.do_api_call", new_callable=AsyncMock)
    async def test_wink_with_default_timeout_when_not_provided(self, do_api_call: AsyncMock) -> None:
        """Test wink applies default timeout when timeout_in_seconds is not provided."""
        pyvlx = MagicMock(spec=PyVLX)
        wink_send = WinkSend(pyvlx=pyvlx, node_id=1)
        self.assertEqual(wink_send.timeout_in_seconds, 5)

        wink_send.success = True
        await wink_send.wink()
        do_api_call.assert_awaited_once()
