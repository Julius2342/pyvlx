PyVLX - controling VELUX windows with Python
============================================

[![CI](https://github.com/Julius2342/pyvlx/actions/workflows/ci.yml/badge.svg)](https://github.com/Julius2342/pyvlx/actions/workflows/ci.yml)

PyVLX uses the Velux KLF 200 interface to control io-Homecontrol devices, e.g. Velux Windows.

Please note: The KLF 200 is discontinued by Velux and even though the KLF 150 is marketed as its replacement device, it does **not** work with this library (it is missing the local API) unfortunately. 

Installation
------------

PyVLX can be installed via:

```bash
pip3 install pyvlx
```

Home Assistant Plugin
---------------------

PyVLX is used within [Home Assistant](https://www.home-assistant.io/integrations/velux/). The HA Velux integration can be added in the HA UI.

*Please note that to connect you need to use the WiFi password, not the web login.*

For debugging frames enable debug logging for the Velux integration in the HA UI.

Basic Operations
----------------

```python
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
```
