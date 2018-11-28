"""Module for storing alias array."""
from .exception import PyVLXException


class AliasArray():
    """Object for storing alias array."""

    def __init__(self, raw=None):
        """Initialize alias array."""
        self.alias_array_ = []
        if raw is not None:
            self.parse_raw(raw)

    def __str__(self):
        """Return human readable string."""
        return ", ".join("{:02x}{:02x}={:02x}{:02x}".format(c[0][0], c[0][1], c[1][0], c[1][1]) for c in self.alias_array_)

    def __bytes__(self):
        """Get raw bytes of alias array."""
        ret = bytes([len(self.alias_array_)])
        for alias in self.alias_array_:
            ret += alias[0] + alias[1]
        ret += bytes((5-len(self.alias_array_))*4)
        return ret

    def parse_raw(self, raw):
        """Parse alias array from raw bytes."""
        if not isinstance(raw, bytes):
            raise PyVLXException("AliasArray::invalid_type_if_raw", type_raw=type(raw))
        if len(raw) != 21:
            raise PyVLXException("AliasArray::invalid_size", size=len(raw))
        nbr_of_alias = raw[0]
        if nbr_of_alias > 5:
            raise PyVLXException("AliasArray::invalid_nbr_of_alias", nbr_of_alias=nbr_of_alias)
        for i in range(0, nbr_of_alias):
            self.alias_array_.append((raw[i*4+1:i*4+3], raw[i*4+3:i*4+5]))
