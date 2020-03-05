PyVLX - controling VELUX windows with Python
============================================

[![Build Status](https://travis-ci.org/Julius2342/pyvlx.svg?branch=master)](https://travis-ci.org/Julius2342/pyvlx)

PyVLX uses the Velux KLF 200 interface to control io-Homecontrol devices, e.g. Velux Windows.

Installation
------------

PyVLX can be installed via:

```bash
pip3 install pyvlx
```

Home Assistant Plugin
---------------------

PyVLX is used within [Home-Assistant](https://www.home-assistant.io/components/velux/). To enable it add the following lines to your ~/.home-assistant/configuration.yml:

```yaml
velux:
    host: "192.168.0.0"
    password: "1ADwl48dka"
```

*Please note that this uses the WiFi password, not the web login.*

For debugging frames add:

```yaml
logger:
  default: warning
  logs:
    homeassistant.components.velux: debug
    pyvlx: debug
```


Basic Operations
----------------

```python
"""Just a demo of the new PyVLX module."""
import asyncio
from pyvlx import PyVLX, Position


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
    # pylint: disable=invalid-name
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(main(LOOP))
    # LOOP.run_forever()
    LOOP.close()
```


