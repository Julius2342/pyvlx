"""Test for slip helper functions."""
import unittest
from typing import Any

from pyvlx.slip import decode, encode, get_next_slip, is_slip, slip_pack


class TestSlip(unittest.TestCase):
    """Test class for slip helper functions."""

    # pylint: disable=invalid-name

    def encode_decode(self, decoded: Any, encoded: Any) -> None:
        """Decode encoded, encode decoded and test results."""
        self.assertEqual(decode(encoded), decoded)
        self.assertEqual(encode(decoded), encoded)

    def test_simple(self) -> None:
        """Test decode and encode."""
        self.encode_decode(
            b"\xc0\xc0\xdb\xdb\xc0\xdb\xc0",
            b"\xdb\xdc\xdb\xdc\xdb\xdd\xdb\xdd\xdb\xdc\xdb\xdd\xdb\xdc",
        )

    def test_empty(self) -> None:
        """Test decode and  encode of empty string."""
        self.encode_decode(b"", b"")

    def test_real_live_example(self) -> None:
        """Test decode of real live example."""
        self.encode_decode(
            b"\x00\x10\x03\x02\x00\x01\x01\x00\x00\xc8\x00\x02\x1e\x06\x00\x03\x00\xc0",
            b"\x00\x10\x03\x02\x00\x01\x01\x00\x00\xc8\x00\x02\x1e\x06\x00\x03\x00\xdb\xdc",
        )

    def test_slip(self) -> None:
        """Test is_slip function."""
        self.assertTrue(is_slip(b"\xc0abc\xc0xx"))
        self.assertFalse(is_slip(b"zz\xc0abc\xc0"))
        self.assertFalse(is_slip(b"\xc0abc"))
        self.assertFalse(is_slip(b"\xc0"))

    def test_slip_pack(self) -> None:
        """Test slip_pack function."""
        self.assertEqual(
            slip_pack(b"\xc0\xc0\xdb\xdb\xc0\xdb\xc0"),
            b"\xc0\xdb\xdc\xdb\xdc\xdb\xdd\xdb\xdd\xdb\xdc\xdb\xdd\xdb\xdc\xc0",
        )

    def test_get_next_slip(self) -> None:
        """Test get_next_slip function."""
        self.assertEqual(
            get_next_slip(
                b"\xc0\xdb\xdc\xdb\xdc\xdb\xdd\xdb\xdd\xdb\xdc\xdb\xdd\xdb\xdc\xc0fnord"
            ),
            (b"\xc0\xc0\xdb\xdb\xc0\xdb\xc0", b"fnord"),
        )

    def test_get_next_slip_no_complete_slip(self) -> None:
        """Test get_next_slip function with no complete slip frame beeing in queue."""
        self.assertEqual(get_next_slip(b"zz\xc0abc\xc0"), (None, b"zz\xc0abc\xc0"))

    def test_get_next_slip_empty_queue(self) -> None:
        """Test get_next_slip function with empty queue."""
        self.assertEqual(get_next_slip(b""), (None, b""))
