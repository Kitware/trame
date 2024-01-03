from trame.app import get_server
from trame.decorators import hot_reload
from trame.widgets import html
from trame.ui.html import DivLayout


# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

# Can be enabled at runtime as well with
# 1. export TRAME_HOT_RELOAD=1
# 2. --hot-reload
server.hot_reload = True


# -----------------------------------------------------------------------------
# Dynamically modify any `ChangeMe` to see the new code execute while
# interacting with the app.
# -----------------------------------------------------------------------------
@ctrl.set("number_reset")
def reset_number():
    print("reset_number::ChangeMe")
    state.number = 6
    state.size = 1
    do_someting()


@state.change("number")
def update_number(number, **kwargs):
    print("update_number::ChangeMe", number)
    do_someting()


@hot_reload
def do_someting():
    print("do_someting::ChangeMe")


@ctrl.set("update_ui")
def update_ui():
    with DivLayout(server):
        html.Div("Some content - ChangeMe")
        html.Input(type="range", v_model_number=("number", 6))
        html.Input(type="range", v_model_number=("size", 2))
        html.Button("Reset", click=ctrl.number_reset)
        html.Button("Update", click=ctrl.update_ui)
        html.Div(
            "{{ number }} x {{ i }} = {{ number * i }}",
            v_for="i in size",
            key="i",
        )


# Need to run before start
update_ui()

# -----------------------------------------------------------------------------
# Automatic UI update on file change using watchdog (pip install watchdog)
# -----------------------------------------------------------------------------

try:
    import asyncio
    from pathlib import Path
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    current_event_loop = asyncio.get_event_loop()

    def update_ui():
        with server.state:
            ctrl.update_ui()

    class UpdateUIOnChange(FileSystemEventHandler):
        def on_modified(self, event):
            current_event_loop.call_soon_threadsafe(update_ui)

    observer = Observer()
    observer.schedule(
        UpdateUIOnChange(), str(Path(__file__).parent.absolute()), recursive=False
    )
    observer.start()
except:
    print("Watchdog not installed so skipping the auto monitoring")

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
