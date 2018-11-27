"""Unit tests string_helper module."""
import unittest

from pyvlx.exception import PyVLXException
from pyvlx.string_helper import bytes_to_string, string_to_bytes


class TestString(unittest.TestCase):
    """Test class for String encoding/decoding."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_encoding(self):
        """Test simple encoding."""
        self.assertEqual(string_to_bytes('fnord', 10), b'fnord' + bytes(5))

    def test_encoding_without_padding(self):
        """Test encoding with exact match of size."""
        self.assertEqual(string_to_bytes('fnord', 5), b'fnord')

    def test_encoding_failure(self):
        """Test error while encoding."""
        with self.assertRaises(PyVLXException):
            string_to_bytes('fnord', 4)

    def test_decoding(self):
        """Test decoding of string."""
        self.assertEqual(bytes_to_string(b'fnord' + bytes(5)), 'fnord')

    def test_decoding_without_padding(self):
        """Test decoding of string without padding."""
        self.assertEqual(bytes_to_string(b'fnord'), 'fnord')
