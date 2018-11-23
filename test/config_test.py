"""Unit test for configuration."""
import unittest
from pyvlx import PyVLX, PyVLXException


# pylint: disable=too-many-public-methods,invalid-name
class TestConfig(unittest.TestCase):
    """Test class for configuration."""

    def test_config_file(self):
        """Test host/password configuration via config.yaml."""
        pyvlx = PyVLX("test/data/test_config.yaml")
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")
        self.assertEqual(pyvlx.config.port, 51200)

    def test_config_file_with_port(self):
        """Test host/password configuration via config.yaml."""
        pyvlx = PyVLX("test/data/test_config_with_port.yaml")
        self.assertEqual(pyvlx.config.port, 1234)

    def test_config_explicit(self):
        """Test host/password configuration via parameter."""
        pyvlx = PyVLX(host="192.168.2.127", password="velux123")
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")
        self.assertEqual(pyvlx.config.port, 51200)

    def test_config_wrong1(self):
        """Test configuration with missing password."""
        with self.assertRaises(PyVLXException):
            PyVLX("test/data/test_config_wrong1.yaml")

    def test_config_wrong2(self):
        """Test configuration with missing host."""
        with self.assertRaises(PyVLXException):
            PyVLX("test/data/test_config_wrong2.yaml")

    def test_config_wrong3(self):
        """Test configuration with missing config node."""
        with self.assertRaises(PyVLXException):
            PyVLX("test/data/test_config_wrong3.yaml")

    def test_config_non_existent(self):
        """Test non existing configuration path."""
        with self.assertRaises(PyVLXException):
            PyVLX("test/data/test_config_non_existent.yaml")
