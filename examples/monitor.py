"""Just a demo of the new PyVLX module."""
import asyncio
import logging

from pyvlx import PyVLX


async def main(loop):
    """Log packets from Bus."""
    # Setting debug
    logging.basicConfig(level=logging.DEBUG)

    # Connecting to KLF 200
    pyvlx = PyVLX('pyvlx.yaml', loop=loop)
    await pyvlx.load_scenes()
    await pyvlx.load_nodes()

    # and wait, increase this timeout if you want to
    # log for a longer time.:)
    await asyncio.sleep(90)

    # Cleanup, KLF 200 is terrible in handling lost connections
    await pyvlx.disconnect()


if __name__ == '__main__':
    myloop = asyncio.new_event_loop()
    myloop.run_until_complete(main(myloop))
    myloop.close()
