"""Unit tests for FrameGetLimitationStatusNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames.frame_get_limitation import (
    FrameGetLimitationStatusNotification)
from pyvlx.const import Originator


class TestFrameGetLimitationStatusNotification(unittest.TestCase):
    """Test class for TestFrameGetLimitationStatusNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetLimitationStatusNotification bytes."""
        frame = FrameGetLimitationStatusNotification()
        frame.session_id = 1
        frame.node_id = 1
        frame.parameter_id = 0
        frame.min_value = 47668
        frame.max_value = 63487
        frame.limit_originator = Originator.USER.value
        frame.limit_time = 0
        self.assertEqual(bytes(frame), b'\x00\x0d\x03\x14\x00\x01\x01\x00\xba\x34\xf7\xff\x01\x00\x9d')

    def test_frame_from_raw(self):
        """Test parse FrameGetLimitationStatusNotification from raw."""
        frame = frame_from_raw(b'\x00\x0d\x03\x14\x00\x01\x01\x00\xba\x34\xf7\xff\x01\x00\x9d')
        self.assertTrue(isinstance(frame, FrameGetLimitationStatusNotification))
        self.assertEqual(frame.limit_originator, Originator.USER)
        self.assertEqual(frame.node_id, 1)
        self.assertEqual(frame.parameter_id, 0)
        self.assertEqual(frame.session_id, 1)
        self.assertEqual(frame.max_value, 63487)
        self.assertEqual(frame.min_value, 47668)
        self.assertEqual(frame.limit_time, 0)

    def test_str(self):
        """Test string representation of FrameGetLimitationStatusNotification."""
        frame = FrameGetLimitationStatusNotification()
        self.assertEqual(str(frame),
                         '<FrameGetLimitationStatusNotification node_id="0" '
                         'session_id="None" min_value="None" max_value="None" '
                         'originator="None" limit_time="None"/>')
