"""Exposure: classes you don't own, read-only names, getters, resources, prompts.

Run:  python examples/10_mcp/04_exposure.py --server

Panel stands for a component class from another library: it knows nothing of
agents, so the app describes it with Panel.mcp_describe(). A subclass hides a
method of its base. The app then exposes each panel under a read-only name, and
the panel selected in the UI under a getter, "selected", which follows the
selection on every call and tells agents what it is for. Only the selected
panel can change, because no other panel has a writable name: agents reach
an object only through names, or through the properties of objects they
reach, and read-only access follows the way they reach it.

The app adds a resource and a prompt of its own. It marks nothing else, so it
is not itself an object agents see.

An agent can then:
    object_list()
    object_get("drafts")
    object_call("selected", "set_color", {"color": "teal"})
    object_update("pinned", {"title": "Hi"})   # refused unless it is selected
    resources/read app://help, prompts/get recolor
"""

from trame.app import TrameApp, TrameComponent
from trame.decorators import mcp
from trame.ui.html import DivLayout
from trame.widgets import html

# -----------------------------------------------------------------------------
# A component class from a library: it declares nothing for agents
# -----------------------------------------------------------------------------


class Panel(TrameComponent):
    """A colored panel with a title."""

    def __init__(self, server, title, color="lightgray", on_change=None):
        super().__init__(server)
        self._title = title
        self._color = color
        self._on_change = on_change

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value
        self._changed()

    @property
    def color(self) -> str:
        return self._color

    @property
    def cache_key(self) -> str:
        return f"{self._title}:{self._color}"

    def set_color(self, color: str) -> None:
        self._color = color
        self._changed()

    def reset(self) -> None:
        self._color = "lightgray"
        self._changed()

    def _changed(self):
        if self._on_change:
            self._on_change()


# -----------------------------------------------------------------------------
# The app: what agents see of those classes, and how they reach them
# -----------------------------------------------------------------------------

# Before any panel is built: a class is described once, for the whole process.
# Listed members only: cache_key stays hidden.
Panel.mcp_describe(
    description="A colored panel the user sees.",
    properties={"title": "Shown at the top of the panel", "color": "A CSS color"},
    methods={
        "set_color": "Change the panel's background color",
        "reset": "Back to the default gray",
    },
)


class PinnedPanel(Panel, mcp={"methods": {"reset": False}}):
    """A panel whose color can change but not be reset."""


HELP = """\
# Panels

The user selects a panel by clicking it. Only the selected panel can change;
the others are read-only. A pinned panel can't be reset.
"""


class PanelsApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.mcp.configure(name="panels", enabled=True)

        refresh = self._refresh
        self.panels = [
            Panel(self.server, "Inbox", on_change=refresh),
            Panel(self.server, "Drafts", "khaki", on_change=refresh),
            PinnedPanel(self.server, "Pinned", "lightblue", on_change=refresh),
        ]
        self.state.selected = 0
        for name, panel in zip(("inbox", "drafts", "pinned"), self.panels):
            panel.mcp_expose(name, read_only=True)
        self.mcp.expose_object(
            lambda: self.panels[self.state.selected],
            "selected",
            description="The panel the user selected, the only one agents can change.",
        )

        self._refresh()
        self._build_ui()

    @mcp.resource("app://help", mime_type="text/markdown")
    def help(self) -> str:
        """How the panels work."""
        return HELP

    @mcp.prompt
    def recolor(self, mood: str = "calm") -> str:
        """Recolor the selected panel to match a mood."""
        return f"Pick a color for a {mood} mood and apply it to the selected panel."

    def _refresh(self):
        self.state.panels = [
            {"title": panel.title, "color": panel.color} for panel in self.panels
        ]

    def _build_ui(self):
        with DivLayout(self.server, style="display: flex; gap: 1rem"):
            html.Div(
                "{{ panel.title }}",
                v_for="(panel, i) in panels",
                key="i",
                click="selected = i",
                style=(
                    "{ background: panel.color, padding: '2rem', cursor: 'pointer',"
                    " outline: i === selected ? '3px solid black' : 'none' }",
                ),
            )


def main():
    app = PanelsApp()
    app.server.start()


if __name__ == "__main__":
    main()
