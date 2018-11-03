"""Just a demo of the new PyVLX module."""
import asyncio
from pyvlx.config import Config
from pyvlx.frame_password_enter import FramePasswordEnterRequest
#from pyvlx.frame_get_scene_list import FrameGetSceneListRequest
#from pyvlx.frame_discover_nodes import FrameDiscoverNodesRequest
from pyvlx.frame_get_node_information import FrameGetNodeInformationRequest
from pyvlx.connection import Connection


async def wait(count, seconds):
    """Wait specified seconds for count times."""
    for i in range(count):
        print("Wait for bus responses: {} of {}".format(i+1, count))
        await asyncio.sleep(seconds)


async def demo(config, loop):
    """Demonstrate functionality of PyVLX."""
    conn = Connection(loop=loop, config=config)
    await conn.connect()
    #conn.write(FramePasswordEnterRequest(password="wrong"))
    #await asyncio.sleep(1)
    conn.write(FramePasswordEnterRequest(password=config.password))
    await asyncio.sleep(1)
    # conn.write(FrameDiscoverNodesRequest())
    # conn.write(FrameGetSceneListRequest())
    conn.write(FrameGetNodeInformationRequest(node_id=0))
    await asyncio.sleep(1)
    conn.write(FrameGetNodeInformationRequest(node_id=1))
    await asyncio.sleep(1)
    conn.write(FrameGetNodeInformationRequest(node_id=2))
    #await asyncio.sleep(1)
    #conn.write(FrameGetNodeInformationRequest(node_id=3))
    #await asyncio.sleep(1)
    #conn.write(FrameGetNodeInformationRequest(node_id=4))
    #await asyncio.sleep(1)
    #conn.write(FrameGetNodeInformationRequest(node_id=5))
    #await asyncio.sleep(1)
    #conn.write(FrameGetNodeInformationRequest(node_id=6))
    #await asyncio.sleep(1)
    #conn.write(FrameGetNodeInformationRequest(node_id=7))
    await wait(5, 1)


async def main(loop):
    """Do main."""
    config = Config(host="192.168.2.102", port=51200, password='velux123')
    await demo(loop=loop, config=config)


# pylint: disable=invalid-name
if __name__ == '__main__':
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main(LOOP))
    # LOOP.run_forever()
    LOOP.close()
