"""Unit test for configuration."""
import unittest
import asyncio

from pyvlx import PyVLX, PyVLXException


# pylint: disable=too-many-public-methods,invalid-name
class TestConfig(unittest.TestCase):
    """Test class for configuration."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    def test_config_file(self):
        """Test host/password configuration via config.yaml."""
        pyvlx = PyVLX("test/data/test_config.yaml")
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")

    def test_config_explicit(self):
        """Test host/password configuration via parameter."""
        pyvlx = PyVLX(host="192.168.2.127", password="velux123")
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")

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


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
unittest.TextTestRunner(verbosity=2).run(SUITE)
