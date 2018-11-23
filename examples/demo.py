"""Just a demo of the new PyVLX module."""
import asyncio

from pyvlx import PyVLX

async def main(loop):
    """Demonstrate functionality of PyVLX."""
    pyvlx = PyVLX('pyvlx.yaml', log_frames=True, loop=loop)
    # Alternative:
    # pyvlx = PyVLX(host="192.168.2.127", password="velux123", loop=loop)

    await pyvlx.connect()
    await pyvlx.load_scenes()
    await pyvlx.scenes["All Windows Closed"].run()

    # BACKUP:
    #
    # get_node_information = GetNodeInformation(connection=connection, node_id=6)
    # await get_node_information.do_api_call()
    # print(get_node_information.node)
    #
    # from pyvlx.get_node_information import GetNodeInformation
    # from pyvlx.get_all_nodes_information import GetAllNodesInformation
    # get_all_nodes_information = GetAllNodesInformation(connection=pyvlx.connection)
    # await get_all_nodes_information.do_api_call()
    # print(get_all_nodes_information.nodes)
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


if __name__ == '__main__':
    # pylint: disable=invalid-name
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main(LOOP))
    # LOOP.run_forever()
    LOOP.close()
