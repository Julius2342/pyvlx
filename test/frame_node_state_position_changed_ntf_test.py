"""Unit tests for FrameNodeStatePositionChangedNotification."""
import unittest
from datetime import datetime

from pyvlx import Position
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frames import FrameNodeStatePositionChangedNotification


class TestFrameNodeStatePositionChangedNotification(unittest.TestCase):
    """Test class for FrameNodeStatePositionChangedNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = \
        b'\x00\x17\x02\x11\x05\x05\xc8\x00\xc8\x00\xf7\xff\xf7\xff' \
        b'\xf7\xff\xf7\xff\x00\x00L\xcf\x00\x00\x87'

    def test_bytes(self):
        """Test FrameNodeStatePositionChangedNotification."""
        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 5
        frame.state = 5
        frame.current_position = Position(position=51200)
        frame.target = Position(position=51200)
        frame.current_position_fp1 = Position()
        frame.current_position_fp2 = Position()
        frame.current_position_fp3 = Position()
        frame.current_position_fp4 = Position()
        frame.remaining_time = 0
        frame.timestamp = 1288634368
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameNodeStatePositionChangedNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameNodeStatePositionChangedNotification))
        self.assertEqual(frame.node_id, 5)
        self.assertEqual(frame.state, 5)
        self.assertEqual(Position(frame.current_position).position, 51200)
        self.assertEqual(Position(frame.target).position, 51200)
        self.assertEqual(Position(frame.current_position_fp1).position, 63487)
        self.assertEqual(Position(frame.current_position_fp2).position, 63487)
        self.assertEqual(Position(frame.current_position_fp3).position, 63487)
        self.assertEqual(Position(frame.current_position_fp4).position, 63487)
        self.assertEqual(frame.remaining_time, 0)
        self.assertEqual(frame.timestamp, 1288634368)

    def test_str(self):
        """Test string representation of FrameNodeStatePositionChangedNotification."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        test_ts = datetime.fromtimestamp(1288634368).strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(
            str(frame),
            '<FrameNodeStatePositionChangedNotification node_id=5 state=5 '
            'current_position=\'0xC800\' target=\'0xC800\' current_position_fp1=\'0xF7FF\' '
            'current_position_fp2=\'0xF7FF\' current_position_fp3=\'0xF7FF\' '
            'current_position_fp4=\'0xF7FF\' remaining_time=0 time=\'{}\'/>'.format(test_ts))
