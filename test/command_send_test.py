"""Unit test for command send module."""
import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from pyvlx import Parameter, PyVLXException
from pyvlx.api import ActivateScene, CommandSend, WinkSend
from pyvlx.api.frames import CommandSendConfirmationStatus, FrameCommandSendConfirmation, FrameCommandSendRequest, FrameSessionFinishedNotification
from pyvlx.api.frames.frame_command_send import FrameCommandRemainingTimeNotification, FrameCommandRunStatusNotification
from pyvlx.api.get_limitation import GetLimitation
from pyvlx.api.set_limitation import SetLimitation


class TestCommandSend(unittest.IsolatedAsyncioTestCase):
    """Test class for CommandSend."""

    def setUp(self) -> None:
        """Set up TestCommandSend."""
        mocked_pyvlx = MagicMock()
        self.command_send = CommandSend(pyvlx=mocked_pyvlx, node_id=23, parameter=Parameter())

    async def test_handle_frame(self) -> None:
        """Test handle_frame function of CommandSend object."""
        frame = MagicMock(spec=FrameCommandSendConfirmation)
        session_id = 1
        self.command_send.session_id = session_id
        frame.session_id = session_id
        self.command_send.wait_for_completion = False
        frame.status = CommandSendConfirmationStatus.ACCEPTED
        self.assertTrue(await self.command_send.handle_frame(frame=frame))
        self.assertTrue(self.command_send.success)

        self.command_send.success = False
        self.command_send.wait_for_completion = True
        frame.status = CommandSendConfirmationStatus.ACCEPTED
        self.assertFalse(await self.command_send.handle_frame(frame=frame))
        self.assertTrue(self.command_send.success)

        self.command_send.success = False
        self.command_send.wait_for_completion = False
        frame.status = CommandSendConfirmationStatus.REJECTED
        self.assertTrue(await self.command_send.handle_frame(frame=frame))
        self.assertFalse(self.command_send.success)

        # make sure we set command_send.success to False on rejection even if it was already True
        self.command_send.success = True
        self.command_send.wait_for_completion = True
        frame.status = CommandSendConfirmationStatus.REJECTED
        self.assertTrue(await self.command_send.handle_frame(frame=frame))
        self.assertFalse(self.command_send.success)

        self.command_send.success = True
        self.command_send.wait_for_completion = False
        frame.status = CommandSendConfirmationStatus.REJECTED
        self.assertTrue(await self.command_send.handle_frame(frame=frame))
        self.assertFalse(self.command_send.success)

        self.command_send.success = False
        self.command_send.wait_for_completion = True
        frame.status = CommandSendConfirmationStatus.REJECTED
        self.assertTrue(await self.command_send.handle_frame(frame=frame))
        self.assertFalse(self.command_send.success)

        # test frame type we ignore during completion wait, must return False
        frame = MagicMock(spec=FrameCommandRemainingTimeNotification)
        frame.session_id = session_id
        self.assertFalse(await self.command_send.handle_frame(frame=frame))

        # test another frame type we ignore during completion wait, must return False
        frame = MagicMock(spec=FrameCommandRunStatusNotification)
        frame.session_id = session_id
        self.assertFalse(await self.command_send.handle_frame(frame=frame))

        frame = MagicMock(spec=FrameSessionFinishedNotification)
        frame.session_id = session_id
        self.assertTrue(await self.command_send.handle_frame(frame=frame))

        frame = MagicMock(spec=FrameSessionFinishedNotification)
        frame.session_id = session_id + 1
        self.assertFalse(await self.command_send.handle_frame(frame=frame))

    @patch("pyvlx.api.ApiEvent.do_api_call", new_callable=AsyncMock)
    async def test_send(self, do_api_call: AsyncMock) -> None:
        """Test send function of CommandSend object."""
        self.command_send.success = True
        await self.command_send.send()
        assert do_api_call.called

        self.command_send.success = False
        with self.assertRaises(PyVLXException):
            await self.command_send.send()

    async def test_do_api_call_marks_quiet_period_before_sending(self) -> None:
        """User command events extend the quiet period immediately before dispatch."""
        mocked_pyvlx = MagicMock()
        mocked_pyvlx.ensure_connected = AsyncMock()
        mocked_pyvlx.get_connected.return_value = True
        mocked_pyvlx.api_call_semaphore = asyncio.Semaphore(1)
        command = CommandSend(pyvlx=mocked_pyvlx, node_id=23, parameter=Parameter())

        async def send_frame() -> None:
            mocked_pyvlx._mark_user_command_dispatched.assert_called_once()
            command.response_received_or_timeout.set()

        with patch.object(command, "send_frame", new_callable=AsyncMock, side_effect=send_frame):
            await command.do_api_call()

        mocked_pyvlx._mark_user_command_dispatched.assert_called_once()
        self.assertTrue(ActivateScene.extends_heartbeat_quiet_period)
        self.assertTrue(GetLimitation.extends_heartbeat_quiet_period)
        self.assertTrue(SetLimitation.extends_heartbeat_quiet_period)
        self.assertTrue(WinkSend.extends_heartbeat_quiet_period)

    @patch("pyvlx.api.command_send.get_new_session_id", callable=MagicMock)
    def test_request_frame(self, new_session_id_request: MagicMock) -> None:
        """Test request_frame function of CommandSend object."""
        self.command_send.session_id = 1
        new_session_id_request.return_value = 5
        assert isinstance(self.command_send.request_frame(), FrameCommandSendRequest)
        assert new_session_id_request.called
        assert self.command_send.session_id == 5 # noqa: PLR2004
