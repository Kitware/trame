from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html, trame

# -----------------------------------------------------------------------------
# Trame app
# -----------------------------------------------------------------------------

server = get_server()
state = server.state

# -----------------------------------------------------------------------------
# State setup
# -----------------------------------------------------------------------------

# initial state with only 1 variable
state.a = 1

# Force state.[b,d] to be client side only (+=1 only local + method call will be out of sync)
state.client_only("b", "d")
# state.trame__client_only += ["d"]


def update_variable(var_name="a", delta=+1):
    state[var_name] += delta


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------
layout = DivLayout(server)

with layout:
    trame.LifeCycleMonitor()


# UI helper to extent layout
def create_variable_editor(name):
    with layout:
        html.Div(
            f'Variable "{name}" = {{{{ {name} }}}}',
            style="padding: 10px;",
        )
        with html.Div(style="padding: 10px;"):
            html.Button(f"{name} (no args)", click=update_variable)
            html.Button(f"{name} +", click=f"{name}+=1")
            html.Button(
                f"{name} args('{name}', 1)", click=(update_variable, f"['{name}', 1]")
            )
            html.Button(
                f"{name} args('{name}', -1)", click=(update_variable, f"['{name}', -1]")
            )
            html.Button(
                f"{name} kwargs(var_name='{name}', delta=1)",
                click=(update_variable, "[]", f"{{ var_name:'{name}', delta:1 }}"),
            )
            html.Button(
                f"{name} kwargs(var_name='{name}', delta=-1) ",
                click=(update_variable, "[]", f"{{ var_name:'{name}', delta:-1 }}"),
            )


# Start with some UI to control a
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
