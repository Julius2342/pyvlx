"""Module for string encoding, decoding."""
from .exception import PyVLXException


def string_to_bytes(string, size):
    """Convert string to bytes add padding."""
    if len(string) > size:
        raise PyVLXException("string_to_bytes::string_to_large")
    encoded = bytes(string, encoding='utf-8')
    return encoded + bytes(size-len(encoded))


def bytes_to_string(raw):
    """Convert bytes to string."""
    ret = bytes()
    for byte in raw:
        if byte == 0x00:
            return ret.decode("utf-8")
        ret += bytes([byte])
    return ret.decode("utf-8")
