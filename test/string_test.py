"""Unit tests string_helper module."""
import unittest

from pyvlx.exception import PyVLXException
from pyvlx.string_helper import bytes_to_string, string_to_bytes


class TestString(unittest.TestCase):
    """Test class for String encoding/decoding."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_encoding(self) -> None:
        """Test simple encoding."""
        self.assertEqual(string_to_bytes("fnord", 10), b"fnord" + bytes(5))

    def test_encoding_without_padding(self) -> None:
        """Test encoding with exact match of size."""
        self.assertEqual(string_to_bytes("fnord", 5), b"fnord")

    def test_encoding_failure(self) -> None:
        """Test error while encoding."""
        with self.assertRaises(PyVLXException):
            string_to_bytes("fnord", 4)

    def test_decoding(self) -> None:
        """Test decoding of string."""
        self.assertEqual(bytes_to_string(b"fnord" + bytes(5)), "fnord")

    def test_decoding_without_padding(self) -> None:
        """Test decoding of string without padding."""
        self.assertEqual(bytes_to_string(b"fnord"), "fnord")

    def test_encode_utf8(self) -> None:
        """Test encoding a string with special characters."""
        self.assertEqual(
            string_to_bytes("Fenster Büro", 16), b"Fenster B\xc3\xbcro\x00\x00\x00"
        )

    def test_decode_utf8(self) -> None:
        """Test decoding a string with special characters."""
        self.assertEqual(
            bytes_to_string(b"Fenster B\xc3\xbcro\x00\x00\x00"), "Fenster Büro"
        )
