"""Module for get system table from gateway."""
from ...const import (Command, NodeTypeWithSubtype, NodePowerMode,
                      NodeRfSupport, ActuatorTurnaroundTime, IoManufacturerId)

from ...exception import PyVLXException

from .frame import FrameBase


class FrameGetSystemTableUpdateNotification(FrameBase):
    """Frame for Notifications of System Table."""

    PAYLOAD_LEN = 52

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_CS_SYSTEM_TABLE_UPDATE_NTF)
        self.addednodeids = []
        self.removednodeids = []

    def get_payload(self):
        """Return Payload."""
        #XXX: bitbanging to be improved
        payload = b''
        for targetbyte in range(0, 26):
            i = 0
            for targetbit in range(0, 8):
                if targetbyte*8 + targetbit in self.addednodeids:
                    i |= (1<<targetbit)
            payload = payload + i.to_bytes(1, "big")
        for targetbyte in range(0, 26):
            i = 0
            for targetbit in range(0, 8):
                if targetbyte*8 + targetbit in self.removednodeids:
                    i |= (1<<targetbit)
            payload = payload + i.to_bytes(1, "big")
        return payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        #XXX: bitbanging to be improved
        for index, item in enumerate(payload[:26]):
            if item & 0x01:
                self.addednodeids.append(index * 8)
            if item & 0x02:
                self.addednodeids.append(index * 8 + 1)
            if item & 0x04:
                self.addednodeids.append(index * 8 + 2)
            if item & 0x08:
                self.addednodeids.append(index * 8 + 3)
            if item & 0x10:
                self.addednodeids.append(index * 8 + 4)
            if item & 0x20:
                self.addednodeids.append(index * 8 + 5)
            if item & 0x40:
                self.addednodeids.append(index * 8 + 6)
            if item & 0x80:
                self.addednodeids.append(index * 8 + 7)

        for index, item in enumerate(payload[26:]):
            if item & 0x01:
                self.removednodeids.append(index * 8)
            if item & 0x02:
                self.removednodeids.append(index * 8 + 1)
            if item & 0x04:
                self.removednodeids.append(index * 8 + 2)
            if item & 0x08:
                self.removednodeids.append(index * 8 + 3)
            if item & 0x10:
                self.removednodeids.append(index * 8 + 4)
            if item & 0x20:
                self.removednodeids.append(index * 8 + 5)
            if item & 0x40:
                self.removednodeids.append(index * 8 + 6)
            if item & 0x80:
                self.removednodeids.append(index * 8 + 7)

    def __str__(self):
        """Return human readable string."""
        return '<{} addednodeids="{}" removednodeids="{}"/>'.format(
            type(self).__name__, self.addednodeids, self.removednodeids)


class FrameGetSystemTableDataRequest(FrameBase):
    """Frame for get system Table request."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_CS_GET_SYSTEMTABLE_DATA_REQ)

    def __str__(self):
        """Return human readable string."""
        return '<{}/>'.format(type(self).__name__)



class FrameGetSystemTableDataConfirmation(FrameBase):
    """Frame for confirmation for node information request."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_CS_GET_SYSTEMTABLE_DATA_CFM)

    def __str__(self):
        """Return human readable string."""
        return '<{}/>'.format(type(self).__name__)


class DtoSystemTableEntry:
    """Object for System Table Entry Data"""

    def __init__(self,
                 systemtableindex=None, actuatoraddress=None, actuatortype=None,
                 powersavemode=None, iomembership=None,
                 rfsupport=None, turnaroundtime=None,
                 iomanufacturerid=None, backbonereferencenumber=None):
        """Initialize DtoVersion class."""
        self.systemtableindex = systemtableindex
        self.actuatoraddress = actuatoraddress
        self.actuatortype = actuatortype
        self.powersavemode = powersavemode
        self.iomembership = iomembership
        self.rfsupport = rfsupport
        self.turnaroundtime = turnaroundtime
        self.iomanufacturerid = iomanufacturerid
        self.backbonereferencenumber = backbonereferencenumber

    def from_payload(self, payload):
        """Init Data Object from binary data."""
        self.systemtableindex = payload[0]
        self.actuatoraddress = payload[1] * 256 * 256 + payload[2] * 256 + payload[3]
        self.actuatortype = NodeTypeWithSubtype(payload[4] * 256 + payload[5])
        self.powersavemode = NodePowerMode(payload[6] & 0x03)
        self.iomembership = (payload[6] & 0x04) >> 2
        self.rfsupport = NodeRfSupport((payload[6] & 0x08) >> 3)
        self.turnaroundtime = ActuatorTurnaroundTime((payload[6] & 0xC0) >> 6)
        self.iomanufacturerid = IoManufacturerId(payload[7])
        self.backbonereferencenumber = payload[8] * 256 * 256 + payload[9] * 256 + payload[10]

    def get_payload(self):
        """Return Payload."""
        payload = bytes(self.systemtableindex)
        payload += self.actuatoraddress.to_bytes(3, 'big')
        payload += bytes(self.actuatortype.value)
        payload += (bytes(self.powersavemode.value) | bytes(self.iomembership << 2) |
                    bytes(self.rfsupport.value << 3) | bytes(self.turnaroundtime.value << 6))
        payload += bytes(self.iomanufacturerid.value)
        payload += self.backbonereferencenumber.to_bytes(3, 'big')
        return payload

    def __str__(self):
        """Return human readable string."""
        return (
            '<{} systemtableindex="{}" actuatoraddress="{}" actuatortype="{}" '
            'powersavemode="{}" iomembership="{}" rfsupport="{}" '
            'turnaroundtime="{}" iomanufacturerid="{}" backbonereferencenumber="{}"/>'.format(
                type(self).__name__, self.systemtableindex, self.actuatoraddress,
                self.actuatortype, self.powersavemode, self.iomembership,
                self.rfsupport, self.turnaroundtime, self.iomanufacturerid,
                self.backbonereferencenumber
            )
        )

class FrameGetSystemTableDataNotification(FrameBase):
    """Frame for notification of node information request."""

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_CS_GET_SYSTEMTABLE_DATA_NTF)
        self.systemtableobjects = []
        self.numberofentry = len(self.systemtableobjects)
        self.remainingnumberofentry = 0

    def get_payload(self):
        """Return Payload."""
        payload = bytes([len(self.systemtableobjects)])
        for systemtableobject in self.systemtableobjects:
            payload += systemtableobject.get_payload()
        payload += bytes([self.remainingnumberofentry])
        return payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        number_of_objects = payload[0]

        predicted_len = number_of_objects * 11 + 2
        if len(payload) != predicted_len:
            raise PyVLXException("system_table_notification_wrong_length")
        self.numberofentry = number_of_objects
        self.remainingnumberofentry = payload[-1]
        self.systemtableobjects = []
        for i in range(number_of_objects):
            entry = payload[(i * 11 + 1) : (i * 11 + 12)]
            obj = DtoSystemTableEntry()
            obj.from_payload(entry)
            self.systemtableobjects.append(obj)

    def __str__(self):
        """Return human readable string."""
        return (
            '<{0} numberofentry="{1}" remainingnumberofentry="{2}">'
            '<systemtableobjects>{3}</systemtableobjects>'
            '<{0}/>'.format(
                type(self).__name__,
                self.numberofentry,
                self.remainingnumberofentry,
                '%s' % ''.join(map(str, self.systemtableobjects))
            )
        )
