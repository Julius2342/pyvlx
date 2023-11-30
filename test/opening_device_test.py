"""Unit test for roller shutter."""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from pyvlx import (
    Awning, Blade, Blind, OpeningDevice, Parameter, Position, RollerShutter,
    Window)


# pylint: disable=too-many-public-methods,invalid-name
class TestOpeningDevice(IsolatedAsyncioTestCase):
    """Test class for roller shutter."""

    @patch("pyvlx.api.CommandSend.send", new_callable=AsyncMock)
    @patch("pyvlx.Node.after_update", new_callable=AsyncMock)
    async def test_set_position(self, commandSend: AsyncMock, afterUpdate: AsyncMock) -> None:
        """Test set_position of OpeningDevice object."""
        test_device = OpeningDevice(pyvlx="PyVLX", node_id=23, name="Test device", serial_number=None)
        await test_device.set_position(position=Position(position_percent=100))
        assert commandSend.called
        assert afterUpdate.called

    def test_window_str(self) -> None:
        """Test string representation of Window object."""
        pyvlx = MagicMock()
        window = Window(
            pyvlx=pyvlx,
            node_id=23,
            name="Test Window",
            rain_sensor=True,
            serial_number="aa:bb:aa:bb:aa:bb:aa:23",
        )
        self.assertEqual(
            str(window),
            '<Window name="Test Window" node_id="23" rain_sensor=True serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="UNKNOWN"/>',
        )

    def test_blind_str(self) -> None:
        """Test string representation of Blind object."""
        pyvlx = MagicMock()
        blind = Blind(
            pyvlx=pyvlx,
            node_id=23,
            name="Test Blind",
            serial_number="aa:bb:aa:bb:aa:bb:aa:23",
        )
        self.assertEqual(
            str(blind),
            '<Blind name="Test Blind" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="UNKNOWN"/>',
        )

    def test_roller_shutter_str(self) -> None:
        """Test string representation of RolllerShutter object."""
        pyvlx = MagicMock()
        roller_shutter = RollerShutter(
            pyvlx=pyvlx,
            node_id=23,
            name="Test Roller Shutter",
            serial_number="aa:bb:aa:bb:aa:bb:aa:23",
            position_parameter=Parameter(Parameter.from_int(int(0.97 * Parameter.MAX))),
        )
        self.assertEqual(
            str(roller_shutter),
            '<RollerShutter name="Test Roller Shutter" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="97 %"/>',
        )

    def test_blade_str(self) -> None:
        """Test string representation of Blade object."""
        pyvlx = MagicMock()
        blade = Blade(
            pyvlx=pyvlx,
            node_id=23,
            name="Test Blade",
            serial_number="aa:bb:aa:bb:aa:bb:aa:23",
        )
        self.assertEqual(
            str(blade),
            '<Blade name="Test Blade" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="UNKNOWN"/>',
        )

    def test_awning_str(self) -> None:
        """Test string representation of Awning object."""
        pyvlx = MagicMock()
        awning = Awning(
            pyvlx=pyvlx,
            node_id=23,
            name="Test Awning",
            serial_number="aa:bb:aa:bb:aa:bb:aa:23",
        )
        self.assertEqual(
            str(awning),
            '<Awning name="Test Awning" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="UNKNOWN"/>',
        )

    def test_eq(self) -> None:
        """Testing eq method with positive results."""
        pyvlx = MagicMock()
        node1 = Blind(
            pyvlx=pyvlx, node_id=23, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        node2 = Blind(
            pyvlx=pyvlx, node_id=23, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        self.assertEqual(node1, node2)

    def test_nq(self) -> None:
        """Testing eq method with negative results."""
        pyvlx = MagicMock()
        node1 = Blind(
            pyvlx=pyvlx, node_id=23, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        node2 = Blind(
            pyvlx=pyvlx, node_id=24, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:24"
        )
        node3 = RollerShutter(
            pyvlx=pyvlx, node_id=23, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node1)
