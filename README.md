PyVLX - controling VELUX windows with Python
============================================

[![Build Status](https://travis-ci.org/Julius2342/pyvlx.svg?branch=master)](https://travis-ci.org/Julius2342/pyvlx)

PyVLX uses the Velux KLF 200 interface to control Velux Windows.

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


If you are VELUX:
-----------------

Hi VELUX Team,

the VELUX KLF 200 is a great device. But there is room for improvement. Here is my wishlist:

  * Make devices directly accessible, which includes *reading and setting the state of windows and shutters*. A direct access to the rain sensor would also be nice.
  * Fix the *security issue* mentioned [here](https://gist.github.com/Julius2342/6282ded9f527e762ea50f42c2c439a1a)! 
  * Allow more than one *simultaneous connections*.
  * Use *https* instead of http for connections.
  * Fix the Bug mentioned [here](https://github.com/Julius2342/pyvlx/blob/master/pyvlx/interface.py#L124) which is an indication of scruffy buffer handling.

:-)





