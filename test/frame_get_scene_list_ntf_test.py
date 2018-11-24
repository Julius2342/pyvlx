"""Unit tests for FrameGetSceneListNotification."""
import unittest
from pyvlx.frame_get_scene_list import FrameGetSceneListNotification
from pyvlx.frame_creation import frame_from_raw


class TestFrameGetSceneListNotification(unittest.TestCase):
    """Test class for FrameGetSceneListNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME1 = \
        b'\x00\xc8\x04\x0e\x03\x00All Window' \
        + b's Closed\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x01Sleeping ' \
        + b'Wide Open\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x02Bath Ope' \
        + b'n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x03\xe2'

    EXAMPLE_FRAME2 = \
        b'\x00F\x04\x0e\x01\x00One Scene\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00w'

    def test_bytes(self):
        """Test FrameGetSceneListNotification."""
        frame = FrameGetSceneListNotification()
        frame.scenes = [(0, 'All Windows Closed'), (1, 'Sleeping Wide Open'), (2, 'Bath Open')]
        frame.remaining_scenes = 3
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME1)

    def test_bytes_one_scene(self):
        """Test FrameGetSceneListNotification with one scene."""
        frame = FrameGetSceneListNotification()
        frame.scenes = [(0, 'One Scene')]
        frame.remaining_scenes = 0
        print(bytes(frame))
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME2)

    def test_frame_from_raw(self):
        """Test parse FrameGetSceneListNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME1)
        self.assertTrue(isinstance(frame, FrameGetSceneListNotification))
        self.assertEqual(frame.scenes, [(0, 'All Windows Closed'), (1, 'Sleeping Wide Open'), (2, 'Bath Open')])
        self.assertEqual(frame.remaining_scenes, 3)

    def test_frame_from_raw_one_scene(self):
        """Test parse FrameGetSceneListNotification from raw with one scene."""
        frame = frame_from_raw(self.EXAMPLE_FRAME2)
        self.assertTrue(isinstance(frame, FrameGetSceneListNotification))
        self.assertEqual(frame.scenes, [(0, 'One Scene')])
        self.assertEqual(frame.remaining_scenes, 0)

    def test_str(self):
        """Test string representation of FrameGetSceneListNotification."""
        frame = FrameGetSceneListNotification()
        frame.scenes = [(0, 'All Windows Closed'), (1, 'Sleeping Wide Open'), (2, 'Bath Open')]
        frame.remaining_scenes = 3
        self.assertEqual(
            str(frame),
            '<FrameGetSceneListNotification scenes=[(0, \'All Windows Closed\'), '
            + '(1, \'Sleeping Wide Open\'), (2, \'Bath Open\')] remaining_scenes=3>')
