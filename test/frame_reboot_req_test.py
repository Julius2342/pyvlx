"""Unit tests for FrameGatewayRebootRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGatewayRebootRequest


class TestFrameGatewayRebootRequest(unittest.TestCase):
    """Test class TestFrameGatewayRebootRequest."""

    EXAMPLE_FRAME = b"\x00\x03\x00\x01\x02"

    def test_bytes(self) -> None:
        """Test FrameGatewayRebootRequest with NO_TYPE."""
        frame = FrameGatewayRebootRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameGatewayRebootRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGatewayRebootRequest))

    def test_str(self) -> None:
        """Test string representation of FrameGatewayRebootRequest."""
        frame = FrameGatewayRebootRequest()
        self.assertEqual(str(frame), '<FrameGatewayRebootRequest/>')
