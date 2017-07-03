import unittest
import asyncio

from pyvlx import PyVLX, PyVLXException

# pylint: disable=too-many-public-methods,invalid-name
class TestConfig(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_config_file(self):
        pyvlx = PyVLX("data/test_config.yaml")
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")

    def test_config_explicit(self):
        pyvlx = PyVLX(host="192.168.2.127", password="velux123")
        self.assertEqual(pyvlx.config.password, "velux123")
        self.assertEqual(pyvlx.config.host, "192.168.2.127")

    def test_config_wrong1(self):
        with self.assertRaises(PyVLXException):
            PyVLX("data/test_config_wrong1.yaml")

    def test_config_wrong2(self):
        with self.assertRaises(PyVLXException):
            PyVLX("data/test_config_wrong2.yaml")

    def test_config_wrong3(self):
        with self.assertRaises(PyVLXException):
            PyVLX("data/test_config_wrong3.yaml")

    def test_config_non_existent(self):
        with self.assertRaises(PyVLXException):
            PyVLX("data/test_config_non_existent.yaml")

SUITE = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
unittest.TextTestRunner(verbosity=2).run(SUITE)
