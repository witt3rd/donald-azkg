---
tags: [python, mcp, fastmcp, guide, api, sdk]
last_refresh: 2025-10-12
---
<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Python MCP SDK: Comprehensive Guide to FastMCP

## Overview

The **Model Context Protocol (MCP)** enables secure, standardized communication between LLM applications and external data sources. This comprehensive guide covers both the official MCP Python SDK and FastMCP, showing how to build hosts, clients, and servers using modern Python practices[^1][^2].

**Latest Update (October 2025)**: FastMCP 2.10 is now fully integrated into the official MCP Python SDK, providing unified codebase with compliance to the June 18, 2025 MCP specification update. Key improvements include middleware architecture, automatic type conversion, OAuth 2.0 authentication, and MCP Registry integration[^13][^14][^15].

## Installation and Setup

### Project Setup with uv

```bash
# Create new project
uv init mcp-project
cd mcp-project

# Install official MCP SDK
uv add "mcp[cli]"

# Install FastMCP 2.0 (advanced features)
uv add fastmcp
```

### Dependencies Structure

```toml
# pyproject.toml
[project]
name = "mcp-project"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "mcp[cli]>=1.9.0",
    "fastmcp>=2.0.0",
    "httpx>=0.25.0",
    "pydantic>=2.0.0"
]
```

## Core MCP Components

### Transport Protocols

MCP supports three transport mechanisms[^3][^4]:

1. **Stdio**: Local communication via standard input/output
2. **SSE (Server-Sent Events)**: HTTP streaming with improved back-pressure handling
3. **HTTP Streaming**: Modern streamable HTTP transport (recommended for production)

**Note (2025 Update)**: Direct WebSocket support has been deprecated in favor of HTTP streaming and SSE, which now offer enhanced back-pressure and fragmentation handling for better reliability on slow or unreliable networks[^14][^15].

## Building MCP Servers

### Basic Server with FastMCP

```python
from mcp.server.fastmcp import FastMCP
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

# Modern typing - no more List, Dict, Optional
@dataclass
class ServerContext:
    config: dict[str, str]
    connections: set[str]

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[ServerContext]:
    """Manage server lifecycle with type-safe context"""
    context = ServerContext(
        config={"version": "1.0.0"},
        connections=set()
    )
    try:
        yield context
    finally:
        # Cleanup
        context.connections.clear()

# Create server with lifespan management
mcp = FastMCP("Data Processor", lifespan=app_lifespan)

@mcp.tool()
def calculate_sum(numbers: list[int]) -> int:
    """Calculate sum of numbers"""
    return sum(numbers)

@mcp.resource("data://{dataset}")
def get_dataset(dataset: str) -> str:
    """Get dataset by name"""
    return f"Dataset: {dataset}"

@mcp.prompt()
def analyze_data(data: str) -> str:
    """Generate analysis prompt"""
    return f"Please analyze this data: {data}"

if __name__ == "__main__":
    mcp.run()
```

### Advanced Server with Multiple Transports

```python
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
import contextlib

# Stateless HTTP server for production
mcp = FastMCP("Production Server", stateless_http=True)

@mcp.tool()
async def fetch_data(url: str) -> dict[str, str]:
    """Fetch data from URL"""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return {"status": str(response.status_code), "data": response.text}

# Run with different transports
if __name__ == "__main__":
    import sys
    transport = sys.argv[^1] if len(sys.argv) > 1 else "stdio"

    if transport == "http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run()  # Default stdio
```

### Low-Level Server Implementation

