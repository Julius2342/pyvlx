"""Unit tests for FrameDiscoverNodesNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameDiscoverNodesNotification


class TestFrameDiscoverNodesNotification(unittest.TestCase):
    """Test class for FrameDiscoverNodesNotification."""
    maxDiff = None
    # pylint: disable=too-many-public-methods,invalid-name
    EXAMPLE1 = (bytes.fromhex('02006f254c0080dd01000000019c62990080dd01000000000AF0')
                + bytes.fromhex('02006f254c0080dd01000000019c62990080dd01000000000AF0')
                + bytes.fromhex('02006f254c0080dd01000000019c62990080dd01000000000AF0')
                + bytes.fromhex('02006f254c0080dd01000000019c62990080dd01000000000AF0')
                + bytes.fromhex('02006f254c0080dd01000000019c62990080dd01000000000AF0')
                + b"\x00")

    def test_bytes(self):
        """Test FrameDiscoverNodesNotification."""
        frame = FrameDiscoverNodesNotification()
        self.assertEqual(
            bytes(frame),
            b"\x00\x86\x01\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x82",
        )

    def test_frame_from_raw(self):
        """Test parse FrameDiscoverNodesNotification from raw."""
        frame = frame_from_raw(
            b"\x00\x86\x01\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x82"
        )
        self.assertTrue(isinstance(frame, FrameDiscoverNodesNotification))

    def test_str(self):
        """Test string representation of FrameDiscoverNodesNotification."""
        frame = FrameDiscoverNodesNotification()
        frame.from_payload(self.EXAMPLE1)

        self.assertEqual(
            str(frame),
            '<FrameDiscoverNodesNotification addednodes="[1, 16, 17, 18, 19, '
            '21, 22, 24, 26, 29, 34, 35, 38, 55, 56, 58, 59, 60, 62, 63, 64, '
            '96, 106, 107, 108, 111, 113, 117, 118, 120, 123, 124, 127, 143, '
            '144, 146, 147, 148, 150, 151, 152, 193, 195, 204, 205, 206, 207]" '
            'rfconnectionerror="[1, 16, 17, 18, 19, 21, 22, 24, 26, 29, 34, 35, '
            '38, 55, 56, 58, 59, 60, 62, 63, 64, 96, 106, 107, 108, 111, 113, '
            '117, 118, 120, 123, 124, 127, 143, 144, 146, 147, 148, 150, 151, '
            '152, 193, 195, 204, 205, 206, 207, 209]" iokeyerrorexistingnode="['
            '8, 9, 10, 11, 13, 14, 16, 18, 21, 26, 27, 30, 47, 48, 50, 51, 52, '
            '54, 55, 56, 88, 98, 99, 100, 103, 105, 109, 110, 112, 115, 116, 119, '
            '135, 136, 138, 139, 140, 142, 143, 144, 185, 187, 196, 197, 198, 199, '
            '201]"removed="[8, 9, 10, 11, 13, 14, 16, 18, 21, 26, 27, 30, 47, 48, '
            '50, 51, 52, 54, 55, 56, 88, 98, 99, 100, 103, 105, 109, 110, 112, 115, '
            '116, 119, 135, 136, 138, 139, 140, 142, 143, 144, 185, 187, 196, 197, '
            '198, 199, 201]" open="[8, 9, 10, 11, 13, 14, 16, 18, 21, 26, 27, 30, '
            '47, 48, 50, 51, 52, 54, 55, 56, 88, 98, 99, 100, 103, 105, 109, 110, '
            '112, 115, 116, 119, 135, 136, 138, 139, 140, 142, 143, 144, 185, 187, '
            '196, 197, 198, 199]" discoverstatus="DiscoverStatus.OK"/>',
        )
