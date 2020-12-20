"""Unit tests for FrameGatewayFactoryDefaultRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGatewayFactoryDefaultRequest


class TestFrameRebootRequest(unittest.TestCase):
    """Test class FrameGatewayFactoryDefaultRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x00\x03\x00"

    def test_bytes(self):
        """Test FrameGatewayFactoryDefaultRequest."""
        frame = FrameGatewayFactoryDefaultRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameGatewayFactoryDefaultRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGatewayFactoryDefaultRequest))

    def test_str(self):
        """Test string representation of FrameGatewayFactoryDefaultRequest."""
        frame = FrameGatewayFactoryDefaultRequest()
        self.assertEqual(str(frame), "<FrameGatewayFactoryDefaultRequest/>")
