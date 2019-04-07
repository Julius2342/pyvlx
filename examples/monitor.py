"""Just a demo of the new PyVLX module."""
import asyncio
import logging

from pyvlx import PyVLX
from pyvlx.log import PYVLXLOG


async def main(loop):
    """Log packets from Bus."""
    # Setting debug
    PYVLXLOG.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    PYVLXLOG.addHandler(stream_handler)

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
    # pylint: disable=invalid-name
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main(LOOP))
    LOOP.close()
