VTK rendering backend information
====================================

This utility function/app depends on VTK and will report the rendering capabilities available.

This aim to be used for debugging cloud deployments either by running a command line within the deployment environment or as a standalone trame application. 

.. code-block:: bash

    # print report to stdout
    python -m trame.tools.vtk --stdout

    # start trame app
    python -m trame.tools.vtk


You can find its configuration as standalone application `here <https://github.com/Kitware/trame/tree/master/examples/deploy/docker/RenderingInfo>`_ 