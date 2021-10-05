from trame.html import Span, vuetify
from trame import get_app_instance


class FullScreenPage:
    def __init__(self, name):
        self.name = name
        self._app = vuetify.VApp(id="app")
        self.children = self._app.children
        self._current_root = self._app

    @property
    def root(self):
        return self._current_root

    @root.setter
    def root(self, new_root):
        if new_root and self._current_root != new_root:
            new_root.children += [self._current_root]
            self._current_root = new_root

    @property
    def html(self):
        return self.root.html

    @property
    def state(self):
        return get_app_instance().state

    @state.setter
    def state(self, value):
        get_app_instance().state.update(value)


class SinglePage(FullScreenPage):
    def __init__(self, name):
        super().__init__(name)
        self.toolbar = vuetify.VAppBar(app=True)
        self.logo = vuetify.VIcon("mdi-menu", classes="mr-4")
        self.title = Span("Trame App", classes="title")
        self.content = vuetify.VMain()
        self.toolbar.children += [self.logo, self.title]
        self._app.children += [self.toolbar, self.content]


class SinglePageWithDrawer(SinglePage):
    def __init__(
        self, name, show_drawer=True, width=200, show_drawer_name="drawerOpen"
    ):
        super().__init__(name)
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