```python
from mcp.server import Server
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

server = Server("low-level-example")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="process_data",
            description="Process data with validation",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "string"},
                    "format": {"type": "string", "enum": ["json", "csv"]}
                },
                "required": ["data"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, object]) -> list[types.TextContent]:
    if name == "process_data":
        data = arguments["data"]
        return [types.TextContent(type="text", text=f"Processed: {data}")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="low-level-example",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Building MCP Clients

### Basic Client Implementation

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from collections.abc import AsyncIterator

async def create_mcp_client() -> AsyncIterator[ClientSession]:
    """Create MCP client with proper typing"""
    server_params = StdioServerParameters(
        command="uv",
        args=["--directory", "/path/to/server", "run", "server.py"],
        env={"DEBUG": "1"}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session

async def main():
    async with create_mcp_client() as session:
        # List available tools
        tools = await session.list_tools()
        print(f"Available tools: {[tool.name for tool in tools.tools]}")

        # Call a tool
        result = await session.call_tool("calculate_sum", {"numbers": [1, 2, 3, 4, 5]})
        print(f"Result: {result}")

        # Read a resource
        content, mime_type = await session.read_resource("data://sales")
        print(f"Resource content: {content}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Streamable HTTP Client

```python
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

async def http_client_example():
    """Example using HTTP streaming transport"""
    async with streamablehttp_client("https://api.example.com/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Use the session
            tools = await session.list_tools()
            result = await session.call_tool("echo", {"message": "Hello MCP!"})
            print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(http_client_example())
```

## Building MCP Hosts

### Host Configuration

The MCP host manages connections to multiple servers through JSON configuration[^5][^6]:

```json
{
  "mcpServers": {
    "local-calculator": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/calculator",
        "run",
        "server.py"
      ],
      "env": {
        "DEBUG": "1",
        "DATA_PATH": "/data"
      },
      "timeout": 30000
    },
    "remote-api": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/remote",
        "run",
        "api_server.py"
      ],
      "env": {
        "API_KEY": "${API_KEY}",
        "BASE_URL": "https://api.example.com"
      }
    },
    "http-service": {
      "url": "https://mcp-service.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${TOKEN}"
      }
    }
  }
}
```

### Host Implementation

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from collections.abc import AsyncIterator
import json
import os
from pathlib import Path

class MCPHost:
    """MCP Host managing multiple server connections"""

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.sessions: dict[str, ClientSession] = {}

    async def load_config(self) -> dict[str, dict[str, object]]:
        """Load MCP configuration"""
        with open(self.config_path) as f:
            config = json.load(f)
        return config["mcpServers"]

    async def connect_stdio_server(self, name: str, config: dict[str, object]) -> ClientSession:
        """Connect to stdio-based MCP server"""
        from mcp import StdioServerParameters

        server_params = StdioServerParameters(
            command=config["command"],
            args=config.get("args", []),
            env=config.get("env", {})
        )

        read, write = await stdio_client(server_params).__aenter__()
        session = ClientSession(read, write)
        await session.initialize()
        return session

    async def connect_http_server(self, name: str, config: dict[str, object]) -> ClientSession:
        """Connect to HTTP-based MCP server"""
        url = config["url"]
        headers = config.get("headers", {})

        read, write, _ = await streamablehttp_client(url, headers=headers).__aenter__()
        session = ClientSession(read, write)
        await session.initialize()
        return session

    async def start(self):
        """Start all configured MCP servers"""
        config = await self.load_config()

        for name, server_config in config.items():
            try:
                if "command" in server_config:
                    session = await self.connect_stdio_server(name, server_config)
                elif "url" in server_config:
                    session = await self.connect_http_server(name, server_config)
                else:
                    continue

                self.sessions[name] = session
                print(f"Connected to MCP server: {name}")

            except Exception as e:
                print(f"Failed to connect to {name}: {e}")

    async def list_all_tools(self) -> dict[str, list[str]]:
        """List tools from all connected servers"""
        all_tools = {}
        for name, session in self.sessions.items():
            try:
                tools = await session.list_tools()
                all_tools[name] = [tool.name for tool in tools.tools]
            except Exception as e:
                print(f"Error listing tools from {name}: {e}")
                all_tools[name] = []
        return all_tools

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict[str, object]):
        """Call a tool on a specific server"""
        if server_name not in self.sessions:
            raise ValueError(f"Server {server_name} not connected")

        session = self.sessions[server_name]
        return await session.call_tool(tool_name, arguments)

# Usage example
async def main():
    host = MCPHost("mcp_config.json")
    await host.start()

    # List all available tools
    tools = await host.list_all_tools()
    print("Available tools:", tools)

    # Call a tool
    result = await host.call_tool("local-calculator", "add", {"a": 5, "b": 3})
    print("Calculation result:", result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Local Development and Testing

### Development Environment Setup

```bash
# Create development environment
uv init mcp-dev
cd mcp-dev

