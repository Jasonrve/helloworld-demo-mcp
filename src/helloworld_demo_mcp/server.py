from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Final

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

APP_NAME: Final[str] = "helloworld-demo-mcp"
TOOL_NAME: Final[str] = "hello_world"
TOOL_DESCRIPTION: Final[str] = "Return a hello-world greeting together with the current UTC time."
DEFAULT_HOST: Final[str] = "0.0.0.0"
DEFAULT_PORT: Final[int] = 3000


@dataclass(frozen=True)
class ServerConfig:
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    transport: str = "streamable-http"


def current_utc_iso() -> str:
    """Return the current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def describe_server() -> str:
    return f"{APP_NAME}: tool={TOOL_NAME}, transport=streamable-http"


def build_server(config: ServerConfig | None = None) -> FastMCP:
    config = config or ServerConfig()
    server = FastMCP(
        APP_NAME,
        instructions="Call hello_world to print a greeting and the current UTC time.",
    )
    server.settings.host = config.host
    server.settings.port = config.port

    @server.tool(name=TOOL_NAME, description=TOOL_DESCRIPTION)
    def hello_world() -> str:
        return f"Hello world! Current UTC time: {current_utc_iso()}"

    @server.custom_route("/healthz", methods=["GET"])
    async def healthz(_request: Request) -> Response:
        return JSONResponse(
            {
                "status": "ok",
                "service": APP_NAME,
                "transport": config.transport,
            }
        )

    return server


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the hello-world MCP demo server.")
    parser.add_argument(
        "--transport",
        choices=("stdio", "streamable-http"),
        default="streamable-http",
        help="MCP transport to use (default: streamable-http).",
    )
    parser.add_argument("--host", default=DEFAULT_HOST, help="HTTP host to bind when using streamable-http.")
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="HTTP port to bind when using streamable-http.",
    )
    parser.add_argument(
        "--describe",
        action="store_true",
        help="Print a short description of the server and exit.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.describe:
        print(describe_server())
        return

    server = build_server(ServerConfig(host=args.host, port=args.port, transport=args.transport))
    server.run(transport=args.transport)


if __name__ == "__main__":
    main()
