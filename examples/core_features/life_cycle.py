from trame.app import get_server
from trame.ui.html import DivLayout

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
ctrl = server.controller

# Need a UI
with DivLayout(server):
    pass

# -----------------------------------------------------------------------------
# Life Cycle events
# -----------------------------------------------------------------------------


@ctrl.add("on_server_ready")
def server_ready(**state):
    print("on_server_ready")


@ctrl.add("on_client_connected")
def client_connected():
    print("on_client_connected")


@ctrl.add("on_client_unmounted")
def client_unmounted():
    print("on_client_unmounted")


@ctrl.add("on_client_exited")
def client_exited():
    print("on_client_exited")


@ctrl.add("on_server_exited")
def server_exited(**state):
    print("on_server_exited")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start(timeout=1)
