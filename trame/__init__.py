import os
import inspect

from pywebvue import App

NEXT_TRIGGER_ID = 0
TRIGGER_MAP = {}
NEXT_APP_ID = 0
APPS = {}
APP_STACK = []
APP = None


def base_directory():
    frame = inspect.stack()[2]
    module = inspect.getmodule(frame[0])
    if module is None:
        return os.getcwd()
    return os.path.abspath(os.path.dirname(module.__file__))


# -----------------------------------------------------------------------------
# App management
# -----------------------------------------------------------------------------


def get_app_instance():
    """
    Return the current active PyWebVue App instance and
    create one if none was available yet.

    (This method is meant for advanced users and should not be needed for most)
    """
    global APP
    if APP:
        return APP

    create_app("Trame Created Application")
    return APP


# -----------------------------------------------------------------------------


def activate_app(app_id):
    """
    When multiple application instances are use this method allow to toggle
    which app should be current based on the app_id.

    (This method is meant for advanced users and should not be needed for most)
    """
    global APP_STACK, APPS, APP
    if app_id in APPS:
        APP_STACK.append(app_id)
        APP = APPS[app_id]
        return True

    return False


# -----------------------------------------------------------------------------


def deactivate_app():
    """
    When multiple application instances are use this method allow to activate
    the previously activated app by desactivating the current one.

    (This method is meant for advanced users and should not be needed for most)
    """
    global APP_STACK, APPS, APP
    if len(APP_STACK):
        app_ip = APP_STACK.pop()
        APP = None
        if len(APP_STACK):
            activate_app(APP_STACK[-1])
        return app_ip


# -----------------------------------------------------------------------------


def create_app(name):
    """
    This will create a PyWebVue application instance,
    activate it and return its app_id so you could
    desactivate and reactivate it later.

    (This method is meant for advanced users and should not be needed for most)
    """
    global NEXT_APP_ID, APPS
    NEXT_APP_ID += 1
    _app_id = f"trame_app_{NEXT_APP_ID}"
    APPS[_app_id] = App(name)
    activate_app(_app_id)
    return _app_id


# -----------------------------------------------------------------------------
# Server start
# -----------------------------------------------------------------------------


def start(layout=None, name=None, favicon=None, on_ready=None, port=None):
    """
    Start web server for serving your application

    Parameters
    ----------
    layout  : None or str or trame.layouts.*
        UI content that should be used for your application
    name    : None or str
        "Title" that you can see in your tab browser.
        This will be filled automatically if a trame.layouts.* layout was provided.
    favicon : None or str
        Relative path to a png image that should be used as favicon
    port    : None or Number
        Port on which the server should run on
    on_ready: None or function
        Function called once the server is ready
    """
    app = get_app_instance()
    if name:
        app.name = name

    if favicon:
        app.favicon = os.path.join(base_directory(), favicon)

    if layout:
        if isinstance(layout, str):
            app.layout = layout
        else:
            app.name = layout.name
            app.layout = layout.html
    else:
        tpl_path = os.path.join(base_directory(), "template.html")
        if os.path.exists(tpl_path):
            app.layout = tpl_path

    app.on_ready = on_ready
    app.run_server(port=port)


# -----------------------------------------------------------------------------
# App state management
# -----------------------------------------------------------------------------


def update_state(key, value=None):
    """
    Method updating current application state that is shared with the Web UI
    """
    _app = get_app_instance()
    _app.set(key, value)


# -----------------------------------------------------------------------------


def get_state(*names):
    """
    Return a list of the values of the given state keys

    Paramters
    ---------
    *names : *str
        List of name of state values to retreive

    Returns
    -------
    [any, ...]
        List of value matching the requested state property names
    """
    _app = get_app_instance()
    results = []
    for name in names:
        results.append(_app.get(name))

    return results


def update_layout(layout):
    """
    Dynamically update current application layout

    Parameters
    ----------
    layout  : str or trame.layouts.*
        UI content that should be used for your application
    """
    _app = get_app_instance()
    _app.layout = layout if isinstance(layout, str) else layout.html


# -----------------------------------------------------------------------------
# Generate trigger helper
# -----------------------------------------------------------------------------


def trigger_key(_fn):
    """
    Providing a function, a generated trigger name will be returned

    Parameters
    ----------
    _fn : function
        Function that we would like to be able to call from the client side.

    Returns
    -------
    str
        Unique name that can be used for a trigger to call that function
    """
    # Return precomputed key
    global TRIGGER_MAP, NEXT_TRIGGER_ID
    if _fn in TRIGGER_MAP:
        return TRIGGER_MAP[_fn]

    # Compute unique trigger key
    NEXT_TRIGGER_ID += 1
    key = f"trigger_{NEXT_TRIGGER_ID}"
    TRIGGER_MAP[_fn] = key

    # Register function trigger
    _app = get_app_instance()
    _app.trigger(key)(_fn)

    return key


# -----------------------------------------------------------------------------
# @decorators
# -----------------------------------------------------------------------------


def change(*_args, **_kwargs):
    """
    @change decorator allow to register a function in a way that it will be
    automatically called when the given list of state names get modified.

    The decorated function is passed the full state as *kwarg when possible.
    This means you should have a method profile similar to `fn(..., *kwargs)`

    Parameters
    ----------
    *_args : *str
        List of name that your function should listen to
    """
    _app = get_app_instance()
    return _app.change(*_args, **_kwargs)


# -----------------------------------------------------------------------------


def trigger(name):
    """
    @trigger decorator allow to register a function as a trigger with a given name

    Parameters
    ----------
    name : str
        Name of the trigger
    """
    _app = get_app_instance()
    return _app.trigger(name)
