"""Unit tests for FrameSetLimitationRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames.frame_set_limitation import FrameSetLimitationRequest
from pyvlx.parameter import (
    IgnorePosition, LimitationTime, LimitationTimeClearAll, Position)


class TestFrameSetLimitation(unittest.TestCase):
    """Test class for FrameSetLimitationRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes_setlimits(self):
        """Test FrameSetLimitationRequest bytes."""
        frame = FrameSetLimitationRequest(
            node_ids=[1], session_id=1, limitation_value_min=Position(position_percent=30),
            limitation_value_max=Position(position_percent=70), limitation_time=LimitationTime(seconds=60))
        self.assertEqual(bytes(frame), b'\x00\x22\x03\x10\x00\x01\x01\x03\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                       b'\x00\x00\x00\x00\x00\x3C\x00\x8C\x00\x01\x83')

    def test_bytes_clearlimits(self):
        """Test FrameSetLimitationRequest bytes for clear limits."""
        frame = FrameSetLimitationRequest(
            node_ids=[1, 2], session_id=2, limitation_value_min=IgnorePosition(),
            limitation_value_max=IgnorePosition(), limitation_time=LimitationTimeClearAll())
        self.assertEqual(bytes(frame), b'\x00\x22\x03\x10\x00\x02\x01\x03\x02\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                       b'\x00\x00\x00\x00\x00\xD4\x00\xD4\x00\xFF\xCF')

    def test_frame_from_raw(self):
        """Test parse FrameSetLimitationRequest from raw."""
        frame = frame_from_raw(b'\x00\x22\x03\x10\x00\x02\x01\x03\x02\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                               b'\x00\x00\x00\x00\x00\xD4\x00\xD4\x00\x00\x30')
        self.assertTrue(isinstance(frame, FrameSetLimitationRequest))

    def test_str(self):
        """Test string representation of FrameSetLimitationRequest."""
        frame = FrameSetLimitationRequest(node_ids=[1], session_id=1, limitation_value_min=Position(position_percent=30),
                                          limitation_value_max=Position(position_percent=70), limitation_time=LimitationTime(seconds=60))
        self.assertEqual(
            str(frame),
            '<FrameSetLimitationRequest node_ids="[1]" session_id="1" '
            'originator="Originator.USER" limitation_value_min="30 %" '
            'limitation_value_max="70 %" limitation_time="60 s" />'
        )
