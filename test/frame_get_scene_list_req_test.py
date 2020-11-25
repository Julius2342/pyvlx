"""Unit tests for FrameGetSceneListRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetSceneListRequest


class TestFrameGetSceneListRequest(unittest.TestCase):
    """Test class for FrameGetSceneListRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetSceneListRequest with NO_TYPE."""
        frame = FrameGetSceneListRequest()
        self.assertEqual(bytes(frame), b"\x00\x03\x04\x0c\x0b")

    def test_frame_from_raw(self):
        """Test parse FrameGetSceneListRequest from raw."""
        frame = frame_from_raw(b"\x00\x03\x04\x0c\x0b")
        self.assertTrue(isinstance(frame, FrameGetSceneListRequest))

    def test_str(self):
        """Test string representation of FrameGetSceneListRequest."""
        frame = FrameGetSceneListRequest()
        self.assertEqual(str(frame), "<FrameGetSceneListRequest/>")
