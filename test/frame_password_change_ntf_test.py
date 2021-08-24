"""Unit tests for PyVLX PasswordChangeNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FramePasswordChangeNotification
from pyvlx.exception import PyVLXException


class TestFramePasswordChange(unittest.TestCase):
    """Test class for FramePasswordChangeNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FramePasswordChangeNotification."""
        frame = FramePasswordChangeNotification(newpassword="fnord")
        self.assertEqual(
            bytes(frame),
            b"\x00#0\x04fnord\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00f",
        )

    def test_bytes_long_pw(self):
        """Test FramePasswordChangeNotification with long new password."""
        frame = FramePasswordChangeNotification(newpassword="x" * 32)
        self.assertEqual(
            bytes(frame), b"\x00#0\x04xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\x17"
        )

    def test_frame_from_raw(self):
        """Test parsing FramePasswordChangeNotification from raw bytes."""
        frame = frame_from_raw(
            b"\x00#0\x04fnord\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00f",
        )
        self.assertTrue(isinstance(frame, FramePasswordChangeNotification))
        self.assertEqual(frame.newpassword, "fnord")

    def test_errors(self):
        """Test FramePasswordChangeNotification with wrong password."""
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordChangeNotification())
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordChangeNotification(newpassword="x" * 33))

    def test_str(self):
        """Test string representation of FramePasswordChangeNotification."""
        frame = FramePasswordChangeNotification(newpassword="fnord")
        self.assertEqual(str(frame), '<FramePasswordChangeNotification newpassword="fn****"/>')

    def test_str_no_password(self):
        """Test string representation of FramePasswordChangeNotification with no password."""
        frame = FramePasswordChangeNotification()
        self.assertEqual(str(frame), '<FramePasswordChangeNotification newpassword="None"/>')
