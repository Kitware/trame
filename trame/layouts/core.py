from trame.html import Span, vuetify


class SinglePage:
    def __init__(self, name):
        self.name = name
        self._app = vuetify.VApp(id="app")
        self.toolbar = vuetify.VAppBar(app=True)
        self.logo = vuetify.VIcon("mdi-menu", classes="mr-4")
        self.title = Span("Trame App", classes="title")
        self.content = vuetify.VMain()
        self.toolbar.children += [self.logo, self.title]
        self._app.children += [self.toolbar, self.content]

    @property
    def html(self):
        return self._app.html


class FullScreenPage:
    def __init__(self, name):
        self.name = name
        self._app = vuetify.VApp(id="app")
        self.children = self._app.children

    @property
    def html(self):
        return self._app.html
