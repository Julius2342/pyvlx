"""Unit tests for data sample obtained from MiSchroe."""
import unittest
import os

from pyvlx.slip import get_next_slip
from pyvlx.const import NodeTypeWithSubtype, NodeVariation
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frames import FrameGetNodeInformationNotification
from pyvlx.frames import FrameGetAllNodesInformationNotification


class TestFrameGetNodeInformationMiSchroe(unittest.TestCase):
    """Test class data sample obtained from MiSchroe."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME1 = \
        "c0:00:7f:02:04:04:00:04:04:46:65:6e:73:74:65:72:" \
        "20:42:c3:bc:72:6f:00:00:00:00:00:00:00:00:00:00:" \
        "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:" \
        "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:" \
        "00:00:00:00:00:00:00:00:00:00:01:01:d5:07:00:01:" \
        "1e:53:36:27:26:10:2f:00:81:05:c8:00:c8:00:00:00:" \
        "f7:ff:f7:ff:f7:ff:00:00:4f:0d:f9:a7:02:d8:02:64:" \
        "00:d8:03:ba:00:00:00:00:00:00:00:00:00:00:00:00:" \
        "00:fb:c0"

    EXAMPLE_FRAME2 = \
        "c0:00:7f:02:10:04:00:04:04:46:65:6e:73:74:65:72:" \
        "20:42:c3:bc:72:6f:00:00:00:00:00:00:00:00:00:00:" \
        "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:" \
        "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:" \
        "00:00:00:00:00:00:00:00:00:00:01:01:d5:07:00:01:" \
        "1e:53:36:27:26:10:2f:00:81:05:c8:00:c8:00:00:00:" \
        "f7:ff:f7:ff:f7:ff:00:00:4f:0d:f9:a8:02:d8:02:64:" \
        "00:d8:03:ba:00:00:00:00:00:00:00:00:00:00:00:00:" \
        "00:e0:c0"

    def setUp(self):
        """Set up test class."""
        os.environ['TZ'] = 'Europe/Berlin'

    def test_frame1_from_raw(self):
        """Test parse EXAMPLE_FRAME1 from raw."""
        slip = bytearray.fromhex(self.EXAMPLE_FRAME1.replace(':', ''))
        raw, _ = get_next_slip(slip)
        frame = frame_from_raw(bytes(raw))
        self.assertTrue(isinstance(frame, FrameGetAllNodesInformationNotification))
        self.assertEqual(frame.node_id, 4)
        self.assertEqual(frame.order, 4)
        self.assertEqual(frame.placement, 4)
        self.assertEqual(frame.name, 'Fenster Büro')
        self.assertEqual(frame.velocity, 0)
        self.assertEqual(frame.node_type, NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR)
        self.assertEqual(frame.product_group, 213)
        self.assertEqual(frame.product_type, 7)
        self.assertEqual(frame.node_variation, NodeVariation.NOT_SET)
        self.assertEqual(frame.power_mode, 1)
        self.assertEqual(frame.build_number, 30)
        self.assertEqual(frame.serial_number, '53:36:27:26:10:2f:00:81')
        self.assertEqual(frame.state, 5)
        self.assertEqual(str(frame.current_position), '100 %')
        self.assertEqual(str(frame.target), '100 %')
        self.assertEqual(str(frame.current_position_fp1), '0 %')
        self.assertEqual(str(frame.current_position_fp2), 'UNKNOWN')
        self.assertEqual(str(frame.current_position_fp3), 'UNKNOWN')
        self.assertEqual(str(frame.current_position_fp4), 'UNKNOWN')
        self.assertEqual(frame.remaining_time, 0)
        self.assertEqual(frame.timestamp, 1326315943)
        self.assertEqual(frame.timestamp_formatted, '2012-01-11 22:05:43')
        self.assertEqual(str(frame.alias_array), 'd802=6400, d803=ba00')
        # Crosscheck, Serializing:
        self.assertEqual(bytes(frame), raw)

    def test_frame2_from_raw(self):
        """Test parse EXAMPLE_FRAME2 from raw."""
        slip = bytearray.fromhex(self.EXAMPLE_FRAME2.replace(':', ''))
        raw, _ = get_next_slip(slip)
        frame = frame_from_raw(bytes(raw))
        self.assertTrue(isinstance(frame, FrameGetNodeInformationNotification))
        self.assertEqual(frame.node_id, 4)
        self.assertEqual(frame.order, 4)
        self.assertEqual(frame.placement, 4)
        self.assertEqual(frame.name, 'Fenster Büro')
        self.assertEqual(frame.velocity, 0)
        self.assertEqual(frame.node_type, NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR)
        self.assertEqual(frame.product_group, 213)
        self.assertEqual(frame.product_type, 7)
        self.assertEqual(frame.node_variation, NodeVariation.NOT_SET)
        self.assertEqual(frame.power_mode, 1)
        self.assertEqual(frame.build_number, 30)
        self.assertEqual(frame.serial_number, '53:36:27:26:10:2f:00:81')
        self.assertEqual(frame.state, 5)
        self.assertEqual(str(frame.current_position), '100 %')
        self.assertEqual(str(frame.target), '100 %')
        self.assertEqual(str(frame.current_position_fp1), '0 %')
        self.assertEqual(str(frame.current_position_fp2), 'UNKNOWN')
        self.assertEqual(str(frame.current_position_fp3), 'UNKNOWN')
        self.assertEqual(str(frame.current_position_fp4), 'UNKNOWN')
        self.assertEqual(frame.remaining_time, 0)
        self.assertEqual(frame.timestamp, 1326315944)
        self.assertEqual(frame.timestamp_formatted, '2012-01-11 22:05:44')
        self.assertEqual(str(frame.alias_array), 'd802=6400, d803=ba00')
        # Crosscheck, Serializing:
        self.assertEqual(bytes(frame), raw)
