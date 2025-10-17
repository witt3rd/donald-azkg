---
tags: [agents, guide, api]
last_refresh: 2025-10-12
---
# Google's Agent2Agent (A2A) Protocol: A Comprehensive Technical Brief

Google's Agent2Agent (A2A) Protocol represents a significant advancement in AI agent interoperability, providing a standardized framework for autonomous agents to discover, communicate, and collaborate across different platforms and vendors. This protocol addresses the fundamental challenge of enabling seamless multi-agent workflows in an increasingly diverse ecosystem of AI systems[1][5]. Launched in April 2025 and donated to the Linux Foundation in June 2025, A2A has evolved to version 0.3 with enhanced enterprise features, though industry momentum has increasingly shifted toward the complementary Model Context Protocol (MCP) as of late 2025.

## Introduction and Purpose

The Agent2Agent Protocol is an open standard designed to facilitate communication and interoperability between independent, potentially opaque AI agent systems[5]. In an ecosystem where agents are built using different frameworks, languages, or by different vendors, A2A provides a common language and interaction model that enables agents to collaborate without needing access to each other's internal state, memory, or tools[1][5].

The protocol emerged from Google's internal expertise in scaling agentic systems, designed specifically to address challenges identified in deploying large-scale multi-agent systems for enterprise customers[13]. A2A tackles what is essentially an M×N integration problem, where M different models need to connect with N different agents, by providing a standardized protocol that reduces this complexity to an N+M setup[4].

## Core Architecture and Design Principles

### Fundamental Design Principles

A2A is built on five core principles that ensure enterprise-ready deployment and scalability[6][12]:

**Simplicity**: The protocol reuses existing, well-understood standards including HTTP, JSON-RPC 2.0, and Server-Sent Events (SSE), ensuring easy integration with existing technology stacks[5][6].

**Enterprise Readiness**: Built-in support for authentication, authorization, security, privacy, tracing, and monitoring through alignment with established enterprise practices and OpenAPI authentication schemes[5][6].

**Asynchronous First**: Designed to handle potentially very long-running tasks and human-in-the-loop interactions, supporting background tasks with meaningful progress updates[5][6].

**Modality Agnostic**: Supports diverse content types including text, audio, video, structured data, forms, and potentially embedded UI components[5][6].

**Opaque Execution**: Agents collaborate based on declared capabilities and exchanged information without needing to share their internal thoughts, plans, or tool implementations[5][6].

### System Architecture

The A2A protocol defines three core actors in its communication model[6][16]:

**User**: The end-user who initiates tasks and provides high-level objectives.

**Client Agent**: The requesting agent that formulates and sends tasks on behalf of the user, acting as a coordinator or project manager.

**Remote Agent**: The recipient agent that performs specific tasks and returns results based on its specialized capabilities.

## Technical Specifications and Protocol Details

### Transport and Data Format

A2A communication must occur over HTTP(S), with the A2A Server exposing its service at a URL defined in its AgentCard[5]. The protocol uses JSON-RPC 2.0 as the payload format for all requests and responses, with the Content-Type header set to application/json[5].

As of version 0.3 (July 2025), A2A also supports **gRPC transport** for high-performance, streaming, and push notifications, providing an alternative to the standard HTTP/JSON-RPC 2.0 transport layer[28].

For streaming operations, the protocol employs Server-Sent Events (SSE) with HTTP 200 OK status and Content-Type of text/event-stream, where each SSE data field contains a complete JSON-RPC 2.0 Response object[5].

### Core Communication Objects

**Agent Cards**: The foundation of A2A discovery and capability advertisement. These are standardized JSON documents typically hosted at /.well-known/agent.json that contain comprehensive metadata about an agent's capabilities, skills, endpoint URL, authentication requirements, and supported input/output modalities[5][6].

**Tasks**: The atomic unit of work in A2A communication, representing structured objects with lifecycle states including submitted, working, input-required, and completed[6]. Tasks serve as containers for the entire workflow between agents.

