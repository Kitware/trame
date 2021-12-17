from trame.internal import (
  change, Controller, flush_state, get_cli_parser, get_state, get_version,
  is_dirty, is_dirty_all, port, start, State, stop, trigger, update_state
)
from trame.layouts import update_layout

__version__ = get_version()

state = State()
"""This object provides pythonic access to the state

For instance, these getters are the same:

>>> field, = get_state("field")
>>> field = state.field

As are these setters:

>>> update_state("field", value)
>>> state.field = value

``get_state()`` should be used instead if more than one argument is to be
passed, and ``update_state()`` should be used instead to specify additional
arguments (e.g. ``force=True``).

The state may also be accessed and updated similar to dictionaries:

>>> value = state["field"]
>>> state["field"] = value
>>> state.update({"field": value})

This object may be imported via

>>> from trame import state
"""

controller = Controller()
"""The controller is a container for function proxies

The function proxies may be used as callbacks even though the function has
not yet been defined. The function may also be re-defined. For example:

>>> from trame import controller as ctrl
>>> layout = SinglePage("Controller test")
>>> with layout.toolbar:
...     vuetify.VSpacer()
...     vuetify.VBtn("Click Me", click=ctrl.on_click)  # not yet defined

>>> ctrl.on_click = lambda: print("Hello, Trame!")  # on_click is now defined

This can be very useful for large projects where the functions may be defined
in separate files after the UI has been constructed, or for re-defining
callbacks when conditions in the application change.
"""

__all__ = [
    # Order these how we want them to show up in the docs

    # Server-related
    "start",
    "stop",
    "port",

    # State-related
    "state",
    "update_state",
    "get_state",
    "flush_state",
    "is_dirty",
    "is_dirty_all",
    "change",

    # Trigger-related
    "trigger",
    "controller",

    # Layout-related
    "update_layout",

    # CLI-related
    "get_cli_parser",

    # These are not exposed in the docs
    "__version__",
]
