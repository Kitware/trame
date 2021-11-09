from genericpath import exists
import os
from pywebvue.utils import read_file_as_base64_url
from trame.html import Span, vuetify, Triggers

import pywebvue
import trame as tr

LOGO_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../html/assets/logo.svg")
)


class FullScreenPage:
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
        self.name = name
        self.favicon = None
        self.triggers = Triggers("_js_trame_triggers")
        if os.path.exists(LOGO_PATH):
            self.favicon = read_file_as_base64_url(LOGO_PATH)
        self.on_ready = on_ready
        self._app = vuetify.VApp(id="app")
        self.children = self._app.children
        self._current_root = self._app

        # Always add triggers
        self._app.children += [self.triggers]

        if favicon:
            file_path = os.path.join(tr.base_directory(), favicon)
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
        String of the html this layout has built up.
        """
        return self.root.html

    @property
    def state(self):
        """
        App state as a dictionary. Setting updates instead of overwriting.
        """
        return tr.get_app_instance().state

    @state.setter
    def state(self, value):
        app = tr.get_app_instance()
        for (k, v) in value.items():
            app.set(k, v)

    def get_state_values(self, *names):
        """
        Query the app state for particular names. Returns whole state dict if no names given.

        :params names: Which values to get from state.
        :type names: list[str] | None

        >>> full_state = get_state()
        >>> full_state.get("greeting")
        "Hello"

        >>> greeting, name  = get_state("greeting", "name")
        >>> f'{greeting}, {name}!'
        "Hello, Trame!"

        >>> greeting, = get_state("greeting")
        >>> greeting
        "Hello"


        """
        return tr.get_state(*names)

    def flush_content(self):
        """Push new content to client"""
        _app = tr.get_app_instance()
        _app.layout = self.html

    def start(self, port=None, debug=False):
        """
        Run the application server.

        :param port: Which port to run the server on
        :param debug: Whether to enable debugging tools. Defaults to False.
        :type debug: bool
        """
        _app = tr.get_app_instance()

        _app.name = self.name
        _app.layout = self.html
        _app.on_ready = tr.print_server_info()

        if self.favicon:
            _app.favicon = self.favicon
        if self.on_ready:
            _app.on_ready = tr.print_server_info(self.on_ready)

        # Dev validation
        tr.validate_key_names()

        _app.run_server(port=port)


class SinglePage(FullScreenPage):
    """
    A layout that takes the whole screen, adding a |layout_vuetify_link| for a header and a footer.

    .. |layout_vuetify_link| raw:: html

        <a href="https://vuetifyjs.com/api/v-app-bar" target="_blank">vuetify app bar</a>

    :param name: Text for this page's browser tab (required)
    :type name: str

    >>> SinglePage("Page with header / app bar").start()
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

        args = tr.get_cli_parser().parse_known_args()[0]
        dev = args.dev if hasattr(args, "dev") else False

        self.title = Span("Trame App", classes="title")
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
                f'<a href="https://kitware.github.io/trame/" class="grey--text lighten-1--text text-caption text-decoration-none" target="_blank">Powered by Trame {tr.__version__}/{pywebvue.__version__}</a>',
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
                # vuetify.VProgressLinear(
                #     active=("busy",),
                #     indeterminate=True,
                #     absolute=True,
                #     bottom=True,
                #     striped=True,
                #     background_opacity=1,
                #     color="#01549b",
                #     background_color="#04a94d",
                #     height=4,
                # ),
            ],
        )
        self._app.children += [self.toolbar, self.content, self.footer]


class SinglePageWithDrawer(SinglePage):
    """
    A layout that takes the whole screen, adding a |layout_vuetify_link| for a header, a drawer, and a footer.

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
        self._app.children += [self.drawer]
        self.logo.click = f"{show_drawer_name} = !{show_drawer_name}"
