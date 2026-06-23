import asyncio
import subprocess
import sys
import time
from pathlib import Path

import pytest
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client

from helloworld_demo_mcp.server import DEFAULT_PORT


@pytest.mark.integration
@pytest.mark.asyncio
async def test_streamable_http_tool_call_round_trip(tmp_path: Path):
    port = DEFAULT_PORT + 7
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "helloworld_demo_mcp.server",
            "--transport",
            "streamable-http",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        base_url = f"http://127.0.0.1:{port}/mcp"
        health_url = f"http://127.0.0.1:{port}/healthz"

        for _ in range(50):
            if proc.poll() is not None:
                stdout, stderr = proc.communicate(timeout=1)
                raise AssertionError(f"Server exited early:\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")
            try:
                import httpx

                health = httpx.get(health_url, timeout=1.0)
                if health.status_code == 200:
                    break
            except Exception:
                time.sleep(0.1)
        else:
            raise AssertionError("Server did not become ready")

        async with streamable_http_client(base_url) as (read_stream, write_stream, _session_id):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tool_list = await session.list_tools()
                assert [tool.name for tool in tool_list.tools] == ["hello_world"]

                result = await session.call_tool("hello_world", {})
                rendered = "\n".join(getattr(item, "text", str(item)) for item in result.content)
                assert "Hello world!" in rendered
                assert "Current UTC time:" in rendered
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)
