"""Unit tests for FrameGetVersionConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetVersionConfirmation


class TestFrameGetVersionConfirmation(unittest.TestCase):
    """Test class for FrameGetVersionConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x0c\x00\t\x01\x02\x03\x04\x05\x06\x17\x0e\x03\x18"

    def test_bytes(self):
        """Test FrameGetVersionConfirmation."""
        frame = FrameGetVersionConfirmation(
            software_version="1.2.3.4.5.6", hardware_version=23
        )
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameGetVersionConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGetVersionConfirmation))
        self.assertEqual(frame.software_version, "1.2.3.4.5.6")
        self.assertEqual(frame.hardware_version, 23)
        self.assertEqual(frame.product, "KLF 200")

    def test_str(self):
        """Test string representation of FrameGetVersionConfirmation."""
        frame = FrameGetVersionConfirmation(
            software_version="1.2.3.4.5.6", hardware_version=23
        )
        self.assertEqual(
            str(frame),
            '<FrameGetVersionConfirmation software_version="1.2.3.4.5.6" hardware_version="23" product="KLF 200"/>',
        )

    def test_version(self):
        """Test version string."""
        frame = FrameGetVersionConfirmation(
            software_version="1.2.3.4.5.6", hardware_version=23
        )
        self.assertEqual(
            frame.version,
            "KLF 200: Software version: 1.2.3.4.5.6, hardware version: 23",
        )

    def test_product(self):
        """Test formatting of product."""
        frame = FrameGetVersionConfirmation()
        self.assertEqual(frame.product, "KLF 200")
        frame.product_type = 42
        frame.product_group = 23
        self.assertEqual(frame.product, "Unknown Product: 23:42")
