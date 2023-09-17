from trame.app import get_server
from trame.widgets import html
from trame.ui.html import DivLayout

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------

server = get_server()
state = server.state

# -----------------------------------------------------------------------------
# State setup
# -----------------------------------------------------------------------------

# Creating new entries to the shared state
state.a = 1
state["b"] = 2

# Force state.d to be client side only
state.client_only("b")
# state.trame__client_only += ["b"]

# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

# UI helper to extent layout
def create_ui_for_state_var(name):
    with html.Div(style="margin: 20px; padding: 20px; border: solid 1px #333;"):
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
with DivLayout(server) as layout:
    create_ui_for_state_var("a")
    create_ui_for_state_var("b")

# -----------------------------------------------------------------------------
# State Listener
# -----------------------------------------------------------------------------


@state.change("a", "b")
def state_change(a, b, **kwargs):
    print(f"State updated a={a} b={b}")


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
