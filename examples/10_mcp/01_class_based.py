"""Class-based app: a tool of the app's own, and methods called on one instance.

Run:  python examples/10_mcp/01_class_based.py --server          # agent access off
      python examples/10_mcp/01_class_based.py --server --mcp    # agent access on

The app shows two cones. It marks reset_resolution() with @mcp.tool: the app
is built once, so it is a tool of its own, which agents call directly. Each Cone
marks set_resolution() with @mcp.method and resolution with @mcp.property:
there are two cones, so agents say which one, by the name the app gave it.

An agent can then:
    reset_resolution()
    object_get("left_cone")
    object_call("left_cone", "set_resolution", {"resolution": 12})

Everything is declared either way; nothing is served until agent access is
on. The "Allow agent access" checkbox toggles `server.mcp.enabled` at runtime.
"""

from typing import Annotated

from trame.app import TrameApp, TrameComponent
from trame.decorators import change, mcp
from trame.ui.html import DivLayout
from trame.widgets import html


class Cone(TrameComponent):
    """A cone in the scene."""

    def __init__(self, server, name):
        super().__init__(server)
        self.resolution_key = f"{name}_resolution"  # the state key the page shows
        self.state[self.resolution_key] = 6

    @mcp.property
    def resolution(self) -> int:
        """Number of facets."""
        return self.state[self.resolution_key]

    @mcp.method
    def set_resolution(
        self, resolution: Annotated[int, {"minimum": 3, "maximum": 60}]
    ) -> str:
        """Set the number of facets of this cone."""
        self.state[self.resolution_key] = resolution
        return f"Resolution set to {resolution}"


class ConeApp(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.left_cone = Cone(self.server, "left_cone")
        self.right_cone = Cone(self.server, "right_cone")
        # The names agents use, and which cone each one is
        self.left_cone.mcp_expose("left_cone", description="The cone on the left.")
        self.right_cone.mcp_expose("right_cone", description="The cone on the right.")

        self.state.agent_access = self.mcp.enabled
        self._build_ui()

    @mcp.tool
    def reset_resolution(self) -> str:
        """Put both cones back to 6 facets."""
        self.left_cone.set_resolution(6)
        self.right_cone.set_resolution(6)
        return "Both cones reset"

    @change("agent_access")
    def _on_agent_access(self, agent_access, **_):
        self.mcp.enabled = agent_access

    def _build_ui(self):
        with DivLayout(self.server):
            with html.Label():
                html.Input(type="checkbox", v_model=("agent_access",))
                html.Span("Allow agent access")
            for cone in (self.left_cone, self.right_cone):
                with html.Div():
                    html.Input(
                        type="range",
                        min=3,
                        max=60,
                        step=1,
                        v_model_number=(cone.resolution_key,),
                    )
                    html.Span(f"{{{{ {cone.resolution_key} }}}} facets")


def main():
    app = ConeApp()
    app.server.start()


if __name__ == "__main__":
    main()
