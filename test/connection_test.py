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
