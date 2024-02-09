Python serve utility
====================================

This executable allow you to run a trame application as a single process for multiple users. 
As opposed to the regular launcher within our docker setup, this will run a single process
and execute each session within its own trame server as an asynchronous task in Python.

This tools is not meant to be used on a production server but could be enough for multi-users demos.

Also this assume that your trame application is using a class construct which expect a server as argument. 

The default example can be executed as follow:

.. code-block:: bash

    python -m trame.tools.serve

The possible arguments are:
  - `--exec`: Trame app to serve (default: `trame.app.demo:Cone`) where `Cone`` is the class to instantiate from the `trame.app.demo` module.
  - `--host`: IP or hostname to serve on (default: `localhost`)
  - `--port`: Port to serve on (default: `8080`)
  - `--ws-heart-beat`: WebSocket heart beat in seconds (default: `30`)
  - `--ws-max-size`: WebSocket maximum message size in bytes (default: `10000000`)
