---
tags: [mcp, protocol, architecture, specification, technical]
---
# MCP Architecture

Client-server architecture enabling standardized communication between AI applications and external systems through JSON-RPC 2.0 protocol.

## Fundamental Architecture

MCP employs a client-server architecture designed to enable seamless communication between AI hosts and external data sources[1][2]. The architecture consists of three primary components that work in concert to facilitate standardized integrations:

### Component Roles

**MCP Hosts**
- Primary AI applications that users interact with
- Examples: Claude Desktop, Visual Studio Code, custom AI workflows[1][6]
- Contain MCP clients for protocol communication
- Manage user consent and security boundaries

**MCP Clients**
- Maintain direct one-to-one connections with individual servers
- Handle protocol communication layer
- Implement capability negotiation
- Manage connection lifecycle[1][4]

**MCP Servers**
- Lightweight programs exposing specific capabilities
- Focus on single domains or data sources (file systems, databases, APIs)
- Enable granular permission control[1][2]
- Typically stateless, focused components[7]

### Design Philosophy

The protocol's design centers on **composability and modularity**. Organizations deploy multiple focused MCP servers rather than monolithic integrations[3]. This approach provides:

- **Reduced security risks** through scoped permissions
- **Improved maintainability** of individual components
- **Enhanced auditability** of server behavior
- **Flexible deployment** patterns (local or remote)[3]

Each server typically focuses on a specific domain, enabling granular control over access permissions and functionality[7].

## Communication Protocol Specifications

### JSON-RPC 2.0 Foundation

At its technical core, MCP utilizes **JSON-RPC 2.0** message formatting to establish stateful connections between clients and servers[2][4]. This provides:

- Structured request-response patterns
- Error handling conventions
- Bidirectional communication support
- Language-agnostic message format

### Transport Mechanisms

MCP supports multiple transport mechanisms to accommodate different deployment scenarios:

#### 1. stdio Transport (Local Deployments)

Servers run as **subprocesses** of the host application:
- Secure local integrations without network exposure
- Communication via standard input/output
- Process isolation for security
- Ideal for development and single-user scenarios[3][6]

**Use cases:**
- IDE integrations
- Local tool access
- Development environments
- Personal productivity tools

#### 2. HTTP with Server-Sent Events (Remote Deployments)

For distributed architectures:
- **Server-to-client**: Server-Sent Events (SSE) for streaming
- **Client-to-server**: Standard HTTP POST requests
- Network-capable for enterprise deployments
- Supports remote server hosting[3][4]

**Use cases:**
- Enterprise server deployments
- Shared team resources
- Cloud-hosted integrations
- Multi-user scenarios

## Connection Lifecycle

The connection lifecycle follows a structured initialization pattern ensuring compatibility and capability negotiation[4]:

### 1. Initialization Request

Client sends `initialize` request containing:
- **Protocol version information** - Ensures compatibility
- **Client capability declarations** - What the client supports
- **Implementation details** - Client identification

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "resources": {},
      "tools": {},
      "prompts": {}
    },
    "clientInfo": {
      "name": "example-client",
      "version": "1.0.0"
    }
  }
}
```

### 2. Server Response

Server responds with:
- **Server protocol version** - Version compatibility check
- **Server capabilities** - Available features (resources, tools, prompts)
- **Server information** - Implementation details

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "resources": {},
      "tools": {},
      "prompts": {}
    },
    "serverInfo": {
      "name": "example-server",
      "version": "1.0.0"
    }
  }
}
```

### 3. Initialized Notification

Client sends `initialized` notification:
- Acknowledges successful connection
- No response expected (notification pattern)
- Signals readiness for normal operations[4]

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

### 4. Normal Operation

After initialization, the connection supports:
- **Request-response patterns** - Synchronous operations (resource reads, tool calls)
- **Notification patterns** - Asynchronous, one-way communications (status updates, events)[4]

## Communication Patterns

### Request-Response Pattern

Used for operations requiring confirmation:
- Resource reads
- Tool executions
- Prompt retrieval
- Capability discovery

**Characteristics:**
- Synchronous operation
- Client expects response
- Error handling built-in
- Timeout management required

### Notification Pattern

Used for asynchronous events:
- Status updates
- Resource changes
- Server events
- Client state updates

**Characteristics:**
- Asynchronous operation
- No response expected
- Fire-and-forget semantics
- Event-driven architecture

## Architectural Benefits

### Composability

Multiple servers can be combined:
- Each server provides focused capabilities
- Clients aggregate functionality across servers
- No server-to-server dependencies required
- Clean separation of concerns

### Scalability

Architecture supports growth:
- Add new servers without modifying existing ones
- Clients discover capabilities dynamically
- Horizontal scaling through multiple server instances
- Load distribution across servers

### Security Boundaries

Clear isolation points:
- Client controls server access
- Server scoped to specific domains
- No cross-server communication
- User consent at host level

### Maintainability

Modular design enables:
- Independent server updates
- Isolated testing and debugging
- Clear ownership boundaries
- Simplified auditing

## Implementation Considerations

### Server Design

Best practices for MCP servers:
- **Single responsibility** - Focus on one domain or data source
- **Stateless preferred** - Minimize session state when possible
- **Error handling** - Comprehensive error reporting
- **Documentation** - Clear capability descriptions

### Client Design

Best practices for MCP clients:
- **Connection management** - Handle reconnection and failures
- **Capability caching** - Cache server capabilities after discovery
- **Timeout handling** - Implement reasonable timeouts
- **User consent** - Always obtain permission before operations

### Deployment Patterns

Common deployment strategies:
- **Local-first** - Start with stdio for development
- **Gradual migration** - Move to HTTP+SSE for production
- **Hybrid approach** - Local for personal tools, remote for shared resources
- **Security zones** - Different servers for different trust levels

## Related Concepts

### Prerequisites
- [[mcp_overview]] - Need to understand MCP fundamentals before diving into architecture

### Extends
- [[mcp_overview]] - Provides detailed technical architecture for MCP protocol

### Extended By
- [[mcp_security]] - Security model built on top of architecture
- [[mcp_implementation]] - Implementation guide provides practical realization of architecture
- [[mcp_resources]] - Need to understand how resources operate within MCP architecture
- [[mcp_tools]] - Need to understand how tools operate within MCP architecture
- [[mcp_prompts]] - Need to understand how prompts are delivered through architecture
- [[adding_to_claude_code]] - Understanding MCP architecture helps with server configuration