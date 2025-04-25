from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html

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


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

with DivLayout(server):
    html.Div(
        "State a={{ a }}", style="padding: 20px; margin: 20px; border: solid 1px #333;"
    )
    html.Button("Method 1", click=method_1)
    html.Button("Method 2", click=(method_2, "['hello', 'world']"))
    html.Button("Method 3", click=(method_3, "[1, 2]", "{ x: 3, y: 4 }"))
    html.Button("alias_1", click=(ctrl.alias_1, "[2]", "{ z: 4 }"))
    html.Button("alias_2", click=(ctrl.alias_2, "[3]", "{ z: 5 }"))
    html.Button("alias_3", click=(ctrl.alias_3, "[4]", "{ z: 6 }"))
    html.Button("a+", click="a+=1")


# Can be defined after usage
ctrl.alias_3 = method_4

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