# Install dependencies
uv add "mcp[cli]" fastmcp httpx pytest pytest-asyncio

# Create project structure
mkdir -p {servers,clients,tests,configs}
```

### Testing Servers Locally

```python
# tests/test_server.py
import pytest
from mcp.server.fastmcp import FastMCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

@pytest.fixture
async def test_server():
    """Create test server"""
    mcp = FastMCP("Test Server")

    @mcp.tool()
    def multiply(a: int, b: int) -> int:
        return a * b

    return mcp

@pytest.fixture
async def client_session(test_server):
    """Create test client session"""
    # This would typically spawn the server process
    # For testing, we'll mock the connection
    pass

async def test_tool_execution():
    """Test MCP tool execution"""
    # Create temporary server for testing
    server_script = """
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Test")

@mcp.tool()
def test_add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    mcp.run()
"""

    # Write to temporary file and test
    # Implementation would use subprocess or similar
    pass
```

### MCP Inspector for Development

```bash
# Test server with MCP Inspector
uv run mcp dev server.py

# Test with dependencies
uv run mcp dev server.py --with pandas --with numpy

# Mount local development code
uv run mcp dev server.py --with-editable .
```

### Local Testing Script

```python
# dev_test.py
import asyncio
import subprocess
import tempfile
from pathlib import Path

