"""Test for Position class."""
import unittest

from pyvlx.exception import PyVLXException
from pyvlx.position import Position


class TestPosition(unittest.TestCase):
    """Test class for Position class."""

    # pylint: disable=invalid-name

    def test_no_position(self):
        """Test empty Position object."""
        self.assertEqual(Position().raw, b'\xF7\xFF')

    def test_raw(self):
        """Test raw assignement."""
        self.assertEqual(Position(raw=b'\x00\x00').raw, b'\x00\x00')
        self.assertEqual(Position(raw=b'\x0A\x05').raw, b'\x0A\x05')
        self.assertEqual(Position(raw=b'\xC8\x00').raw, b'\xC8\x00')

    def test_position(self):
        """Test initiaization with position value."""
        self.assertEqual(Position(position=0).position, 0)
        self.assertEqual(Position(position=10).position, 10)
        self.assertEqual(Position(position=1234).position, 1234)
        self.assertEqual(Position(position=12345).position, 12345)
        self.assertEqual(Position(position=51200).position, 51200)

    def test_percent(self):
        """Test initialization with percent value."""
        self.assertEqual(Position(position_percent=0).position_percent, 0)
        self.assertEqual(Position(position_percent=5).position_percent, 5)
        self.assertEqual(Position(position_percent=50).position_percent, 50)
        self.assertEqual(Position(position_percent=95).position_percent, 95)
        self.assertEqual(Position(position_percent=100).position_percent, 100)

    def test_conversion(self):
        """Test conversion from one form to other."""
        self.assertEqual(Position(raw=b'\x0A\x05').position, 2565)
        self.assertEqual(Position(position_percent=50).position, 25600)
        self.assertEqual(Position(position=12345).position_percent, 24)

    def test_exception(self):
        """Test wrong initialization of Position."""
        with self.assertRaises(PyVLXException):
            Position(position=2.5)
        with self.assertRaises(PyVLXException):
            Position(position=-1)
        with self.assertRaises(PyVLXException):
            Position(position=51201)
        with self.assertRaises(PyVLXException):
            Position(position_percent=2.5)
        with self.assertRaises(PyVLXException):
            Position(position_percent=-1)
        with self.assertRaises(PyVLXException):
            Position(position_percent=101)
        with self.assertRaises(PyVLXException):
            Position(raw=b'\xC8\x01')
        with self.assertRaises(PyVLXException):
            Position(raw=b'\xC9\x00')

    def test_known(self):
        """Test 'known' property."""
        self.assertTrue(Position(raw=b'\x12\x00').known)
        self.assertTrue(Position(raw=b'\xC8\x00').known)
        self.assertFalse(Position(raw=b'\xF7\xFF').known)

    def test_open_closed(self):
        """Test open and closed property."""
        position_open = Position(position_percent=0)
        self.assertFalse(position_open.closed)
        self.assertTrue(position_open.open)
        position_closed = Position(position_percent=100)
        self.assertTrue(position_closed.closed)
        self.assertFalse(position_closed.open)
        position_half = Position(position_percent=50)
        self.assertFalse(position_half.closed)
        self.assertFalse(position_half.open)

    def test_str(self):
        """Test string representation."""
        self.assertEqual(str(Position(raw=b'\xF7\xFF')), "UNKNOWN")
        self.assertEqual(str(Position(position_percent=50)), "50 %")
