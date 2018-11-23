"""Module for retrieving node information from API."""
from pyvlx.frame_get_all_nodes_information import FrameGetAllNodesInformationRequest, \
    FrameGetAllNodesInformationConfirmation, FrameGetAllNodesInformationNotification, \
    FrameGetAllNodesInformationFinishedNotification
from pyvlx.api_event import ApiEvent
from .node_helper import convert_frame_to_node


class GetAllNodesInformation(ApiEvent):
    """Class for retrieving node informationfrom API."""

    def __init__(self, connection):
        """Initialize SceneList class."""
        super().__init__(connection)
        self.number_of_nodes = 0
        self.success = False
        self.nodes = []

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetAllNodesInformationConfirmation):
            self.number_of_nodes = frame.number_of_nodes
            # We are still waiting for FrameGetAllNodesInformationNotification
            return False
        if isinstance(frame, FrameGetAllNodesInformationNotification):
            node = convert_frame_to_node(frame)
            if node is not None:
                self.nodes.append(node)
        if isinstance(frame, FrameGetAllNodesInformationFinishedNotification):
            if self.number_of_nodes != len(self.nodes):
                print("Warning: number of received scenes does not match expected number")
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetAllNodesInformationRequest()
