"""Unit tests for PyVLX PasswordEnterRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FramePasswordEnterRequest
from pyvlx.exception import PyVLXException


class TestFramePasswordEnter(unittest.TestCase):
    """Test class for FramePasswordEnterRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FramePasswordEnterRequest."""
        frame = FramePasswordEnterRequest(password="fnord")
        self.assertEqual(
            bytes(frame),
            b"\x00#0\x00fnord\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00b",
        )

    def test_bytes_long_pw(self):
        """Test FramePasswordEnterRequest with long password."""
        frame = FramePasswordEnterRequest(password="x" * 32)
        self.assertEqual(
            bytes(frame), b"\x00#0\x00xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\x13"
        )

    def test_frame_from_raw(self):
        """Test parsing FramePasswordEnterRequest from raw bytes."""
        frame = frame_from_raw(
            b"\x00#0\x00fnord\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00b"
        )
        self.assertTrue(isinstance(frame, FramePasswordEnterRequest))
        self.assertEqual(frame.password, "fnord")

    def test_frame_from_raw_long(self):
        """Test parsing FramePasswordEnterRequest from raw bytes with long password."""
        frame = frame_from_raw(b"\x00#0\x00xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\x13")
        self.assertTrue(isinstance(frame, FramePasswordEnterRequest))
        self.assertEqual(frame.password, "x" * 32)

    def test_errors(self):
        """Test FramePasswordEnterRequest with wrong password."""
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordEnterRequest())
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordEnterRequest(password="x" * 33))

    def test_str(self):
        """Test string representation of FramePasswordEnterRequest."""
        frame = FramePasswordEnterRequest(password="fnord")
        self.assertEqual(str(frame), '<FramePasswordEnterRequest password="fn****"/>')

    def test_str_no_password(self):
        """Test string representation of FramePasswordEnterRequest with no password."""
        frame = FramePasswordEnterRequest()
        self.assertEqual(str(frame), '<FramePasswordEnterRequest password="None"/>')
