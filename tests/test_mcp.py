def test_mcp_exports():
    from trame.app.mcp import (  # noqa: F401
        MCP,
        Image,
        MCPDisabledError,
        MCPExposable,
        PermissionDeniedError,
        ToolError,
        ValidationError,
        claude_command,
        codex_command,
    )
    from trame.decorators import mcp

    for name in ("method", "property", "tool", "resource", "prompt", "constructor"):
        assert callable(getattr(mcp, name))


def test_app_methods_reach_agents():
    import asyncio

    from trame.app import TrameApp, get_server
    from trame.decorators import mcp

    class AgentApp(TrameApp):
        @mcp.method
        def greet(self, name: str) -> str:
            return f"Hello {name}"

    app = AgentApp(get_server("test_app_methods_reach_agents"))
    app.mcp_expose("app")
    result = asyncio.run(app.mcp._objects.call("app", "greet", {"name": "trame"}))
    assert result == "Hello trame"
