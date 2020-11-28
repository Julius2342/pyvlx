"""Unit tests for FrameGetSystemTableDataNotification."""
import unittest

from pyvlx.api.frames import FrameGetSystemTableDataNotification
from pyvlx.const import (NodeTypeWithSubtype, NodePowerMode, NodeRfSupport,
                         ActuatorTurnaroundTime, IoManufacturerId)

class TestFrameGetSystemTableDataNotification(unittest.TestCase):
    """Test class for FrameGetSystemTableDataNotification."""
    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME1 = (
        b'\x02\x00o%L\x00\x80\xdd\x01\x00\x00\x00\x01\x9cb\x99\x00\x80\xdd\x01\x00\x00\x00\x00'
    )

    EXAMPLE_FRAME2 = (
        b'\x00\x00'
    )

    def test_empty_frame_from_payload(self):
        """Test parse FrameGetSystemTableDataNotification from raw."""
        frame = FrameGetSystemTableDataNotification()
        frame.from_payload(self.EXAMPLE_FRAME2)
        self.assertTrue(isinstance(frame, FrameGetSystemTableDataNotification))
        self.assertEqual(len(frame.systemtableobjects), 0,)
        self.assertEqual(frame.numberofentry, 0)
        self.assertEqual(frame.remainingnumberofentry, 0)


    def test_frame_from_payload(self):
        """Test parse FrameGetSystemTableDataNotification from raw."""
        frame = FrameGetSystemTableDataNotification()
        frame.from_payload(self.EXAMPLE_FRAME1)
        self.assertTrue(isinstance(frame, FrameGetSystemTableDataNotification))
        self.assertEqual(frame.systemtableobjects[0].systemtableindex, 0,)
        self.assertEqual(frame.systemtableobjects[0].actuatoraddress, 7284044,)
        self.assertEqual(frame.systemtableobjects[0].actuatortype,
                         NodeTypeWithSubtype.ROLLER_SHUTTER,)
        self.assertEqual(frame.systemtableobjects[0].powersavemode,
                         NodePowerMode.LOW_POWER_MODE,)
        self.assertEqual(frame.systemtableobjects[0].iomembership, 1,)
        self.assertEqual(frame.systemtableobjects[0].rfsupport, NodeRfSupport.RF_SUPPORT,)
        self.assertEqual(frame.systemtableobjects[0].turnaroundtime, ActuatorTurnaroundTime.MS_40,)
        self.assertEqual(frame.systemtableobjects[0].iomanufacturerid, IoManufacturerId.VELUX,)
        self.assertEqual(frame.systemtableobjects[0].backbonereferencenumber, 0,)
        self.assertEqual(frame.systemtableobjects[1].systemtableindex, 1,)
        self.assertEqual(frame.systemtableobjects[1].actuatoraddress, 10248857,)
        self.assertEqual(frame.systemtableobjects[1].actuatortype,
                         NodeTypeWithSubtype.ROLLER_SHUTTER,)
        self.assertEqual(frame.systemtableobjects[1].powersavemode, NodePowerMode.LOW_POWER_MODE,)
        self.assertEqual(frame.systemtableobjects[1].iomembership, 1,)
        self.assertEqual(frame.systemtableobjects[1].rfsupport, NodeRfSupport.RF_SUPPORT,)
        self.assertEqual(frame.systemtableobjects[1].turnaroundtime, ActuatorTurnaroundTime.MS_40,)
        self.assertEqual(frame.systemtableobjects[1].iomanufacturerid, IoManufacturerId.VELUX,)
        self.assertEqual(frame.systemtableobjects[1].backbonereferencenumber, 0,)
        self.assertEqual(frame.numberofentry, 2)
        self.assertEqual(frame.remainingnumberofentry, 0)

    def test_str(self):
        """Test string representation of FrameGetSystemTableDataNotification."""
        frame = FrameGetSystemTableDataNotification()
        frame.from_payload(self.EXAMPLE_FRAME1)
        self.assertEqual(
            str(frame),
            '<FrameGetSystemTableDataNotification numberofentry="2" remainingnumberofentry="0">'
            '<systemtableobjects>'
            '<DtoSystemTableEntry systemtableindex="0" actuatoraddress="7284044" '
            'actuatortype="NodeTypeWithSubtype.ROLLER_SHUTTER" '
            'powersavemode="NodePowerMode.LOW_POWER_MODE" '
            'iomembership="1" rfsupport="NodeRfSupport.RF_SUPPORT" '
            'turnaroundtime="ActuatorTurnaroundTime.MS_40" '
            'iomanufacturerid="IoManufacturerId.VELUX" backbonereferencenumber="0"/>'
            '<DtoSystemTableEntry systemtableindex="1" actuatoraddress="10248857" '
            'actuatortype="NodeTypeWithSubtype.ROLLER_SHUTTER" '
            'powersavemode="NodePowerMode.LOW_POWER_MODE" '
            'iomembership="1" rfsupport="NodeRfSupport.RF_SUPPORT" '
            'turnaroundtime="ActuatorTurnaroundTime.MS_40" '
            'iomanufacturerid="IoManufacturerId.VELUX" backbonereferencenumber="0"/>'
            '</systemtableobjects><FrameGetSystemTableDataNotification/>',
        )