async def test_mcp_server(server_path: Path):
    """Test MCP server locally"""
    # Start server process
    proc = subprocess.Popen([
        "uv", "run", "--directory", str(server_path.parent),
        "python", str(server_path)
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Test basic communication
        # This would use the MCP protocol
        pass
    finally:
        proc.terminate()
        proc.wait()

async def main():
    server_path = Path("servers/calculator.py")
    await test_mcp_server(server_path)

if __name__ == "__main__":
    asyncio.run(main())
```

## Modern Python Typing Best Practices

### Type Annotations (Python 3.13+)

```python
from collections.abc import Mapping, Sequence, Iterable, AsyncIterator
from typing import Protocol, TypeAlias
from pathlib import Path

# Use built-in generics instead of typing module
UserMap: TypeAlias = dict[str, str | int]
DataList: TypeAlias = list[dict[str, object]]

# Use union syntax instead of Union/Optional
def process_data(data: str | bytes | None) -> str:
    if data is None:
        return "empty"
    return str(data)

# Use Protocol for flexible interfaces
class DataProcessor(Protocol):
    async def process(self, data: bytes) -> dict[str, object]: ...
    def validate(self, schema: dict[str, object]) -> bool: ...

# Prefer abstract types for parameters
def handle_items(items: Iterable[str]) -> list[str]:
    return [item.upper() for item in items]

# Use concrete types for return values
def create_config() -> dict[str, str]:
    return {"version": "1.0", "mode": "production"}
```

### MCP-Specific Typing

```python
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import Tool, Resource, Prompt
from dataclasses import dataclass
from collections.abc import AsyncIterator

@dataclass
class ToolResult:
    """Strongly typed tool result"""
    success: bool
    data: dict[str, object]
    error: str | None = None

class TypedMCPServer:
    """Type-safe MCP server wrapper"""

    def __init__(self, name: str):
        self.mcp = FastMCP(name)
        self.tools: dict[str, Tool] = {}

    def register_tool(self, func: callable) -> None:
        """Register tool with type validation"""
        tool = self.mcp.tool()(func)
        self.tools[func.__name__] = tool

    async def call_tool_typed(self, name: str, args: dict[str, object]) -> ToolResult:
        """Type-safe tool calling"""
        try:
            result = await self.mcp.call_tool(name, args)
            return ToolResult(success=True, data=result)
        except Exception as e:
            return ToolResult(success=False, data={}, error=str(e))
```

## Advanced Features

### FastMCP 2.10+ Advanced Features

**New in 2025**: FastMCP now includes middleware architecture, automatic type conversion, and MCP Registry integration[^13][^15].

```python
from fastmcp import FastMCP
from fastmcp.proxy import ProxyServer
from fastmcp.compose import compose_servers

# Server composition
server1 = FastMCP("Database Server")
server2 = FastMCP("API Server")

# Compose multiple servers
combined = compose_servers([server1, server2])

# Proxy server for protocol conversion
proxy = ProxyServer(
    target_server="http://localhost:8080/mcp",
    transport_mapping={"stdio": "http"}
)

# Generate server from OpenAPI spec
from fastmcp.generators import from_openapi
api_server = from_openapi("https://api.example.com/openapi.json")
```

### Middleware Architecture (2025)

```python
from fastmcp import FastMCP
from fastmcp.middleware import Middleware

class LoggingMiddleware(Middleware):
    async def process_request(self, request):
        print(f"Request: {request}")
        return await self.next(request)

class RateLimitMiddleware(Middleware):
    async def process_request(self, request):
        # Implement rate limiting logic
        return await self.next(request)

mcp = FastMCP("Server with Middleware")
mcp.add_middleware(LoggingMiddleware())
mcp.add_middleware(RateLimitMiddleware())

@mcp.tool()
def protected_operation(data: str) -> str:
    """Operation with middleware protection"""
    return f"Processed: {data}"
```

### MCP Registry Integration (2025)

```python
from fastmcp import FastMCP
from mcp.registry import RegistryClient

mcp = FastMCP("Discoverable Server")

# Register with MCP Registry for service discovery
async def register_server():
    registry = RegistryClient("https://registry.mcp.example.com")
    await registry.register(
        server_id="my-server",
        endpoint="http://localhost:8080/mcp",
        capabilities=["tools", "resources", "prompts"]
    )

@mcp.tool()
def registered_tool(data: str) -> str:
    """Tool discoverable via MCP Registry"""
    return f"Result: {data}"
```

### Authentication and Security

**2025 Update**: OAuth 2.0 is now the recommended standard for authentication, replacing legacy token-based approaches. Middleware-based enforcement is preferred for auth layers and permission checks[^14][^15].

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.provider import TokenVerifier, TokenInfo
from mcp.server.auth.settings import AuthSettings

class OAuth2TokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> TokenInfo:
        # OAuth 2.0 token verification via introspection endpoint
        # Implements RFC 7662 token introspection
        return TokenInfo(
            sub="user123",
            scopes=["mcp:read", "mcp:write"],
            active=True
        )

mcp = FastMCP(
    "Secure Server",
    token_verifier=OAuth2TokenVerifier(),
    auth=AuthSettings(
        issuer_url="https://auth.example.com",
        resource_server_url="http://localhost:3001",
        required_scopes=["mcp:read", "mcp:write"],
        oauth2_enabled=True  # New in 2025
    )
)

@mcp.tool()
async def secure_operation(data: str) -> str:
    """Protected operation requiring OAuth 2.0 authentication"""
    return f"Processed: {data}"
```

## Production Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install dependencies
RUN uv sync --frozen

# Expose port for HTTP transport
EXPOSE 8080

# Run server
CMD ["uv", "run", "python", "src/server.py"]
```

### Production Configuration

```python
# production_server.py
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
import os

# Production server with HTTP transport
mcp = FastMCP(
    "Production Server",
    stateless_http=True,
    json_response=True  # Better for load balancing
)

@mcp.tool()
async def production_tool(data: str) -> dict[str, str]:
    """Production-ready tool"""
    return {"result": f"Processed: {data}", "version": "1.0.0"}

# Mount to FastAPI for advanced features
app = FastAPI(title="MCP Production Server")
app.mount("/mcp", mcp.streamable_http_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

## Best Practices Summary

### Development Workflow

1. **Project Structure**: Use `uv` for dependency management[^2][^7]
2. **Testing**: Use MCP Inspector for development testing[^8]
3. **Typing**: Follow Python 3.13+ typing practices with strict type enforcement[^9][^10][^16]
4. **Transports**: Prefer HTTP streaming for production[^11]
5. **Configuration**: Use JSON configuration for hosts[^5]
6. **Registry Integration**: Register servers with MCP Registry for discoverability[^14]

### Performance Considerations

- Use stateless HTTP servers for scalability[^1]
- Implement proper error handling and timeouts[^5]
- Use async/await for I/O operations[^1]
- Consider server composition for modularity[^12]
- Leverage middleware for cross-cutting concerns without overhead[^15]
- Use automatic type conversion to reduce error rates[^15]

### Security Guidelines

- Implement OAuth 2.0 authentication for production servers[^14][^15]
- Use environment variables for sensitive configuration[^5]
- Validate all inputs and outputs with dataclass schemas[^16]
- Implement auth and permission checks via middleware[^15]
- Follow context isolation and explicit tool whitelisting[^16]

### Migration from Legacy Features (2025)

- **Deprecated**: Legacy tool registration methods - use new type signature conventions[^15][^16]
- **Deprecated**: Direct WebSocket transports - migrate to HTTP streaming or SSE[^14][^15]
- **Deprecated**: Ad-hoc serialization methods - use standardized interfaces[^15]
- **Required**: Pin both FastMCP and official SDK to matching protocol versions[^14]

This comprehensive guide provides the foundation for building robust MCP applications using modern Python practices. The examples demonstrate real-world usage patterns while following the latest typing conventions and development practices.

<div style="text-align: center">⁂</div>

[^1]: <https://github.com/modelcontextprotocol/python-sdk>
[^2]: <https://github.com/hideya/mcp-python-sdk>
[^3]: <https://mcp-framework.com/docs/Transports/http-stream-transport/>
[^4]: <https://modelcontextprotocol.io/docs/concepts/transports>
[^5]: <https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-configuration.html>
[^6]: <https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-understanding-config.html>
[^7]: <https://github.com/wanderingnature/mcp-typed-prompts>
[^8]: <https://www.stainless.com/mcp/how-to-test-mcp-servers>
[^9]: <https://github.com/jlowin/fastmcp>
[^10]: <https://www.reddit.com/r/mcp/comments/1k0v8n3/announcing_fastmcp_20/>
[^11]: <https://brightdata.com/blog/ai/sse-vs-streamable-http>
[^12]: <https://cdn.cdata.com/help/DJK/mcp/pg_connectionmcp.htm>
[^13]: <https://pypi.org/project/fastmcp/1.0/>
[^14]: <https://modelcontextprotocol.info/blog/mcp-next-version-update/>
[^15]: <https://gofastmcp.com/updates>
[^16]: <https://pypi.org/project/mcp/1.9.0/>

## Related Concepts

### Prerequisites

- [[mcp_implementation]] - Need general implementation knowledge before Python-specific SDK

### Related Topics

- [[csharp_mcp_sdk_docs]] - Alternative language SDK for MCP
- [[claude_agent_sdk]] - Agent SDK uses MCP SDK for custom tool development and integration
- [[claude_agent_sdk_production]] - Production examples of MCP server integration with Agent SDK

### Extends

- [[mcp_implementation]] - Python-specific implementation of MCP SDK

### Extended By

- [[fastmcp_shutdown]] - Specific FastMCP implementation issue

### Alternatives

- [[csharp_mcp_sdk_docs]] - Use C# instead of Python for MCP development
