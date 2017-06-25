import unittest
import asyncio

from pyvlx import PyVLX, Scenes, Scene

# pylint: disable=too-many-public-methods,invalid-name
class TestScenes(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()


    def test_get_item(self):
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)

        scene1 = Scene(pyvlx, 0, 'Scene_1')
        scenes.add(scene1)
        scene2 = Scene(pyvlx, 1, 'Scene_2')
        scenes.add(scene2)
        scene3 = Scene(pyvlx, 2, 'Scene_3')
        scenes.add(scene3)
        scene4 = Scene(pyvlx, 3, 'Scene_4')
        scenes.add(scene4)

        self.assertEqual(scenes['Scene_1'], scene1)
        self.assertEqual(scenes['Scene_2'], scene2)
        self.assertEqual(scenes['Scene_3'], scene3)
        self.assertEqual(scenes['Scene_4'], scene4)

        self.assertEqual(scenes[0], scene1)
        self.assertEqual(scenes[1], scene2)
        self.assertEqual(scenes[2], scene3)
        self.assertEqual(scenes[3], scene4)


    def test_iter(self):
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)

        scene1 = Scene(pyvlx, 0, 'Scene_1')
        scenes.add(scene1)
        scene2 = Scene(pyvlx, 1, 'Scene_2')
        scenes.add(scene2)
        scene3 = Scene(pyvlx, 2, 'Scene_3')
        scenes.add(scene3)
        scene4 = Scene(pyvlx, 3, 'Scene_4')
        scenes.add(scene4)

        self.assertEqual(
            tuple(scenes.__iter__()),
            (scene1, scene2, scene3, scene4))


    def test_len(self):
        pyvlx = PyVLX()
        scenes = Scenes(pyvlx)
        self.assertEqual(len(scenes), 0)
        scene1 = Scene(pyvlx, 0, 'Scene_1')
        scenes.add(scene1)
        self.assertEqual(len(scenes), 1)

        scene2 = Scene(pyvlx, 1, 'Scene_2')
        scenes.add(scene2)
        self.assertEqual(len(scenes), 2)

        scene3 = Scene(pyvlx, 2, 'Scene_3')
        scenes.add(scene3)
        self.assertEqual(len(scenes), 3)

        scene4 = Scene(pyvlx, 3, 'Scene_4')
        scenes.add(scene4)
        self.assertEqual(len(scenes), 4)


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestScenes)
unittest.TextTestRunner(verbosity=2).run(SUITE)
