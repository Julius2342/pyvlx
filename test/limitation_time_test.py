"""Test for Position class."""
import unittest

from pyvlx.parameter import (
    LimitationTime, LimitationTimeClearAll, LimitationTimeClearMaster,
    LimitationTimeUnlimited)


class TestLimitationTime(unittest.TestCase):
    """Test class for LimitationTime classes."""

    # pylint: disable=invalid-name

    def test_limitation_time_fixed(self):
        """Test fixed limitation time."""
        self.assertEqual(LimitationTime().raw, b"\xFE")
        self.assertEqual(LimitationTime(29).raw, b"\x00")
        self.assertEqual(LimitationTime(30).raw, b"\x00")
        self.assertEqual(LimitationTime(59).raw, b"\x01")
        self.assertEqual(LimitationTime(60).raw, b"\x01")
        self.assertEqual(LimitationTime(7589).raw, b"\xFC")
        self.assertEqual(LimitationTime(7590).raw, b"\xFC")
        self.assertEqual(LimitationTime(7591).raw, b"\xFC")

    def test_limitation_time_constants(self):
        """Test limitation time constants."""
        self.assertEqual(LimitationTimeUnlimited().raw, b"\xFD")
        self.assertEqual(LimitationTimeClearMaster().raw, b"\xFE")
        self.assertEqual(LimitationTimeClearAll().raw, b"\xFF")
