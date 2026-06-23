"""Hello-world MCP demo package."""

from .server import APP_NAME, TOOL_NAME, build_server, current_utc_iso, describe_server

__all__ = [
    "APP_NAME",
    "TOOL_NAME",
    "build_server",
    "current_utc_iso",
    "describe_server",
]

__version__ = "0.1.0"
