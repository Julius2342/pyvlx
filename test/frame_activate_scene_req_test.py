"""Unit tests for FrameActivateSceneRequest."""
import unittest
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frames import FrameActivateSceneRequest


class TestFrameActivateSceneRequest(unittest.TestCase):
    """Test class FrameActivateSceneRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameActivateSceneRequest with NO_TYPE."""
        frame = FrameActivateSceneRequest(scene_id=4, session_id=1000)
        self.assertEqual(bytes(frame), b'\x00\t\x04\x12\x03\xe8\x01\x03\x04\x00\xf2')

    def test_frame_from_raw(self):
        """Test parse FrameActivateSceneRequest from raw."""
        frame = frame_from_raw(b'\x00\t\x04\x12\x03\xe8\x01\x03\x04\x00\xf2')
        self.assertTrue(isinstance(frame, FrameActivateSceneRequest))
        self.assertEqual(frame.scene_id, 4)
        self.assertEqual(frame.session_id, 1000)

    def test_str(self):
        """Test string representation of FrameActivateSceneRequest."""
        frame = FrameActivateSceneRequest(scene_id=4, session_id=1000)
        self.assertEqual(
            str(frame),
            '<FrameActivateSceneRequest scene_id=4 session_id=1000/>')
