"""Unit tests for frame module."""
import unittest

from pyvlx import PyVLXException
from pyvlx.api.frames.frame import FrameBase
from pyvlx.const import Command


class TestFrame(unittest.TestCase):
    """Test class FrameBase class."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_validate_payload_len_no_payload_len_defined(self):
        """Test validate_payload_len_function without any PAYLOAD_LEN defined."""
        frame = FrameBase(command=Command.GW_GET_NODE_INFORMATION_REQ)
        frame.validate_payload_len(bytes(23))

    def test_validate_payload_len_payload_len_defined(self):
        """Test validate_payload_len_function with defined PAYLOAD_LEN."""
        frame = FrameBase(command=Command.GW_GET_NODE_INFORMATION_REQ)
        # pylint: disable=invalid-name
        frame.PAYLOAD_LEN = 23
        frame.validate_payload_len(bytes(23))

    def test_validate_payload_len_payload_len_error(self):
        """Test validate_payload_len_function with wrong PAYLOAD_LEN."""
        frame = FrameBase(command=Command.GW_GET_NODE_INFORMATION_REQ)
        frame.PAYLOAD_LEN = 42
        with self.assertRaises(PyVLXException):
            frame.validate_payload_len(bytes(23))
