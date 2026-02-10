"""Test for Intensity class."""
import unittest

from pyvlx import CurrentIntensity, Intensity, Parameter, UnknownIntensity
from pyvlx.exception import PyVLXException


class TestIntensity(unittest.TestCase):
    """Test class for Intensity class."""

    # pylint: disable=invalid-name

    def test_no_intensity(self) -> None:
        """Test empty Intensity object."""
        self.assertEqual(Intensity().raw, b"\xF7\xFF")

    def test_raw(self) -> None:
        """Test raw assignment."""
        self.assertEqual(Intensity(Parameter(raw=b"\x00\x00")).raw, b"\x00\x00")
        self.assertEqual(Intensity(Parameter(raw=b"\x0A\x05")).raw, b"\x0A\x05")
        self.assertEqual(Intensity(Parameter(raw=b"\xC8\x00")).raw, b"\xC8\x00")

    def test_intensity(self) -> None:
        """Test initialization with intensity value."""
        self.assertEqual(Intensity(intensity=0).intensity, 0)
        self.assertEqual(Intensity(intensity=10).intensity, 10)
        self.assertEqual(Intensity(intensity=1234).intensity, 1234)
        self.assertEqual(Intensity(intensity=12345).intensity, 12345)
        self.assertEqual(Intensity(intensity=51200).intensity, 51200)

    def test_percent(self) -> None:
        """Test initialization with percent value."""
        # Verify that percentages work correctly: 0% = off, 100% = fully on
        self.assertEqual(Intensity(intensity_percent=0).intensity_percent, 0)
        self.assertEqual(Intensity(intensity_percent=5).intensity_percent, 5)
        self.assertEqual(Intensity(intensity_percent=50).intensity_percent, 50)
        self.assertEqual(Intensity(intensity_percent=95).intensity_percent, 95)
        self.assertEqual(Intensity(intensity_percent=100).intensity_percent, 100)

    def test_conversion(self) -> None:
        """Test conversion from one form to other."""
        # 0% = off = raw 200 (0xC8) in first byte
        intensity_off = Intensity(intensity_percent=0)
        self.assertEqual(intensity_off.raw, b"\xC8\x00")
        self.assertEqual(intensity_off.intensity, 51200)

        # 100% = fully on = raw 0 in first byte
        intensity_on = Intensity(intensity_percent=100)
        self.assertEqual(intensity_on.raw, b"\x00\x00")
        self.assertEqual(intensity_on.intensity, 0)

        # 50% = half brightness = raw 100 in first byte
        intensity_half = Intensity(intensity_percent=50)
        self.assertEqual(intensity_half.raw, b"\x64\x00")
        self.assertEqual(intensity_half.intensity, 25600)
        self.assertEqual(intensity_half.intensity_percent, 50)

        # Test reverse conversion from raw
        self.assertEqual(Intensity(Parameter(raw=b"\xC8\x00")).intensity_percent, 0)
        self.assertEqual(Intensity(Parameter(raw=b"\x00\x00")).intensity_percent, 100)
        self.assertEqual(Intensity(Parameter(raw=b"\x64\x00")).intensity_percent, 50)

    def test_exception(self) -> None:
        """Test wrong initialization of Intensity."""
        with self.assertRaises(PyVLXException):
            Intensity(intensity=2.5)  # type: ignore
        with self.assertRaises(PyVLXException):
            Intensity(intensity=-1)
        with self.assertRaises(PyVLXException):
            Intensity(intensity=51201)
        with self.assertRaises(PyVLXException):
            Intensity(intensity_percent=2.5)  # type: ignore
        with self.assertRaises(PyVLXException):
            Intensity(intensity_percent=-1)
        with self.assertRaises(PyVLXException):
            Intensity(intensity_percent=101)

    def test_known(self) -> None:
        """Test 'known' property."""
        self.assertTrue(Intensity(Parameter(raw=b"\x12\x00")).known)
        self.assertTrue(Intensity(Parameter(raw=b"\xC8\x00")).known)
        self.assertFalse(Intensity(Parameter(raw=b"\xF7\xFF")).known)

        # Well, not really known. But at least not unknown:
        self.assertTrue(Intensity(Parameter(raw=b"\xD2\x00")).known)

    def test_on_off(self) -> None:
        """Test on and off property."""
        # 100% intensity = fully on = FULL_BRIGHTNESS = 0x0000
        intensity_on = Intensity(intensity_percent=100)
        self.assertFalse(intensity_on.off)
        self.assertTrue(intensity_on.on)

        # 0% intensity = off = NO_BRIGHTNESS = 0xC800
        intensity_off = Intensity(intensity_percent=0)
        self.assertTrue(intensity_off.off)
        self.assertFalse(intensity_off.on)

        # From raw values
        intensity_on_raw = Intensity(intensity=0)
        self.assertTrue(intensity_on_raw.on)
        self.assertFalse(intensity_on_raw.off)

        intensity_off_raw = Intensity(intensity=51200)
        self.assertFalse(intensity_off_raw.on)
        self.assertTrue(intensity_off_raw.off)

        # Half intensity is neither fully on nor off
        intensity_half = Intensity(intensity_percent=50)
        self.assertFalse(intensity_half.off)
        self.assertFalse(intensity_half.on)

    def test_str(self) -> None:
        """Test string representation."""
        self.assertEqual(str(Intensity(Parameter(raw=b"\xF7\xFF"))), "UNKNOWN")
        self.assertEqual(str(Intensity(intensity_percent=50)), "50 %")
        self.assertEqual(str(Intensity(intensity_percent=0)), "0 %")
        self.assertEqual(str(Intensity(intensity_percent=100)), "100 %")

    def test_unknown_intensity_class(self) -> None:
        """Test UnknownIntensity class."""
        self.assertEqual(UnknownIntensity().raw, b"\xF7\xFF")

    def test_current_intensity_class(self) -> None:
        """Test CurrentIntensity class."""
        self.assertEqual(CurrentIntensity().raw, b"\xD2\x00")

    def test_percent_to_raw_mapping(self) -> None:
        """Test that percent correctly maps to raw values (inverted for Intensity)."""
        # For Intensity: 0% (off) should give raw value 200 (0xC8)
        self.assertEqual(Intensity.from_percent(0), b"\xC8\x00")
        # For Intensity: 100% (fully on) should give raw value 0
        self.assertEqual(Intensity.from_percent(100), b"\x00\x00")
        # For Intensity: 50% should give raw value 100 (0x64)
        self.assertEqual(Intensity.from_percent(50), b"\x64\x00")
        # For Intensity: 25% should give raw value 150 (0x96)
        self.assertEqual(Intensity.from_percent(25), b"\x96\x00")
        # For Intensity: 75% should give raw value 50 (0x32)
        self.assertEqual(Intensity.from_percent(75), b"\x32\x00")

    def test_raw_to_percent_mapping(self) -> None:
        """Test that raw values correctly map to percent (inverted for Intensity)."""
        # For Intensity: raw value 200 (0xC8) should give 0% (off)
        self.assertEqual(Intensity.to_percent(b"\xC8\x00"), 0)
        # For Intensity: raw value 0 should give 100% (fully on)
        self.assertEqual(Intensity.to_percent(b"\x00\x00"), 100)
        # For Intensity: raw value 100 (0x64) should give 50%
        self.assertEqual(Intensity.to_percent(b"\x64\x00"), 50)
        # For Intensity: raw value 150 (0x96) should give 25%
        self.assertEqual(Intensity.to_percent(b"\x96\x00"), 25)
        # For Intensity: raw value 50 (0x32) should give 75%
        self.assertEqual(Intensity.to_percent(b"\x32\x00"), 75)
