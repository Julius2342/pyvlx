"""Test for Position class."""
import unittest

from pyvlx import Parameter, Position
from pyvlx.exception import PyVLXException


class TestParameterPosition(unittest.TestCase):
    """Test class for Position class."""

    def test_from_parameter(self) -> None:
        """Test from parameter from another parameter."""
        param1 = Parameter(raw=b'\xC8\x00')
        param2 = Parameter(raw=b'\x00\x00')
        wrong_object = b'\x00\x00'
        with self.assertRaises(PyVLXException):
            Parameter.from_parameter(self=param1, parameter=wrong_object)  # type: ignore
        Parameter.from_parameter(self=param1, parameter=param2)
        self.assertEqual(param1.raw, param2.raw)

    def test_from_int(self) -> None:
        """Test from int output from parameter int input."""
        wrong_object = b'\x00\x00'
        with self.assertRaises(PyVLXException):
            Parameter.from_int(wrong_object)  # type: ignore
        not_valid_int = 100.3
        with self.assertRaises(PyVLXException):
            Parameter.from_int(not_valid_int)  # type: ignore
        int_out_of_range = Parameter.MAX + 1
        with self.assertRaises(PyVLXException):
            Parameter.from_int(int_out_of_range)  # type: ignore
        self.assertEqual(Parameter.from_int(51200), b'\xc8\x00')

    def test_to_int(self) -> None:
        """Test from int output from parameter int input."""
        raw = b'\xc8\x00'
        self.assertEqual(Parameter.to_int(raw=raw), 51200)

    def test_is_valid_int(self) -> None:
        """Test if int is valid, between 0 and 51200."""
        valid_int1 = 0
        valid_int2 = 51200
        out_of_range_int = 51201
        self.assertTrue(Parameter.is_valid_int(valid_int1))
        self.assertTrue(Parameter.is_valid_int(valid_int2))
        self.assertFalse(Parameter.is_valid_int(out_of_range_int))

    def test_from_raw(self) -> None:
        """Test raw output from byte input."""
        with self.assertRaises(PyVLXException):
            Parameter.from_raw(raw=0xC800)  # type: ignore
        with self.assertRaises(PyVLXException):
            Parameter.from_raw(raw=b'\x00')
        self.assertEqual(Parameter.from_raw(raw=b'\xd2\x01'), b'\xf7\xff')
        self.assertEqual(Parameter.from_raw(raw=b'\xd2\x01'), b'\xf7\xff')
        self.assertEqual(Parameter.from_raw(raw=b'\xd1\x01'), b'\xf7\xff')
        self.assertEqual(Parameter.from_raw(raw=b'\xd4\x01'), b'\xf7\xff')
        self.assertEqual(Parameter.from_raw(raw=b'\xd8\x01'), b'\xf7\xff')
        self.assertNotEqual(Parameter.from_raw(raw=b'\xd2\x00'), b'\xf7\xff')
        self.assertNotEqual(Parameter.from_raw(raw=b'\xd2\x00'), b'\xf7\xff')
        self.assertNotEqual(Parameter.from_raw(raw=b'\xd1\x00'), b'\xf7\xff')
        self.assertNotEqual(Parameter.from_raw(raw=b'\xd4\x00'), b'\xf7\xff')
        self.assertEqual(Parameter.from_raw(raw=b'\x00\x00'), b'\x00\x00')
        self.assertEqual(Parameter.from_raw(raw=b'\xc8\x00'), b'\xc8\x00')
        self.assertEqual(Parameter.from_raw(raw=b'\xc8\x01'), b'\xf7\xff')

    def test_from_to_percent(self) -> None:
        """Test position percent output from position percent input."""
        self.assertEqual(Position.to_percent(Position.from_percent(0)), 0)
        self.assertEqual(Position.to_percent(Position.from_percent(1)), 1)
        self.assertEqual(Position.to_percent(Position.from_percent(25)), 25)
        self.assertEqual(Position.to_percent(Position.from_percent(50)), 50)
        self.assertEqual(Position.to_percent(Position.from_percent(75)), 75)
        self.assertEqual(Position.to_percent(Position.from_percent(99)), 99)
        self.assertEqual(Position.to_percent(Position.from_percent(100)), 100)

    def test_to_percent(self) -> None:
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

    def test_equal(self) -> None:
        """Test from parameter from another parameter."""
        param1 = Parameter(raw=b'\xC8\x00')
        param2 = Parameter(raw=b'\x00\x00')
        param3 = Parameter(raw=b'\xC8\x00')
        wrong_object = b'\x00\x00'
        self.assertEqual(param1.__eq__(wrong_object), NotImplemented)  # pylint: disable=C2801
        self.assertFalse(param1 == param2)
        self.assertTrue(param1 == param3)
