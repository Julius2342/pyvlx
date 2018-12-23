"""Module for Position class."""
from .exception import PyVLXException


class Parameter():
    """General object for storing parameters."""

    UNKNOWN_VALUE = 63487  # F7 FF
    CURRENT_POSITION = 53760  # D2 00
    MAX = 51200  # C8 00
    MIN = 0  # 00 00
    ON = 0  # 00 00
    OFF = 51200  # C8 00

    def __init__(self, raw=None):
        """Initialize Parameter class."""
        self.raw = self.from_int(Position.UNKNOWN_VALUE)
        if raw is not None:
            self.raw = self.from_raw(raw)

    def from_parameter(self, parameter):
        """Set internal raw state from parameter."""
        if not isinstance(parameter, Parameter):
            raise Exception("parameter::from_parameter_wrong_object")
        self.raw = parameter.raw

    @staticmethod
    def from_int(value):
        """Create raw out of position vlaue."""
        if not isinstance(value, int):
            raise PyVLXException("value_has_to_be_int")
        if not Parameter.is_valid_int(value):
            raise PyVLXException("value_out_of_range")
        return bytes([value >> 8 & 255, value & 255])

    @staticmethod
    def is_valid_int(value):
        """Test if value can be rendered out of int."""
        if 0 <= value <= Parameter.MAX:  # This includes ON and OFF
            return True
        if value == Parameter.UNKNOWN_VALUE:
            return True
        if value == Parameter.CURRENT_POSITION:
            return True
        return False

    @staticmethod
    def from_raw(raw):
        """Test if raw packets are valid for initialization of Position."""
        if not isinstance(raw, bytes):
            raise PyVLXException("Position::raw_must_be_bytes")
        if len(raw) != 2:
            raise PyVLXException("Position::raw_must_be_two_bytes")
        if raw != Position.from_int(Position.CURRENT_POSITION) and \
                raw != Position.from_int(Position.UNKNOWN_VALUE) and \
                Position.to_int(raw) > Position.MAX:
            raise PyVLXException("position::raw_exceed_limit", raw=raw)
        return raw

    def __eq__(self, other):
        """Equal operator."""
        return self.raw == other.raw

    def __str__(self):
        """Return string representation of object."""
        return '0x' + ''.join('{:02X}'.format(x) for x in self.raw)


class SwitchParameter(Parameter):
    """Class for storing On or Off values."""

    def __init__(self, parameter=None):
        """Initialize Parameter class."""
        super().__init__()
        if parameter is not None:
            self.from_parameter(parameter)

    def set_on(self):
        """Set parameter to 'on' state."""
        self.raw = self.from_int(Parameter.ON)

    def set_off(self):
        """Set parameter to 'off' state."""
        self.raw = self.from_int(Parameter.OFF)

    def is_on(self):
        """Return True if oarameter is in 'on' state."""
        return self.raw == self.from_int(Parameter.ON)

    def is_off(self):
        """Return True if oarameter is in 'off' state."""
        return self.raw == self.from_int(Parameter.OFF)


class SwitchParameterOn(SwitchParameter):
    """Switch Parameter in switched 'on' state."""

    def __init__(self):
        """Initialize SwitchParameterOn class."""
        super().__init__()
        self.set_on()


class SwitchParameterOff(SwitchParameter):
    """Switch Parameter in switched 'off' state."""

    def __init__(self):
        """Initialize SwitchParameterOff class."""
        super().__init__()
        self.set_off()


class Position(Parameter):
    """Class for storing a position."""

    def __init__(self, parameter=None, position=None, position_percent=None):
        """Initialize Position class."""
        super().__init__()
        if parameter is not None:
            self.from_parameter(parameter)
        elif position is not None:
            self.position = position
        elif position_percent is not None:
            self.position_percent = position_percent

    def __bytes__(self):
        """Convert object in byte representation."""
        return self.raw

    @property
    def known(self):
        """Known property, true if position is not in an unknown position."""
        return self.raw != self.from_int(Position.UNKNOWN_VALUE)

    @property
    def open(self):
        """Return true if position is set to fully open."""
        return self.raw == self.from_int(Position.MIN)

    @property
    def closed(self):
        """Return true if position is set to fully closed."""
        return self.raw == bytes([self.MAX >> 8 & 255, self.MAX & 255])

    @property
    def position(self):
        """Position property."""
        return self.to_int(self.raw)

    @position.setter
    def position(self, position):
        """Setter of internal raw via position."""
        self.raw = self.from_int(position)

    @property
    def position_percent(self):
        """Position percent property."""
        # inclear why it returns a <property object> here
        return int(self.to_percent(self.raw))

    @position_percent.setter
    def position_percent(self, position_percent):
        """Setter of internal raw via percent position."""
        self.raw = self.from_percent(position_percent)

    @staticmethod
    def to_int(raw):
        """Create int position value out of raw."""
        return raw[0] * 256 + raw[1]

    @staticmethod
    def from_percent(position_percent):
        """Create raw value out of percent position."""
        if not isinstance(position_percent, int):
            raise PyVLXException("Position::position_percent_has_to_be_int")
        if position_percent < 0:
            raise PyVLXException("Position::position_percent_has_to_be_positive")
        if position_percent > 100:
            raise PyVLXException("Position::position_percent_out_of_range")
        return bytes([position_percent*2, 0])

    @staticmethod
    def to_percent(raw):
        """Create percent position value out of raw."""
        # The first byte has the vlue from 0 to 200. Ignoring the second one.
        return int(raw[0]/2)

    def __str__(self):
        """Return string representation of object."""
        if self.raw == self.from_int(Position.UNKNOWN_VALUE):
            return "UNKNOWN"
        return "{} %".format(self.position_percent)


class UnknownPosition(Position):
    """Unknown position."""

    def __init__(self):
        """Initialize UnknownPosition class."""
        super().__init__(position=Position.UNKNOWN_VALUE)


class CurrentPosition(Position):
    """Current position, used to stop devices."""

    def __init__(self):
        """Initialize CurrentPosition class."""
        super().__init__(position=Position.CURRENT_POSITION)
