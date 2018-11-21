"""Unit tests for FrameGetAllNodesInformationConfirmation."""
import unittest
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frame_get_all_nodes_information import FrameGetAllNodesInformationConfirmation


class TestFrameGetAllNodesInformationConfirmation(unittest.TestCase):
    """Test class for FrameGetAllNodesInformationConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_discover_node_request(self):
        """Test FrameGetAllNodesInformationConfirmation."""
        frame = FrameGetAllNodesInformationConfirmation(number_of_nodes=23)
        self.assertEqual(bytes(frame), b'\x00\x05\x02\x03\x00\x17\x13')

    def test_discover_node_request_from_raw(self):
        """Test parse FrameGetAllNodesInformationConfirmation from raw."""
        frame = frame_from_raw(b'\x00\x05\x02\x03\x00\x17\x13')
        self.assertTrue(isinstance(frame, FrameGetAllNodesInformationConfirmation))
        self.assertEqual(frame.number_of_nodes, 23)

    def test_str(self):
        """Test string representation of FrameGetAllNodesInformationConfirmation."""
        frame = FrameGetAllNodesInformationConfirmation(number_of_nodes=23)
        self.assertEqual(
            str(frame),
            '<FrameGetAllNodesInformationConfirmation status=\'AllNodesInformationStatus.OK\' number_of_nodes=23/>')