**Messages**: Used for conversational exchanges between client and remote agents, enabling clarification, additional input requests, and progress updates[6].

**Artifacts**: Immutable results created by the remote agent, such as generated files, analysis summaries, or structured data outputs[6].

**Parts**: Self-contained data blocks within messages or artifacts, supporting various content types including plain text, file blobs, JSON, and other structured formats[6].

### Agent Card Structure

The AgentCard object provides comprehensive agent metadata with the following key components[5]:

- Basic identification (name, description, version, provider information)
- Service endpoint URL for A2A communication
- Supported protocol capabilities (streaming, push notifications)
- Authentication and security requirements
- Default input/output content types (MIME types)
- Detailed skill definitions with examples and modality specifications

Each skill within an AgentCard includes a unique identifier, human-readable name and description, categorization tags, usage examples, and specific input/output mode overrides[5].

### Security Framework

A2A implements enterprise-grade security through multiple mechanisms[5][16]:

**Authentication Schemes**: Support for various OpenAPI-compatible authentication methods including API keys, HTTP authentication, OAuth2, and OpenID Connect.

**Signed Security Cards**: Introduced in version 0.3, signed security cards enhance agent identification and trust management, representing a significant upgrade in authentication capabilities[28].

**Permission Model**: Local-first, explicit permission model where hosts maintain strict control over which agents can be accessed and what capabilities they can use.

**Transport Security**: Mandatory HTTPS for production deployments, with HTTP permitted only for local development and testing. Enhanced emphasis on robust authentication and encrypted communication channels across all transport options[28].

**Sandboxed Execution**: Each MCP client handles communication to one MCP server, maintaining isolation for security purposes.

## Operational Workflow

### Discovery Phase

The A2A workflow begins with capability discovery, where client agents locate and evaluate potential remote agents through their published Agent Cards[6]. This discovery can occur through various mechanisms including DNS lookups, registries, marketplaces, or private catalogs.

### Task Execution Workflow

A typical A2A interaction follows this sequence[6]:

1. **User Initiation**: A user provides a high-level request to a client agent
2. **Agent Discovery**: The client agent discovers suitable remote agents via Agent Cards
3. **Task Creation**: The client agent sends a task/send request containing a unique Task ID, session information, and initial message with structured parts
4. **Processing**: The remote agent processes the task and responds with immediate results, intermediate messages, or requests for additional input
5. **State Management**: Tasks transition through defined states with real-time updates via streaming or push notifications
6. **Completion**: Final results are delivered as artifacts, with the client agent retrieving complete task information via task/get requests

### Streaming and Asynchronous Support

For long-running tasks, A2A provides robust asynchronous capabilities[5][6]:

**Server-Sent Events**: Real-time streaming of progress updates and partial results during task execution.

**Push Notifications**: Webhook-based notifications for disconnected clients, ensuring task completion awareness even during network interruptions.

**State Persistence**: Task state management allows for resumption of long-running operations and human-in-the-loop scenarios.

## Relationship to Model Context Protocol (MCP)

A2A and MCP serve complementary but distinct roles in the AI ecosystem[1][4]. While both protocols address integration challenges, they operate at different architectural layers:

### MCP Focus: Agent-to-Resource Integration

The Model Context Protocol, developed by Anthropic, standardizes how AI models integrate with external data sources and tools[3][4]. MCP follows a client-server architecture where AI applications connect to MCP servers that expose specific capabilities through structured inputs and outputs[4]. It essentially functions as a "USB port" for AI applications, providing universal interfaces to data sources and services[10].

MCP addresses the challenge of connecting individual agents or models to external resources, tools, and data sources through three core primitives[4]:

- **Resources**: For accessing data and content
- **Tools**: For performing actions and function calls
- **Prompts**: For providing templates and guidance

### A2A Focus: Agent-to-Agent Communication

In contrast, A2A facilitates dynamic, multimodal communication between different agents as peers[1]. Rather than connecting agents to resources, A2A enables agents to collaborate, delegate tasks, and manage shared workflows across different platforms and vendors[1][6].

