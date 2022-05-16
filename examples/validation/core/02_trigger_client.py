from trame.app import get_server
from trame.widgets import html, trame
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


def monitor_life_cycles(life_cycle):
    print(f"Life cycle: {life_cycle}")


def call_method_1():
    print("Server: call_method_1")
    server.js_call("ref_name", "emit", "method1", "a")


def call_method_2():
    print("Server: call_method_2")
    ctrl.call("method2", "b")


def call_method_3():
    print("Server: call_method_3")
    ctrl.call("method3")


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = DivLayout(server)

with layout:
    html.Div("State a={{ a }} - template timestep {{ tts }}", style="padding: 20px;")
    client_triggers = trame.ClientTriggers(
        ref="ref_name",
        created=(monitor_life_cycles, "['created']"),
        mounted=(monitor_life_cycles, "['mounted']"),
        beforeDestroy=(monitor_life_cycles, "['beforeDestroy']"),
        method1="window.console.log('method 1', $event)",
        method2="window.console.log('method 2', $event)",
        method3="window.console.log('method 3', $event)",
    )
    ctrl.call = client_triggers.call

    with html.Div(style="padding: 10px;") as div:
        html.Button(f"Method 1", click=call_method_1)
        html.Button(f"Method 2", click=call_method_2)
        html.Button(f"Method 3", click=call_method_3)
        html.Button(f"a+", click="a+=1")
        div.add_child("")

    trame.LifeCycleMonitor(type="error", events=("['created', 'destroyed']",))


# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
