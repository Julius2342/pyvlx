"""Just a demo of the PyVLX module."""
import asyncio
import logging

from pyvlx import Position, PyVLX


async def main(loop):
    """Demonstrate functionality of PyVLX."""
    pyvlx = PyVLX('pyvlx.yaml', loop=loop)
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
    logging.basicConfig(level=logging.DEBUG)

    myloop = asyncio.new_event_loop()
    myloop.run_until_complete(main(myloop))
    # loop.run_forever()
    myloop.close()
