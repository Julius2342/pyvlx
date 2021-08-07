"""Unit tests frame_creation module."""
import unittest

from pyvlx.api.frames import calc_crc, extract_from_frame
from pyvlx.exception import PyVLXException


class TestFrameHelper(unittest.TestCase):
    """Test class for frame_creation module."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_crc(self):
        """Test crc calculation."""
        self.assertEqual(calc_crc(b""), 0)
        self.assertEqual(calc_crc(b"\x01"), 1)
        self.assertEqual(calc_crc(b"\x01\x02"), 3)
        self.assertEqual(calc_crc(b"\x01\x02\x03"), 0)
        self.assertEqual(calc_crc(b"\x01\x02\x03\xff"), 255)

    def test_extract_from_frame(self):
        """Test extract_from_frame method."""
        with self.assertRaises(PyVLXException):
            extract_from_frame(bytes(4))
        with self.assertRaises(PyVLXException):
            extract_from_frame(
                bytes(b"\x01\x04\x00\x00\x02\x06")
            )  # invalid length (first 2 bytes)
        with self.assertRaises(PyVLXException):
            extract_from_frame(bytes(b"\x00\x04\x00\x00\x02\x07"))  # invalid crc
        with self.assertRaises(PyVLXException):
            extract_from_frame(bytes(b"\x00\x04\xFF\xFF\x02\x06"))  # invalid crc
