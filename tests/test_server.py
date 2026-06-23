from helloworld_demo_mcp.server import APP_NAME, TOOL_NAME, build_server, describe_server


def test_describe_server_mentions_hello_world_tool():
    assert describe_server() == f"{APP_NAME}: tool={TOOL_NAME}, transport=streamable-http"


def test_server_registers_one_explicit_tool(monkeypatch):
    registrations = []

    def fake_tool(self, *args, **kwargs):
        registrations.append(kwargs)

        def decorator(fn):
            return fn

        return decorator

    monkeypatch.setattr("mcp.server.fastmcp.FastMCP.tool", fake_tool)

    build_server()

    assert registrations == [
        {
            "name": "hello_world",
            "description": "Return a hello-world greeting together with the current UTC time.",
        }
    ]


def test_health_route_is_registered(monkeypatch):
    routes = []

    def fake_custom_route(self, path, methods=None, name=None, include_in_schema=True):
        routes.append((path, tuple(methods or []), include_in_schema))

        def decorator(fn):
            return fn

        return decorator

    monkeypatch.setattr("mcp.server.fastmcp.FastMCP.custom_route", fake_custom_route)

    build_server()

    assert ("/healthz", ("GET",), True) in routes
