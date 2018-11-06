"""Unit tests for PyVLX PasswordEnterRequest Frames."""
import unittest
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frame_password_enter import FramePasswordEnterRequest
from pyvlx.exception import PyVLXException


class TestFramePasswordEnter(unittest.TestCase):
    """Test class for PyVLX PasswordEnterRequest Frames."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_password_enter_request(self):
        """Test FramePasswordEnterRequest."""
        frame = FramePasswordEnterRequest(password="fnord")
        self.assertEqual(
            bytes(frame),
            b'\x00#0\x00fnord\x00\x00\x00\x00\x00' +
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00b')

    def test_password_enter_request_long_pw(self):
        """Test FramePasswordEnterRequest with long password."""
        frame = FramePasswordEnterRequest(password="x" * 32)
        self.assertEqual(
            bytes(frame),
            b'\x00#0\x00xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\x13')

    def test_password_enter_request_from_raw(self):
        """Test parsing FramePasswordEnterRequest from raw bytes."""
        frame = frame_from_raw(
            b'\x00#0\x00fnord\x00\x00\x00\x00\x00' +
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00b')
        self.assertTrue(isinstance(frame, FramePasswordEnterRequest))
        self.assertEqual(frame.password, 'fnord')

    def test_password_enter_request_from_raw_long(self):
        """Test parsing FramePasswordEnterRequest from raw bytes with long password."""
        frame = frame_from_raw(b'\x00#0\x00xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\x13')
        self.assertTrue(isinstance(frame, FramePasswordEnterRequest))
        self.assertEqual(frame.password, "x" * 32)

    def test_password_enter_request_error(self):
        """Test FramePasswordEnterRequest with wrong password."""
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordEnterRequest())
        with self.assertRaises(PyVLXException):
            bytes(FramePasswordEnterRequest(password="x" * 33))
