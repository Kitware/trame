import asyncio
from threading import Thread, current_thread


class AppServerThread(Thread):
    def __init__(self, app, port=None, **kwargs):
        Thread.__init__(self, **kwargs)
        self._app = app
        self._port = port
        self._loop = None
        self._thread_id = None

    def run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._thread_id = current_thread()
        self._app.run_server(port=self._port, thread=True)

    def stop(self):
        self._loop.call_soon_threadsafe(self._app.stop_server)

    @property
    def port(self):
        return self._app.server_port


def compose_callbacks(*args):
    def __fn(**kwargs):
        for _fn in args:
            if _fn is None:
                continue
            try:
                _fn(**kwargs)
            except TypeError:
                _fn()

    return __fn
