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

    await pyvlx.load_nodes()
    for node in pyvlx.nodes:
        print(node)

    await pyvlx.nodes['Treppe'].open()
    await pyvlx.nodes['Treppe'].close()


if __name__ == '__main__':
    # pylint: disable=invalid-name
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main(LOOP))
    # LOOP.run_forever()
    LOOP.close()
