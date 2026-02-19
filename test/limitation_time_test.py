"""Test for LimitationTime class."""
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
        self.assertEqual(LimitationTime(seconds=29).raw, b"\x00")
        self.assertEqual(LimitationTime(seconds=30).raw, b"\x00")
        self.assertEqual(LimitationTime(seconds=59).raw, b"\x01")
        self.assertEqual(LimitationTime(seconds=60).raw, b"\x01")
        self.assertEqual(LimitationTime(seconds=7589).raw, b"\xFC")
        self.assertEqual(LimitationTime(seconds=7590).raw, b"\xFC")
        self.assertEqual(LimitationTime(seconds=7591).raw, b"\xFC")

    def test_limitation_time_constants(self):
        """Test limitation time constants."""
        self.assertEqual(LimitationTimeUnlimited().raw, b"\xFD")
        self.assertEqual(LimitationTimeClearMaster().raw, b"\xFE")
        self.assertEqual(LimitationTimeClearAll().raw, b"\xFF")

    def test_str(self):
        """Test string representation of LimitationTime."""
        self.assertEqual(str(LimitationTime(seconds=30)), "30 s")
        self.assertEqual(str(LimitationTimeUnlimited()), "UNLIMITED")
        self.assertEqual(str(LimitationTimeClearMaster()), "CLEAR_MASTER")
        self.assertEqual(str(LimitationTimeClearAll()), "CLEAR_ALL")
