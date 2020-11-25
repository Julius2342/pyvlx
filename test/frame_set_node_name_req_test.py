"""Unit tests for FrameSetNodeNameRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameSetNodeNameRequest


class TestFrameSetNodeNameRequest(unittest.TestCase):
    """Test class FrameSetNodeNameRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = (
        b"\x00D\x02\x08\x04Fnord\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x1b"
    )

    def test_bytes(self):
        """Test FrameSetNodeNameRequest with NO_TYPE."""
        frame = FrameSetNodeNameRequest(node_id=4, name="Fnord")
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameSetNodeNameRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameSetNodeNameRequest))
        self.assertEqual(frame.node_id, 4)
        self.assertEqual(frame.name, "Fnord")

    def test_str(self):
        """Test string representation of FrameSetNodeNameRequest."""
        frame = FrameSetNodeNameRequest(node_id=4, name="Fnord")
        self.assertEqual(
            str(frame), '<FrameSetNodeNameRequest node_id="4" name="Fnord"/>'
        )
