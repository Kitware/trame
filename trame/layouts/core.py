import asyncio
import os
from pywebvue.utils import read_file_as_base64_url
from trame.html import Span, vuetify, Triggers

import pywebvue
import trame as tr
import trame.internal as tri

LOGO_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../html/assets/logo.svg")
)


class AbstractLayout:
    def __init__(self, _root_elem, name, favicon=None, on_ready=None):
        self.name = name
        self.favicon = None
        self.triggers = Triggers("_js_trame_triggers")
        if os.path.exists(LOGO_PATH):
            self.favicon = read_file_as_base64_url(LOGO_PATH)
        self.on_ready = on_ready
        self.children = _root_elem.children
        self._current_root = _root_elem

        # Always add triggers
        self.children += [self.triggers]

        if favicon:
            file_path = os.path.join(tri.base_directory(), favicon)
            if os.path.exists(file_path):
                self.favicon = file_path
            else:
                print(f"Invalid path to favicon: {file_path}")

    @property
    def root(self):
        """
        Top level Vue component. Useful for providing / injecting into children components. Setting makes old root child of new root.
        """
        return self._current_root

    @root.setter
    def root(self, new_root):
        if new_root and self._current_root != new_root:
            new_root.children += [self._current_root]
            self._current_root = new_root

    @property
    def html(self):
        """
        Compute corresponding layout String which represent the html part.
        """
        return self.root.html

    @property
    def state(self):
        """
        Return App state as a dictionary or extend it when setting.
        This is a safe way to build the state incrementaly.

        >>> layout.state = { "a": 1, "b": 2 }
        >>> print(layout.state)
        ... {"a": 1, "b": 2}
        >>> layout.state = { "c": 3, "d": 4 }
        >>> print(layout.state)
        ... {"a": 1, "b": 2, "c": 3, "d": 4}

        """
        return tri.get_app_instance().state

    @state.setter
    def state(self, value):
        _app = tri.get_app_instance()
        for (k, v) in value.items():
            _app.set(k, v)

    def flush_content(self):
        """Push new content to client"""
        _app = tri.get_app_instance()
        _app.layout = self.html

    def start(self, port=None, debug=False):
        """
        Start the application server.

        :param port: Which port to run the server on
        :param debug: Whether to enable debugging tools. Defaults to False.
        :type debug: bool
        """
        _app = tri.get_app_instance()

        _app.name = self.name
        _app.layout = self.html
        _app.on_ready = tri.print_server_info()

        if self.favicon:
            _app.favicon = self.favicon
        if self.on_ready:
            _app.on_ready = tri.print_server_info(self.on_ready)

        # Dev validation
        tri.validate_key_names()

        _app.run_server(port=port)

    def start_thread(
        self, port=None, print_server_info=False, on_server_listening=None, **kwargs
    ):
        _app = tri.get_app_instance()
        _app.name = self.name
        _app.layout = self.html

        if self.favicon:
            _app.favicon = self.favicon

        if print_server_info:
            _app.on_ready = tri.print_server_info(
                tri.compose_callbacks(self.on_ready, on_server_listening)
            )
        else:
            _app.on_ready = compose_callbacks(self.on_ready, on_server_listening)

        # Dev validation
        tri.validate_key_names()
        server_thread = tri.AppServerThread(_app, port, **kwargs)
        server_thread.start()
        return server_thread

    def start_desktop_window(self, on_msg=None, **kwargs):
        from multiprocessing import Queue

        _msg_queue = Queue()

        _app = tri.get_app_instance()
        _app.name = self.name
        _app.layout = self.html

        async def process_msg():
            keep_processing = True
            while keep_processing:
                await asyncio.sleep(0.5)
                if not _msg_queue.empty():
                    msg = _msg_queue.get_nowait()
                    if on_msg:
                        on_msg(msg)
                    if msg == "closing":
                        keep_processing = False
                        _app.stop_server()

        asyncio.get_event_loop().create_task(process_msg())

        if self.favicon:
            _app.favicon = self.favicon

        def start_client(**_):
            client_process = tri.ClientWindowProcess(
                title=_app.name, port=_app.server_port, msg_queue=_msg_queue, **kwargs
            )
            client_process.start()

        _app.on_ready = compose_callbacks(self.on_ready, start_client)

        # Dev validation
        tri.validate_key_names()

        _app.run_server(port=0)


