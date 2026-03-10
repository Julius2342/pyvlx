"""Just a demo of the new PyVLX module."""
import asyncio

from pyvlx import Position, PyVLX


async def main() -> None:
    """Demonstrate functionality of setting a limit."""
    pyvlx = PyVLX('pyvlx.yaml')

    # Runing scenes:
    await pyvlx.load_nodes()
    await pyvlx.nodes['Bath'].set_position_limitations(position_max=Position(position_percent=30))
    await pyvlx.nodes['Bath'].close()
    await pyvlx.nodes['Bath'].clear_position_limitations()
    await pyvlx.nodes['Bath'].close()

    await pyvlx.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
