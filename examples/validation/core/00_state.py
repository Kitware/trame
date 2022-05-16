from trame.app import get_server
from trame.widgets import html, trame
from trame.ui.html import DivLayout

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------

server = get_server()
state = server.state

# -----------------------------------------------------------------------------
# State setup
# -----------------------------------------------------------------------------

# => start with only 1 variable
state.a = 1

# Force state.d to be client side only
state.client_only("d")
# state.trame__client_only += ["d"]

# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------
layout = DivLayout(server)

# UI helper to extent layout
def create_variable_editor(name):
    with layout:
        html.Div(
            f"Variable \"{name}\" {{{{ {name} }}}} == get({{{{ get('{name}') }}}})",
            style="padding: 10px;",
        )
        with html.Div(style="padding: 10px;"):
            html.Button(f"{name}+", click=f"{name} += 1")
            html.Button(f"{name}-", click=f"{name} -= 1")
            html.Button(f"{name}=5", click=f"{name} = 5")
            html.Button(f"set({name}+)", click=f"set('{name}', {name} + 1)")
            html.Button(f"set({name}-)", click=f"set('{name}', {name} - 1)")
            html.Button(f"set({name}=5)", click=f"set('{name}', 5)")


# Start with some UI to control a
with layout:
    trame.LifeCycleMonitor()
    create_variable_editor("a")

# -----------------------------------------------------------------------------
# State Listener to a and add new state entries
# -----------------------------------------------------------------------------


@state.change("a", "d")
def state_change(a, b=None, c=None, d=None, **kwargs):
    print(f"State updated a={a} b={b} c={c} d={d}")
    if a == 5 and not state.has("b"):
        state.b = 1
        create_variable_editor("b")
        state.change("b")(state_change)

    if a == 10 and not state.has("c"):
        state.c = 1
        create_variable_editor("c")
        state.change("c")(state_change)

    if a == 15 and not state.has("d"):
        # Make "d" variable client only...
        state.d = 1
        create_variable_editor("d")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
