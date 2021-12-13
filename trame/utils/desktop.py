import asyncio
from multiprocessing import Process
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


class ClientWindowProcess(Process):
    def __init__(
        self, title=None, port=None, msg_queue=None, file_dialog=None, **kwargs
    ):
        Process.__init__(self)
        self._title = title
        self._port = port
        self._msg_queue = msg_queue
        self._window_args = kwargs
        self._file_dialog = file_dialog
        self._main_window = None

    def _open_file_dialog(self):
        result = self._main_window.create_file_dialog(**self._file_dialog)
        self._msg_queue.put(["file_dialog", result])

    def exit(self):
        self._main_window.destroy()
        self._msg_queue.put("closing")

    def run(self):
        try:
            import webview
        except ImportError:
            print("trame.start_desktop_window() require pywebview==3.4")
            return

        self._main_window = webview.create_window(
            title=self._title,
            url=f"http://localhost:{self._port}/",
            **self._window_args,
        )
        self._main_window.closing += self.exit

        if self._file_dialog:
            webview.start(func=self._open_file_dialog)
        else:
            webview.start()
