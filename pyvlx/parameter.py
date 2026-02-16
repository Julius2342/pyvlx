"""Module for Position class."""
import math
from typing import Optional

from .exception import PyVLXException


class Parameter:
    """General object for storing parameters."""

    UNKNOWN_VALUE = 0xF7FF  # F7 FF
    CURRENT = 0xD200  # D2 00
    MAX = 0xC800  # C8 00
    MIN = 0x0000  # 00 00
    ON = 0x0000  # 00 00
    OFF = 0xC800  # C8 00
    TARGET = 0xD100  # D1 00
    IGNORE = 0xD400  # D4 00
    DUAL_SHUTTER_CURTAINS = 0xD808  # D8 08

    def __init__(self, raw: Optional[bytes] = None):
        """Initialize Parameter class."""
        self.raw = self.from_int(Position.UNKNOWN_VALUE)
        if raw is not None:
            self.raw = self.from_raw(raw)

    def __bytes__(self) -> bytes:
        """Convert object in byte representation."""
        return self.raw

    def from_parameter(self, parameter: "Parameter") -> None:
        """Set internal raw state from parameter."""
        if not isinstance(parameter, Parameter):
            raise PyVLXException("parameter::from_parameter_wrong_object")
        self.raw = parameter.raw

    @staticmethod
    def from_int(value: int) -> bytes:
        """Create raw out of position value."""
        if not isinstance(value, int):
            raise PyVLXException("value_has_to_be_int")
        if not Parameter.is_valid_int(value):
            raise PyVLXException("value_out_of_range")
        return bytes([value >> 8 & 255, value & 255])

    @staticmethod
    def to_int(raw: bytes) -> int:
        """Create int position value out of raw."""
        return raw[0] * 256 + raw[1]

    @staticmethod
    def is_valid_int(value: int) -> bool:
        """Test if value can be rendered out of int."""
        if 0 <= value <= Parameter.MAX:  # This includes ON and OFF
            return True
        valid_values = {
            Parameter.UNKNOWN_VALUE,
            Parameter.IGNORE,
            Parameter.CURRENT,
            Parameter.TARGET,
            Parameter.DUAL_SHUTTER_CURTAINS,
        }
        if value in valid_values:
            return True
        return False

    @staticmethod
    def from_raw(raw: bytes) -> bytes:
        """Test if raw packets are valid for initialization of Position."""
        if not isinstance(raw, bytes):
            raise PyVLXException("Position::raw_must_be_bytes")
        if len(raw) != 2:
            raise PyVLXException("Position::raw_must_be_two_bytes")
        if (
            raw != Position.from_int(Position.CURRENT)
            and raw != Position.from_int(Position.IGNORE)
            and raw != Position.from_int(Position.TARGET)
            and raw != Position.from_int(Position.UNKNOWN_VALUE)
            and Position.to_int(raw) > Position.MAX
        ):
            return Position.from_int(Position.UNKNOWN_VALUE)
        return raw

    @staticmethod
    def from_percent(percent: int) -> bytes:
        """Create raw value out of percent position."""
        if not isinstance(percent, int):
            raise PyVLXException("Position::percent_has_to_be_int")
        if percent < 0:
            raise PyVLXException("Position::percent_has_to_be_positive")
        if percent > 100:
            raise PyVLXException("Position::percent_out_of_range")
        return bytes([percent * 2, 0])

    @staticmethod
    def to_percent(raw: bytes) -> int:
        """Create percent position value out of raw."""
        # The first byte has the vlue from 0 to 200. Ignoring the second one.
        # Adding 0.5 allows a slight tolerance for devices (e.g. Velux SML) that
        # do not return exactly 51200 as final position when closed.
        return int(raw[0] / 2 + 0.5)

    def __eq__(self, other: object) -> bool:
        """Equal operator."""
        if not isinstance(other, Parameter):
            return NotImplemented
        return self.raw == other.raw

    def __str__(self) -> str:
        """Return string representation of object."""
        if self.raw == self.from_int(Position.UNKNOWN_VALUE):
            return "UNKNOWN"
        if self.raw == self.from_int(Position.CURRENT):
            return "CURRENT"
        if self.raw == self.from_int(Position.TARGET):
            return "TARGET"
        if self.raw == self.from_int(Position.IGNORE):
            return "IGNORE"
        if self.raw == self.from_int(Position.DUAL_SHUTTER_CURTAINS):
            return "DUAL"
        return "{} %".format(int(self.to_percent(self.raw)))


