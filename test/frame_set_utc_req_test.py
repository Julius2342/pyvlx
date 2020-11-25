"""Unit tests for FrameSetUTCRequest."""
import unittest
from datetime import datetime

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameSetUTCRequest


class TestFrameSetUTCRequest(unittest.TestCase):
    """Test class FrameSetUTCRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x07 \x00[\xfd\xaanE"
    EXAMPLE_TS = 1543350894

    def test_bytes(self):
        """Test FrameSetUTCRequest with NO_TYPE."""
        frame = FrameSetUTCRequest(timestamp=self.EXAMPLE_TS)
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameSetUTCRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameSetUTCRequest))
        self.assertEqual(frame.timestamp, self.EXAMPLE_TS)

    def test_str(self):
        """Test string representation of FrameSetUTCRequest."""
        frame = FrameSetUTCRequest(timestamp=1543350894)
        test_ts = datetime.fromtimestamp(1543350894).strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(str(frame), '<FrameSetUTCRequest time="{}"/>'.format(test_ts))
