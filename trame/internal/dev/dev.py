def main():
    """
    This function is called when using the `trame` executable.
    trame executable aim to provide additional functionalities for
    development such as dynamically reloading the Python application
    without restarting the server or the client.

    >>> trame app.py --dev

    trame executable assume you will have a `layout` variable inside
    your main script and will provide a reload button in the footer
    of your UI so you can control, when you actually want to reprocess
    your server side changes. This is especially usefull when adjusting
    UI styles.

    This functionality is in Alpha but we aim to improve it based on
    needs and feedback from the community.
    """
    import importlib

    from trame.internal.app import get_app_instance

    _app = get_app_instance()
    parser = _app.cli_parser
    parser.add_argument("script", help="The script to run")
    args, _unknown = parser.parse_known_args()

    spec = importlib.util.spec_from_file_location("app", args.script)
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)

    setup_dev(app, clear_changes=True)

    app.layout.start()


def setup_dev(*reload_list, clear_changes=False, clear_triggers=True):
    """
    Set up a development environment for the trame app if --dev was passed
    as a command line argument. If enabled, a reload button will appear at the
    bottom of the web browser which will reload the modules that were passed as
    arguments.

    :param reload_list: positional arguments of the modules to reload when the
                        reload button is pressed.
    :type reload_list: python modules
    :param clear_changes: whether or not to clear changes on reload
    :type clear_changes: bool
    :param clear_triggers: whether or not to clear triggers on reload
    :type clear_triggers: bool
    :rtype: bool
    :returns: whether the program is running in dev mode or not
    """
    from trame.internal.app import get_app_instance

    _app = get_app_instance()
    parser = _app.cli_parser
    args, _unknown = parser.parse_known_args()

    if not args.dev:
        # We are not running in development mode
        return False

    # Register reload trigger
    def reload():
        print("\nReloading application...")

        if clear_changes:
            _app._change_callbacks.clear()

        if clear_triggers:
            # Never clear these triggers
            trigger_whitelist = [
                "js_error",
                "server_reload",
            ]
            _remove_keys(_app._triggers, trigger_whitelist)

        _app.reload_app()

        def reload_modules(*modules):
            for m in modules:
                m.__loader__.exec_module(m)

                if hasattr(m, 'on_reload'):
                    m.on_reload(reload_modules)

        for module in reload_list:
            reload_modules(module)

            if hasattr(module, 'layout'):
                module.layout.flush_content()

        print(" > done !\n")

    # Set the reload trigger
    _app.trigger("server_reload")(reload)

    return True


def _remove_keys(d, whitelist=None):
    # Remove all keys from a dict except for those in the whitelist
    if whitelist is None:
        whitelist = []

    pop_keys = [k for k in d if k not in whitelist]
    for key in pop_keys:
        d.pop(key)
