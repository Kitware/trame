from trame.app import get_server
from trame.widgets import html
from trame.ui.html import DivLayout

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# State setup
# -----------------------------------------------------------------------------

state.a = 1

# -----------------------------------------------------------------------------
# Methods call
# -----------------------------------------------------------------------------


@ctrl.set("alias_1")
def method_1(*args, **kwargs):
    print(f"Server: method_1 {args=} {kwargs=}")
    state.a += 1


@ctrl.add("alias_2")
def method_2(*args, **kwargs):
    print(f"Server: method_2 {args=} {kwargs=}")
    state.a += 2


@ctrl.add("alias_2")
def method_3(*args, **kwargs):
    print(f"Server: method_3 {args=} {kwargs=}")
    state.a += 3


def method_4(*args, **kwargs):
    print(f"Server: method_4 {args=} {kwargs=}")
    state.a += 10


ctrl.alias_3 = method_4

# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = DivLayout(server)

with DivLayout(server):
    html.Div(
        "State a={{ a }}", style="padding: 20px; margin: 20px; border: solid 1px #333;"
    )
    html.Button(f"Method 1", click=method_1)
    html.Button(f"Method 2", click=(method_2, "['hello', 'world']"))
    html.Button(f"Method 3", click=(method_3, "[1, 2]", "{ x: 3, y: 4 }"))
    html.Button(f"alias_1", click=(ctrl.alias_1, "[2]", "{ z: 4 }"))
    html.Button(f"alias_2", click=(ctrl.alias_2, "[3]", "{ z: 5 }"))
    html.Button(f"a+", click="a+=1")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
