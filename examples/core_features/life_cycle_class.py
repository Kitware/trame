#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "trame",
# ]
# ///
from trame.app import TrameApp
from trame.decorators import life_cycle
from trame.ui.html import DivLayout


class LifeCycle(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)

        # build ui
        with DivLayout(self.server) as self.ui:
            pass

    @life_cycle.server_ready
    def server_ready(self, **state):
        print("on_server_ready")

    @life_cycle.client_connected
    def client_connected(self):
        print("on_client_connected")

    @life_cycle.client_exited
    def client_exited(self):
        print("on_client_exited")

    @life_cycle.server_exited
    def server_exited(self, **state):
        print("on_server_exited")


def main():
    app = LifeCycle()
    app.server.start(timeout=1)


if __name__ == "__main__":
    main()
