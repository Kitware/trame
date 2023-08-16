Python widgets generator
====================================

This utility function takes a YAML api description of Vue.js library that expose components and generate the Python code for you.

The idea behind that YAML description is to capture all the pieces in a compact and efficient manner.

.. code-block:: bash

    python -m trame.tools.widgets --config ./api.yaml --output /path/to/fill


The configuration file should be as follow.

.. code-block:: yaml

    trame_{name}: # python package name
        module:
            {name}: # module name
                vue2:  # vue2 or vue3
                    scripts:
                        - https://url_to_javascript_file.js # fetch from URL
                        - ./relative/path/file.js           # copy from path
                        - name: new_file_name.js            # create from inline content
                          content: ...
                    styles: [] # url, path, inline content
                    vue_use: [] # list of Vue.use(...)
        widgets:
            {name}: # widget name
                directives: [] # list of directive to register globaly
                ComponentName: # python class name for vue component
                    help: ... # class doc string header
                    component: vue-component-name # component vue name
                    properties: # list of component properties
                      - name: prop_name
                        help: ... # help for doc string
                      - name: [prop_name_py, prop-name-js]
                        help: ... # help for doc string
                    events: # list of component events
                      - name: event_name
                        help: ... # help for doc string
                      - name: [event_name_py, event-name-js]
                        help: ... # help for doc string
                NextComponentName:
                    component: next-component-name
                    properties: []
                    events: []

This will generate the following file tree

.. code-block:: console

    .
    ├── trame
    │   ├── __init__.py
    │   ├── modules
    │   │   ├── __init__.py
    │   │   └── {name}.py
    │   └── widgets
    │       ├── __init__.py
    │       └── {name}.py
    └── trame_{name}
        ├── __init__.py
        ├── module
        │   ├── __init__.py
        │   └── {name}
        │       ├── __init__.py
        │       ├── vue2
        │       │   ├── url_to_javascript_file.js
        │       │   ├── file.js
        │       │   └── new_file_name.js
        │       ├── vue2.py
        └── widgets
            ├── __init__.py
            └── {name}.py
