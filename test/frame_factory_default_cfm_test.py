"""Unit tests for FrameGatewayFactoryDefaultConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGatewayFactoryDefaultConfirmation


class TestFrameGatewayFactoryDefaultConfirmation(unittest.TestCase):
    """Test class FrameGatewayFactoryDefaultConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x00\x04\x07"

    def test_bytes(self):
        """Test FrameGatewayFactoryDefaultConfirmation."""
        frame = FrameGatewayFactoryDefaultConfirmation()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameGatewayFactoryDefaultConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGatewayFactoryDefaultConfirmation))

    def test_str(self):
        """Test string representation of FrameGatewayFactoryDefaultConfirmation."""
        frame = FrameGatewayFactoryDefaultConfirmation()
        self.assertEqual(str(frame), "<FrameGatewayFactoryDefaultConfirmation/>")
