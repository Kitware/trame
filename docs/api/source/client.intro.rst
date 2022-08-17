Introduction
===================================================

Trame is driven by Python but sometime, JavaScript expression needs to be written.
This document aims to gather tools and utilities available on the "client side" for you to use.

State variables
---------------------------------------------------

The first thing you have access is obviously the various state variables that you've defined.

.. code-block:: python

    from trame.app import get_server

    server = get_server()
    state = server.state

    state.welcome = "hello"
    state.name = "seb"

    # ...
    with layout:
       vuetify.VTextField(v_model=("welcome",)) # welcome is a reactive variable that is linked to state.welcome from Python
       vuetify.VTextField(v_model=("name",))    # name is a reactive variable that is linked to state.name from Python


Methods available
---------------------------------------------------

On top of the state variables, a couple of methods are also available for you to use when needed.


.. function:: set(key, value)

    Given a variable name as a string you can set its value to something new like shown in the example below.

    :param key: The name of the state variable to set
    :type key: str


    :param value: The value to set that variable to


    .. code-block:: python

        vuetify.VTextField(v_model=("var_name", "a"))
        vuetify.VTextField(v_model=("var_value", "value"))
        vuetify.VBtn("Set value", click="set(var_name, var_value)")

.. function:: get(key=null)

    Given a variable name, its value will be returned. If nothing is provided, the full state will be returned as a dictionary.

    :param key: The name of the state variable to retrieve
    :type key: str

    :return: Return the value stored within that state variable

.. function:: setAll(obj={})

    Given an object, set all key/value pair into the state before flushing it.

    :param obj: Map gathering the set of key/value pair to update
    :type obj: {}


    .. code-block:: python

        vuetify.VBtn("Reset many vars", click="setAll({ a: 1, b: true, c: 'hello' })")


.. function:: flushState(...keys)

    Force push one or many local state variables to the server. This is especially useful when dynamically editing nested content.

    :param ...keys: Names of all the variables that needs to be push back to Python
    :type ...keys: str


    .. code-block:: python

        # ...
        state.slider_values = [1, 2, 3, 4]

        with layout:
            vuetify.VSlider(
                v_for="v, index in slider_values",
                key="index",
                v_model="slider_values[index]",
                change="flushState('slider_values')"
            )


.. function:: registerDecorator(...args)

    Used internally to register special serializers for exchanging data between Python and JS.

.. function:: trigger(name, args=[], kwargs={})

    Call a method from JavaScript to Python.

    :param name: Name of the trigger to execute
    :type name: str

    :param args: List of arguments to provide to the method call
    :type args: []

    :param kwargs: List of keyword arguments to provide to the method call
    :type kwargs: {}

    :returns: A promise matching the return value of the Python method.

    .. code-block:: python

        @ctrl.trigger("exec_prog")
        def exec_function(*args, **kwargs):
            print("exec_function", args, kwargs)

        # ...
        with layout:
            vuetify.VBtn("Exec", click="trigger('exec_prog', [1, 2, 3], { b: 2 })")

    or you can do

    .. code-block:: python

        def exec_function(*args, **kwargs):
            print("exec_function", args, kwargs)

        # ...
        with layout:
            vuetify.VBtn("Exec", click=(exec_function, "[1, 2, 3]", "{ b: 2 }"))

    and even


    .. code-block:: python

        def exec_function(*args, **kwargs):
            print("exec_function", args, kwargs)

        # ...
        with layout:
            vuetify.VBtn("Exec", click=f"trigger('{ctrl.trigger_name(exec_function)}', [1, 2, 3], { b: 2 })")


.. function:: getRef(name)

    Lookup a Vue.js reference within your template.

    :param name: Name of the ref to lookup
    :type name: str

    :returns: The reference to vue component with that ref

.. function:: execAction(action)

    This allow to call method or update a property on a given vue component using its ref.

    The action object can only be one of the two structures:

    .. code-block:: javascript

        action = {ref, type: 'method', method, args}
        action = {ref, type: 'property', property, value}




Variables available
---------------------------------------------------


.. js:data:: tts

    tts stands for "Template Time Stamp" which represent an integer that will only change when a trame layout is getting updated.

.. js:data:: utils

    This object aims to be editable by the user so custom helper functions could be used.
    By default, we currently `the following content <client.utils.html>`_.