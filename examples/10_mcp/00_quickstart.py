"""Quick start: let agents drive a trame app through MCP.

Run:  python examples/10_mcp/00_quickstart.py --server
Then use one of the commands the console prints to start a Claude Code or
Codex session connected to the app.

The app exposes one state key and one tool, then turns agent access on.
Launch with --no-mcp to keep it off.
"""

from trame.app import get_server
from trame.ui.html import DivLayout
from trame.widgets import html

server = get_server("quickstart")
state = server.state

state.resolution = 6

# Agents read and write it as a property of the "state" object
state.mcp_expose(
    "resolution",
    type=int,
    schema={"minimum": 3, "maximum": 60},  # checked on every agent write
    description="Number of facets of the cone",
)


@server.mcp.tool
def reset_resolution() -> str:
    """Reset the resolution to its default value (6)."""
    state.resolution = 6
    return "Resolution reset to 6"


server.mcp.enabled = True  # serve what is declared above (--no-mcp overrides)

with DivLayout(server):
    html.H1("Resolution: {{ resolution }}")
    html.Input(
        type="range",
        min=3,
        max=60,
        step=1,
        v_model_number=("resolution",),
    )

if __name__ == "__main__":
    server.start()
