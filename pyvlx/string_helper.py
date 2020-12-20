"""Module for string encoding, decoding."""
from .exception import PyVLXException


def string_to_bytes(string, size):
    """Convert string to bytes add padding."""
    if len(string) > size:
        raise PyVLXException("string_to_bytes::string_to_large")
    encoded = bytes(string, encoding="utf-8")
    return encoded + bytes(size - len(encoded))


def bytes_to_string(raw):
    """Convert bytes to string."""
    ret = bytes()
    for byte in raw:
        if byte == 0x00:
            return ret.decode("utf-8")
        ret += bytes([byte])
    return ret.decode("utf-8")

def bytes_from_statusflags(flaglist, length):
    """Returns binary Coded list of flags
    Least significant bit in first byte holds information
    of the actuator node with index 0"""
    payload = b''
    for targetbyte in range(0, length):
        i = 0
        for targetbit in range(0, 8):
            if targetbyte*8 + targetbit in flaglist:
                i |= (1<<targetbit)
        payload = payload + i.to_bytes(1, "big")
    return payload

def statusflags_from_bytes(payload):
    """Extracts Status Flags form binary Coded list
    Least significant bit in first byte holds information
    of the actuator node with index 0"""
    #XXX: bitbanging to be improved

    flaglist = []
    for index, item in enumerate(payload):
        if item & 0x01:
            flaglist.append(index * 8)
        if item & 0x02:
            flaglist.append(index * 8 + 1)
        if item & 0x04:
            flaglist.append(index * 8 + 2)
        if item & 0x08:
            flaglist.append(index * 8 + 3)
        if item & 0x10:
            flaglist.append(index * 8 + 4)
        if item & 0x20:
            flaglist.append(index * 8 + 5)
        if item & 0x40:
            flaglist.append(index * 8 + 6)
        if item & 0x80:
            flaglist.append(index * 8 + 7)
    return flaglist
