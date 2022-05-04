import argparse
import importlib
from trame.app import get_server


def enable_modules(_server, *names):
    for module_name in names:
        m = importlib.import_module(f"trame.modules.{module_name}")
        _server.enable_module(m)


def main():
    parser = argparse.ArgumentParser(description="Client generator for trame")

    parser.add_argument(
        "--output",
        help="Directory to fill with trame client code",
        required=True,
    )

    args, module_names = parser.parse_known_args()

    server = get_server("www-generator")
    enable_modules(server, "www")
    enable_modules(server, *module_names)
    server.write_www(args.output)


if __name__ == "__main__":
    main()
