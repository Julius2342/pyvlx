import asyncio

from pyvlx import RollerShutter, PyVLX, Blind
from pyvlx.const import NodeTypeWithSubtype
from pyvlx.frames import FrameGetNodeInformationNotification
from pyvlx.node_helper import convert_frame_to_node

HOST = "192.168.178.76"
PASSWORD = "BD92c2J37R"


async def main():
    pyvlx = PyVLX(host=HOST, password=PASSWORD)
    await pyvlx.connect()
    await pyvlx.load_nodes()
    await pyvlx.load_scenes()
    await pyvlx.update_version()
    for node in pyvlx.nodes:
        if isinstance(node, Blind):
            print("Node is type of %s and the name is %s and position is %s and orientation is %s" %(type(node).__name__, node.name, node.position, node.orientation))
        if isinstance(node, RollerShutter):
            print("Node is type of %s and the name is %s and position is %s" %(type(node).__name__, node.name, node.position))
    await pyvlx.disconnect()

asyncio.run(main())