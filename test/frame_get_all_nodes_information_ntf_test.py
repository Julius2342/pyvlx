"""Unit tests for FrameGetAllNodesInformationNotification."""
import unittest
import os

from pyvlx.const import NodeTypeWithSubtype, NodeVariation
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frames import FrameGetAllNodesInformationNotification
from pyvlx.alias_array import AliasArray


class TestFrameGetAllNodesInformationNotification(unittest.TestCase):
    """Test class for FrameGetAllNodesInformationNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = \
        b'\x00\x7f\x02\x04\x17\x04\xd2\x02Fnord23\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x03\x00@\x17\r\x01\x01\x07\x01\x02' \
        + b'\x03\x04\x05\x06\x06\x08\x01\x00\x0c\x00{\x04\xd2\t)\r\x80\x11' \
        + b'\xd7\x00\x01\x03\x03\x02\x03\x0501234567890123456789\x73'

    def test_bytes(self):
        """Test FrameGetAllNodesInformationNotification."""
        frame = FrameGetAllNodesInformationNotification()
        frame.node_id = 23
        frame.order = 1234
        frame.placement = 2
        frame.name = "Fnord23"
        frame.velocity = 3
        frame.node_type = NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND
        frame.product_group = 23
        frame.product_type = 13
        frame.node_variation = NodeVariation.TOPHUNG
        frame.power_mode = 1
        frame.build_number = 7
        frame._serial_number = b'\x01\x02\x03\x04\x05\x06\x06\x08'  # pylint: disable=protected-access
        frame.state = 1
        frame.current_position.position = 12
        frame.target.position = 123
        frame.current_position_fp1.position = 1234
        frame.current_position_fp2.position = 2345
        frame.current_position_fp3.position = 3456
        frame.current_position_fp4.position = 4567
        frame.remaining_time = 1
        frame.timestamp = 50528771
        frame.alias_array = AliasArray(raw=b'\x0501234567890123456789')
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameGetAllNodesInformationNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGetAllNodesInformationNotification))
        self.assertEqual(frame.node_id, 23)
        self.assertEqual(frame.order, 1234)
        self.assertEqual(frame.placement, 2)
        self.assertEqual(frame.name, "Fnord23")
        self.assertEqual(frame.velocity, 3)
        self.assertEqual(frame.node_type, NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND)
        self.assertEqual(frame.product_group, 23)
        self.assertEqual(frame.product_type, 13)
        self.assertEqual(frame.node_variation, NodeVariation.TOPHUNG)
        self.assertEqual(frame.power_mode, 1)
        self.assertEqual(frame.build_number, 7)
        self.assertEqual(frame.serial_number, '01:02:03:04:05:06:06:08')
        self.assertEqual(frame.state, 1)
        self.assertEqual(frame.current_position.position, 12)
        self.assertEqual(frame.target.position, 123)
        self.assertEqual(frame.current_position_fp1.position, 1234)
        self.assertEqual(frame.current_position_fp2.position, 2345)
        self.assertEqual(frame.current_position_fp3.position, 3456)
        self.assertEqual(frame.current_position_fp4.position, 4567)
        self.assertEqual(frame.remaining_time, 1)
        self.assertEqual(frame.timestamp, 50528771)
        self.assertEqual(str(frame.alias_array), '3031=3233, 3435=3637, 3839=3031, 3233=3435, 3637=3839')

    def test_str(self):
        """Test string representation of FrameGetAllNodesInformationNotification."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertEqual(
            str(frame),
            '<FrameGetAllNodesInformationNotification node_id=23 order=1234 placement=2 '
            'name=\'Fnord23\' velocity=3 node_type=\'NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND\' '
            'product_group=23 product_type=13 node_variation=NodeVariation.TOPHUNG '
            'power_mode=1 build_number=7 serial_number=\'01:02:03:04:05:06:06:08\' state=1 '
            'current_position=\'0 %\' target=\'0 %\' current_position_fp1=\'2 %\' '
            'current_position_fp2=\'4 %\' current_position_fp3=\'6 %\' current_position_fp4=\'8 %\' '
            'remaining_time=1 time=\'1971-08-08 20:46:11\' '
            'alias_array=\'3031=3233, 3435=3637, 3839=3031, 3233=3435, 3637=3839\'/>')