class SwitchParameter(Parameter):
    """Class for storing On or Off values."""

    def __init__(
        self, parameter: Optional[Parameter] = None, state: Optional[int] = None
    ):
        """Initialize Parameter class."""
        super().__init__()
        if parameter is not None:
            self.from_parameter(parameter)
        elif state is not None:
            self.state = state

    @property
    def state(self) -> int:
        """Position property."""
        return self.to_int(self.raw)

    @state.setter
    def state(self, state: int) -> None:
        """Setter of internal raw via state."""
        self.raw = self.from_int(state)

    def set_on(self) -> None:
        """Set parameter to 'on' state."""
        self.raw = self.from_int(Parameter.ON)

    def set_off(self) -> None:
        """Set parameter to 'off' state."""
        self.raw = self.from_int(Parameter.OFF)

    def is_on(self) -> bool:
        """Return True if parameter is in 'on' state."""
        return self.raw == self.from_int(Parameter.ON)

    def is_off(self) -> bool:
        """Return True if parameter is in 'off' state."""
        return self.raw == self.from_int(Parameter.OFF)

    def __str__(self) -> str:
        """Return string representation of object."""
        if self.raw == self.from_int(Parameter.ON):
            return "ON"
        if self.raw == self.from_int(Parameter.OFF):
            return "OFF"
        return "UNKNOWN"


class SwitchParameterOn(SwitchParameter):
    """Switch Parameter in switched 'on' state."""

    def __init__(self) -> None:
        """Initialize SwitchParameterOn class."""
        super().__init__(state=Parameter.ON)


class SwitchParameterOff(SwitchParameter):
    """Switch Parameter in switched 'off' state."""

    def __init__(self) -> None:
        """Initialize SwitchParameterOff class."""
        super().__init__(state=Parameter.OFF)


class Position(Parameter):
    """Class for storing a position."""

    def __init__(
        self,
        parameter: Optional[Parameter] = None,
        position: Optional[int] = None,
        position_percent: Optional[int] = None,
    ):
        """Initialize Position class."""
        super().__init__()
        if parameter is not None:
            self.from_parameter(parameter)
        elif position is not None:
            self.position = position
        elif position_percent is not None:
            self.position_percent = position_percent

    @property
    def known(self) -> bool:
        """Known property, true if position is not in an unknown position."""
        return self.raw != self.from_int(Position.UNKNOWN_VALUE)

    @property
    def open(self) -> bool:
        """Return true if position is set to fully open."""
        return self.raw == self.from_int(Position.MIN)

    @property
    def closed(self) -> bool:
        """Return true if position is set to fully closed."""
        # Consider closed even if raw is not exactly 51200 (tolerance for devices like Velux SML)
        return self.to_percent(self.raw) == self.to_percent(self.from_int(Position.MAX))

    @property
    def position(self) -> int:
        """Position property."""
        return self.to_int(self.raw)

    @position.setter
    def position(self, position: int) -> None:
        """Setter of internal raw via position."""
        self.raw = self.from_int(position)

    @property
    def position_percent(self) -> int:
        """Position percent property."""
        # unclear why it returns a <property object> here
        return int(self.to_percent(self.raw))

    @position_percent.setter
    def position_percent(self, position_percent: int) -> None:
        """Setter of internal raw via percent position."""
        self.raw = self.from_percent(percent=position_percent)


class UnknownPosition(Position):
    """Unknown position."""

    def __init__(self) -> None:
        """Initialize UnknownPosition class."""
        super().__init__(position=Position.UNKNOWN_VALUE)


class CurrentPosition(Position):
    """Current position, used to stop devices."""

    def __init__(self) -> None:
        """Initialize CurrentPosition class."""
        super().__init__(position=Position.CURRENT)


class TargetPosition(Position):
    """Class for using a target position."""

    def __init__(self) -> None:
        """Initialize TargetPosition class."""
        super().__init__(position=Position.TARGET)


class IgnorePosition(Position):
    """The Ignore is used where a parameter in the frame is to be ignored."""

    def __init__(self) -> None:
        """Initialize CurrentPosition class."""
        super().__init__(position=Position.IGNORE)


