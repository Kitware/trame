import os
import asyncio
import inspect

from pywebvue import App

from trame.utils.version import get_version

__version__ = get_version()


NEXT_TRIGGER_ID = 0
TRIGGER_MAP = {}
NEXT_APP_ID = 0
APPS = {}
APP_STACK = []
APP = None

BASE_DIRECTORY = None


def base_directory():
    global BASE_DIRECTORY
    if BASE_DIRECTORY:
        return BASE_DIRECTORY

    frame = inspect.stack()[2]
    module = inspect.getmodule(frame[0])
    if module is None:
        BASE_DIRECTORY = os.getcwd()
    else:
        BASE_DIRECTORY = os.path.abspath(os.path.dirname(module.__file__))
    return BASE_DIRECTORY


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


def start(layout=None, name=None, favicon=None, on_ready=None, port=None, debug=False):
    """
    Start the Trame web server for your application

    :param layout: UI content that should be used for your application
    :type layout: None | str | trame.layouts.*
    :param name: "Title" that you can see in your tab browser. This will be filled automatically if a trame.layouts.* layout was provided.
    :type name: None | str
    :param favicon: Relative path to a png image that should be used as favicon
    :type favicon: None | str
    :param port: Port on which the server should run on. Default is 8080. This overrides a port from the command line ``--port/-p`` option.
    :type port: None | Number
    :param on_ready: Function called once the server is ready
    :type on_ready: None | function
    :param debug: Whether to print debugging information
    :type debug: bool

    >>> start(on_ready=initialize)
    """
    app = get_app_instance()
    app.cli_parser.add_argument("--server", help="Prevent your browser from opening at startup", action='store_true')
    app._debug = debug
    app.on_ready = print_server_info()
    if name:
        app.name = name

    if layout:
        if isinstance(layout, str):
            app.layout = layout
        else:
            app.name = layout.name
            app.layout = layout.html
            if layout.favicon:
                app.favicon = layout.favicon
            if layout.on_ready:
                app.on_ready = print_server_info(layout.on_ready)
    else:
        tpl_path = os.path.join(base_directory(), "template.html")
        if os.path.exists(tpl_path):
            app.layout = tpl_path
        else:
            print("Error: We could not find your layout or template.html file.")

    if on_ready:
        app.on_ready = print_server_info(on_ready)

    if favicon:
        app.favicon = os.path.join(base_directory(), favicon)

    # Dev validation
    validate_key_names()

    app.run_server(port=port)


# -----------------------------------------------------------------------------
# App state management
# -----------------------------------------------------------------------------


def update_state(key, value=None):
    """
    Method updating current application state that is shared with the Web UI

    :param key: The key for the value we wish to update
    :type key: str
    :param value: The new value
    :type value: Any

    >>> update_state("workload_finished",  True)

    """
    _app = get_app_instance()
    _app.set(key, value)
    return value


# -----------------------------------------------------------------------------


def get_state(*names):
    """
    Return a dictionary of all state keys, or a list of the values of the given state keys

    :param names: List of names of state values to retreive
    :type names: list[str]
    :rtype: dict[str, Any] | List[Any]
    :returns: Either a dict of all state keys or a list of values matching the given state property names

    >>> full_state = get_state()
    >>> full_state.get("greeting")
    "Hello"

    >>> greeting, name  = get_state("greeting", "name")
    >>> f'{greeting}, {name}!'
    "Hello, Trame!"

    >>> greeting, = get_state("greeting")
    >>> greeting
    "Hello"


    """
    _app = get_app_instance()

    if len(names):
        results = []
        for name in names:
            results.append(_app.get(name))
        return results

    return _app.state


def update_layout(layout):
    """
    Dynamically update current application layout

    :param layout: UI content for your application
    :type layout: str | trame.layouts.*

    >>> layout.title.content = "Workload finished!"
    >>> update_layout(layout)

    """
    _app = get_app_instance()
    _app.layout = layout if isinstance(layout, str) else layout.html


def enable_module(module):
    """
    Load a PyWebVue module

    :param module: The module to load
    """
    _app = get_app_instance()
    _app.enable_module(module)


def js_call(ref=None, method=None, args=[]):
    """Python call method on JS element"""
    _app = get_app_instance()
    _app.update(ref=ref, method=method, args=args)


def js_property(ref=None, property=None, value=None):
    """Python update property on JS element"""
    _app = get_app_instance()
    _app.update(ref=ref, property=property, value=value)


