"""Frames for receiving system table from gateway."""
from pyvlx.actutator import Actutator
from pyvlx.const import (Command, Manufactor, NodeTypeWithSubtype, PowerMode, TurnAround )
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

class FrameGetSystemTableNotification(FrameBase):
    """Frame for scene list notification."""

    def __init__(self) -> None:
        """Init Frame."""
        super().__init__(Command.GW_CS_GET_SYSTEMTABLE_DATA_NTF)
        self.actutators = []
        self.remaining_objects = 0

    def get_payload(self) -> bytes:
        """Return Payload."""
        #TODO Paquet are limited to 200 bytes so KLF200 would never send more that 10 entries at once
        ret = bytes([len(self.actutators)])
        for i in self.actutators:
            ret += self.actutators[i].idx
            ret += self.actutators[i].address
            ret += self.actutators[i].subtype
            ret += (self.actutators[i].turn_around_time + self.actutators[i].rf * 16
                 + self.actutators[i].io * 32 + self.actutators[i].power_save_mode * 64)
            ret += self.actutators[i].manufactor
            ret += self.actutators[i].backbone
        ret += bytes([self.remaining_objects])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        number_of_objects = payload[0]
        predicted_len = number_of_objects * 11 + 2
        if len(payload) != predicted_len:
            raise PyVLXException("system_objects_notification_wrong_length")
        self.remaining_objects = payload[number_of_objects * 11 + 1 ]
        self.actutators = []
        for i in range(number_of_objects):
            self.actutators.append(Actutator(
                payload[(i * 11 + 1)],
                payload[(i * 11 + 2) : (i * 11 + 5)],
                NodeTypeWithSubtype( int.from_bytes( payload[(i * 11 + 5) : (i * 11 + 7)] ) ) ,
                PowerMode( payload[(i * 11 + 7)] >> 6 & 3 ), #bit 0-1 power_save_mode
                payload[(i * 11 + 7)] >> 5 & 1,              #bit2 io membership
                payload[(i * 11 + 7)] >> 4 & 1,              #bit3 rf support
                                                             #bit4-5 reserved
                TurnAround( payload[(i * 11 + 7)] % 4 ),     #bit6-7 actutatortime
                Manufactor( payload[(i * 11 + 8)] ),
                payload[(i * 11 + 9) : (i * 11 + 12)]
            ))

    def __str__(self) -> str:
        """Return human readable string."""
        ret = '<FrameGetSystemTableNotification objects="{}" remaining_objects="{}">'.format(
            len(self.actutators), self.remaining_objects
        )
        for actutator in self.actutators :
            ret += str(actutator)
        return ret + "</FrameGetSystemTableNotification>"
