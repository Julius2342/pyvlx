"""Unit tests for PyVLX PasswordChangeRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FramePasswordChangeRequest
from pyvlx.exception import PyVLXException


class TestFramePasswordChange(unittest.TestCase):
    """Test class for FramePasswordChangeRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FramePasswordChangeRequest."""
        frame = FramePasswordChangeRequest(currentpassword="fnord", newpassword="bfeld")
        self.assertEqual(
            bytes(frame),
            b"\x00C0\x02fnord\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00bfeld\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00i",
        )

    def test_bytes_long_newpw(self):
        """Test FramePasswordChangeRequest with long new password."""
        frame = FramePasswordChangeRequest(currentpassword="fnord", newpassword="x" * 32)
        self.assertEqual(
            bytes(frame), b"\x00C0\x02fnord\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\x00"
        )

    def test_bytes_long_oldpw(self):
        """Test FramePasswordChangeRequest with long old password."""
        frame = FramePasswordChangeRequest(currentpassword="x" * 32, newpassword="bfeld")
        self.assertEqual(
            bytes(frame), b"\x00C0\x02xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbfeld\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18"
        )

    def test_bytes_long_bothpw(self):
        """Test FramePasswordChangeRequest with long passwords."""
        frame = FramePasswordChangeRequest(currentpassword="x" * 32, newpassword="y" * 32)
        self.assertEqual(
            bytes(frame), b"\x00C0\x02xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyq"
        )

    def test_frame_from_raw(self):
        """Test parsing FramePasswordChangeRequest from raw bytes."""
        frame = frame_from_raw(
            b"\x00C0\x02fnord\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00bfeld\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00i"
        )
        self.assertTrue(isinstance(frame, FramePasswordChangeRequest))
        self.assertEqual(frame.newpassword, "bfeld")
        self.assertEqual(frame.currentpassword, "fnord")

    def test_errors(self):
        """Test FramePasswordChangeRequest with wrong password."""
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordChangeRequest())
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordChangeRequest(currentpassword="fnord"))
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordChangeRequest(currentpassword="fnord", newpassword="x" * 33))
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordChangeRequest(newpassword="fnord", currentpassword="x" * 33))
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordChangeRequest(newpassword="x" * 33, currentpassword="x" * 33))

    def test_str(self):
        """Test string representation of FramePasswordChangeRequest."""
        frame = FramePasswordChangeRequest(currentpassword="fnord", newpassword="bfeld")
        self.assertEqual(str(frame), '<FramePasswordChangeRequest currentpassword="fn****" newpassword="bf****"/>')

    def test_str_no_password(self):
        """Test string representation of FramePasswordChangeRequest with no password."""
        frame = FramePasswordChangeRequest()
        self.assertEqual(str(frame), '<FramePasswordChangeRequest currentpassword="None" newpassword="None"/>')
