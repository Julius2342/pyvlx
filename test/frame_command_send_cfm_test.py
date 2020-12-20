"""Unit tests for FrameCommandSendConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    CommandSendConfirmationStatus, FrameCommandSendConfirmation)


class TestFrameCommandSendConfirmation(unittest.TestCase):
    """Test class FrameCommandSendConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameCommandSendConfirmation."""
        frame = FrameCommandSendConfirmation(
            session_id=1000, status=CommandSendConfirmationStatus.ACCEPTED
        )
        self.assertEqual(bytes(frame), b"\x00\x06\x03\x01\x03\xe8\x01\xee")

    def test_bytes_error(self):
        """Test failed FrameCommandSendConfirmation."""
        frame = FrameCommandSendConfirmation(
            session_id=1000, status=CommandSendConfirmationStatus.REJECTED
        )
        self.assertEqual(bytes(frame), b"\x00\x06\x03\x01\x03\xe8\x00\xef")

    def test_frame_from_raw(self):
        """Test parse FrameCommandSendConfirmation from raw."""
        frame = frame_from_raw(b"\x00\x06\x03\x01\x03\xe8\x00\xef")
        self.assertTrue(isinstance(frame, FrameCommandSendConfirmation))
        self.assertEqual(frame.status, CommandSendConfirmationStatus.REJECTED)
        self.assertEqual(frame.session_id, 1000)

    def test_str(self):
        """Test string representation of FrameCommandSendConfirmation."""
        frame = FrameCommandSendConfirmation(
            session_id=1000, status=CommandSendConfirmationStatus.ACCEPTED
        )
        self.assertEqual(
            str(frame),
            '<FrameCommandSendConfirmation session_id="1000" status="CommandSendConfirmationStatus.ACCEPTED"/>',
        )
