"""Unit test for roller shutter."""

import unittest
import asyncio

from pyvlx import PyVLXException, InvalidToken


# pylint: disable=too-many-public-methods,invalid-name
class TestException(unittest.TestCase):
    """Test class for roller shutter."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    def test_str(self):
        exception = PyVLXException("fnord fnord")
        self.assertEqual(
            str(exception),
            '<PyVLXException description="fnord fnord" />')

    def test_invalid_token(self):
        exception = InvalidToken(23)
        self.assertEqual(
            str(exception),
            '<PyVLXException description="Invalid Token" />')
        self.assertEqual(
            exception.error_code,
            23)

SUITE = unittest.TestLoader().loadTestsFromTestCase(TestException)
unittest.TextTestRunner(verbosity=2).run(SUITE)
