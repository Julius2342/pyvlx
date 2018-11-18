PyVLX - controling VELUX windows with Python
============================================

[![Build Status](https://travis-ci.org/Julius2342/pyvlx.svg?branch=master)](https://travis-ci.org/Julius2342/pyvlx)

PyVLX uses the Velux KLF 200 interface to control io-Homecontrol devices, e.g. Velux Windows.

NEW API!!!
----------

Velux published a new API. Connecting to the new API is still work in progress.

The [current state can be found here](https://github.com/Julius2342/pyvlx/blob/master/examples/demo.py).

This wrapper can already:

* Login to KLF 200 with password
* Retrieve scene list
* Run/activate scene
* Set position of specific window (50%)

Stay tuned!

<!--
Installation
------------

PyVLX can be installed via:

```bash
pip3 install pyvlx
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

    # logout from device
    await pyvlx.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

-->




