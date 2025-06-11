"""Frames for receiving system table from gateway."""
from pyvlx.actuator import Actuator
from pyvlx.const import (
    Command, Manufactor, NodeTypeWithSubtype, PowerMode, TurnAround)
from pyvlx.exception import PyVLXException

from .frame import FrameBase


class FrameGetSystemTableRequest(FrameBase):
    """Frame for requesting system table."""

    PAYLOAD_LEN = 0

    def __init__(self) -> None:
        """Init Frame."""
        super().__init__(Command.GW_CS_GET_SYSTEMTABLE_DATA_REQ)

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{}/>'.format(type(self).__name__)


class FrameGetSystemTableConfirmation(FrameBase):
    """Frame for confirmation for system table request."""

    PAYLOAD_LEN = 0

    def __init__(self) -> None:
        """Init Frame."""
        super().__init__(Command.GW_CS_GET_SYSTEMTABLE_DATA_CFM)

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{}/>'.format(type(self).__name__)


class ActuatorList(list):
    """a useless class for MyPy."""

    def __init__(self, init: list[Actuator]) -> None:
        """Init a list."""
        self.acts: list[Actuator] = init

    def __getitem__(self, key: int) -> Actuator:  # type: ignore[override]
        """Get an item."""
        return super().__getitem__(key)

    def __setitem__(self, key: int, value: Actuator) -> None:  # type: ignore[override]
        """Set an item."""
        self.acts[key] = value


class FrameGetSystemTableNotification(FrameBase):
    """Frame for scene list notification."""

    def __init__(self) -> None:
        """Init Frame."""
        super().__init__(Command.GW_CS_GET_SYSTEMTABLE_DATA_NTF)
        self.actuators = ActuatorList([])
        self.remaining_objects = 0

    def get_payload(self) -> bytes:
        """Return Payload."""
        # TODO Paquet are limited to 200 bytes so KLF200 would never send more that 10 entries at once
        ret = bytes([len(self.actuators)])
        for i in self.actuators:
            ret += bytes(self.actuators[i].idx)
            ret += self.actuators[i].address
            ret += bytes(self.actuators[i].subtype.value)
            ret += bytes(self.actuators[i].turn_around_time.value + self.actuators[i].rf * 16
                         + self.actuators[i].io * 32 + self.actuators[i].power_save_mode.value * 64)
            ret += bytes(self.actuators[i].manufactor.value)
            ret += self.actuators[i].backbone
        ret += bytes([self.remaining_objects])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        number_of_objects = payload[0]
        predicted_len = number_of_objects * 11 + 2
        if len(payload) != predicted_len:
            raise PyVLXException("system_objects_notification_wrong_length")
        self.remaining_objects = payload[number_of_objects * 11 + 1]
        for i in range(number_of_objects):
            self.actuators.append(Actuator(
                payload[(i * 11 + 1)],
                payload[(i * 11 + 2) : (i * 11 + 5)],
                NodeTypeWithSubtype(int.from_bytes(payload[(i * 11 + 5) : (i * 11 + 7)])) ,
                PowerMode(payload[(i * 11 + 7)] >> 6 & 3),  # bit 0-1 power_save_mode
                bool(payload[(i * 11 + 7)] >> 5 & 1),       # bit2 io membership
                bool(payload[(i * 11 + 7)] >> 4 & 1),       # bit3 rf support
                                                            # bit4-5 reserved
                TurnAround(payload[(i * 11 + 7)] % 4),      # bit6-7 actuatortime
                Manufactor(payload[(i * 11 + 8)]),
                payload[(i * 11 + 9) : (i * 11 + 12)]
            ))

    def __str__(self) -> str:
        """Return human readable string."""
        ret = '<FrameGetSystemTableNotification objects="{}" remaining_objects="{}">'.format(
            len(self.actuators), self.remaining_objects
        )
        for actuator in self.actuators :
            ret += str(actuator)
        return ret + "</FrameGetSystemTableNotification>"
