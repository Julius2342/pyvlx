"""Unit test for interface object."""
import unittest
import asyncio
import json

from pyvlx import Interface, InvalidToken


# pylint: disable=too-many-public-methods,invalid-name
class TestInterface(unittest.TestCase):
    """Test class for interface object."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    def test_invalid_token(self):
        """Test response with error 'invalid token'."""
        get_response = \
            '{"result":false,"deviceStatus":"IDLE","data":{},"errors":[406]}'
        json_response = json.loads(get_response)

        with self.assertRaises(InvalidToken):
            Interface.evaluate_response(json_response)


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestInterface)
unittest.TextTestRunner(verbosity=2).run(SUITE)
