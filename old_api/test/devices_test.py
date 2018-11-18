"""Unit test for devices container within PyVLX."""

import unittest
from unittest.mock import patch
import asyncio
import json

from pyvlx import PyVLX, PyVLXException, Devices, Window, RollerShutter


# pylint: disable=too-many-public-methods,invalid-name
class TestDevices(unittest.TestCase):
    """Test class for devices container."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    def test_get_item(self):
        """Test get_item."""
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        window1 = Window(pyvlx, 0, 'Window_1', 0, 0)
        devices.add(window1)
        window2 = Window(pyvlx, 1, 'Window_2', 0, 0)
        devices.add(window2)
        window3 = Window(pyvlx, 2, 'Window_3', 0, 0)
        devices.add(window3)
        window4 = Window(pyvlx, 3, 'Window_4', 0, 0)
        devices.add(window4)
        self.assertEqual(devices['Window_1'], window1)
        self.assertEqual(devices['Window_2'], window2)
        self.assertEqual(devices['Window_3'], window3)
        self.assertEqual(devices['Window_4'], window4)
        self.assertEqual(devices[0], window1)
        self.assertEqual(devices[1], window2)
        self.assertEqual(devices[2], window3)
        self.assertEqual(devices[3], window4)

    def test_get_item_failed(self):
        """Test get_item with non existing object."""
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        window1 = Window(pyvlx, 0, 'Window_1', 0, 0)
        devices.add(window1)
        with self.assertRaises(KeyError):
            devices['Window_2']  # pylint: disable=pointless-statement
        with self.assertRaises(IndexError):
            devices[1]  # pylint: disable=pointless-statement

    def test_iter(self):
        """Test iterator."""
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        window1 = Window(pyvlx, 0, 'Window_1', 0, 0)
        devices.add(window1)
        window2 = Window(pyvlx, 1, 'Window_2', 0, 0)
        devices.add(window2)
        window3 = Window(pyvlx, 2, 'Window_3', 0, 0)
        devices.add(window3)
        window4 = Window(pyvlx, 3, 'Window_4', 0, 0)
        devices.add(window4)
        self.assertEqual(
            tuple(devices.__iter__()),
            (window1, window2, window3, window4))

    def test_len(self):
        """Test len."""
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        self.assertEqual(len(devices), 0)
        window1 = Window(pyvlx, 0, 'Window_1', 0, 0)
        devices.add(window1)
        self.assertEqual(len(devices), 1)
        window2 = Window(pyvlx, 1, 'Window_2', 0, 0)
        devices.add(window2)
        self.assertEqual(len(devices), 2)
        window3 = Window(pyvlx, 2, 'Window_3', 0, 0)
        devices.add(window3)
        self.assertEqual(len(devices), 3)
        window4 = Window(pyvlx, 3, 'Window_4', 0, 0)
        devices.add(window4)
        self.assertEqual(len(devices), 4)

    def test_add_item_failed(self):
        """Test add() with wrong type."""
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        with self.assertRaises(TypeError):
            devices.add(devices)
        with self.assertRaises(TypeError):
            devices.add("device")

    def test_load_windows(self):
        """Test load configuration with windows."""
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        get_response = \
            '{"token":"aEGjVG0T3jj1VNEJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":[{"name":"Window 1","category":"Window op' + \
            'ener","id":0,"typeId":4,"subtype":1,"scenes":["All windows c' + \
            'losed","Sleeping wide Open","Sleeping slight open"]},{"name"' + \
            ':"Window 2","category":"Window opener","id":1,"typeId":4,"su' + \
            'btype":1,"scenes":["All windows closed","Sleeping wide Open"' + \
            ',"Sleeping slight open"]},{"name":"Window 3","category":"Win' + \
            'dow opener","id":2,"typeId":4,"subtype":1,"scenes":["All win' + \
            'dows closed","Sleeping wide Open","Sleeping slight open"]},{' + \
            '"name":"Window 4","category":"Window opener","id":3,"typeId"' + \
            ':4,"subtype":1,"scenes":["All windows closed","Sleeping wide' + \
            'Open","Sleeping slight open"]}],"errors":[]}'
        devices.data_import(json.loads(get_response))
        self.assertEqual(len(devices), 4)
        self.assertEqual(devices[0], Window(pyvlx, 0, 'Window 1', 1, 4))
        self.assertEqual(devices[1], Window(pyvlx, 1, 'Window 2', 1, 4))
        self.assertEqual(devices[2], Window(pyvlx, 2, 'Window 3', 1, 4))
        self.assertEqual(devices[3], Window(pyvlx, 3, 'Window 4', 1, 4))

    def test_load_windows_and_roller_shutters(self):
        """Test load configuration with windows and rollershutters."""
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        get_response = \
            '{"token":"aEGjVG0T3jj1VNEJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":[{"name": "Volet roulant cour", "id": 0, ' + \
            '"scenes": ["Fermer volet cour", "Ouvrir volet cour"], "categ' + \
            'ory": "Roller shutter", "typeId": 2, "subtype": 0}, {"name":' + \
            '"Fenêtre cour", "id": 1, "scenes": ["Fermer fenetre cour", "' + \
            'Ouvrir fenetre cour"], "category": "Window opener", "typeId"' + \
            ': 4, "subtype": 1}, {"name": "Fenêtre jardin", "id": 2, "sce' + \
            'nes": ["Fermer fenetre jardin", "Ouvrir fenetre jardin"], "c' + \
            'ategory": "Window opener", "typeId": 4, "subtype": 1}, {"nam' + \
            'e": "Volet roulant jardin", "id": 3, "scenes": ["Fermer vole' + \
            't jardin", "Ouvrir Volet jardin"], "category": "Roller shutt' + \
            'er", "typeId": 2, "subtype": 0}]}'
        devices.data_import(json.loads(get_response))
        self.assertEqual(len(devices), 4)
        self.assertEqual(
            devices[0],
            RollerShutter(pyvlx, 0, 'Volet roulant cour', 0, 2))
        self.assertEqual(
            devices[1],
            Window(pyvlx, 1, 'Fenêtre cour', 1, 4))
        self.assertEqual(
            devices[2],
            Window(pyvlx, 2, 'Fenêtre jardin', 1, 4))
        self.assertEqual(
            devices[3],
            RollerShutter(pyvlx, 3, 'Volet roulant jardin', 0, 2))

    def test_load_no_data_element(self):
        """Test response with no data element."""
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        get_response = \
            '{"token":"aEGjVG0T3jj1VNEJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE"}'
        with self.assertRaises(PyVLXException):
            devices.data_import(json.loads(get_response))

    @patch('pyvlx.Interface.api_call')
    def test_load_interface_call(self, mock_apicall):
        """Test if interface is called correctly."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        get_response = \
            '{"token":"aEGjVG0T3jj1VNEJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":[{"name": "Volet roulant cour", "id": 0, ' + \
            '"scenes": ["Fermer volet cour", "Ouvrir volet cour"], "categ' + \
            'ory": "Roller shutter", "typeId": 2, "subtype": 0}, {"name":' + \
            '"Fenêtre cour", "id": 1, "scenes": ["Fermer fenetre cour", "' + \
            'Ouvrir fenetre cour"], "category": "Window opener", "typeId"' + \
            ': 4, "subtype": 1}, {"name": "Fenêtre jardin", "id": 2, "sce' + \
            'nes": ["Fermer fenetre jardin", "Ouvrir fenetre jardin"], "c' + \
            'ategory": "Window opener", "typeId": 4, "subtype": 1}, {"nam' + \
            'e": "Volet roulant jardin", "id": 3, "scenes": ["Fermer vole' + \
            't jardin", "Ouvrir Volet jardin"], "category": "Roller shutt' + \
            'er", "typeId": 2, "subtype": 0}]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        self.loop.run_until_complete(asyncio.Task(
            devices.load()))
        mock_apicall.assert_called_with('products', 'get')
        self.assertEqual(len(devices), 4)
        self.assertEqual(
            devices[0],
            RollerShutter(pyvlx, 0, 'Volet roulant cour', 0, 2))
        self.assertEqual(
            devices[1],
            Window(pyvlx, 1, 'Fenêtre cour', 1, 4))
        self.assertEqual(
            devices[2],
            Window(pyvlx, 2, 'Fenêtre jardin', 1, 4))
        self.assertEqual(
            devices[3],
            RollerShutter(pyvlx, 3, 'Volet roulant jardin', 0, 2))

    @patch('pyvlx.Interface.api_call')
    def test_load_interface_call_failed(self, mock_apicall):
        """Test if error is raised if no data element is in response."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        get_response = \
            '{"token":"aEGjV20T32j1V3EJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        with self.assertRaises(PyVLXException):
            self.loop.run_until_complete(asyncio.Task(
                devices.load()))

    @patch('pyvlx.Interface.api_call')
    def test_load_interface_call_failed_no_category(self, mock_apicall):
        """Test if error is raised if no data element is in response."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        get_response = \
            '{"token":"aEGjV20T32j1V3EJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":[{"name": "Fnord"}],"errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        with self.assertRaises(PyVLXException):
            self.loop.run_until_complete(asyncio.Task(
                devices.load()))

    @patch('pyvlx.Interface.api_call')
    def test_load_interface_call_failed_wrong_category(self, mock_apicall):
        """Test if error is raised if no data element is in response."""
        async def return_async_value(val):
            return val
        pyvlx = PyVLX()
        devices = Devices(pyvlx)
        get_response = \
            '{"token":"aEGjV20T32j1V3EJTFmMBw==","result":true,"deviceSta' + \
            'tus":"IDLE","data":[{"name": "Fnord", "category": "xyz"}],"errors":[]}'
        mock_apicall.return_value = return_async_value(json.loads(get_response))
        with self.assertLogs('pyvlx.log', level='WARNING'):
            self.loop.run_until_complete(asyncio.Task(
                devices.load()))


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDevices)
unittest.TextTestRunner(verbosity=2).run(SUITE)
