---
tags: [mcp, protocol, implementation, sdk, deployment, guide]
---
# MCP Implementation Guide

Practical guide to implementing MCP servers and clients using official SDKs, with configuration and deployment strategies.

## SDK Ecosystem

MCP provides comprehensive Software Development Kits (SDKs) across multiple programming languages, enabling broad adoption across diverse technology stacks[5][8]. These SDKs handle the complexity of protocol implementation, providing high-level abstractions for server and client development while maintaining compatibility with the underlying JSON-RPC specification[5].

### Available SDKs

**Official SDK Support:**

| Language | Repository | Status | Use Cases |
|----------|-----------|--------|-----------|
| TypeScript | `@modelcontextprotocol/sdk` | Stable | Node.js servers, web clients |
| Python | `mcp` package | Stable | Python servers, CLI tools |
| Java | MCP Java SDK | Stable | Enterprise Java applications |
| Kotlin | MCP Kotlin SDK | Stable | Android, JVM applications |
| C# | MCP.NET | Stable | .NET applications, Windows[5][8] |

**Community SDKs:**
- Rust (community-maintained)
- Go (community-maintained)
- Ruby (community-maintained)

The availability of multiple language SDKs reduces implementation barriers and enables organizations to build MCP integrations using their preferred development tools and frameworks[5].

## Getting Started

### Installing SDKs

**TypeScript/JavaScript:**
```bash
npm install @modelcontextprotocol/sdk
```

**Python:**
```bash
pip install mcp
```

**C#:**
```bash
dotnet add package MCP
```

### Basic Server Implementation

**Python Example:**
```python
from mcp.server import Server, Resource, Tool
from mcp.server.stdio import stdio_server

# Create server instance
app = Server("my-server")

# Define a resource
@app.resource("file://config.json")
async def get_config():
    return {
        "uri": "file://config.json",
        "mimeType": "application/json",
        "text": '{"setting": "value"}'
    }

# Define a tool
@app.tool("calculate")
async def calculate(operation: str, a: float, b: float):
    if operation == "add":
        return f"Result: {a + b}"
    elif operation == "multiply":
        return f"Result: {a * b}"
    else:
        raise ValueError(f"Unknown operation: {operation}")

# Run the server
if __name__ == "__main__":
    stdio_server(app)
```

