"""Unit tests for AliasArray module."""
import unittest

from pyvlx.api.frames.alias_array import AliasArray
from pyvlx.exception import PyVLXException


class TestAliasArray(unittest.TestCase):
    """Test class for AliasArray."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_empty(self) -> None:
        """Test empty alias array."""
        alias_array = AliasArray()
        self.assertEqual(bytes(alias_array), bytes(21))
        self.assertEqual(str(alias_array), "")

    def test_empty_raw(self) -> None:
        """Test empty alias array initialized from raw."""
        alias_array = AliasArray(raw=bytes(21))
        self.assertEqual(bytes(alias_array), bytes(21))
        self.assertEqual(str(alias_array), "")

    def test_from_one_element(self) -> None:
        """Test alias_array with one element."""
        alias_array = AliasArray(raw=b"\x01abcd" + bytes(16))
        self.assertEqual(bytes(alias_array), b"\x01abcd" + bytes(16))
        self.assertEqual(str(alias_array), "6162=6364")

    def test_from_four_elements(self) -> None:
        """Test alias_array with one element."""
        alias_array = AliasArray(raw=b"\x05abcd1234efgh5678ijkl")
        self.assertEqual(bytes(alias_array), b"\x05abcd1234efgh5678ijkl")
        self.assertEqual(
            str(alias_array), "6162=6364, 3132=3334, 6566=6768, 3536=3738, 696a=6b6c"
        )

    def test_deserialize_failure(self) -> None:
        """Test error while deserializing."""
        with self.assertRaises(PyVLXException):
            AliasArray(raw="string")  # type: ignore[arg-type]
        with self.assertRaises(PyVLXException):
            AliasArray(raw=bytes(20))
        with self.assertRaises(PyVLXException):
            AliasArray(raw=b"\x06" + bytes(20))
