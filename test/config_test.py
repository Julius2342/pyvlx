"""Unit test for configuration."""
import unittest
from asyncio import AbstractEventLoop
from unittest.mock import MagicMock

from pyvlx import PyVLX, PyVLXException


# pylint: disable=too-many-public-methods,invalid-name
class TestConfig(unittest.TestCase):
    """Test class for configuration."""

    def setUp(self) -> None:
        """Set up TestCommandSend."""
        self.mocked_loop = MagicMock(spec=AbstractEventLoop)

    def test_config_file(self) -> None:
        """Test host/password configuration via config.yaml."""
        pyvlx = PyVLX(loop=self.mocked_loop, path="test/data/test_config.yaml")  # pylint: disable=E1123
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")
        self.assertEqual(pyvlx.config.port, 51200)

    def test_config_file_with_port(self) -> None:
        """Test host/password configuration via config.yaml."""
        pyvlx = PyVLX(loop=self.mocked_loop, path="test/data/test_config_with_port.yaml")  # pylint: disable=E1123
        self.assertEqual(pyvlx.config.port, 1234)

    def test_config_explicit(self) -> None:
        """Test host/password configuration via parameter."""
        pyvlx = PyVLX(loop=self.mocked_loop, host="192.168.2.127", password="velux123")  # pylint: disable=E1123
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")
        self.assertEqual(pyvlx.config.port, 51200)

    def test_config_wrong1(self) -> None:
        """Test configuration with missing password."""
        with self.assertRaises(PyVLXException):
            PyVLX(loop=self.mocked_loop, path="test/data/test_config_wrong1.yaml")  # pylint: disable=E1123

    def test_config_wrong2(self) -> None:
        """Test configuration with missing host."""
        with self.assertRaises(PyVLXException):
            PyVLX(loop=self.mocked_loop, path="test/data/test_config_wrong2.yaml")  # pylint: disable=E1123

    def test_config_wrong3(self) -> None:
        """Test configuration with missing config node."""
        with self.assertRaises(PyVLXException):
            PyVLX(loop=self.mocked_loop, path="test/data/test_config_wrong3.yaml")  # pylint: disable=E1123

    def test_config_non_existent(self) -> None:
        """Test non existing configuration path."""
        with self.assertRaises(PyVLXException):
            PyVLX(loop=self.mocked_loop, path="test/data/test_config_non_existent.yaml")  # pylint: disable=E1123