# -----------------------------------------------------------------------------
# App CLI handling
# -----------------------------------------------------------------------------


def get_cli_parser():
    """Run or add args to CLI parser

    :returns: Parser from argparse

    >>> parser = get_cli_parser()
    >>> parser.add_argument("-o", "--output", help="Working directory")
    >>> args = parser.parse_known_args()
    >>> print(args.output)
    """
    _app = get_app_instance()
    return _app.cli_parser


def flush_state(*args):
    """
    Force push selected keys of the server state to the client.

    :param args: Which keys to flush
    :type args: list[str]

    >>> flush_state('myNestedDict')
    """
    _app = get_app_instance()
    return _app.flush_state(*args)


def is_dirty(*args):
    """
    See which key in an @change has been modified.

    :param args: Which keys to check for modification
    :type args: list[str]
    :return: True if any of the keys in `args` are modified.
    :rtype: bool

    >>> @change('sound_settings', 'picture_settings')
    ... def show_changed_settings(sound_settings, picture_settings, **kwargs):
    ...     if is_dirty('sound_settings'):
    ...         print(sound_settings)
    ...     if is_dirty('picture_settings'):
    ...         print(picture_settings)

    """
    _app = get_app_instance()
    return _app.is_dirty(*args)


def is_dirty_all(*args):
    """
    See whether all keys in an @change have been modified.

    :param args: Which keys to check for modification
    :type args: list[str]
    :return: True if all of the keys in `args` are modified.
    :rtype: bool

    >>> @change('sound_settings', 'picture_settings')
    ... def save_changed_settings(sound_settings, picture_settings, **kwargs):
    ...     if is_dirty_all('sound_settings', 'picture_settings'):
    ...         print("Cannot save both sound and picture settings at once")
    ...         raise

    """
    _app = get_app_instance()
    return _app.is_dirty_all(*args)


# -----------------------------------------------------------------------------
# Generate trigger helper
# -----------------------------------------------------------------------------


def trigger_key(_fn):
    """
    Providing a function, a generated trigger name will be returned

    Parameters
    ----------
    :param _fn: Function that we would like to be able to call from the client side.
    :type _fn: function
    :returns: Unique name that can be used for a trigger to call that function
    :rtype: str
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
    The @change decorator allows us to register a function so that it will be
    automatically called when the given list of state names gets modified.

    The decorated function is passed the full state as ``**kwargs`` when possible.
    This means you should have a method profile similar to ``fn(..., **kwargs)``

    :param _args: List of names that your function should listen to
    :type _args: `list[str]`

    >>> @change('settings')
    ... def show_settings(settings, **kwargs):
    ...     print(settings)

    """
    _app = get_app_instance()
    return _app.change(*_args, **_kwargs)


# -----------------------------------------------------------------------------


def trigger(name):
    """
    @trigger decorator allows you to register a function as a trigger with a given name.

    Parameters
    ----------
    :param name: Name which this trigger function should listen to.
    :type name: str

    >>> @trigger('blue_button_clicked')
    ... def log_clicks():
    ...     print("The blue button was clicked")

    """
    _app = get_app_instance()
    return _app.trigger(name)


# -----------------------------------------------------------------------------
# Dev tools
# -----------------------------------------------------------------------------

def print_server_info(_fn=None):
    def ready(**kwargs):
        parser = get_cli_parser()
        args = parser.parse_known_args()[0]
        local_url = f"http://{args.host}:{args.port}/"

        import socket
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)

        print()
        print(" App running at:")
        print(f" - Local:   {local_url}")
        print(f" - Network: http://{host_ip}:{args.port}/")
        print()
        print("Note that for multi-users you need to use and configure a launcher.")

        if _fn:
            try:
                _fn(**kwargs)
            except TypeError:
                _fn()

        if not args.server:
            import webbrowser
            import asyncio
            loop = asyncio.get_event_loop()
            loop.call_later(0.1, lambda: webbrowser.open(local_url))
            print("And to prevent your browser from opening, add '--server' to your command line.")
        print()

    return ready

def validate_key_names():
    _app = get_app_instance()
    errors = []
    for key in _app.state:
        if " " in key:
            errors.append(f"  - '{key}'")

    if errors:
        print("=" * 60)
        print(
            f"Warning: {len(errors)} key{'s' if len(errors) > 1 else ''} inside your state contains spaces"
        )
        print("=" * 60)
        for message in errors:
            print(message)
        print("=" * 60)
