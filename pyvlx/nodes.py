"""Module for storing nodes."""
from .exception import PyVLXException
from .get_all_nodes_information import GetAllNodesInformation
from .get_node_information import GetNodeInformation
from .node import Node
from .node_helper import convert_frame_to_node


class Nodes:
    """Object for storing node objects."""

    def __init__(self, pyvlx):
        """Initialize Nodes object."""
        self.pyvlx = pyvlx
        self.__nodes = []

    def __iter__(self):
        """Iterator."""
        yield from self.__nodes

    def __getitem__(self, key):
        """Return node by name or by index."""
        if isinstance(key, int):
            for node in self.__nodes:
                if node.node_id == key:
                    return node
        for node in self.__nodes:
            if node.name == key:
                return node
        raise KeyError

    def __contains__(self, key):
        """Check if key is in index."""
        if isinstance(key, int):
            for node in self.__nodes:
                if node.node_id == key:
                    return True
        if isinstance(key, Node):
            for node in self.__nodes:
                if node == key:
                    return True
        for node in self.__nodes:
            if node.name == key:
                return True
        return False

    def __len__(self):
        """Return number of nodes."""
        return len(self.__nodes)

    def add(self, node):
        """Add Node, replace existing node if node with node_id is present."""
        if not isinstance(node, Node):
            raise TypeError()
        for i, j in enumerate(self.__nodes):
            if j.node_id == node.node_id:
                self.__nodes[i] = node
                return
        self.__nodes.append(node)

    def clear(self):
        """Clear internal node array."""
        self.__nodes = []

    async def load(self, node_id=None):
        """Load nodes from KLF 200, if no node_id is specified all nodes are loaded."""
        if node_id is not None:
            await self._load_node(node_id=node_id)
        else:
            await self._load_all_nodes()

    async def _load_node(self, node_id):
        """Load single node via API."""
        get_node_information = GetNodeInformation(pyvlx=self.pyvlx, node_id=node_id)
        await get_node_information.do_api_call()
        if not get_node_information.success:
            raise PyVLXException("Unable to retrieve node information")
        notification_frame = get_node_information.notification_frame
        node = convert_frame_to_node(self.pyvlx, notification_frame)
        if node is not None:
            self.add(node)

    async def _load_all_nodes(self):
        """Load all nodes via API."""
        get_all_nodes_information = GetAllNodesInformation(pyvlx=self.pyvlx)
        await get_all_nodes_information.do_api_call()
        if not get_all_nodes_information.success:
            raise PyVLXException("Unable to retrieve node information")
        self.clear()
        for notification_frame in get_all_nodes_information.notification_frames:
            node = convert_frame_to_node(self.pyvlx, notification_frame)
            if node is not None:
                self.add(node)
