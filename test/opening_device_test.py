"""Unit test for roller shutter."""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from pyvlx import (
    Awning, Blade, Blind, CurrentPosition, OpeningDevice, Parameter, Position,
    PyVLX, RollerShutter, Window)
from pyvlx.connection import Connection
from pyvlx.const import LimitationTime, LimitationType, Velocity
from pyvlx.parameter import IgnorePosition


# pylint: disable=too-many-public-methods,invalid-name
class TestOpeningDevice(IsolatedAsyncioTestCase):
    """Test class for roller shutter."""

    mocked_pyvlx = MagicMock(spec=PyVLX)
    connection = MagicMock(spec=Connection)
    mocked_pyvlx.attach_mock(mock=connection, attribute="connection")

    @patch("pyvlx.api.CommandSend.send", new_callable=AsyncMock)
    @patch("pyvlx.Node.after_update", new_callable=AsyncMock)
    async def test_set_position(self, commandSend: AsyncMock, afterUpdate: AsyncMock) -> None:
        """Test set_position of OpeningDevice object."""
        opening_device = OpeningDevice(pyvlx=self.mocked_pyvlx, node_id=23, name="Test device")
        await opening_device.set_position(position=Position(position_percent=100))
        assert commandSend.called
        assert afterUpdate.called

    @patch("pyvlx.opening_device.OpeningDevice.set_position", new_callable=AsyncMock)
    async def test_open(self, set_position: AsyncMock) -> None:
        """Test open function of OpeningDevice object."""
        opening_device = OpeningDevice(pyvlx=self.mocked_pyvlx, node_id=23, name="Test device")
        velocity = Velocity.DEFAULT
        wait_for_completion = False
        await opening_device.open(velocity=velocity, wait_for_completion=wait_for_completion)
        set_position.assert_awaited_once_with(
            position=Position(position_percent=opening_device.open_position_target),
            velocity=velocity,
            wait_for_completion=wait_for_completion)

    @patch("pyvlx.opening_device.OpeningDevice.set_position", new_callable=AsyncMock)
    async def test_close(self, set_position: AsyncMock) -> None:
        """Test close function of OpeningDevice object."""
        opening_device = OpeningDevice(pyvlx=self.mocked_pyvlx, node_id=23, name="Test device")
        velocity = Velocity.DEFAULT
        wait_for_completion = False
        await opening_device.close(velocity=velocity, wait_for_completion=wait_for_completion)
        set_position.assert_awaited_once_with(
            position=Position(position_percent=opening_device.close_position_target),
            velocity=velocity,
            wait_for_completion=wait_for_completion)

    @patch("pyvlx.opening_device.OpeningDevice.set_position", new_callable=AsyncMock)
    async def test_stop(self, set_position: AsyncMock) -> None:
        """Test stop function of OpeningDevice object."""
        opening_device = OpeningDevice(pyvlx=self.mocked_pyvlx, node_id=23, name="Test device")
        wait_for_completion = False
        await opening_device.stop(wait_for_completion=wait_for_completion)
        set_position.assert_awaited_once_with(
            position=CurrentPosition(),
            wait_for_completion=wait_for_completion)

    @patch("pyvlx.opening_device.SetLimitation")
    @patch("pyvlx.Node.after_update", new_callable=AsyncMock)
    async def test_set_position_limitations(self, after_update: AsyncMock, mock_set_limitation: MagicMock) -> None:
        """Test set_position_limitations of OpeningDevice object."""
        opening_device = OpeningDevice(pyvlx=self.mocked_pyvlx, node_id=23, name="Test device")
        position_min = Position(position_percent=10)
        position_max = Position(position_percent=90)

        mock_set_limitation_instance = AsyncMock()
        mock_set_limitation_instance.success = True
        mock_set_limitation.return_value = mock_set_limitation_instance
        await opening_device.set_position_limitations(position_min=position_min, position_max=position_max)

        mock_set_limitation.assert_called_once_with(
            pyvlx=self.mocked_pyvlx,
            node_id=23,
            limitation_value_min=position_min,
            limitation_value_max=position_max
        )
        mock_set_limitation.return_value.do_api_call.assert_awaited_once()
        after_update.assert_awaited_once()
        self.assertEqual(opening_device.limitation_min, position_min)
        self.assertEqual(opening_device.limitation_max, position_max)

    @patch("pyvlx.opening_device.SetLimitation")
    @patch("pyvlx.Node.after_update", new_callable=AsyncMock)
    async def test_set_position_limitations_default(self, after_update: AsyncMock, mock_set_limitation: MagicMock) -> None:
        """Test set_position_limitations of OpeningDevice object with default parameters."""
        opening_device = OpeningDevice(pyvlx=self.mocked_pyvlx, node_id=23, name="Test device")

        mock_set_limitation_instance = AsyncMock()
        mock_set_limitation_instance.success = True
        mock_set_limitation.return_value = mock_set_limitation_instance

        await opening_device.set_position_limitations()

        mock_set_limitation.assert_called_once_with(
            pyvlx=self.mocked_pyvlx,
            node_id=23,
            limitation_value_min=IgnorePosition(),
            limitation_value_max=IgnorePosition()
        )
        mock_set_limitation_instance.do_api_call.assert_awaited_once()
        after_update.assert_awaited_once()
        self.assertEqual(opening_device.limitation_min, IgnorePosition())
        self.assertEqual(opening_device.limitation_max, IgnorePosition())

    @patch("pyvlx.opening_device.SetLimitation")
    @patch("pyvlx.Node.after_update", new_callable=AsyncMock)
    async def test_clear_position_limitations(self, after_update: AsyncMock, mock_set_limitation: MagicMock) -> None:
        """Test clear_position_limitations of OpeningDevice object."""
        opening_device = OpeningDevice(pyvlx=self.mocked_pyvlx, node_id=23, name="Test device")
        opening_device.limitation_min = Position(position_percent=10)
        opening_device.limitation_max = Position(position_percent=90)

        mock_set_limitation_instance = AsyncMock()
        mock_set_limitation_instance.success = True
        mock_set_limitation.return_value = mock_set_limitation_instance

        await opening_device.clear_position_limitations()

        mock_set_limitation.assert_called_once_with(
            pyvlx=self.mocked_pyvlx,
            node_id=23,
            limitation_time=LimitationTime.CLEAR_ALL
        )
        mock_set_limitation_instance.do_api_call.assert_awaited_once()
        after_update.assert_awaited_once()
        self.assertEqual(opening_device.limitation_min, IgnorePosition())
        self.assertEqual(opening_device.limitation_max, IgnorePosition())

    @patch("pyvlx.opening_device.GetLimitation")
    async def test_get_limitation_min(self, mock_get_limitation: MagicMock) -> None:
        """Test get_limitation_min of OpeningDevice object."""
        opening_device = OpeningDevice(pyvlx=self.mocked_pyvlx, node_id=23, name="Test device")

        mock_get_limitation_instance = AsyncMock()
        mock_get_limitation_instance.success = True
        mock_get_limitation_instance.min_value = 10
        mock_get_limitation.return_value = mock_get_limitation_instance

        result = await opening_device.get_limitation_min()

        mock_get_limitation.assert_called_once_with(
            pyvlx=self.mocked_pyvlx,
            node_id=23,
            limitation_type=LimitationType.MIN_LIMITATION
        )
        mock_get_limitation_instance.do_api_call.assert_awaited_once()
        self.assertEqual(result, Position(position_percent=10))
        self.assertEqual(opening_device.limitation_min, Position(position_percent=10))

    @patch("pyvlx.opening_device.GetLimitation")
    async def test_get_limitation_max(self, mock_get_limitation: MagicMock) -> None:
        """Test get_limitation_max of OpeningDevice object."""
        opening_device = OpeningDevice(pyvlx=self.mocked_pyvlx, node_id=23, name="Test device")

        mock_get_limitation_instance = AsyncMock()
        mock_get_limitation_instance.success = True
        mock_get_limitation_instance.max_value = 90
        mock_get_limitation.return_value = mock_get_limitation_instance

        result = await opening_device.get_limitation_max()

        mock_get_limitation.assert_called_once_with(
            pyvlx=self.mocked_pyvlx,
            node_id=23,
            limitation_type=LimitationType.MAX_LIMITATION
        )
        mock_get_limitation_instance.do_api_call.assert_awaited_once()
        self.assertEqual(result, Position(position_percent=90))
        self.assertEqual(opening_device.limitation_max, Position(position_percent=90))

    def test_window_str(self) -> None:
        """Test string representation of Window object."""
        pyvlx = self.mocked_pyvlx
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
        pyvlx = self.mocked_pyvlx
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
        pyvlx = self.mocked_pyvlx
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
        pyvlx = self.mocked_pyvlx
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
        pyvlx = self.mocked_pyvlx
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
        pyvlx = self.mocked_pyvlx
        node1 = Blind(
            pyvlx=pyvlx, node_id=23, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        node2 = Blind(
            pyvlx=pyvlx, node_id=23, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        self.assertEqual(node1, node2)

    def test_nq(self) -> None:
        """Testing eq method with negative results."""
        pyvlx = self.mocked_pyvlx
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
