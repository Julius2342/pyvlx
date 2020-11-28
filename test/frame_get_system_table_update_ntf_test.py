"""Unit tests for FrameGetSystemTableDataNotification."""
import unittest

from pyvlx.api.frames import FrameGetSystemTableUpdateNotification

class TestFrameGetSystemTableUpdateNotification(unittest.TestCase):
    """Test class for FrameGetSystemTableDataNotification."""
    # pylint: disable=too-many-public-methods,invalid-name
    maxDiff = None
    EXAMPLE_PAYLOAD = bytes.fromhex(
        '0102040810204080010204081020408001020408102040800102'
        'FF00000000000000000000000000000000000000000000000000'
        )

    def test_frame_from_payload(self):
        """Test parse FrameGetSystemTableDataNotification from raw."""
        frame = FrameGetSystemTableUpdateNotification()
        frame.from_payload(self.EXAMPLE_PAYLOAD)
        self.assertTrue(isinstance(frame, FrameGetSystemTableUpdateNotification))
        self.assertTrue(frame.addednodeids == [0, 9, 18, 27, 36, 45, 54, 63, 64, 73, 82,
                                               91, 100, 109, 118, 127, 128, 137, 146, 155,
                                               164, 173, 182, 191, 192, 201])
        self.assertTrue(frame.removednodeids == [0, 1, 2, 3, 4, 5, 6, 7])

    def test_str(self):
        """Test string representation of FrameGetSystemTableDataNotification."""
        frame = FrameGetSystemTableUpdateNotification()
        frame.from_payload(self.EXAMPLE_PAYLOAD)
        self.assertEqual(
            str(frame),
            '<FrameGetSystemTableUpdateNotification addednodeids="[0, 9, 18, 27, 36, 45, 54,'
            ' 63, 64, 73, 82, 91, 100, 109, 118, 127, 128, 137, 146, 155, 164, 173, 182, 191,'
            ' 192, 201]" removednodeids="[0, 1, 2, 3, 4, 5, 6, 7]"/>',
        )
