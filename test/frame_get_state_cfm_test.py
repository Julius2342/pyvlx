"""Unit tests for FrameGetStateConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    FrameGetStateConfirmation, GatewayState, GatewaySubState)


class TestFrameGetStateConfirmation(unittest.TestCase):
    """Test class FrameGetStateConfirmation."""

    EXAMPLE_FRAME = b"\x00\t\x00\r\x03\x80\x00\x00\x00\x00\x87"

    def test_bytes(self) -> None:
        """Test FrameGetStateConfirmation with NO_TYPE."""
        frame = FrameGetStateConfirmation()
        frame.gateway_state = GatewayState.BEACON_MODE_NOT_CONFIGURED
        frame.gateway_sub_state = GatewaySubState.PERFORMING_TASK_COMMAND
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameGetStateConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGetStateConfirmation))
        self.assertEqual(frame.gateway_state, GatewayState.BEACON_MODE_NOT_CONFIGURED)
        self.assertEqual(
            frame.gateway_sub_state, GatewaySubState.PERFORMING_TASK_COMMAND
        )

    def test_str(self) -> None:
        """Test string representation of FrameGetStateConfirmation."""
        frame = FrameGetStateConfirmation()
        frame.gateway_state = GatewayState.BEACON_MODE_NOT_CONFIGURED
        frame.gateway_sub_state = GatewaySubState.PERFORMING_TASK_COMMAND
        self.assertEqual(
            str(frame),
            "<FrameGetStateConfirmation "
            'gateway_state="GatewayState.BEACON_MODE_NOT_CONFIGURED" '
            'gateway_sub_state="GatewaySubState.PERFORMING_TASK_COMMAND"/>',
        )
