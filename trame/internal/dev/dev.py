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
    from trame.internal.app import get_app_instance
    from trame.internal.utils import log_js_error

    _app = get_app_instance()
    parser = _app.cli_parser
    parser.add_argument("script", help="The script to run")
    parser.add_argument(
        "--dev", help="Allow to dynamically reload server", action="store_true"
    )
    args, _unknown = parser.parse_known_args()

    import importlib.util

    spec = importlib.util.spec_from_file_location("app", args.script)
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)

    # Register reload trigger
    def reload():
        print("\nReloading application...")
        _app._change_callbacks.clear()
        _app._triggers.clear()
        _app.reload_app()

        # Keep sys trame ones
        _app._triggers["server_reload"] = reload
        _app._triggers["js_error"] = log_js_error

        spec = importlib.util.spec_from_file_location("app", args.script)
        app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app)
        app.layout.flush_content()
        print(" > done !\n")

    _app.trigger("server_reload")(reload)

    app.layout.start(debug=args.dev)
