"""Unit tests for FrameGetSceneListConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetSceneListConfirmation


class TestFrameGetSceneListConfirmation(unittest.TestCase):
    """Test class for FrameGetSceneListConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetSceneListConfirmation."""
        frame = FrameGetSceneListConfirmation(count_scenes=12)
        self.assertEqual(bytes(frame), b"\x00\x04\x04\r\x0c\x01")

    def test_frame_from_raw(self):
        """Test parse FrameGetSceneListConfirmation from raw."""
        frame = frame_from_raw(b"\x00\x04\x04\r\x0c\x01")
        self.assertTrue(isinstance(frame, FrameGetSceneListConfirmation))
        self.assertEqual(frame.count_scenes, 12)

    def test_str(self):
        """Test string representation of FrameGetSceneListConfirmation."""
        frame = FrameGetSceneListConfirmation(count_scenes=12)
        self.assertEqual(str(frame), '<FrameGetSceneListConfirmation count_scenes="12"/>')
