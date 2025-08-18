Update launcher retry array
==============================

This small utility let you run a command line to update an existing HTML file
with a new launcher-retry content.

In order to use that tool, you will need to provide the path of the base
application to use as template along with the content of the launcher-retry.
This tool will then update the HTML file provided.


.. code-block:: bash

    python -m trame.tools.retry --input ./www-content/index.html --retry "[3000, 2000, 1000]"
    # => Update ./www-content/index.html using data-launcher-retry="[3000, 2000, 1000]" instead of the default empty array.
