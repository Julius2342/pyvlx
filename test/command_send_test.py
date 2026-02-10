"""Unit test for command send module."""
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from pyvlx import Parameter, PyVLXException
from pyvlx.api import CommandSend
from pyvlx.api.frames import (
    CommandSendConfirmationStatus, FrameCommandRemainingTimeNotification,
    FrameCommandRunStatusNotification, FrameCommandSendConfirmation,
    FrameCommandSendRequest, FrameSessionFinishedNotification)


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

        self.command_send.success = False
        self.command_send.wait_for_completion = True
        frame.status = CommandSendConfirmationStatus.REJECTED
        self.assertFalse(await self.command_send.handle_frame(frame=frame))
        self.assertFalse(self.command_send.success)

        frame = MagicMock(spec=FrameCommandRemainingTimeNotification)
        frame.session_id = session_id
        self.assertFalse(await self.command_send.handle_frame(frame=frame))

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

    @patch("pyvlx.api.command_send.get_new_session_id", callable=MagicMock)
    def test_request_frame(self, new_session_id_request: MagicMock) -> None:
        """Test request_frame function of CommandSend object."""
        self.command_send.session_id = 1
        new_session_id_request.return_value = 5
        assert isinstance(self.command_send.request_frame(), FrameCommandSendRequest)
        assert new_session_id_request.called
        assert self.command_send.session_id == 5
