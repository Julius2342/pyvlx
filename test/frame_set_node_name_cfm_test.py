"""Unit tests for FrameSetNodeNameConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    FrameSetNodeNameConfirmation, SetNodeNameConfirmationStatus)


class TestFrameSetNodeNameConfirmation(unittest.TestCase):
    """Test class for FrameSetNodeNameConfirmation."""

    EXAMPLE_FRAME = b"\x00\x05\x02\t\x00\x17\x19"
    EXAMPLE_FRAME_ERR = b"\x00\x05\x02\t\x01\x17\x18"

    def test_bytes(self) -> None:
        """Test FrameSetNodeNameConfirmation."""
        frame = FrameSetNodeNameConfirmation(node_id=23)
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_bytes_error(self) -> None:
        """Test failed FrameSetNodeNameConfirmation."""
        frame = FrameSetNodeNameConfirmation(
            node_id=23, status=SetNodeNameConfirmationStatus.ERROR_REQUEST_REJECTED
        )
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME_ERR)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameSetNodeNameConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameSetNodeNameConfirmation))
        self.assertEqual(frame.status, SetNodeNameConfirmationStatus.OK)
        self.assertEqual(frame.node_id, 23)

    def test_str(self) -> None:
        """Test string representation of FrameSetNodeNameConfirmation."""
        frame = FrameSetNodeNameConfirmation(node_id=23)
        self.assertEqual(
            str(frame),
            '<FrameSetNodeNameConfirmation node_id="23" status="SetNodeNameConfirmationStatus.OK"/>',
        )
