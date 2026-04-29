"""Unit tests for connection module."""
import asyncio
import ssl
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from pyvlx.config import Config
from pyvlx.connection import Connection
from pyvlx.exception import PyVLXException


class TestConnection(IsolatedAsyncioTestCase):
    """Test class for Connection."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.pyvlx = MagicMock()
        self.config = Config(
            pyvlx=self.pyvlx,
            host="192.168.1.10",
            password="velux123",
        )
        self.connection = Connection(config=self.config)

    async def test_connect_timeout_raises_pyvlx_exception(self) -> None:
        """Test connect raises PyVLXException when socket connect times out."""
        mock_loop = MagicMock()
        mock_loop.create_connection = AsyncMock(side_effect=asyncio.TimeoutError)

        with patch("pyvlx.connection.asyncio.get_running_loop", return_value=mock_loop):
            with self.assertRaises(PyVLXException) as raised_exception:
                await self.connection.connect()

        self.assertFalse(self.connection.connected)
        self.assertIsNone(self.connection.transport)
        self.assertIn("timed out after", str(raised_exception.exception))

    async def test_ssl_error_raises_pyvlx_exception(self) -> None:
        """Test connect raises PyVLXException when an SSL error occurs."""
        mock_loop = MagicMock()
        mock_loop.create_connection = AsyncMock(side_effect=ssl.SSLError("SSL error"))

        with patch("pyvlx.connection.asyncio.get_running_loop", return_value=mock_loop):
            with self.assertRaises(PyVLXException) as raised_exception:
                await self.connection.connect()

        self.assertFalse(self.connection.connected)
        self.assertIsNone(self.connection.transport)
        self.assertIn("SSL error", str(raised_exception.exception))

    async def test_connect_success_sets_connected_state(self) -> None:
        """Test connect stores transport and marks connection as connected."""
        mock_loop = MagicMock()
        fake_transport = MagicMock(spec=asyncio.Transport)
        mock_loop.create_connection = AsyncMock(return_value=(fake_transport, MagicMock()))

        with patch("pyvlx.connection.asyncio.get_running_loop", return_value=mock_loop):
            await self.connection.connect()

        self.assertTrue(self.connection.connected)
        self.assertEqual(self.connection.transport, fake_transport)

    async def test_disconnect_schedules_connection_closed_callback(self) -> None:
        """Test disconnect schedules connection closed callbacks when an event loop is running."""
        fake_transport = MagicMock(spec=asyncio.Transport)
        callback = AsyncMock()
        self.connection.transport = fake_transport
        self.connection.connected = True
        self.connection.register_connection_closed_cb(callback)

        self.connection.disconnect()

        fake_transport.close.assert_called_once()
        self.assertFalse(self.connection.connected)
        tasks = list(self.connection.tasks)
        self.assertEqual(len(tasks), 1)
        await asyncio.gather(*tasks)
        callback.assert_awaited_once()

    def test_disconnect_without_running_loop_skips_connection_closed_callbacks(self) -> None:
        """Test disconnect does not create callback coroutines without a running event loop."""
        fake_transport = MagicMock(spec=asyncio.Transport)
        callback = MagicMock()
        self.connection.transport = fake_transport
        self.connection.connected = True
        self.connection.register_connection_closed_cb(callback)

        with patch("pyvlx.connection.asyncio.get_running_loop", side_effect=RuntimeError):
            self.connection.disconnect()

        fake_transport.close.assert_called_once()
        self.assertFalse(self.connection.connected)
        callback.assert_not_called()

    def test_destructor_closes_transport_without_connection_closed_callbacks(self) -> None:
        """Test __del__ closes the transport without scheduling async callbacks."""
        fake_transport = MagicMock(spec=asyncio.Transport)
        callback = MagicMock()
        self.connection.transport = fake_transport
        self.connection.connected = True
        self.connection.register_connection_closed_cb(callback)

        self.connection.__del__()

        fake_transport.close.assert_called_once()
        self.assertFalse(self.connection.connected)
        callback.assert_not_called()
