#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
# ]
# ///

from trame.app import TrameApp


class AppWithCLI(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)

        # Argparse available on server
        parser = self.server.cli
        parser.add_argument("-o", "--output", help="Working directory")
        (args, unknown) = parser.parse_known_args()

        print("args.output", args.output)
        print("unknown", unknown)


def main():
    app = AppWithCLI()
    app.server.start(
        open_browser=False,  # skip browser opening
        show_connection_info=False,  # no banner
        timeout=1,  # auto exit after 1s
    )


if __name__ == "__main__":
    main()
