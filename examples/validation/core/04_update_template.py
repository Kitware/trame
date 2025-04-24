from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html, trame

LINE_COUNT = 1

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
layout = DivLayout(server)


def add_new_line():
    global LINE_COUNT
    with layout as c:
        c.root.add_child(f"<br>New line {LINE_COUNT}")
        LINE_COUNT += 1


with layout:
    html.Button("Add a new line ({{ tts }})", click=add_new_line)
    trame.LifeCycleMonitor(type="error", events=("['created']",))

# -----------------------------------------------------------------------------
# start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
