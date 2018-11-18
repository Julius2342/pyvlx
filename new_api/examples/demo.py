"""Just a demo of the new PyVLX module."""
import asyncio
from pyvlx.config import Config
# from pyvlx.frame_discover_nodes import FrameDiscoverNodesRequest
# from pyvlx.frame_get_node_information import FrameGetNodeInformationRequest
# from pyvlx.frame_activate_scene import FrameActivateSceneRequest
# from pyvlx.frame_command_send import FrameCommandSendRequest
from pyvlx.connection import Connection
from pyvlx.login import Login
from pyvlx.scene_list import SceneList


async def wait(count, seconds):
    """Wait specified seconds for count times."""
    for i in range(count):
        print("Wait for bus responses: {} of {}".format(i+1, count))
        await asyncio.sleep(seconds)


async def demo(config, loop):
    """Demonstrate functionality of PyVLX."""
    connection = Connection(loop=loop, config=config)
    await connection.connect()

    login = Login(connection=connection, password=config.password)
    await login.do_api_call()

    if login.success:
        scene_list = SceneList(connection=connection)
        await scene_list.do_api_call()
        print(scene_list.scenes)
    return

    # conn.write(FrameGetNodeInformationRequest(node_id=0))
    # await asyncio.sleep(1)

    # conn.write(FrameCommandSendRequest(node_ids=[0], position=100, session_id=5))
    # await asyncio.sleep(1)
    # conn.write(FrameCommandSendRequest(node_ids=[1], position=100, session_id=6))
    # await asyncio.sleep(1)
    # conn.write(FrameCommandSendRequest(node_ids=[2], position=100, session_id=7))
    # await asyncio.sleep(1)
    # conn.write(FrameCommandSendRequest(node_ids=[3], position=100, session_id=8))
    # await asyncio.sleep(1)
    # conn.write(FrameCommandSendRequest(node_ids=[4], position=100, session_id=9))
    # await wait(15, 5)

    # conn.write(FrameDiscoverNodesRequest())
    # conn.write(FrameGetSceneListRequest())

    # conn.write(FrameActivateSceneRequest(scene_id=3, session_id=23))
    # conn.write(FrameGetNodeInformationRequest(node_id=0))
    # await asyncio.sleep(1)
    # conn.write(FrameGetNodeInformationRequest(node_id=1))
    # await asyncio.sleep(1)
    # conn.write(FrameGetNodeInformationRequest(node_id=2))
    # await asyncio.sleep(1)
    # conn.write(FrameGetNodeInformationRequest(node_id=3))
    # await asyncio.sleep(1)
    # conn.write(FrameGetNodeInformationRequest(node_id=4))
    # await asyncio.sleep(1)
    # conn.write(FrameGetNodeInformationRequest(node_id=5))
    # await asyncio.sleep(1)
    # conn.write(FrameGetNodeInformationRequest(node_id=6))
    # await asyncio.sleep(1)
    # conn.write(FrameGetNodeInformationRequest(node_id=7))
    # await wait(5, 5)


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