**TypeScript Example:**
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// Create server instance
const server = new Server(
  {
    name: "my-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

// Define a resource
server.setRequestHandler("resources/read", async (request) => {
  const uri = request.params.uri;
  return {
    contents: [
      {
        uri,
        mimeType: "text/plain",
        text: "Resource content here",
      },
    ],
  };
});

// Define a tool
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "greet") {
    return {
      content: [
        {
          type: "text",
          text: `Hello, ${args.name}!`,
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Run the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Configuration

### Local Configuration (VS Code)

VS Code provides integrated MCP server management through workspace settings[6]:

**Configuration file:** `.vscode/mcp-settings.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${env:POSTGRES_CONNECTION_STRING}"
      }
    }
  }
}
```

**Configuration options:**
- `command` - Executable to run
- `args` - Command line arguments
- `env` - Environment variables (supports `${env:VAR_NAME}` substitution)

**Benefits:**
- Project-specific server configurations
- Team sharing via source control
- Environment variable integration
- Automatic server lifecycle management[6]

### Enterprise Configuration (Microsoft Copilot Studio)

Microsoft Copilot Studio provides graphical interfaces for MCP server configuration and management[15]:

**Configuration approach:**
1. Navigate to Copilot Studio admin panel
2. Select "Connectors" section
3. Add new MCP connector
4. Configure:
   - Server URL (for remote servers)
   - Authentication method
   - Network settings (VNet integration)
   - Security policies (DLP)

**Enterprise features:**
- Centralized server management
- Role-based access control
- Network security integration
- Compliance controls
- Usage analytics[15]

### Environment Variables

Best practice for credential management:

**Local development (.env file):**
```bash
# Database credentials
DB_HOST=localhost
DB_USER=dbuser
DB_PASSWORD=secretpassword

# API keys
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxx

# Server configuration
SERVER_PORT=3000
LOG_LEVEL=debug
```

**Loading environment variables:**

Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
api_key = os.getenv("GITHUB_TOKEN")
```

TypeScript:
```typescript
import * as dotenv from "dotenv";
dotenv.config();

const dbHost = process.env.DB_HOST;
const apiKey = process.env.GITHUB_TOKEN;
```

**Security considerations:**
- Never commit `.env` files to source control
- Use different credentials per environment
- Rotate credentials regularly
- Use secret management services in production

## Deployment Patterns

### Local Development (stdio)

**Use case:** Development, testing, single-user scenarios

**Characteristics:**
- Server runs as subprocess
- Communication via stdin/stdout
- No network exposure
- Simple to debug[3][6]

**Deployment:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

**Benefits:**
- Fast iteration
- Easy debugging
- Secure by default
- No infrastructure needed

### Remote Deployment (HTTP + SSE)

**Use case:** Production, multi-user, enterprise scenarios

**Characteristics:**
- Server runs as web service
- HTTP POST for client-to-server
- SSE for server-to-client
- Network accessible[3][4]

**Deployment architecture:**
```text
Client → Load Balancer → MCP Server Instances
                       ↓
                   Database / Services
```

**Infrastructure considerations:**
- Container deployment (Docker, Kubernetes)
- Load balancing for scalability
- Health checks and monitoring
- SSL/TLS termination
- Rate limiting

**Example Docker deployment:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server.py .

EXPOSE 8000
CMD ["python", "server.py", "--transport", "http", "--port", "8000"]
```

### Hybrid Deployment

**Use case:** Mix of local and remote servers

**Strategy:**
- Local servers for personal files, local tools
- Remote servers for shared resources, databases
- Choose transport based on security and performance needs

**Configuration:**
```json
{
  "mcpServers": {
    "local-files": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "~/Documents"]
    },
    "shared-database": {
      "url": "https://mcp-db.company.com",
      "auth": {
        "type": "oauth",
        "clientId": "${env:OAUTH_CLIENT_ID}"
      }
    }
  }
}
```

## Pre-Built Servers

The MCP ecosystem includes production-ready servers for popular systems[7][8]:

### Official Servers

**File System Access:**
```bash
npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/directory
```

**GitHub Integration:**
```bash
npx -y @modelcontextprotocol/server-github
# Requires GITHUB_TOKEN environment variable
```

**PostgreSQL Database:**
```bash
npx -y @modelcontextprotocol/server-postgres
# Requires POSTGRES_CONNECTION_STRING environment variable
```

**Google Drive:**
```bash
npx -y @modelcontextprotocol/server-google-drive
# Requires Google OAuth credentials
```

**Slack Integration:**
```bash
npx -y @modelcontextprotocol/server-slack
# Requires Slack API token
```

### Community Servers

Extensive community-contributed servers available at:
- https://github.com/modelcontextprotocol/servers
- NPM registry (`@modelcontextprotocol/*` packages)
- Community repositories

**Popular community servers:**
- Database servers (MySQL, MongoDB, Redis)
- Cloud services (AWS, Azure, GCP)
- Development tools (Git, Docker)
- Productivity tools (Notion, Todoist)

## Development Tools

### Debugging

**Enable debug logging:**

Python:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

TypeScript:
```typescript
process.env.DEBUG = "mcp:*";
```

**Test with MCP Inspector:**
The MCP Inspector tool provides interactive testing:
```bash
npx @modelcontextprotocol/inspector python server.py
```

Features:
- Interactive server testing
- View available resources/tools
- Execute tools with custom parameters
- Inspect request/response messages

### Testing

**Unit testing resources:**

Python:
```python
import pytest
from mcp.server import Server

@pytest.fixture
def server():
    app = Server("test-server")
    # Register resources and tools
    return app

async def test_resource_read(server):
    result = await server.handle_resource_read("file://test.txt")
    assert result["contents"][0]["text"] == "expected content"
```

**Integration testing:**
```python
async def test_full_workflow():
    # Start server
    server = await start_test_server()

    # Connect client
    client = await connect_test_client(server)

    # Test discovery
    tools = await client.list_tools()
    assert "my_tool" in [t.name for t in tools]

    # Test execution
    result = await client.call_tool("my_tool", {"param": "value"})
    assert result.success
```

### Documentation

**Document your server:**

**README should include:**
1. **Purpose** - What the server does
2. **Installation** - How to install and configure
3. **Configuration** - Required environment variables and settings
4. **Available Resources** - What resources are exposed
5. **Available Tools** - What tools are available
6. **Security** - Authentication and permission requirements
7. **Examples** - Usage examples and workflows

**API documentation:**
Generate from code comments:
```python
@app.tool("send_email")
async def send_email(to: str, subject: str, body: str):
    """
    Sends an email to specified recipients.

    Args:
        to: Email address of recipient
        subject: Email subject line
        body: Email body content (plain text)

    Returns:
        Confirmation message with message ID

    Raises:
        ValueError: If email address is invalid
        ConnectionError: If SMTP server is unreachable
    """
    # Implementation
```

## Reference Implementations

Study official reference implementations for best practices[7]:

**Simple servers:**
- `server-filesystem` - File access patterns
- `server-memory` - In-memory resource management

**Complex servers:**
- `server-github` - OAuth flows, API integration
- `server-postgres` - Database connections, query handling

**Learning resources:**
- Official documentation: https://modelcontextprotocol.io
- Example repository: https://github.com/modelcontextprotocol/servers
- Community discussions: GitHub issues and discussions

## Production Considerations

### Monitoring

**Key metrics to track:**
- Request rate (requests per second)
- Response time (latency percentiles)
- Error rate (4xx, 5xx errors)
- Resource utilization (CPU, memory)
- Active connections

**Monitoring tools:**
- Application Performance Monitoring (APM)
- Structured logging (JSON logs)
- Metrics collection (Prometheus, Grafana)
- Distributed tracing (OpenTelemetry)

### Scaling

**Horizontal scaling:**
- Stateless server design
- Load balancing across instances
- Session affinity if needed
- Auto-scaling based on load

**Performance optimization:**
- Cache frequently accessed resources
- Implement connection pooling (databases)
- Use async/await for I/O operations
- Batch requests when possible

### Reliability

**Error handling:**
- Comprehensive error catching
- Meaningful error messages
- Graceful degradation
- Retry logic with exponential backoff

**Health checks:**
```python
@app.health_check
async def health():
    # Check database connection
    # Check external API availability
    # Check resource access
    return {"status": "healthy"}
```

**Graceful shutdown:**
```python
import signal

async def shutdown(server):
    # Close connections
    # Finish pending requests
    # Clean up resources
    await server.stop()

signal.signal(signal.SIGTERM, lambda: shutdown(server))
```

## Troubleshooting

### Common Issues

**Server won't start:**
- Check command path and arguments
- Verify environment variables are set
- Review server logs for error messages
- Test server independently

**Client can't connect:**
- Verify server is running
- Check transport configuration (stdio vs HTTP)
- Review network/firewall settings
- Validate authentication credentials

**Tools not appearing:**
- Check tool registration code
- Verify server capabilities declaration
- Review client discovery logs
- Test with MCP Inspector

**Permission denied errors:**
- Review scope configuration
- Check file system permissions
- Verify authentication tokens
- Review user consent logs

### Debug Checklist

1. **Server logs** - Enable debug logging
2. **Transport** - Verify correct transport type
3. **Authentication** - Check credentials
4. **Network** - Test connectivity (for remote servers)
5. **Configuration** - Validate JSON syntax
6. **Environment** - Verify environment variables
7. **Versions** - Check SDK version compatibility

## Migration Guide

### From Custom Integration to MCP

**Assessment:**
1. Identify current integration points
2. Map to MCP capabilities (resources, tools, prompts)
3. Plan phased migration

**Migration steps:**
1. **Pilot:** Implement one MCP server for key functionality
2. **Test:** Validate with subset of users
3. **Expand:** Gradually migrate remaining integrations
4. **Deprecate:** Remove old custom integration code

**Benefits:**
- Standardized approach
- Reduced maintenance burden
- Better security model
- Ecosystem compatibility

## Related Concepts

### Prerequisites
- [[mcp_overview]] - Need to understand MCP fundamentals before implementation
- [[mcp_architecture]] - Need to understand architecture before implementing
- [[mcp_security]] - Need to understand security requirements for implementation

### Related Topics
- [[mcp_resources]] - Implementation of resource servers
- [[mcp_tools]] - Implementation of tool servers
- [[mcp_prompts]] - Implementation of prompt servers
- [[adding_mcp_to_claude_code]] - Related to implementing MCP in practice

### Extends
- [[mcp_architecture]] - Practical implementation of the architecture

### Extended By
- [[python_mcp_sdk]] - Python-specific SDK implementation details
- [[csharp_mcp_sdk_docs]] - C#-specific SDK implementation details