### Complementary Architecture

Google positions A2A as complementary to MCP rather than competitive[1][8]. This architectural relationship can be understood as:

**MCP Layer**: Connects individual agents to their capabilities, tools, and data sources - essentially defining what each agent can do.

**A2A Layer**: Enables communication and collaboration between agents - defining how agents work together.

A comprehensive multi-agent system would typically employ both protocols: MCP to ensure each agent has access to necessary tools and data, and A2A to coordinate collaboration between multiple specialized agents[1][4].

As of late 2025, while A2A and MCP remain technically complementary and share some JSON compatibility, the industry has increasingly favored MCP as the preferred standard for agent integration[28][29]. Many platforms are now building direct MCP support while reducing emphasis on A2A development, though both protocols continue to serve distinct architectural roles in multi-agent systems[28].

## Implementation Considerations for System Design

### Technical Integration Points

Systems incorporating A2A should consider the following integration requirements[5][18]:

**Protocol Support**: Implementation of JSON-RPC 2.0 over HTTP(S) with SSE streaming capabilities for real-time updates.

**Agent Card Management**: Capability to publish and consume Agent Card specifications, including dynamic updates as agent capabilities evolve.

**Authentication Infrastructure**: Support for multiple authentication schemes aligned with OpenAPI specifications, including enterprise-grade security controls.

**Task Lifecycle Management**: Robust state management for long-running tasks with appropriate error handling and recovery mechanisms.

**Multimodal Content Handling**: Support for diverse content types and MIME type negotiation between agents.

### Enterprise Deployment Considerations

Enterprise adoption of A2A requires attention to several operational factors[16][18]:

**Security and Compliance**: Implementation of appropriate threat modeling, access controls, and audit trails for agent interactions.

**Scalability**: Design for high-volume agent-to-agent communication with appropriate load balancing and resource management.

**Monitoring and Observability**: Comprehensive logging and monitoring of agent interactions for debugging and performance optimization.

**Governance**: Establishment of policies for agent registration, capability approval, and interaction boundaries.

## Current Adoption and Ecosystem

A2A has gained significant traction since its introduction, with over 50 technology partners initially including MongoDB, Atlassian, SAP, PayPal, and Cohere adopting the protocol[13]. By July 2025, adoption expanded to over 150 organizations with major enterprise integrations at Adobe, ServiceNow, S&P Global, and Twilio[28]. Notable enterprise use cases include Tyson Foods and Gordon Food Service using A2A for supply chain optimization and data sharing between agents[28].

In June 2025, Google donated the A2A Protocol to the Linux Foundation, establishing it as a community-driven project under open governance[28][29].

Google has released official Python SDKs for A2A development and continues to enhance the protocol with regular specification updates[18]. The protocol reached version 0.3 in July 2025, introducing gRPC support, signed security cards, improved Python SDK, enterprise orchestration features, and a more stabilized API[28][30]. Comprehensive developer tooling includes the Agent Development Kit (ADK), deployment support via Agent Engine, Cloud Run, and GKE, and marketplace integrations such as Agentspace and the AI Agent Marketplace[28].

The ecosystem is expanding to include platforms that provide enhanced capabilities for building, deploying, and securing A2A agents, establishing the infrastructure necessary for sophisticated multi-agent systems across enterprise environments[18]. However, as of late 2025, industry momentum has increasingly consolidated around the Model Context Protocol (MCP), with many platforms now building direct MCP support while de-emphasizing A2A development[28]. Google Cloud has begun adding MCP compatibility into its AI agent services, reflecting this ecosystem shift[28]. Despite reduced momentum for new A2A features, Google and partners continue to maintain legacy support for existing enterprise A2A deployments[28].

## Conclusion

Google's A2A Protocol represents a crucial advancement in AI agent interoperability, providing the standardized communication framework necessary for sophisticated multi-agent systems. By addressing the fundamental challenges of agent discovery, secure communication, and collaborative task management, A2A enables organizations to build complex, distributed AI workflows that leverage specialized agents across different platforms and vendors.

