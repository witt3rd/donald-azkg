---
tags: [mcp, protocol, ai, overview]
---
# Model Context Protocol (MCP) - Overview

MCP is an open protocol that standardizes how AI applications integrate with external data sources and tools - essentially "USB-C for AI applications."

## What is MCP?

Model Context Protocol (MCP) represents a paradigm shift in how artificial intelligence systems integrate with external data sources and tools, addressing the fundamental challenge of AI isolation through a standardized, open protocol framework. Introduced by Anthropic in November 2024, MCP has rapidly gained adoption across the AI ecosystem, with major technology companies including Microsoft, GitHub, and OpenAI integrating the protocol into their platforms[1][8][15].

The protocol essentially functions as "a USB-C port for AI applications," providing a universal standard that transforms the complex M×N integration problem into a simplified M+N approach, where M represents AI applications and N represents external systems[1][13]. This means instead of building custom integrations between every AI application and every data source, each component only needs to implement MCP once to work with all other MCP-compatible systems.

## Why MCP Matters

**Before MCP:** Each AI application needed custom integrations with every data source and tool:

- Duplicated effort across applications
- Inconsistent security models
- Difficult to maintain and audit
- Limited interoperability

**With MCP:** Universal protocol enables:

- Write once, use everywhere integrations
- Standardized security and privacy controls
- Composable, modular architecture
- Ecosystem of reusable servers and tools

## Core Concepts

MCP consists of three main capabilities that AI applications can leverage:

1. **Resources** - Read-only access to data sources (like files, databases, APIs)
2. **Tools** - Functions the AI can execute with side effects (like sending emails, creating tasks)
3. **Prompts** - Reusable templates and workflows that combine resources and tools

Each capability is exposed through lightweight MCP servers that connect to AI applications via a client-server architecture.

## MCP Knowledge Map

This note serves as the entry point to understanding MCP. For detailed information, see:

### Architecture & Technical Details

- [[mcp_architecture]] - Client-server design, transport mechanisms, connection lifecycle, and communication patterns

### Core Capabilities

- [[mcp_resources]] - Read-only data access layer, dynamic discovery, and resource patterns
- [[mcp_tools]] - Function execution framework, parameter design, and side effects
- [[mcp_prompts]] - Template system, workflow design, and parameterization

### Implementation & Security

- [[mcp_security]] - Authentication, authorization, user consent, privacy controls, and access management
- [[mcp_implementation]] - SDK ecosystem, language support, configuration, deployment, and reference implementations

## Key Adoption Points

**Major Integrations:**

- Microsoft Copilot Studio - Enterprise agent platform with MCP support[15]
- GitHub - Official MCP server for repository interaction[10]
- Claude Desktop - Native MCP client for local integrations[1]
- VS Code - Integrated MCP server management[6]

**Enterprise Adopters:**

- Block - Internal knowledge base integration[8][11]
- Apollo - CRM and document access[8][11]

**Development Tools:**

- Zed, Replit, Sourcegraph - Code intelligence with MCP[11]
- AI2SQL - Natural language database queries[11]

## Quick Start Resources

For developers looking to build with MCP:

1. **Learn the architecture**: Start with [[mcp_architecture]] to understand how components communicate
2. **Choose your capability**: Decide if you need [[mcp_resources]], [[mcp_tools]], or [[mcp_prompts]]
3. **Implement securely**: Review [[mcp_security]] for best practices
4. **Build your server**: Use [[mcp_implementation]] for SDK selection and deployment

## Strategic Value

Model Context Protocol represents a foundational advancement in AI system integration, providing a standardized framework that addresses the critical challenge of AI isolation from external data sources and tools. The protocol's client-server architecture, comprehensive security model, and flexible implementation options make it suitable for diverse deployment scenarios, from individual developer tools to enterprise-scale AI platforms.

With growing adoption across major technology companies and a robust ecosystem of SDKs and reference implementations, MCP is positioned to become the standard method for AI system integration, enabling more capable and contextually aware AI applications while maintaining necessary security and privacy protections.

## Related Concepts

### Related Topics

- [[llm_agents]] - Claude Code agents use MCP for tool access and integration

### Extended By

- [[mcp_architecture]] - Architecture provides technical foundation for MCP
- [[mcp_resources]] - Resources implement one of three core MCP capabilities
- [[mcp_tools]] - Tools implement one of three core MCP capabilities
- [[mcp_prompts]] - Prompts implement one of three core MCP capabilities
- [[mcp_security]] - Need to understand MCP fundamentals before security model
- [[mcp_implementation]] - Need to understand MCP fundamentals before implementation
- [[filesystem]] - Need to understand MCP protocol
- [[adding_mcp_to_claude_code]] - Need to understand MCP fundamentals before configuring servers
