import json

from trame.app import get_server

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
ctrl = server.controller

# -----------------------------------------------------------------------------
# Life Cycle events
# -----------------------------------------------------------------------------


def server_ready(**state):
    print("on_server_ready")
    print("  => current state:")
    print(json.dumps(state, indent=2))
    print("-" * 60)


def client_connected():
    print("on_client_connected")


def client_unmounted():
    print("on_client_unmounted")


def client_exited():
    print("on_client_exited")


def server_exited(**state):
    print("on_server_exited")
    print("  => current state:")
    print(json.dumps(state, indent=2))
    print("-" * 60)


# -----------------------------------------------------------------------------
# Life Cycle registration
# -----------------------------------------------------------------------------

ctrl.on_server_ready.add(server_ready)
ctrl.on_client_connected.add(client_connected)
ctrl.on_client_unmounted.add(client_unmounted)
ctrl.on_client_exited.add(client_exited)
ctrl.on_server_exited.add(server_exited)

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
