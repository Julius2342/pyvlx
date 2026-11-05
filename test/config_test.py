"""Unit test for configuration."""
import unittest
from unittest.mock import MagicMock, patch

from pyvlx import PyVLX, PyVLXException


class TestConfig(unittest.TestCase):
    """Test class for configuration."""

    def test_config_file(self) -> None:
        """Test host/password configuration via config.yaml."""
        pyvlx = PyVLX(path="test/data/test_config.yaml")
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")
        self.assertEqual(pyvlx.config.port, 51200)

    def test_config_file_with_port(self) -> None:
        """Test host/password configuration via config.yaml."""
        pyvlx = PyVLX(path="test/data/test_config_with_port.yaml")
        self.assertEqual(pyvlx.config.port, 1234)

    def test_heartbeat_quiet_period_configuration(self) -> None:
        """Test the heartbeat quiet period defaults and can be configured."""
        default = PyVLX()
        self.assertEqual(default.heartbeat_quiet_period, 60.0)
        self.assertFalse(default.heartbeat_quiet_period_active)
        self.assertEqual(PyVLX(heartbeat_quiet_period=15).heartbeat_quiet_period, 15)
        disabled = PyVLX(heartbeat_quiet_period=0)
        self.assertEqual(disabled.heartbeat_quiet_period, 0)
        disabled._mark_user_command_dispatched()
        self.assertFalse(disabled.heartbeat_quiet_period_active)
        self.assertEqual(PyVLX(heartbeat_quiet_period=-1).heartbeat_quiet_period, 0.0)

    def test_heartbeat_quiet_period_log_includes_wall_time(self) -> None:
        """Command dispatch logs a human-readable quiet-period end time."""
        pyvlx = PyVLX(heartbeat_quiet_period=60)

        with self.assertLogs("pyvlx", level="DEBUG") as logs:
            pyvlx._mark_user_command_dispatched()

        self.assertIn("until ", logs.output[0])
        self.assertRegex(logs.output[0], r"\d{4}-\d{2}-\d{2}T")

    @patch("pyvlx.pyvlx.time.monotonic")
    def test_heartbeat_quiet_period_expires_and_resets(self, monotonic: MagicMock) -> None:
        """Test commands reset the quiet period deadline and polling resumes at expiry."""
        pyvlx = PyVLX(heartbeat_quiet_period=60)

        monotonic.return_value = 10
        pyvlx._mark_user_command_dispatched()
        monotonic.return_value = 69
        self.assertTrue(pyvlx.heartbeat_quiet_period_active)
        monotonic.return_value = 70
        self.assertFalse(pyvlx.heartbeat_quiet_period_active)

        monotonic.return_value = 80
        pyvlx._mark_user_command_dispatched()
        monotonic.return_value = 139
        self.assertTrue(pyvlx.heartbeat_quiet_period_active)
        monotonic.return_value = 140
        self.assertFalse(pyvlx.heartbeat_quiet_period_active)

    def test_config_explicit(self) -> None:
        """Test host/password configuration via parameter."""
        pyvlx = PyVLX(host="192.168.2.127", password="velux123")
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")
        self.assertEqual(pyvlx.config.port, 51200)

    def test_config_wrong1(self) -> None:
        """Test configuration with missing password."""
        with self.assertRaises(PyVLXException):
            PyVLX(path="test/data/test_config_wrong1.yaml")

    def test_config_wrong2(self) -> None:
        """Test configuration with missing host."""
        with self.assertRaises(PyVLXException):
            PyVLX(path="test/data/test_config_wrong2.yaml")

    def test_config_wrong3(self) -> None:
        """Test configuration with missing config node."""
        with self.assertRaises(PyVLXException):
            PyVLX(path="test/data/test_config_wrong3.yaml")

    def test_config_non_existent(self) -> None:
        """Test non existing configuration path."""
        with self.assertRaises(PyVLXException):
            PyVLX(path="test/data/test_config_non_existent.yaml")
