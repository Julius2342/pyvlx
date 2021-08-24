"""Unit tests for FrameGetLimitationStatus."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames.frame_get_limitation import FrameGetLimitationStatus
from pyvlx.const import LimitationType


class TestFrameGetLimitationStatus(unittest.TestCase):
    """Test class for FrameGetLimitationStatus."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetLimitationStatus bytes."""
        frame = FrameGetLimitationStatus(node_ids=[1], session_id=1, limitation_type=LimitationType.MIN_LIMITATION)
        self.assertEqual(bytes(frame), b'\x00\x1c\x03\x12\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                       b'\x00\x00\x0c')

        frame = FrameGetLimitationStatus(node_ids=[1, 2], session_id=2, limitation_type=LimitationType.MAX_LIMITATION)
        self.assertEqual(bytes(frame), b'\x00\x1c\x03\x12\x00\x02\x02\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                       b'\x00\x01\x0f')

    def test_frame_from_raw(self):
        """Test parse FrameGetLimitationStatus from raw."""
        frame = frame_from_raw(b'\x00\x1c\x03\x12\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                               b'\x0c')
        self.assertTrue(isinstance(frame, FrameGetLimitationStatus))

    def test_str(self):
        """Test string representation of FrameGetLimitationStatus."""
        frame = FrameGetLimitationStatus(node_ids=[1], session_id=1, limitation_type=LimitationType.MIN_LIMITATION)
        self.assertEqual(str(frame), '<FrameGetLimitationStatus node_ids="[1]" session_id="1" originator="Originator.USER" />')
