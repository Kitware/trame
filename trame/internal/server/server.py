import os

from trame.internal.app import get_app_instance
from trame.internal.utils import (
    base_directory, print_server_info, validate_key_names
)


def start(layout=None, name=None, favicon=None, on_ready=None, port=None, debug=False):
    """
    Start the web server for your application

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


def stop():
    app = get_app_instance()
    app.stop_server()


def port():
    app = get_app_instance()
    return app.server_port
