"""Unit tests for FrameActivateSceneRequest."""
import unittest

from pyvlx.frame_creation import frame_from_raw
from pyvlx.frames import FrameActivateSceneRequest
from pyvlx.const import Originator, Priority


class TestFrameActivateSceneRequest(unittest.TestCase):
    """Test class FrameActivateSceneRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b'\x00\t\x04\x12\x03\xe8\x02\x03\x04\x00\xf1'

    def test_bytes(self):
        """Test FrameActivateSceneRequest with NO_TYPE."""
        frame = FrameActivateSceneRequest(scene_id=4, session_id=1000, originator=Originator.RAIN)
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameActivateSceneRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameActivateSceneRequest))
        self.assertEqual(frame.scene_id, 4)
        self.assertEqual(frame.session_id, 1000)
        self.assertEqual(frame.originator, Originator.RAIN)
        self.assertEqual(frame.priority, Priority.USER_LEVEL_2)

    def test_str(self):
        """Test string representation of FrameActivateSceneRequest."""
        frame = FrameActivateSceneRequest(scene_id=4, session_id=1000)
        self.assertEqual(
            str(frame),
            '<FrameActivateSceneRequest scene_id=4 session_id=1000 originator=Originator.USER/>')
