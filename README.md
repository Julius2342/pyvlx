PyVLX - controling VELUX windows with Python
============================================

[![Build Status](https://travis-ci.org/Julius2342/pyvlx.svg?branch=master)](https://travis-ci.org/Julius2342/pyvlx)

PyVLX uses the Velux KLF 200 interface to control Velux Windows.

Installation
------------

PyVLX can be installed via:

```bash
pip3 install pyvlx
pip3 install aiohttp
```


Basic Operations
----------------

```python
from pyvlx import PyVLX
import asyncio

async def main():
    pyvlx = PyVLX('pyvlx.yaml') 
    # Alternative: pyvlx = PyVLX(host='192.168.2.127',password='velux123')

    await pyvlx.load_devices()
    print(pyvlx.devices[1])
    print(pyvlx.devices['Window 4'])

    await pyvlx.load_scenes()
    print(pyvlx.scenes[0])
    print(pyvlx.scenes['Open all windows'])

    # opening/ closing windows by running scenes, yay!
    await pyvlx.scenes[1].run()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```


