---
tags: [mcp, api, agents, integration, reference, tools]
---
# Agents, MCP Server Tools, and Raw APIs

## Definitions and Roles

An agent is a system that uses an LLM to reason about tasks, create execution plans, and invoke tools to accomplish goals. The agent handles user interaction, maintains conversation context, decomposes complex requests into steps, and orchestrates tool execution. Agents do not directly implement capabilities; they determine what needs to be done and coordinate the execution through available tools.

MCP (Model Context Protocol) servers expose tools that agents can invoke. These servers implement a standardized protocol for tool discovery, description, and invocation over STDIO or SHTTP. When an agent needs to execute an action, it presents the available MCP tools to an LLM along with the current task context. The LLM selects which tools to call and provides the necessary arguments. The agent then invokes these tools through the MCP server. MCP tools typically do not use LLMs themselves; they execute specific, deterministic operations.

MCP tools are not simple API wrappers. They combine multiple API calls into higher-level operations that match how LLMs reason about tasks. For example, instead of exposing separate database query, filter, and update endpoints, an MCP tool might provide a single "update_matching_records" operation. This semantic abstraction makes tools easier for LLMs to select and use correctly.

## Why Not Direct API Usage

Agents can technically call raw APIs directly, but this creates several problems. First, the agent must translate API specifications into tool descriptions the LLM can understand. Then it must convert the LLM's tool calls back into proper API requests with correct headers, authentication, and parameter formatting. This translation code lives in the agent, coupling it to each API's implementation details.

When APIs change, the agent code must be updated. As more APIs are integrated, the agent accumulates more translation and integration code. The agent ends up containing more API-specific code than reasoning logic. Additionally, raw APIs often use technical parameters that don't map well to how LLMs reason about tasks, making tool selection less reliable.

There's also a performance consideration. Frontier models are trained on the OpenAI JSON schema format for tool definitions, which MCP uses. The OpenAI API itself enforces this schema when providing tools for models to reason about. When agents use custom API handling, they must either convert to this standard format or use alternative representations that LLMs may not handle as effectively. Models perform better with the standardized tool calling format they were trained on.

MCP solves these problems by standardizing how tools are described, discovered, and invoked using the same JSON schema format that frontier models expect. The protocol handles the mechanics of tool calling, letting agents focus on reasoning and planning. MCP servers handle API-specific details like authentication, error handling, and response parsing. When APIs change, only the MCP server needs updating, not the agent.

## Security Advantages

MCP provides substantial security improvements over direct API access. When agents call raw APIs directly, they must manage credentials, implement access controls, and handle security policies independently. This distributed approach creates multiple points of vulnerability and inconsistent security enforcement.

MCP servers act as a security control plane between agents and backend systems. Credentials remain within the MCP server layer, never exposed to the LLM or agent. The MCP server authenticates to backend APIs on behalf of the agent, eliminating credential sprawl and enabling centralized key rotation. Access control decisions happen at the MCP layer, where policies can be consistently enforced based on agent identity, user context, or other factors.

MCP proxies and gateway services extend these security capabilities. They provide a single enforcement point for rate limiting, preventing agents from overwhelming backend systems through accidental loops or malicious requests. All agent-to-tool interactions flow through the MCP layer, enabling comprehensive audit logging of requests, responses, and metadata. This centralized logging supports security monitoring, anomaly detection, and compliance requirements that would be difficult to implement with direct API access.

Data filtering and redaction can be systematically applied at the MCP layer. Before responses reach the agent, the MCP server can remove sensitive information, mask personally identifiable data, or apply other data governance policies. This filtering happens consistently for all agents without requiring modifications to agent code or prompt engineering.

The MCP layer also provides isolation between agents and backend systems. If an agent is compromised, the attacker cannot directly access backend APIs or extract credentials. The MCP server limits what actions the compromised agent can perform based on its defined permissions. This containment reduces the blast radius of security incidents.

Version negotiation and capability declaration in MCP prevent insecure fallback behaviors. Both clients and servers explicitly declare supported versions and features, avoiding accidental exposure through outdated or incompatible integrations. The declarative nature of MCP tool definitions also simplifies security review and validation before deployment.

## Architecture

The standard architecture separates concerns across three layers. Agents handle reasoning, planning, and orchestration using LLMs. MCP servers provide tools with semantic interfaces that make sense for LLM reasoning. Raw APIs implement the actual functionality without LLM-specific considerations.

This separation allows each layer to evolve independently. Agents can improve their reasoning without touching API integration code. MCP tools can be updated for new API versions without modifying agents. APIs can be replaced entirely as long as the MCP tool interface remains consistent.

While nothing technically prevents an MCP tool from using an LLM internally or an agent from calling APIs directly, these patterns violate the architectural separation. Agents should use MCP tools for actions. MCP tools should provide meaningful operations, not just wrap individual API endpoints. This convention creates systems where each component has a clear, focused responsibility.

## Summary: Key Talking Points

**Role Distinction**
- Agents: LLM-powered reasoning, planning, and orchestration
- MCP Tools: Deterministic actions with semantic interfaces for LLM consumption  
- Raw APIs: Backend functionality without LLM considerations

**Why MCP Over Direct API Access**
- Eliminates translation burden between LLM reasoning and API mechanics
- Uses standardized JSON schema format that frontier models are trained on
- Prevents agent code from accumulating API-specific integration logic
- Isolates API changes to MCP layer, not agent code

**Security Benefits**
- Credentials stay in MCP layer, never exposed to agents
- Centralized access control and policy enforcement
- Single point for audit logging and compliance monitoring
- Rate limiting prevents runaway agent requests
- Data filtering/redaction before reaching agents
- Isolation limits blast radius of compromised agents

**Architectural Advantages**
- Clean separation of concerns across layers
- Independent evolution of each component
- MCP tools provide semantic abstraction, not simple API wrapping
- Standardized protocol reduces integration complexity

## Related Concepts

### Prerequisites
- [[agents]] - Need to understand agent architecture before MCP integration

### Related Topics
- [[a2a]] - A2A and MCP are complementary protocols
- [[alita]] - Alita uses MCP to dynamically create and manage tools
- [[mcp_tools]] - Agents use MCP tools for task execution
- [[filesystem]] - Agents use filesystem tools via MCP

### Extends
- [[agents]] - Extends agents with MCP tool integration