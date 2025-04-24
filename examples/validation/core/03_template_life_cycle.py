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

state.a = 1


def add():
    state.a += 1


# -----------------------------------------------------------------------------
# UI setup
# -----------------------------------------------------------------------------

layout = DivLayout(server)
with layout as c:
    c.root.add_child("a={{ a }} <br> template_ts={{ tts }} <br> ")
    html.Button("a+", click="a+=1")
    html.Button("set(a+)", click="set('a', a+1)")
    html.Button("server", click=add)
    trame.LifeCycleMonitor()

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
