"""Unit tests for FrameGetNodeInformationNotification."""
import unittest
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frame_get_node_information import FrameGetNodeInformationNotification
from pyvlx.const import NodeTypeWithSubtype, NodeVariation


class TestFrameGetNodeInformationNotification(unittest.TestCase):
    """Test class for FrameGetNodeInformationNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = \
        b'\x00\x7f\x02\x10\x17\x04\xd2\x02Fnord23\x00\x00\x00\x00\x00' \
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        b'\x00\x00\x00\x00\x00\x00\x00\x03\x00@\x17\r\x01\x01\x07\x01' \
        b'\x02\x03\x04\x05\x06\x06\x08\x01\x00\x0c\x00{\x04\xd2\t)\r\x80' \
        b'\x11\xd7\x00\x01\x03\x03\x02\x03\x1701234567890123456789u'

    def test_bytes(self):
        """Test FrameGetNodeInformationNotification."""
        frame = FrameGetNodeInformationNotification()
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
        frame.timestamp = b'\x03\x03\x02\x03'
        frame.nbr_of_alias = 23
        frame.alias_array = b'01234567890123456789'
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameGetNodeInformationNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGetNodeInformationNotification))
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
        self.assertEqual(frame.timestamp, b'\x03\x03\x02\x03')
        self.assertEqual(frame.nbr_of_alias, 23)
        self.assertEqual(frame.alias_array, b'01234567890123456789')

    def test_str(self):
        """Test string representation of FrameGetNodeInformationNotification."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertEqual(
            str(frame),
            '<FrameGetNodeInformationNotification node_id=23 oder=1234 placement=2 '
            'name=\'Fnord23\' velocity=3 node_type=\'NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND\' '
            'product_group=23 product_type=13 node_variation=NodeVariation.TOPHUNG '
            'power_mode=1 build_number=7 serial_number=\'01:02:03:04:05:06:06:08\' state=1 '
            'current_position=\'0 %\' target=\'0 %\' current_position_fp1=\'2 %\' '
            'current_position_fp2=\'4 %\' current_position_fp3=\'6 %\' current_position_fp4=\'8 %\' '
            'remaining_time=1 timestamp=b\'\\x03\\x03\\x02\\x03\' nbr_of_alias=23 '
            'alias_array=\'30:31:32:33:34:35:36:37:38:39:30:31:32:33:34:35:36:37:38:39\'/>')
