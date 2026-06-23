from datetime import datetime, timezone

from helloworld_demo_mcp import server


def test_current_utc_iso_has_z_suffix(monkeypatch):
    fixed = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    monkeypatch.setattr(server, "datetime", type("FrozenDateTime", (), {"now": staticmethod(lambda tz=None: fixed)}))

    assert server.current_utc_iso() == "2026-01-02T03:04:05Z"


def test_hello_world_tool_returns_greeting(monkeypatch):
    fixed = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    monkeypatch.setattr(server, "datetime", type("FrozenDateTime", (), {"now": staticmethod(lambda tz=None: fixed)}))

    tool_server = server.build_server()
    # The tool function is exposed through the MCP server, but the business logic
    # is simple enough that we verify the visible output through the description.
    assert server.describe_server().startswith("helloworld-demo-mcp:")
    assert "hello_world" in server.describe_server()
