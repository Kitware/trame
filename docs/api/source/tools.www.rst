wwww: Static Web Client generator
===================================================

This small utility let you run a command line to generate a static directory
that you can serve with Nginx/Apache for your trame application.

You just need to provide the `--output` directory if you don't want to add
to the current directory along with the list of module names that your application
is using or plan to use.

The following command line provide an example of what it could look like:

.. code-block:: bash

    python -m trame.tools.www --output ./www-content www vuetify vtk plotly

Here is a list of known modules (so far)

* deckgl
* markdown
* matplotlib
* paraview
* plotly
* router
* trame
* vega
* vtk
* vuetify
* www <-- Main client code