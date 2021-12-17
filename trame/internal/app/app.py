from pywebvue import App

from trame.internal.utils import log_js_error


NEXT_APP_ID = 0
APPS = {}
APP_STACK = []
APP = None


# -----------------------------------------------------------------------------


def get_app_instance():
    """
    Return the current active PyWebVue App instance or
    create one if none were available yet

    (This method is meant for advanced users and should not be needed for most)
    """
    global APP
    if APP:
        return APP

    create_app("Application")
    return APP


# -----------------------------------------------------------------------------


def activate_app(app_id):
    """
    When multiple application instances are use this method allows you to
    toggle which app should be current based on the app_id.

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
    When multiple application instances are used, this method allows you to
    activate the previously activated app by deactivating the current one.

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
    activate it, and return its app_id for you to
    desactivate or reactivate it later.

    (This method is meant for advanced users and should not be needed for most)
    """
    global NEXT_APP_ID, APPS
    NEXT_APP_ID += 1
    _app_id = f"trame_app_{NEXT_APP_ID}"
    _app = App(name)

    # Default app initialization
    _app.trigger("js_error")(log_js_error)
    _app.cli_parser.add_argument(
        "--server",
        help="Prevent your browser from opening at startup",
        action="store_true",
    )

    APPS[_app_id] = _app
    activate_app(_app_id)
    return _app_id


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
