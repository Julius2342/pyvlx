"""Unit tests _helper module."""
import unittest
from pyvlx import PyVLX, Window, Blind, RollerShutter
from pyvlx.node_helper import convert_frame_to_node
from pyvlx.frames import FrameGetNodeInformationNotification
from pyvlx.const import NodeTypeWithSubtype


class TestNodeHelper(unittest.TestCase):
    """Test class for helper functions of node_helper."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_window(self):
        """Test convert_frame_to_node with window."""
        frame = FrameGetNodeInformationNotification()
        frame.node_id = 23
        frame.name = "Fnord23"
        frame.node_type = NodeTypeWithSubtype.WINDOW_OPENER
        pyvlx = PyVLX()
        node = convert_frame_to_node(pyvlx, frame)
        self.assertEqual(node, Window(pyvlx=pyvlx, name="Fnord23", node_id=23))

    def test_window_with_rain_sensor(self):
        """Test convert_frame_to_node with window with rain sensor."""
        frame = FrameGetNodeInformationNotification()
        frame.node_id = 23
        frame.name = "Fnord23"
        frame.node_type = NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR
        pyvlx = PyVLX()
        node = convert_frame_to_node(pyvlx, frame)
        self.assertEqual(node, Window(pyvlx=pyvlx, name="Fnord23", node_id=23, rain_sensor=True))

    def test_blind(self):
        """Test convert_frame_to_node with blind."""
        frame = FrameGetNodeInformationNotification()
        frame.node_id = 23
        frame.name = "Fnord23"
        frame.node_type = NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND
        pyvlx = PyVLX()
        node = convert_frame_to_node(pyvlx, frame)
        self.assertEqual(node, Blind(pyvlx=pyvlx, name="Fnord23", node_id=23))

    def test_roller_shutter(self):
        """Test convert_frame_to_node roller shutter."""
        frame = FrameGetNodeInformationNotification()
        frame.node_id = 23
        frame.name = "Fnord23"
        frame.node_type = NodeTypeWithSubtype.ROLLER_SHUTTER
        pyvlx = PyVLX()
        node = convert_frame_to_node(pyvlx, frame)
        self.assertEqual(node, RollerShutter(pyvlx=pyvlx, name="Fnord23", node_id=23))

    def test_no_type(self):
        """Test convert_frame_to_node with no type (convert_frame_to_node should return None)."""
        frame = FrameGetNodeInformationNotification()
        frame.node_id = 23
        frame.name = "Fnord23"
        frame.node_type = NodeTypeWithSubtype.NO_TYPE
        pyvlx = PyVLX()
        self.assertEqual(convert_frame_to_node(pyvlx, frame), None)
