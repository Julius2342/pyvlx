import unittest
import asyncio

from pyvlx import PyVLX, Devices, Window

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
        window2 = Window(pyvlx, 1, "Window_2", 0, 0)
        devices.add(window2)
        window3 = Window(pyvlx, 2, 'Window_3', 0, 0)
        devices.add(window3)
        window4 = Window(pyvlx, 3, "Window_4", 0, 0)
        devices.add(window4)

        self.assertEqual(devices["Window_1"], window1)
        self.assertEqual(devices["Window_2"], window2)
        self.assertEqual(devices["Window_3"], window3)
        self.assertEqual(devices["Window_4"], window4)

        self.assertEqual(devices[0], window1)
        self.assertEqual(devices[1], window2)
        self.assertEqual(devices[2], window3)
        self.assertEqual(devices[3], window4)


    def test_iter(self):
        pyvlx = PyVLX()
        devices = Devices(pyvlx)

        window1 = Window(pyvlx, 0, 'Window_1', 0, 0)
        devices.add(window1)
        window2 = Window(pyvlx, 1, "Window_2", 0, 0)
        devices.add(window2)
        window3 = Window(pyvlx, 2, 'Window_3', 0, 0)
        devices.add(window3)
        window4 = Window(pyvlx, 3, "Window_4", 0, 0)
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

        window2 = Window(pyvlx, 1, "Window_2", 0, 0)
        devices.add(window2)
        self.assertEqual(len(devices), 2)

        window3 = Window(pyvlx, 2, 'Window_3', 0, 0)
        devices.add(window3)
        self.assertEqual(len(devices), 3)

        window4 = Window(pyvlx, 3, "Window_4", 0, 0)
        devices.add(window4)
        self.assertEqual(len(devices), 4)


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDevices)
unittest.TextTestRunner(verbosity=2).run(SUITE)