The protocol's emphasis on enterprise-ready features, combined with its complementary relationship to MCP, positions A2A as a foundational technology for the next generation of AI systems. Version 0.3 (July 2025) brought significant enhancements including gRPC transport support, signed security cards, and improved enterprise orchestration capabilities, establishing A2A as a mature specification now governed by the Linux Foundation[28][30].

For system designers, A2A offers a mature, standards-based approach to implementing multi-agent collaboration while maintaining security, scalability, and operational control necessary for enterprise deployment. However, as of late 2025, industry adoption is increasingly consolidating around MCP, with A2A seeing reduced momentum for new feature development while maintaining strong support for existing enterprise deployments[28]. Organizations should consider both protocols' roles in their multi-agent architecture, with MCP handling tool and resource integration while A2A manages inter-agent communication for systems requiring that capability.

## Related Concepts

### Related Topics

- [[llm_agents]] - A2A enables agent-to-agent communication for systems described in agents.md
- [[agent_mcp_apis]] - A2A and MCP are complementary protocols for agent integration
- [[debate]] - A2A protocol facilitates agent-to-agent debate communication

### Extended By

- [[llm_agents]] - A2A protocol enables multi-agent interoperability

## References

[1] <https://google.github.io/A2A/>
[2] <https://developers.google.com/identity/protocols/oauth2>
[3] <https://www.anthropic.com/news/model-context-protocol>
[4] <https://wandb.ai/onlineinference/mcp/reports/The-Model-Context-Protocol-MCP-by-Anthropic-Origins-functionality-and-impact--VmlldzoxMTY5NDI4MQ>
[5] <https://google.github.io/A2A/specification/>
[6] <https://www.datacamp.com/blog/a2a-agent2agent>
[7] <https://www.agentcard.net>
[8] <https://www.koyeb.com/blog/a2a-and-mcp-start-of-the-ai-agent-protocol-wars>
[9] <https://cloud.google.com/docs/security/encryption-in-transit/application-layer-transport-security>
[10] <https://modelcontextprotocol.io/introduction>
[11] <https://www.infoq.com/news/2024/12/anthropic-model-context-protocol/>
[12] <https://a2aprotocol.ai>
[13] <https://composio.dev/blog/agent2agent-a-practical-guide-to-build-agents/>
[14] <https://www.youtube.com/watch?v=56BXHCkngss>
[15] <https://github.com/modelcontextprotocol>
[16] <https://cloudsecurityalliance.org/blog/2025/04/30/threat-modeling-google-s-a2a-protocol-with-the-maestro-framework>
[17] <https://en.wikipedia.org/wiki/Model_Context_Protocol>
[18] <https://developers.googleblog.com/en/agents-adk-agent-engine-a2a-enhancements-google-io/>
[19] <https://www.youtube.com/watch?v=7j_NE6Pjv-E>
[20] <https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/introducing-model-context-protocol-mcp-in-copilot-studio-simplified-integration-with-ai-apps-and-agents/>
[21] <https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/>
[22] <https://github.com/google/A2A>
[23] <https://developers.google.com/workspace/sites/docs/1.0/developers_guide_protocol>
[24] <https://blogs.windows.com/windowsexperience/2025/05/19/securing-the-model-context-protocol-building-a-safer-agentic-future-on-windows/>
[25] <https://modelcontextprotocol.io/specification/2025-03-26>
[26] <https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/agent-in-the-middle-abusing-agent-cards-in-the-agent-2-agent-protocol-to-win-all-the-tasks/>
[27] <https://usa.yamaha.com/products/audio_visual/av_receivers_amps/rx-a2a/specs.html>
[28] <https://blog.fka.dev/blog/2025-09-11-what-happened-to-googles-a2a/>
[29] <https://www.ibm.com/think/topics/agent2agent-protocol>
[30] <https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade>
