"""Unit test for PyVLX object."""

import unittest
from unittest.mock import patch
import asyncio
import json
from pyvlx import PyVLX


# pylint: disable=too-many-public-methods,invalid-name
class TestScene(unittest.TestCase):
    """Test class for PyVLX."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    @patch('pyvlx.Interface.api_call')
    def test_connect_api_call(self, mock_apicall):
        """Test connect to interface."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX(password="mypassword", host="testhost")
        get_response = \
            '{"token":"b1tfR54h5w6lQH1rb2U5Gw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":{},"errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        self.loop.run_until_complete(asyncio.Task(
            pyvlx.connect()))
        mock_apicall.assert_called_with(
            'auth', 'login',
            {'password': 'mypassword'},
            add_authorization_token=False)
        self.assertEqual(pyvlx.interface.token, "b1tfR54h5w6lQH1rb2U5Gw==")

    @patch('pyvlx.Interface.api_call')
    def test_disconnect_api_call(self, mock_apicall):
        """Test disconnect from interface."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX(password="mypassword", host="testhost")
        get_response = \
            '{"token":"b1tfR54h5w6lQH1rb2U5Gw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":{},"errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        pyvlx.interface.token = "b1tfR54h5w6lQH1rb2U5Gw=="
        self.loop.run_until_complete(asyncio.Task(
            pyvlx.disconnect()))
        mock_apicall.assert_called_with(
            'auth', 'logout',
            {}, add_authorization_token=True)
        self.assertEqual(pyvlx.interface.token, None)

    @patch('pyvlx.Interface.api_call')
    def test_load_scenes_api_call(self, mock_apicall):
        """Test disconnect from interface."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX(password="mypassword", host="testhost")
        get_response = \
            '{"token":"b1tfR54h5w6lQH1rb2U5Gw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":{},"errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        self.loop.run_until_complete(asyncio.Task(
            pyvlx.load_scenes()))
        mock_apicall.assert_called_with('scenes', 'get')

    @patch('pyvlx.Interface.api_call')
    def test_load_devices_api_call(self, mock_apicall):
        """Test disconnect from interface."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX(password="mypassword", host="testhost")
        get_response = \
            '{"token":"b1tfR54h5w6lQH1rb2U5Gw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":{},"errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        self.loop.run_until_complete(asyncio.Task(
            pyvlx.load_devices()))
        mock_apicall.assert_called_with('products', 'get')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestScene)
unittest.TextTestRunner(verbosity=2).run(SUITE)
