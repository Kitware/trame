from __future__ import annotations

import os
import json

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from trame_server import Server


class TrameServerMonitor:
    """Helper class capture sever state from log"""

    def __init__(self: TrameServerMonitor, log_path: str | os.PathLike) -> None:
        self._log_path = log_path
        self._last_state = {}
        self.port = 0
        self.update()

    def update(self: TrameServerMonitor) -> None:
        last_state_line = "STATE: {}"
        with open(self._log_path, "r") as f:
            for line in f:
                print(line)
                if "SERVER_PORT:" in line:
                    self.port = int(line[13:])
                if line[:7] == "STATE: ":
                    last_state_line = line

        self._last_state = json.loads(last_state_line[7:])

    def get_state(self: TrameServerMonitor) -> dict:
        self.update()
        return self._last_state

    def get(self: TrameServerMonitor, name: str):
        self.update()
        return self._last_state.get(name)


def remove_page_urls(base_path: str | os.PathLike) -> None:
    """Selenium capture page_url.txt which will change through
    tests and therefore we need to remove them."""
    for root, dirs, files in os.walk(base_path):
        if "page_url.txt" in files:
            full_path = os.path.join(root, "page_url.txt")
            os.remove(full_path)
            print(f" - remove: {full_path}")


def print_state(**kwargs):
    """Helper to print the server state in a way TrameServerMonitor can understand"""
    print("STATE:", json.dumps(kwargs), flush=True)


def enable_testing(server: Server, *state_monitor):
    """Register state monitoring for TrameServerMonitor and port extractor"""
    server.state.change(*state_monitor)(print_state)

    @server.controller.add("on_server_ready")
    def print_server_port(**kwargs):
        print("SERVER_PORT:", server.port, flush=True)
