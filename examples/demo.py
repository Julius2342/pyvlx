"""Just a demo of the new PyVLX module."""
import asyncio
from pyvlx import PyVLX, Position


async def main(loop):
    """Demonstrate functionality of PyVLX."""
    pyvlx = PyVLX('pyvlx.yaml', log_frames=True, loop=loop)
    # Alternative:
    # pyvlx = PyVLX(host="192.168.2.127", password="velux123", loop=loop)

    # Runing scenes:
    await pyvlx.load_scenes()
    await pyvlx.scenes["All Windows Closed"].run()

    # Changing position of windows:
    await pyvlx.load_nodes()
    await pyvlx.nodes['Bath'].open()
    await pyvlx.nodes['Bath'].close()
    await pyvlx.nodes['Bath'].set_position(Position(position_percent=45))

    # Changing of on-off switches:
    # await pyvlx.nodes['CoffeeMaker'].set_on()
    # await pyvlx.nodes['CoffeeMaker'].set_off()

    # You can easily rename nodes:
    # await pyvlx.nodes["Window 10"].rename("Window 11")

    await pyvlx.disconnect()

if __name__ == '__main__':
    # pylint: disable=invalid-name
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main(LOOP))
    # LOOP.run_forever()
    LOOP.close()
