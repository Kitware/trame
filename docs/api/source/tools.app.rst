Application file generator
==============================

This small utility let you run a command line to generate a derived HTML file
from the original `static web client output <https://trame.readthedocs.io/en/latest/tools.www.html>`_ 
to run a specific application from a launcher configuration.

In order to use that tool, you will need to provide the path of the base
application to use as template along with the name of the application you
aim to run from your launcher config.
This tool will then create a new HTML file within the same directory that
will start the provided application name rather than the default "trame" one.


.. code-block:: bash

    python -m trame.tools.app --input ./www-content --name MySuperApp
    # => create file MySuperApp.html from ./www-content/index.html
