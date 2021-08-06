"""Unit tests for FrameNodeInformationChangedNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameNodeInformationChangedNotification
from pyvlx.const import NodeVariation


class TestFrameNodeInformationChangedNotification(unittest.TestCase):
    """Test class for FrameNodeInformationChangedNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = (
        b"\x00H\x02\x0c\x17Fnord23\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04"
        b"\xd2\x02\x01\xd4"
    )

    def test_bytes(self):
        """Test FrameNodeInformationChangedNotification."""
        frame = FrameNodeInformationChangedNotification()
        frame.node_id = 23
        frame.order = 1234
        frame.placement = 2
        frame.name = "Fnord23"
        frame.node_variation = NodeVariation.TOPHUNG
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameNodeInformationChangedNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameNodeInformationChangedNotification))
        self.assertEqual(frame.node_id, 23)
        self.assertEqual(frame.order, 1234)
        self.assertEqual(frame.placement, 2)
        self.assertEqual(frame.node_variation, NodeVariation.TOPHUNG)
        self.assertEqual(frame.name, "Fnord23")

    def test_str(self):
        """Test string representation of FrameNodeInformationChangedNotification."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertEqual(
            str(frame),
            '<FrameNodeInformationChangedNotification node_id="23" name="Fnord23" '
            'order="1234" placement="2" node_variation="NodeVariation.TOPHUNG"/>',
        )