class FullScreenPage(AbstractLayout):
    """
    A layout that takes the whole screen.

    :param name: Text for this page's browser tab (required)
    :type name: str
    :param favicon: Filename of image for this page's browser tab
    :type favicon: str
    :param on_ready: Function to run on startup
    :type on_ready: function

    >>> FullScreenPage("Simple Page").start()
    """

    def __init__(self, name, favicon=None, on_ready=None):
        super().__init__(vuetify.VApp(id="app"), name, favicon, on_ready)


class SinglePage(FullScreenPage):
    """
    A layout that takes the whole screen, adding a |layout_vuetify_link| for a `toolbar`, a VMain as `content` and a VFooter as a `footer`.

    .. |layout_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-app-bar" target="_blank">vuetify app bar</a>

    :param name: Text for this page's browser tab (required)
    :type name: str

    >>> layout = SinglePage("Page with header / app bar")

    The toolbar starts with 2 children, a `logo` and a `title` which are accessible at
    the root of the layout object.

    >>> layout.toolbar.children += ["More stuff to the toolbar"]
    >>> layout.logo.children = [VIcon("mdi-menu")]
    >>> layout.title.set_text("My Super App")

    Then we have `content` and `footer`. Content is by default empty but the footer
    has the default trame information regarding its versions and feature feedback
    on when the server is busy with a spining progress.

    You can quickly hide the footer by calling the following.

    >>> layout.footer.hide()
    """

    def __init__(self, name, favicon=None, on_ready=None):
        super().__init__(name, favicon, on_ready)
        self.toolbar = vuetify.VAppBar(app=True)
        if os.path.exists(LOGO_PATH):
            self.logo = Span(
                f'<img height="32px" width="32px" src="{read_file_as_base64_url(LOGO_PATH)}" />',
                classes="mr-2",
                style="display: flex; align-content: center;",
            )
        else:
            self.logo = vuetify.VIcon("mdi-menu", classes="mr-4")

        args = tri.get_cli_parser().parse_known_args()[0]
        dev = args.dev if hasattr(args, "dev") else False

        self.title = Span("trame app", classes="title")
        self.content = vuetify.VMain()
        self.toolbar.children += [self.logo, self.title]
        self.footer = vuetify.VFooter(
            app=True,
            classes="my-0 py-0",
            children=[
                vuetify.VProgressCircular(
                    indeterminate=("busy",),
                    background_opacity=1,
                    bg_color="#01549b",
                    color="#04a94d",
                    size=16,
                    width=3,
                    classes="ml-n3 mr-1",
                ),
                f'<a href="https://kitware.github.io/trame/" class="grey--text lighten-1--text text-caption text-decoration-none" target="_blank">Powered by trame {tr.__version__}/{pywebvue.__version__}</a>',
                vuetify.VSpacer(),
                vuetify.VBtn(
                    vuetify.VIcon("mdi-autorenew", x_small=True),
                    v_if=("__dev_reload", dev),
                    x_small=True,
                    icon=True,
                    click="trigger('server_reload')",
                    classes="mx-2",
                ),
                '<a href="https://www.kitware.com/" class="grey--text lighten-1--text text-caption text-decoration-none" target="_blank">© 2021 Kitware Inc.</a>',
            ],
        )
        self.children += [self.toolbar, self.content, self.footer]


class SinglePageWithDrawer(SinglePage):
    """
    A layout that takes the whole screen, adding a |layout_vuetify_link| for a toolbar, a content, a drawer, and a footer.

    :param name: Text for this page's browser tab (required)
    :type name: str
    :param show_drawer: Whether the drawer is open. Default True
    :type show_drawer: bool
    :param width: How many pixels wide the drawer should be
    :type width: Number
    :param show_drawer_name: The name referencing the drawer's state. Default "drawerOpen".
    :type show_drawer_name: str

    >>> SinglePageWithDrawer("Page with drawer").start()
    """

    def __init__(
        self,
        name,
        favicon=None,
        on_ready=None,
        show_drawer=True,
        width=200,
        show_drawer_name="drawerOpen",
    ):
        super().__init__(name, favicon, on_ready)
        self.drawer = vuetify.VNavigationDrawer(
            app=True,
            clipped=True,
            stateless=True,
            v_model=(show_drawer_name, show_drawer),
            width=width,
        )
        self.toolbar.clipped_left = True
        self.children += [self.drawer]
        self.logo.click = f"{show_drawer_name} = !{show_drawer_name}"


def update_layout(layout):
    """
    Flush layout to the client

    :param layout: UI content for your application
    :type layout: str | trame.layouts.*

    >>> layout.title.set_text("Workload finished!")
    >>> update_layout(layout)

    """
    _app = tri.get_app_instance()
    _app.layout = layout if isinstance(layout, str) else layout.html
