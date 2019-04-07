"""Just a demo of the new PyVLX module."""
import asyncio
import logging

from pyvlx import PyVLX
from pyvlx.log import PYVLXLOG
from pyvlx.house_status_monitor import house_status_monitor_enable


async def main(loop):
    """Logging daemon."""
    # Setting debug
    PYVLXLOG.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    PYVLXLOG.addHandler(stream_handler)

    # Connecting to KLF 200
    pyvlx = PyVLX('pyvlx.yaml', loop=loop)
    await pyvlx.connect()
    await pyvlx.update_version()
    await house_status_monitor_enable(pyvlx=pyvlx)

    # and wait :)
    await asyncio.sleep(30)

    # Cleanup, KLF 200 is terrible in handling lost connections
    await pyvlx.disconnect()


if __name__ == '__main__':
    # pylint: disable=invalid-name
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main(LOOP))
    LOOP.close()
