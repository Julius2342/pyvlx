"""Test for Position class."""
import unittest

from pyvlx import Parameter, Position


class TestParameterPosition(unittest.TestCase):
    """Test class for Position class."""

    def test_to_percent(self):
        """Test position percent output from position int input."""
        self.assertEqual(Position.to_percent(Parameter.from_int(0)), 0)
        self.assertEqual(Position.to_percent(Parameter.from_int(1)), 0)
        self.assertEqual(Position.to_percent(Parameter.from_int(3)), 0)
        self.assertEqual(Position.to_percent(Parameter.from_int(256)), 1)
        self.assertEqual(Position.to_percent(Parameter.from_int(512)), 1)
        self.assertEqual(Position.to_percent(Parameter.from_int(5120)), 10)
        self.assertEqual(Position.to_percent(Parameter.from_int(12800)), 25)
        self.assertEqual(Position.to_percent(Parameter.from_int(25600)), 50)
        self.assertEqual(Position.to_percent(Parameter.from_int(38400)), 75)
        self.assertEqual(Position.to_percent(Parameter.from_int(50688)), 99)
        self.assertEqual(Position.to_percent(Parameter.from_int(51050)), 100)
        self.assertEqual(Position.to_percent(Parameter.from_int(51200)), 100)

    def test_from_to_percent(self):
        """Test position percent output from position percent input."""
        self.assertEqual(Position.to_percent(Position.from_percent(0)), 0)
        self.assertEqual(Position.to_percent(Position.from_percent(1)), 1)
        self.assertEqual(Position.to_percent(Position.from_percent(25)), 25)
        self.assertEqual(Position.to_percent(Position.from_percent(50)), 50)
        self.assertEqual(Position.to_percent(Position.from_percent(75)), 75)
        self.assertEqual(Position.to_percent(Position.from_percent(99)), 99)
        self.assertEqual(Position.to_percent(Position.from_percent(100)), 100)
