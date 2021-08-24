"""Unit tests for FrameGetNetworkSetupConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import DHCPParameter, FrameGetNetworkSetupConfirmation


class TestFrameGetNetworkSetupConfirmation(unittest.TestCase):
    """Test class for FrameGetNetworkSetupConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name
    TESTFRAME = bytes.fromhex('001000e1c0a80de3ffffff00c0a80d0100ec')

    def test_bytes(self):
        """Test FrameGetNetworkSetupConfirmation."""
        frame = FrameGetNetworkSetupConfirmation(
            ipaddress=b'\xc0\xa8\r\xe3', netmask=b'\xff\xff\xff\x00',
            gateway=b'\xc0\xa8\r\x01', dhcp=DHCPParameter.ENABLE)
        self.assertEqual(bytes(frame),
                         b"\x00\x10\x00\xe1\xc0\xa8\r\xe3\xff\xff\xff\x00\xc0\xa8\r\x01\x00\xec")

    def test_frame_from_raw(self):
        """Test parse FrameGetNetworkSetupConfirmation from raw."""
        frame = frame_from_raw(self.TESTFRAME)
        self.assertTrue(isinstance(frame, FrameGetNetworkSetupConfirmation))
        self.assertEqual(frame.ipaddress, '192.168.13.227')
        self.assertEqual(frame.netmask, '255.255.255.0')
        self.assertEqual(frame.gateway, '192.168.13.1')
        self.assertEqual(frame.dhcp, DHCPParameter.DISABLE)

    def test_str(self):
        """Test string representation of FrameGetNetworkSetupConfirmation."""
        frame = FrameGetNetworkSetupConfirmation(
            ipaddress=b'\xc0\xa8\r\xe3', netmask=b'\xff\xff\xff\x00',
            gateway=b'\xc0\xa8\r\x01', dhcp=DHCPParameter.DISABLE)
        self.assertEqual(
            str(frame),
            '<FrameGetNetworkSetupConfirmation ipaddress="192.168.13.227" '
            'netmask="255.255.255.0" gateway="192.168.13.1" dhcp="DHCPParameter.DISABLE"/>',
        )
