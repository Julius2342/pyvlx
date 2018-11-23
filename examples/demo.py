"""Just a demo of the new PyVLX module."""
import asyncio
from pyvlx.config import Config
from pyvlx.connection import Connection
from pyvlx.login import Login
from pyvlx.scene_list import SceneList
from pyvlx.get_node_information import GetNodeInformation
from pyvlx.get_all_nodes_information import GetAllNodesInformation


async def frame_received_callback(frame):
    """Log frame for better debugging."""
    # print("Frame: ", frame)
    # pylint: disable=unused-argument
    pass


async def demo(config, loop):
    """Demonstrate functionality of PyVLX."""
    connection = Connection(loop=loop, config=config)
    connection.register_frame_received_cb(frame_received_callback)
    await connection.connect()

    login = Login(connection=connection, password=config.password)
    await login.do_api_call()

    if not login.success:
        print("Unable to login. Giving up""")
        return

    scene_list = SceneList(connection=connection)
    await scene_list.do_api_call()
    print(scene_list.scenes)

    get_node_information = GetNodeInformation(connection=connection, node_id=6)
    await get_node_information.do_api_call()
    print(get_node_information.node)

    print("---------------------------------------")

    get_all_nodes_information = GetAllNodesInformation(connection=connection)
    await get_all_nodes_information.do_api_call()
    print(get_all_nodes_information.nodes)

    # from pyvlx.activate_scene import ActivateScene
    # activate_scene = ActivateScene(connection=connection, scene_id=2)
    # await activate_scene.do_api_call()

    # activate_scene = ActivateScene(connection=connection, scene_id=0)
    # await activate_scene.do_api_call()

    # BACKUP:
    #
    # from pyvlx.frame_command_send import FrameCommandSendRequest
    # connection.write(FrameGetNodeInformationRequest(node_id=0))
    # await asyncio.sleep(1)
    # connection.write(FrameCommandSendRequest(node_ids=[0], position=100, session_id=5))
    # await asyncio.sleep(1)
    # connection.write(FrameCommandSendRequest(node_ids=[1], position=100, session_id=6))
    # await asyncio.sleep(1)
    # connection.write(FrameCommandSendRequest(node_ids=[2], position=100, session_id=7))
    # await asyncio.sleep(1)
    # connection.write(FrameCommandSendRequest(node_ids=[3], position=100, session_id=8))
    # await asyncio.sleep(1)
    # connection.write(FrameCommandSendRequest(node_ids=[4], position=100, session_id=9))


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
