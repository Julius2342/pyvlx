"""Module for Position class."""
from .exception import PyVLXException


class Position():
    """Class for storing a position."""

    UNKNOWN_POSITION = b'\xF7\xFF'
    MAX = 51200

    def __init__(self, raw=None, position=None, position_percent=None):
        """Initialize Position class."""
        if raw is not None:
            self.raw = self.from_raw(raw)
        elif position is not None:
            self.position = position
        elif position_percent is not None:
            self.position_percent = position_percent
        else:
            self.raw = Position.UNKNOWN_POSITION

    def __bytes__(self):
        """Convert object in byte representation."""
        return self.raw

    @property
    def known(self):
        """Known property, true if position is not in an unknown position."""
        return self.raw != Position.UNKNOWN_POSITION

    @property
    def open(self):
        """Return true if position is set to fully open."""
        return self.raw == b'\x00\x00'

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
    def from_int(position):
        """Create raw out of position vlaue."""
        if not isinstance(position, int):
            raise PyVLXException("Position::position_has_to_be_int")
        if position < 0:
            raise PyVLXException("Position::position_has_to_be_positive")
        if position > Position.MAX:
            raise PyVLXException("Position::position_out_of_range")
        return bytes([position >> 8 & 255, position & 255])

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

    @staticmethod
    def from_raw(raw):
        """Test if raw packets are valid for initialization of Position."""
        if not isinstance(raw, bytes):
            raise PyVLXException("Position::raw_must_be_bytes")
        if len(raw) != 2:
            raise PyVLXException("Position::raw_must_be_two_bytes")
        if raw != Position.UNKNOWN_POSITION and Position.to_int(raw) > Position.MAX:
            raise PyVLXException("position::raw_exceed_limit", raw=raw)
        return raw

    def __str__(self):
        """Return string representation of object."""
        if self.raw == Position.UNKNOWN_POSITION:
            return "UNKNOWN"
        return "{} %".format(self.position_percent)

    def __eq__(self, other):
        """Equal operator."""
        return self.raw == other.raw
