"""Unit tests for FrameGetNodeInformationNotification."""
import unittest
from datetime import datetime

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetNodeInformationNotification
from pyvlx.api.frames.alias_array import AliasArray
from pyvlx.const import (
    NodeTypeWithSubtype, NodeVariation, OperatingState, Velocity)
from pyvlx.exception import PyVLXException
from pyvlx.parameter import Position


class TestFrameGetNodeInformationNotification(unittest.TestCase):
    """Test class for FrameGetNodeInformationNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = (
        b"\x00\x7f\x02\x10\x17\x04\xd2\x02Fnord23\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x01\x00@\x17\r\x01\x01\x07\x01"
        b"\x02\x03\x04\x05\x06\x06\x08\x01\x00\x0c\x00{\x04\xd2\t)\r\x80"
        b"\x11\xd7\x00\x01\x03\x03\x02\x03\x0501234567890123456789\x65"
    )

    def test_bytes(self) -> None:
        """Test FrameGetNodeInformationNotification."""
        frame = FrameGetNodeInformationNotification()
        frame.node_id = 23
        frame.order = 1234
        frame.placement = 2
        frame.name = "Fnord23"
        frame.velocity = Velocity.SILENT
        frame.node_type = NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND
        frame.product_group = 23
        frame.product_type = 13
        frame.node_variation = NodeVariation.TOPHUNG
        frame.power_mode = 1
        frame.build_number = 7
        frame.serial_number = "01:02:03:04:05:06:06:08"
        frame.state = OperatingState.ERROR_EXECUTING
        frame.current_position = Position(position=12)
        frame.target = Position(position=123)
        frame.current_position_fp1 = Position(position=1234)
        frame.current_position_fp2 = Position(position=2345)
        frame.current_position_fp3 = Position(position=3456)
        frame.current_position_fp4 = Position(position=4567)
        frame.remaining_time = 1
        frame.timestamp = 50528771
        frame.alias_array = AliasArray(raw=b"\x0501234567890123456789")
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameGetNodeInformationNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGetNodeInformationNotification))
        self.assertEqual(frame.node_id, 23)
        self.assertEqual(frame.order, 1234)
        self.assertEqual(frame.placement, 2)
        self.assertEqual(frame.name, "Fnord23")
        self.assertEqual(frame.velocity, Velocity.SILENT)
        self.assertEqual(frame.node_type, NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND)
        self.assertEqual(frame.product_group, 23)
        self.assertEqual(frame.product_type, 13)
        self.assertEqual(frame.node_variation, NodeVariation.TOPHUNG)
        self.assertEqual(frame.power_mode, 1)
        self.assertEqual(frame.build_number, 7)
        self.assertEqual(frame.serial_number, "01:02:03:04:05:06:06:08")
        self.assertEqual(frame.state, OperatingState.ERROR_EXECUTING)
        self.assertEqual(Position(frame.current_position).position, 12)
        self.assertEqual(Position(frame.target).position, 123)
        self.assertEqual(Position(frame.current_position_fp1).position, 1234)
        self.assertEqual(Position(frame.current_position_fp2).position, 2345)
        self.assertEqual(Position(frame.current_position_fp3).position, 3456)
        self.assertEqual(Position(frame.current_position_fp4).position, 4567)
        self.assertEqual(frame.remaining_time, 1)
        self.assertEqual(frame.timestamp, 50528771)
        self.assertEqual(
            str(frame.alias_array),
            "3031=3233, 3435=3637, 3839=3031, 3233=3435, 3637=3839",
        )

    def test_str(self) -> None:
        """Test string representation of FrameGetNodeInformationNotification."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        test_ts = datetime.fromtimestamp(50528771).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(
            str(frame),
            '<FrameGetNodeInformationNotification node_id="23" order="1234" placement="2" '
            'name="Fnord23" velocity="Velocity.SILENT" node_type="NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND" '
            'product_group="23" product_type="13" node_variation="NodeVariation.TOPHUNG" '
            'power_mode="1" build_number="7" serial_number="01:02:03:04:05:06:06:08" state="ERROR_EXECUTING" '
            'current_position="0 %" target="0 %" current_position_fp1="2 %" '
            'current_position_fp2="5 %" current_position_fp3="7 %" current_position_fp4="9 %" '
            'remaining_time="1" time="{}" '
            'alias_array="3031=3233, 3435=3637, 3839=3031, 3233=3435, 3637=3839"/>'.format(
                test_ts
            ),
        )

    def test_serial_number(self) -> None:
        """Test serial number property."""
        frame = FrameGetNodeInformationNotification()
        frame.serial_number = "01:02:03:04:05:06:06:08"
        self.assertEqual(frame.serial_number, "01:02:03:04:05:06:06:08")

    def test_serial_number_none(self) -> None:
        """Test serial number property with no value set."""
        frame = FrameGetNodeInformationNotification()
        frame.serial_number = None
        self.assertEqual(frame.serial_number, None)

    def test_serial_number_not_set(self) -> None:
        """Test serial number property with not set."""
        frame = FrameGetNodeInformationNotification()
        self.assertEqual(frame.serial_number, None)

    def test_wrong_serial_number(self) -> None:
        """Test setting a wrong serial number."""
        frame = FrameGetNodeInformationNotification()
        with self.assertRaises(PyVLXException):
            frame.serial_number = "01:02:03:04:05:06:06"
