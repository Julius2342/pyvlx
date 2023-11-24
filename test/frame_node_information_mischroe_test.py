"""Unit tests for data sample obtained from MiSchroe."""
import unittest
from datetime import datetime

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    FrameGetAllNodesInformationNotification,
    FrameGetNodeInformationNotification)
from pyvlx.const import (
    NodeTypeWithSubtype, NodeVariation, OperatingState, Velocity)
from pyvlx.parameter import Position
from pyvlx.slip import get_next_slip


class TestFrameGetNodeInformationMiSchroe(unittest.TestCase):
    """Test class data sample obtained from MiSchroe."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME1 = (
        "c0:00:7f:02:04:04:00:04:04:46:65:6e:73:74:65:72:"
        "20:42:c3:bc:72:6f:00:00:00:00:00:00:00:00:00:00:"
        "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:"
        "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:"
        "00:00:00:00:00:00:00:00:00:00:01:01:d5:07:00:01:"
        "1e:53:36:27:26:10:2f:00:81:05:c8:00:c8:00:00:00:"
        "f7:ff:f7:ff:f7:ff:00:00:4f:0d:f9:a7:02:d8:02:64:"
        "00:d8:03:ba:00:00:00:00:00:00:00:00:00:00:00:00:"
        "00:fb:c0"
    )

    EXAMPLE_FRAME2 = (
        "c0:00:7f:02:10:04:00:04:04:46:65:6e:73:74:65:72:"
        "20:42:c3:bc:72:6f:00:00:00:00:00:00:00:00:00:00:"
        "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:"
        "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:"
        "00:00:00:00:00:00:00:00:00:00:01:01:d5:07:00:01:"
        "1e:53:36:27:26:10:2f:00:81:05:c8:00:c8:00:00:00:"
        "f7:ff:f7:ff:f7:ff:00:00:4f:0d:f9:a8:02:d8:02:64:"
        "00:d8:03:ba:00:00:00:00:00:00:00:00:00:00:00:00:"
        "00:e0:c0"
    )

    def test_frame1_from_raw(self) -> None:
        """Test parse EXAMPLE_FRAME1 from raw."""
        slip = bytearray.fromhex(self.EXAMPLE_FRAME1.replace(":", ""))
        raw, _ = get_next_slip(slip)
        frame = frame_from_raw(bytes(raw))
        self.assertTrue(isinstance(frame, FrameGetAllNodesInformationNotification))
        self.assertEqual(frame.node_id, 4)
        self.assertEqual(frame.order, 4)
        self.assertEqual(frame.placement, 4)
        self.assertEqual(frame.name, "Fenster Büro")
        self.assertEqual(frame.velocity, Velocity.DEFAULT)
        self.assertEqual(
            frame.node_type, NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR
        )
        self.assertEqual(frame.product_group, 213)
        self.assertEqual(frame.product_type, 7)
        self.assertEqual(frame.node_variation, NodeVariation.NOT_SET)
        self.assertEqual(frame.power_mode, 1)
        self.assertEqual(frame.build_number, 30)
        self.assertEqual(frame.serial_number, "53:36:27:26:10:2f:00:81")
        self.assertEqual(frame.state, OperatingState.DONE)
        self.assertEqual(str(Position(frame.current_position)), "100 %")
        self.assertEqual(str(Position(frame.target)), "100 %")
        self.assertEqual(str(Position(frame.current_position_fp1)), "0 %")
        self.assertEqual(str(frame.current_position_fp2), "UNKNOWN")
        self.assertEqual(str(frame.current_position_fp3), "UNKNOWN")
        self.assertEqual(str(frame.current_position_fp4), "UNKNOWN")
        self.assertEqual(frame.remaining_time, 0)
        self.assertEqual(frame.timestamp, 1326315943)
        test_ts = datetime.fromtimestamp(1326315943).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(frame.timestamp_formatted, test_ts)
        self.assertEqual(str(frame.alias_array), "d802=6400, d803=ba00")
        # Crosscheck, Serializing:
        self.assertEqual(bytes(frame), raw)

    def test_frame2_from_raw(self) -> None:
        """Test parse EXAMPLE_FRAME2 from raw."""
        slip = bytearray.fromhex(self.EXAMPLE_FRAME2.replace(":", ""))
        raw, _ = get_next_slip(slip)
        frame = frame_from_raw(bytes(raw))
        self.assertTrue(isinstance(frame, FrameGetNodeInformationNotification))
        self.assertEqual(frame.node_id, 4)
        self.assertEqual(frame.order, 4)
        self.assertEqual(frame.placement, 4)
        self.assertEqual(frame.name, "Fenster Büro")
        self.assertEqual(frame.velocity, Velocity.DEFAULT)
        self.assertEqual(
            frame.node_type, NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR
        )
        self.assertEqual(frame.product_group, 213)
        self.assertEqual(frame.product_type, 7)
        self.assertEqual(frame.node_variation, NodeVariation.NOT_SET)
        self.assertEqual(frame.power_mode, 1)
        self.assertEqual(frame.build_number, 30)
        self.assertEqual(frame.serial_number, "53:36:27:26:10:2f:00:81")
        self.assertEqual(frame.state, OperatingState.DONE)
        self.assertEqual(str(Position(frame.current_position)), "100 %")
        self.assertEqual(str(Position(frame.target)), "100 %")
        self.assertEqual(str(Position(frame.current_position_fp1)), "0 %")
        self.assertEqual(str(Position(frame.current_position_fp2)), "UNKNOWN")
        self.assertEqual(str(Position(frame.current_position_fp3)), "UNKNOWN")
        self.assertEqual(str(Position(frame.current_position_fp4)), "UNKNOWN")
        self.assertEqual(frame.remaining_time, 0)
        self.assertEqual(frame.timestamp, 1326315944)
        test_ts = datetime.fromtimestamp(1326315944).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(frame.timestamp_formatted, test_ts)
        self.assertEqual(str(frame.alias_array), "d802=6400, d803=ba00")
        # Crosscheck, Serializing:
        self.assertEqual(bytes(frame), raw)
