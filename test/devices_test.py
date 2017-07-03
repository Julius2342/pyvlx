import unittest
import asyncio
import json

from pyvlx import PyVLX, PyVLXException, Devices, Window, RollerShutter

# pylint: disable=too-many-public-methods,invalid-name
class TestDevices(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()


    def test_get_item(self):
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


    def test_iter(self):
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


    def test_load_windows(self):
        pyvlx = PyVLX()
        devices = Devices(pyvlx)

        get_response = '{"token":"aEGjVG0T3jj1VNEJTFmMBw==","result":true,"deviceStatus":"IDLE","data":[{"name":"Window 1","category":"Window opener","id":0,"typeId":4,"subtype":1,"scenes":["All windows closed","Sleeping wide Open","Sleeping slight open"]},{"name":"Window 2","category":"Window opener","id":1,"typeId":4,"subtype":1,"scenes":["All windows closed","Sleeping wide Open","Sleeping slight open"]},{"name":"Window 3","category":"Window opener","id":2,"typeId":4,"subtype":1,"scenes":["All windows closed","Sleeping wide Open","Sleeping slight open"]},{"name":"Window 4","category":"Window opener","id":3,"typeId":4,"subtype":1,"scenes":["All windows closed","Sleeping wide Open","Sleeping slight open"]}],"errors":[]}'
        devices.data_import(json.loads(get_response))

        self.assertEqual(len(devices), 4)
        self.assertEqual(devices[0], Window(pyvlx, 0, 'Window 1', 1, 4))
        self.assertEqual(devices[1], Window(pyvlx, 1, 'Window 2', 1, 4))
        self.assertEqual(devices[2], Window(pyvlx, 2, 'Window 3', 1, 4))
        self.assertEqual(devices[3], Window(pyvlx, 3, 'Window 4', 1, 4))


    def test_load_windows_and_roller_shutters(self):
        pyvlx = PyVLX()
        devices = Devices(pyvlx)

        get_response = '{"token":"aEGjVG0T3jj1VNEJTFmMBw==","result":true,"deviceStatus":"IDLE","data":[{"name": "Volet roulant cour", "id": 0, "scenes": ["Fermer volet cour", "Ouvrir volet cour"], "category": "Roller shutter", "typeId": 2, "subtype": 0}, {"name": "Fenêtre cour", "id": 1, "scenes": ["Fermer fenetre cour", "Ouvrir fenetre cour"], "category": "Window opener", "typeId": 4, "subtype": 1}, {"name": "Fenêtre jardin", "id": 2, "scenes": ["Fermer fenetre jardin", "Ouvrir fenetre jardin"], "category": "Window opener", "typeId": 4, "subtype": 1}, {"name": "Volet roulant jardin", "id": 3, "scenes": ["Fermer volet jardin", "Ouvrir Volet jardin"], "category": "Roller shutter", "typeId": 2, "subtype": 0}]}'
        devices.data_import(json.loads(get_response))

        self.assertEqual(len(devices), 4)
        self.assertEqual(devices[0], RollerShutter(pyvlx, 0, 'Volet roulant cour', 0, 2))
        self.assertEqual(devices[1], Window(pyvlx, 1, 'Fenêtre cour', 1, 4))
        self.assertEqual(devices[2], Window(pyvlx, 2, 'Fenêtre jardin', 1, 4))
        self.assertEqual(devices[3], RollerShutter(pyvlx, 3, 'Volet roulant jardin', 0, 2))


    def test_load_no_data_element(self):
        pyvlx = PyVLX()
        devices = Devices(pyvlx)

        get_response = '{"token":"aEGjVG0T3jj1VNEJTFmMBw==","result":true,"deviceStatus":"IDLE"}'
        with self.assertRaises(PyVLXException):
            devices.data_import(json.loads(get_response))


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDevices)
unittest.TextTestRunner(verbosity=2).run(SUITE)
