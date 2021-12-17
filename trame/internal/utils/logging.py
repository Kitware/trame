from .cli import get_cli_parser


def log_js_error(message):
    print(f" > JS error | {message}")


def print_server_info(_fn=None):
    """Provide network info so clients can connect to the started server"""
    from trame.internal.app import get_app_instance

    def ready(**kwargs):
        parser = get_cli_parser()
        args = parser.parse_known_args()[0]
        local_url = f"http://{args.host}:{args.port}/"
        app = get_app_instance()
        real_port = app.server_port

        import socket

        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)

            print()
            print("App running at:")
            print(f" - Local:   {local_url}")
            print(f" - Network: http://{host_ip}:{real_port}/")

        except socket.gaierror:
            pass

        print()
        print("Note that for multi-users you need to use and configure a",
              "launcher.")

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
            print("And to prevent your browser from opening, "
                  "add '--server' to your command line.")
        print()

    return ready


def validate_key_names():
    """Warn user when invalid key names have been used"""
    from trame.internal.app import get_app_instance

    _app = get_app_instance()
    errors = []
    for key in _app.state:
        if " " in key:
            errors.append(f"  - '{key}'")

    if errors:
        suffix = "s" if len(errors) > 1 else ""
        print("=" * 60)
        print(f"Warning: {len(errors)} key{suffix} inside your state"
              "contains spaces")
        print("=" * 60)
        for message in errors:
            print(message)
        print("=" * 60)
