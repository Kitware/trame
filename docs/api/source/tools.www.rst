Static Web Client generator
===================================================

This small utility let you run a command line to generate a static directory
that you can serve with Nginx/Apache for your trame application.

You just need to provide the `--output` directory if you don't want to add
to the current directory. Then you can provide the list of module names that your application
is using or plan to use. If no modules are provided, the executable will do a lookup in `trame.modules.*` and enable all of the them.
The initialization order is not guarante.

The following command line provide an example of what it could look like:

.. code-block:: bash

    python -m trame.tools.www --output ./www-content www vuetify vtk plotly

Or you can also do the following as only the pieces needed will be downloaded by the client when needed.

.. code-block:: bash

    mkdir ./www-all
    cd www-all
    python -m trame.tools.www

Here is a list of known modules: deckgl, markdown, matplotlib, paraview, plotly, router, trame, vega, vtk, vuetify, www (main client)

With the add-on support of vue3 backend, you can now provide which client you want to enable by providing `--client-type vue2` or `--client-type vue3`.
Keep in mind that vue2 UI template are not 100% compatible with their vue3 counter part...