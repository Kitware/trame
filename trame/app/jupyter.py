import asyncio
from trame.app import get_server
from IPython import display
from trame_server.utils.asynchronous import handle_task_result


def show(_server, ui=None, **kwargs):
    if isinstance(_server, str):
        _server = get_server(_server)

    def on_ready(**_):
        params = f"?ui={ui}" if ui else ""
        src = f"{kwargs.get('protocol', 'http')}://{kwargs.get('host', 'localhost')}:{_server.port}/index.html{params}"
        loop = asyncio.get_event_loop()
        loop.call_later(0.1, lambda: display_iframe(src, **kwargs))
        _server.controller.on_server_ready.discard(on_ready)

    if _server._running_stage == 0:
        _server.controller.on_server_ready.add(on_ready)
        _server.start(
            exec_mode="task",
            port=0,
            open_browser=False,
            show_connection_info=False,
            disableLogging=True,
            timeout=0,
        )
    elif _server._running_stage == 1:
        _server.controller.on_server_ready.add(on_ready)
    elif _server._running_stage == 2:
        on_ready()


def display_iframe(src, **kwargs):
    """Convenience method to display an iframe for the given url source"""

    # Set some defaults. The kwargs can override these.
    # width and height are both required.
    iframe_kwargs = {
        "width": "100%",
        "height": 600,
        **kwargs,
    }
    iframe = display.IFrame(src=src, **iframe_kwargs)
    return display.display(iframe)


def run(name, **kwargs):
    """Run and display a Jupyter server proxy process with the given name

    Note that the proxy process must be registered with Jupyter by setting
    the `jupyter_serverproxy_servers` entrypoint in its setup.py or setup.cfg
    file.
    """
    src = f"/{name}"
    return display_iframe(src, **kwargs)
