"""Unit tests for FrameGatewayRebootConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGatewayRebootConfirmation


class TestFrameGatewayRebootConfirmation(unittest.TestCase):
    """Test class TestFrameGatewayRebootConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x00\x02\x01"

    def test_bytes(self):
        """Test FrameGatewayRebootConfirmation with NO_TYPE."""
        frame = FrameGatewayRebootConfirmation()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameGatewayRebootConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGatewayRebootConfirmation))

    def test_str(self):
        """Test string representation of FrameGatewayRebootConfirmation."""
        frame = FrameGatewayRebootConfirmation()
        self.assertEqual(str(frame), '<FrameGatewayRebootConfirmation/>')
