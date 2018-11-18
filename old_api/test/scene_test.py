"""Unit test for scene."""

import unittest
from unittest.mock import patch
import asyncio
import json
from pyvlx import PyVLX, Scene


# pylint: disable=too-many-public-methods,invalid-name
class TestScene(unittest.TestCase):
    """Test class for scene."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    def test_get_name(self):
        """Test get_name()."""
        pyvlx = PyVLX()
        scene = Scene(pyvlx, 2, 'Scene 1')
        self.assertEqual(scene.get_name(), "Scene 1")

    def test_str(self):
        """Test string representation of Scene object."""
        pyvlx = PyVLX()
        scene = Scene(pyvlx, 2, 'Scene 1')
        self.assertEqual(
            str(scene),
            '<Scene name="Scene 1" id="2" />')

    @patch('pyvlx.Interface.api_call')
    def test_load_interface_call(self, mock_apicall):
        """Test if interface is called correctly."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX()
        scene = Scene(pyvlx, 2, 'Scene 1')
        get_response = \
            '{"token":"aEGjVG0T3jj1VNEJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        self.loop.run_until_complete(asyncio.Task(
            scene.run()))
        mock_apicall.assert_called_with('scenes', 'run', {'id': 2})


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestScene)
unittest.TextTestRunner(verbosity=2).run(SUITE)