class Intensity(Parameter):
    """Class for storing an intensity, used in DimmableDevice.

    - 0% means off
    - 100% means fully on
    """

    def __init__(
        self,
        parameter: Optional[Parameter] = None,
        intensity: Optional[int] = None,
        intensity_percent: Optional[int] = None,
    ):
        """Initialize Intensity class."""
        super().__init__()
        if parameter is not None:
            self.from_parameter(parameter)
        elif intensity is not None:
            self.intensity = intensity
        elif intensity_percent is not None:
            self.intensity_percent = intensity_percent

    @property
    def known(self) -> bool:
        """Known property, true if intensity is not in an unknown intensity."""
        return self.raw != self.from_int(Intensity.UNKNOWN_VALUE)

    @property
    def on(self) -> bool:  # pylint: disable=invalid-name
        """Intensity at maximum power (fully on)."""
        return self.raw == self.from_int(Intensity.ON)

    @property
    def off(self) -> bool:
        """Intensity off state (no power)."""
        return self.raw == self.from_int(Intensity.OFF)

    @property
    def intensity(self) -> int:
        """Intensity property."""
        return self.to_int(self.raw)

    @intensity.setter
    def intensity(self, intensity: int) -> None:
        """Setter of internal raw via intensity."""
        self.raw = self.from_int(intensity)

    @staticmethod
    def from_percent(percent: int) -> bytes:
        """Create raw value out of percent intensity.

        For Intensity, 0% = off , 100% = fully on.
        This inverts the raw value: 0% -> 200, 100% -> 0.
        """
        if not isinstance(percent, int):
            raise PyVLXException("Intensity::percent_has_to_be_int")
        if percent < 0:
            raise PyVLXException("Intensity::percent_has_to_be_positive")
        if percent > 100:
            raise PyVLXException("Intensity::percent_out_of_range")
        # Invert: 0% = off (200), 100% = on (0)
        return bytes([(100 - percent) * 2, 0])

    @staticmethod
    def to_percent(raw: bytes) -> int:
        """Create percent intensity value out of raw.

        For Intensity, raw value 0 = 100% (fully on), raw value 200 = 0% (off).
        """
        # Invert: raw 0 = 100%, raw 200 = 0%
        return int(100 - raw[0] / 2 + 0.5)

    @property
    def intensity_percent(self) -> int:
        """Intensity percent property."""
        return int(self.to_percent(self.raw))

    @intensity_percent.setter
    def intensity_percent(self, intensity_percent: int) -> None:
        """Setter of internal raw via percent intensity."""
        self.raw = self.from_percent(percent=intensity_percent)

    def __str__(self) -> str:
        """Return string representation of object."""
        if self.raw == self.from_int(Intensity.UNKNOWN_VALUE):
            return "UNKNOWN"
        if self.raw == self.from_int(Intensity.CURRENT):
            return "CURRENT"
        if self.raw == self.from_int(Intensity.TARGET):
            return "TARGET"
        if self.raw == self.from_int(Intensity.IGNORE):
            return "IGNORE"
        return "{} %".format(self.intensity_percent)


class UnknownIntensity(Intensity):
    """Unknown intensity."""

    def __init__(self) -> None:
        """Initialize UnknownIntensity class."""
        super().__init__(intensity=Intensity.UNKNOWN_VALUE)


class CurrentIntensity(Intensity):
    """Current intensity, used to stop devices."""

    def __init__(self) -> None:
        """Initialize CurrentIntensity class."""
        super().__init__(intensity=Intensity.CURRENT)


class DualRollerShutterPosition(Position):
    """Position to be provided when addressing the upper or lower curtain of a dual roller shutter by using FP1 or FP2."""

    def __init__(self) -> None:
        """Initialize CurrentPosition class."""
        super().__init__(position=Position.DUAL_SHUTTER_CURTAINS)


class LimitationTime(Parameter):
    """Class for storing limitation time for position limitation."""

    UNLIMITED = 253
    CLEAR_MASTER = 254
    CLEAR_ALL = 255

    def __init__(self,
                 parameter: Optional[Parameter] = None,
                 seconds: Optional[int] = None,
                 limit_raw: Optional[bytes] = None) -> None:
        """Initialize limitation time from seconds, bus value or another limitation time object."""
        super().__init__()
        if parameter is not None:
            self.from_parameter(parameter)
        elif limit_raw is not None:
            self.raw = limit_raw
        elif seconds is not None:
            if seconds > 7590:
                self.raw = bytes([252])
            else:
                self.raw = bytes([math.ceil(seconds / 30) - 1])
        else:
            self.raw = bytes([LimitationTime.CLEAR_MASTER])

    def __str__(self) -> str:
        """Return string representation of object."""
        if self.raw == bytes([LimitationTime.UNLIMITED]):
            return "UNLIMITED"
        if self.raw == bytes([LimitationTime.CLEAR_MASTER]):
            return "CLEAR_MASTER"
        if self.raw == bytes([LimitationTime.CLEAR_ALL]):
            return "CLEAR_ALL"
        return "{} s".format((self.raw[0] + 1) * 30)


class LimitationTimeUnlimited(LimitationTime):
    """Limitation time does not end."""

    def __init__(self) -> None:
        """Initialize object representing unlimited Time."""
        super().__init__(limit_raw=bytes([LimitationTime.UNLIMITED]))


class LimitationTimeClearMaster(LimitationTime):
    """Clear all limitation entries for this Master."""

    def __init__(self) -> None:
        """Initialize object representing clear all limits for master."""
        super().__init__(limit_raw=bytes([LimitationTime.CLEAR_MASTER]))


class LimitationTimeClearAll(LimitationTime):
    """Clear all limitation entries."""

    def __init__(self) -> None:
        """Initialize object representing clear all limits."""
        super().__init__(limit_raw=bytes([LimitationTime.CLEAR_ALL]))
