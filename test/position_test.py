"""Test for Position class."""
import unittest

from pyvlx import (
    CurrentPosition, Parameter, Position, SwitchParameter, SwitchParameterOff,
    SwitchParameterOn, UnknownPosition)
from pyvlx.exception import PyVLXException


class TestPosition(unittest.TestCase):
    """Test class for Position class."""

    # pylint: disable=invalid-name

    def test_no_position(self) -> None:
        """Test empty Position object."""
        self.assertEqual(Position().raw, b"\xF7\xFF")

    def test_raw(self) -> None:
        """Test raw assignment."""
        self.assertEqual(Position(Parameter(raw=b"\x00\x00")).raw, b"\x00\x00")
        self.assertEqual(Position(Parameter(raw=b"\x0A\x05")).raw, b"\x0A\x05")
        self.assertEqual(Position(Parameter(raw=b"\xC8\x00")).raw, b"\xC8\x00")

    def test_position(self) -> None:
        """Test initialization with position value."""
        self.assertEqual(Position(position=0).position, 0)
        self.assertEqual(Position(position=10).position, 10)
        self.assertEqual(Position(position=1234).position, 1234)
        self.assertEqual(Position(position=12345).position, 12345)
        self.assertEqual(Position(position=51200).position, 51200)

    def test_percent(self) -> None:
        """Test initialization with percent value."""
        self.assertEqual(Position(position_percent=0).position_percent, 0)
        self.assertEqual(Position(position_percent=5).position_percent, 5)
        self.assertEqual(Position(position_percent=50).position_percent, 50)
        self.assertEqual(Position(position_percent=95).position_percent, 95)
        self.assertEqual(Position(position_percent=100).position_percent, 100)

    def test_conversion(self) -> None:
        """Test conversion from one form to other."""
        self.assertEqual(Position(Parameter(raw=b"\x0A\x05")).position, 2565)
        self.assertEqual(Position(position_percent=50).position, 25600)
        self.assertEqual(Position(position=12345).position_percent, 24)

    def test_fallback_to_unknown(self) -> None:
        """Test fallback to unknown."""
        self.assertEqual(Parameter(raw=b"\xC8\x01"), Parameter(raw=Parameter.from_int(Parameter.UNKNOWN_VALUE)))
        self.assertEqual(Parameter(raw=b"\xC9\x00"), Parameter(raw=Parameter.from_int(Parameter.UNKNOWN_VALUE)))
        self.assertEqual(Parameter(raw=b"\xD8\x00"), Parameter(raw=Parameter.from_int(Parameter.UNKNOWN_VALUE)))
        self.assertEqual(Parameter(raw=b"\xfe\x01"), Parameter(raw=Parameter.from_int(Parameter.UNKNOWN_VALUE)))

    def test_exception(self) -> None:
        """Test wrong initialization of Position."""
        with self.assertRaises(PyVLXException):
            Position(position=2.5)  # type: ignore
        with self.assertRaises(PyVLXException):
            Position(position=-1)
        with self.assertRaises(PyVLXException):
            Position(position=51201)
        with self.assertRaises(PyVLXException):
            Position(position_percent=2.5)  # type: ignore
        with self.assertRaises(PyVLXException):
            Position(position_percent=-1)
        with self.assertRaises(PyVLXException):
            Position(position_percent=101)
        with self.assertRaises(PyVLXException):
            Parameter(raw=b"\x00\x00\x00")
        with self.assertRaises(PyVLXException):
            Parameter(raw="\x00\x00")  # type: ignore

    def test_known(self) -> None:
        """Test 'known' property."""
        self.assertTrue(Position(Parameter(raw=b"\x12\x00")).known)
        self.assertTrue(Position(Parameter(raw=b"\xC8\x00")).known)
        self.assertFalse(Position(Parameter(raw=b"\xF7\xFF")).known)

        # Well, not really know. But at least not unknown:
        self.assertTrue(Position(Parameter(raw=b"\xD2\x00")).known)

    def test_open_closed(self) -> None:
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

    def test_str(self) -> None:
        """Test string representation."""
        self.assertEqual(str(Position(Parameter(raw=b"\xF7\xFF"))), "UNKNOWN")
        self.assertEqual(str(Position(position_percent=50)), "50 %")

    def test_unknown_position_class(self) -> None:
        """Test UnknownPosition class."""
        self.assertEqual(UnknownPosition().raw, b"\xF7\xFF")

    def test_current_position_class(self) -> None:
        """Test CurrentPosition class."""
        self.assertEqual(CurrentPosition().raw, b"\xD2\x00")

    def test_on_off(self) -> None:
        """Test SwitchParameter parameter."""
        parameter = SwitchParameter()
        self.assertFalse(parameter.is_on())
        self.assertFalse(parameter.is_off())
        parameter.set_on()
        self.assertTrue(parameter.is_on())
        self.assertFalse(parameter.is_off())
        parameter.set_off()
        self.assertFalse(parameter.is_on())
        self.assertTrue(parameter.is_off())

    def test_parsing_on_off(self) -> None:
        """Test parsing OnOFf from raw."""
        parameter_on = SwitchParameter(Parameter(raw=b"\x00\x00"))
        self.assertTrue(parameter_on.is_on())
        self.assertFalse(parameter_on.is_off())
        parameter_off = SwitchParameter(Parameter(raw=b"\xC8\x00"))
        self.assertFalse(parameter_off.is_on())
        self.assertTrue(parameter_off.is_off())

    def test_switch_parameter_on_class(self) -> None:
        """Test SwitchParameterOn class."""
        self.assertTrue(SwitchParameterOn().is_on())
        self.assertFalse(SwitchParameterOn().is_off())

    def test_switch_parameter_off_class(self) -> None:
        """Test SwitchParameterOff class."""
        self.assertFalse(SwitchParameterOff().is_on())
        self.assertTrue(SwitchParameterOff().is_off())
