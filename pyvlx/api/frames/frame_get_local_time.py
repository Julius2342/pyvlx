"""Module for get local time classes."""
import struct
from ...const import Command
from .frame import FrameBase


class FrameGetLocalTimeRequest(FrameBase):
    """Frame for requesting local time."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_LOCAL_TIME_REQ)


class FrameGetLocalTimeConfirmation(FrameBase):
    """Frame for response for get local time requests."""

    PAYLOAD_LEN = 15

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_LOCAL_TIME_CFM)
        self.utctime = 0
        self.second = 0
        self.minute = 0
        self.hour = 0
        self.dayofmonth = 0
        self.month = 0
        self.year = 0
        self.weekday = 0
        self.dayofyear = 0
        self.daylightsavingflag = 0

    def get_payload(self):
        """Return Payload."""
        payload = struct.pack(">I", self.utctime)
        payload += self.second.to_bytes(1, byteorder="big")
        payload += self.minute.to_bytes(1, byteorder="big")
        payload += self.hour.to_bytes(1, byteorder="big")
        payload += self.dayofmonth.to_bytes(1, byteorder="big")
        payload += self.month.to_bytes(1, byteorder="big")
        payload += self.year.to_bytes(2, byteorder="big")
        payload += self.weekday.to_bytes(1, byteorder="big")
        payload += self.dayofyear.to_bytes(2, byteorder="big")
        payload += self.daylightsavingflag.to_bytes(1, byteorder="big")
        return payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.utctime = struct.unpack(">I", payload[0:4])[0]
        self.second = payload[4]
        self.minute = payload[5]
        self.hour = payload[6]
        self.dayofmonth = payload[7]
        self.month = payload[8]
        self.year = int.from_bytes(payload[9:11], byteorder='big', signed=True)
        self.weekday = payload[11]
        self.dayofyear = int.from_bytes(payload[12:14], byteorder='big', signed=True)
        self.daylightsavingflag = int.from_bytes(payload[14:15], byteorder='big', signed=True)

    def __str__(self):
        """Return human readable string."""
        return ('<{} utctime="{}" second="{}" minute="{}" hour="{}" dayofmonth="{}" '
                'month="{}" year="{}" weekday="{}" dayofyear="{}" daylightsavingflag="{}"/>'.format(
                    type(self).__name__, self.utctime, self.second, self.minute, self.hour,
                    self.dayofmonth, self.month, self.year, self.weekday, self.dayofyear,
                    self.daylightsavingflag))
