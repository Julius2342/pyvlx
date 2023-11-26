"""Unit tests for FrameNodeStatePositionChangedNotification."""
import unittest
from datetime import datetime

from pyvlx import Position
from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameNodeStatePositionChangedNotification
from pyvlx.const import OperatingState


class TestFrameNodeStatePositionChangedNotification(unittest.TestCase):
    """Test class for FrameNodeStatePositionChangedNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = (
        b"\x00\x17\x02\x11\x05\x05\xc8\x00\xc8\x00\xf7\xff\xf7\xff"
        b"\xf7\xff\xf7\xff\x00\x00L\xcf\x00\x00\x87"
    )

    def test_bytes(self) -> None:
        """Test FrameNodeStatePositionChangedNotification."""
        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 5
        frame.state = OperatingState.DONE
        frame.current_position = Position(position=51200)
        frame.target = Position(position=51200)
        frame.current_position_fp1 = Position()
        frame.current_position_fp2 = Position()
        frame.current_position_fp3 = Position()
        frame.current_position_fp4 = Position()
        frame.remaining_time = 0
        frame.timestamp = 1288634368
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameNodeStatePositionChangedNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameNodeStatePositionChangedNotification))
        self.assertEqual(frame.node_id, 5)
        self.assertEqual(frame.state, OperatingState.DONE)
        self.assertEqual(Position(frame.current_position).position, 51200)
        self.assertEqual(Position(frame.target).position, 51200)
        self.assertEqual(Position(frame.current_position_fp1).position, 63487)
        self.assertEqual(Position(frame.current_position_fp2).position, 63487)
        self.assertEqual(Position(frame.current_position_fp3).position, 63487)
        self.assertEqual(Position(frame.current_position_fp4).position, 63487)
        self.assertEqual(frame.remaining_time, 0)
        self.assertEqual(frame.timestamp, 1288634368)

    def test_str(self) -> None:
        """Test string representation of FrameNodeStatePositionChangedNotification."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        test_ts = datetime.fromtimestamp(1288634368).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(
            str(frame),
            '<FrameNodeStatePositionChangedNotification node_id="5" state="DONE" '
            'current_position="100 %" target="100 %" current_position_fp1="UNKNOWN" '
            'current_position_fp2="UNKNOWN" current_position_fp3="UNKNOWN" '
            'current_position_fp4="UNKNOWN" remaining_time="0" time="{}"/>'.format(
                test_ts
            ),
        )
