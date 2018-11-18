"""Module for string encoding, decoding."""
from .exception import PyVLXException


def string_to_bytes(string, size):
    """Convert string to bytes add padding."""
    if len(string) > size:
        raise PyVLXException("string_to_bytes::string_to_large")
    return bytes(string, encoding='ascii') \
        + bytes(size-len(string))


def bytes_to_string(raw):
    """Convert bytes to string."""
    ret = str()
    for byte in raw:
        if byte == 0x00:
            return ret
        ret += chr(byte)
    return ret
