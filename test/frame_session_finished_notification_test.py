"""Unit tests for FrameSessionFinishedNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameSessionFinishedNotification


class TestFrameSessionFinishedNotification(unittest.TestCase):
    """Test class FrameSessionFinishedNotification."""

    def test_bytes(self) -> None:
        """Test FrameSessionFinishedNotification."""
        frame = FrameSessionFinishedNotification(session_id=1000)
        self.assertEqual(bytes(frame), b"\x00\x05\x03\x04\x03\xe8\xe9")

    def test_frame_from_raw(self) -> None:
        """Test parse FrameSessionFinishedNotification from raw."""
        frame = frame_from_raw(b"\x00\x05\x03\x04\x03\xe8\xe9")
        self.assertTrue(isinstance(frame, FrameSessionFinishedNotification))
        self.assertEqual(frame.session_id, 1000)

    def test_str(self) -> None:
        """Test string representation of FrameSessionFinishedNotification."""
        frame = FrameSessionFinishedNotification(session_id=1000)
        self.assertEqual(
            str(frame), '<FrameSessionFinishedNotification session_id="1000"/>'
        )
