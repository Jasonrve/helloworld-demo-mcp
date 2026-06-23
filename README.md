# helloworld-demo-mcp

A tiny **MCP server over streamable HTTP** that exposes one tool: `hello_world`.

The tool returns a plain English greeting plus the current UTC time.

## What is included

- one MCP tool: `hello_world`
- streamable HTTP transport for MCP clients
- a `/healthz` endpoint for container probes
- a Docker image
- a Helm chart
- GitHub Actions to build and publish the image to GitHub Container Registry

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Run the server locally

```bash
helloworld-demo-mcp --transport streamable-http --host 127.0.0.1 --port 3000
```

Or print a short description and exit:

```bash
helloworld-demo-mcp --describe
```

## Call the MCP tool

The server exposes its MCP endpoint at `/mcp` when running in streamable HTTP mode.

Example with an MCP client:

```python
import asyncio

from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    async with streamablehttp_client("http://127.0.0.1:3000/mcp") as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("hello_world", {})
            print(result)


asyncio.run(main())
```

## Docker

Build and run the container:

```bash
docker build -t helloworld-demo-mcp:local .
docker run --rm -p 3000:3000 helloworld-demo-mcp:local
```

The health check should then succeed:

```bash
curl http://127.0.0.1:3000/healthz
```

## Helm

Render the chart:

```bash
helm template helloworld-demo-mcp charts/helloworld-demo-mcp
```

Install it into a namespace:

```bash
helm upgrade --install helloworld-demo-mcp charts/helloworld-demo-mcp \
  --namespace helloworld-demo-mcp \
  --create-namespace
```

## GitHub Container Registry

The GitHub Actions workflow publishes images to:

```text
ghcr.io/Jasonrve/helloworld-demo-mcp
```

Tags are emitted for the branch SHA and for release tags when you push them.
