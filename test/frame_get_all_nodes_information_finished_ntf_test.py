"""Unit tests for FrameGetAllNodesInformationFinishedNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetAllNodesInformationFinishedNotification


class TestFrameGetAllNodesInformationFinishedNotification(unittest.TestCase):
    """Test class for FrameGetAllNodesInformationFinishedNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetAllNodesInformationFinishedNotification."""
        frame = FrameGetAllNodesInformationFinishedNotification()
        self.assertEqual(bytes(frame), b"\x00\x03\x02\x05\x04")

    def test_frame_from_raw(self):
        """Test parse FrameGetAllNodesInformationFinishedNotification from raw."""
        frame = frame_from_raw(b"\x00\x03\x02\x05\x04")
        self.assertTrue(
            isinstance(frame, FrameGetAllNodesInformationFinishedNotification)
        )

    def test_str(self):
        """Test string representation of FrameGetAllNodesInformationFinishedNotification."""
        frame = FrameGetAllNodesInformationFinishedNotification()
        self.assertEqual(
            str(frame), "<FrameGetAllNodesInformationFinishedNotification/>"
        )
