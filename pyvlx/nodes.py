"""Module for storing nodes."""
from .get_node_information import GetNodeInformation
from .get_all_nodes_information import GetAllNodesInformation
from .node_helper import convert_frame_to_node
from .exception import PyVLXException


class Nodes:
    """Object for storing node objects."""

    def __init__(self, pyvlx):
        """Initalize Nodes object."""
        self.pyvlx = pyvlx
        self.__nodes = []

    def __iter__(self):
        """Iterator."""
        yield from self.__nodes

    def __getitem__(self, key):
        """Return device by name or by index."""
        for device in self.__nodes:
            if device.name == key:
                return device
        if isinstance(key, int):
            return self.__nodes[key]
        raise KeyError

    def __len__(self):
        """Return number of nodes."""
        return len(self.__nodes)

    def add(self, device):
        """Add device."""
        self.__nodes.append(device)

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
        self.add(node)

    async def _load_all_nodes(self):
        """Load all nodes via API."""
        get_all_nodes_information = GetAllNodesInformation(pyvlx=self.pyvlx)
        await get_all_nodes_information.do_api_call()
        if not get_all_nodes_information.success:
            raise PyVLXException("Unable to retrieve node information")
        for notification_frame in get_all_nodes_information.notification_frames:
            node = convert_frame_to_node(self.pyvlx, notification_frame)
            self.add(node)

        # XXX At the moment the nodes are just added not replaces.:w
