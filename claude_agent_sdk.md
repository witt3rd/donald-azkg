---
tags: [python, typescript, agents, sdk, api, claude-code]
---
# Claude Agent SDK: Building Production AI Agents

**Claude Agent SDK** is a comprehensive toolkit for building autonomous, production-grade AI agents on top of Anthropic's Claude models, providing programmatic access to a controlled computing environment, advanced context handling, and robust integration patterns for complex multi-step workflows.

## What It Is

The Claude Agent SDK is available as official TypeScript and Python libraries that offer structured APIs, terminal/file system access, orchestration utilities, and integration with Claude models. The SDK enables agents that can not only generate text but also manipulate files, execute shell commands, coordinate multi-step operations, and securely plug into external tools and data sources.

### Core Value Proposition

Unlike direct API calls to Claude (which return text completions) or Claude Code (which is an interactive IDE tool), the Agent SDK provides:

**Programmatic agent orchestration** - Build agents in code that run autonomously without human interaction per step.

**Computing environment control** - File operations, command execution, and system interaction in a sandboxed runtime.

**Persistent context management** - Cross-session memory via CLAUDE.md and selective context loading to avoid token bloat.

**Built-in verification loops** - Action → Verification → Correction patterns for reliable task completion.

**Production-ready architecture** - Error handling, retry logic, observable logs, permission controls, and integration patterns.

## Architecture and Components

### Agent Execution Loop

Four-phase loop that repeats until task completion:

1. **Gather context** - Load relevant files, project state, and prior decisions
2. **Take action** - Execute tool calls (file edits, commands, API calls)
3. **Verify work** - Check results via semantic validation or rule-based checks
4. **Iterate** - Continue if unsatisfied, complete if goal achieved

This loop provides reliability through continuous validation rather than assuming single-shot correctness.

### Context Management

**Persistent storage** - CLAUDE.md files store project context, decisions, and agent memory across sessions.

**Selective loading** - Dynamic context retrieval prevents token bloat by loading only relevant files/data per step.

**Cross-session continuity** - Agents resume from prior state, maintaining knowledge and progress.

**Token optimization** - Prompt caching, streaming mode, and context compaction reduce costs and latency.

### Tooling and Action Layer

**File and code operations** - Read, write, edit files across project directories with path restrictions.

**Command execution** - Run shell commands, scripts, and CLI tools in sandboxed environment.

**Built-in integrations** - Web search, HTTP APIs, and common developer tools available out-of-box.

**Custom tool extension** - Model Context Protocol (MCP) support for integrating proprietary tools, databases, services.

### Permission Controls

**Fine-grained access** - Per-tool allow/deny lists prevent unauthorized operations.

**System prompts** - Define agent scope, expertise, and behavioral constraints.

**Execution policies** - Timeout limits, resource quotas, and file system boundaries.

**Audit logging** - Track all agent actions for security review and compliance.

### Sandboxed Runtime

**Constrained environment** - Agents execute in isolated sandbox with strict boundaries.

**Resource limits** - CPU, memory, and disk quotas prevent resource exhaustion.

**Timeout enforcement** - Operations terminate if they exceed time limits.

**File system isolation** - Restrict agent access to designated directories only.

### Error Handling

**Built-in retry logic** - Automatic retry with exponential backoff for transient failures.

**Diagnostics** - Detailed error messages and stack traces for debugging.

**Rule-based validation** - Check outputs against expected patterns or schemas.

**LLM-assisted validation** - Use Claude to verify semantic correctness of outputs.

**Observable logs** - Comprehensive logging for monitoring and troubleshooting.

### Claude Model Integration

**Native prompt caching** - Cache system prompts and context for faster, cheaper inference.

**Streaming mode** - Low-latency streaming for interactive use cases.

**Batch/single-shot** - Choose between streaming or batch processing based on needs.

**System prompt injection** - Configure agent behavior, expertise, and constraints via prompts.

**Multi-model support** - Route to Anthropic Claude; fallback to Bedrock, Vertex, or other providers.

### Integration and Extensibility

**Model Context Protocol (MCP)** - Standardized integration with external tools, databases, services.

**Self-hosted MCP servers** - Run private MCP servers for proprietary tool integration.

**Custom tool development** - Build domain-specific tools with MCP SDK.

**Third-party integrations** - Connect to existing MCP servers for common tools (GitHub, Jira, databases).

## Installation and Setup

### Python Installation

```bash
# Install Agent SDK
pip install claude-agent-sdk

# Set API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Or use with Bedrock/Vertex
export AWS_REGION="us-west-2"
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

### TypeScript/Node.js Installation

```bash
# Install Agent SDK
npm install @anthropic/agent-sdk

# Set API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Configuration

```python
# config.py
from claude_agent_sdk import AgentConfig

config = AgentConfig(
    api_key="your-api-key",
    model="claude-sonnet-4-5",  # Recommended for coding agents
    working_directory="/path/to/project",
    allowed_tools=["file_read", "file_write", "bash"],
    max_iterations=10,
    timeout_seconds=300
)
```

## How to Use: Code Examples

### Basic Agent (Python)

```python
from claude_agent_sdk import Agent, FileTool

# Create agent with file access
agent = Agent(
    tools=[FileTool(allowed_paths=["./project"])],
    system_prompt="You are a Python code refactoring assistant. Focus on readability and maintainability.",
)

# Run autonomous task
result = agent.run_task(
    goal="Refactor all functions in main.py for better readability.",
    files=["./project/main.py"]
)

print(result['summary'])
print(f"Files modified: {result['files_modified']}")
print(f"Iterations: {result['iterations']}")
```

### Agent with Command Execution

```python
from claude_agent_sdk import Agent, FileTool, BashTool

agent = Agent(
    tools=[
        FileTool(allowed_paths=["./src"]),
        BashTool(allowed_commands=["pytest", "black", "mypy"])
    ],
    system_prompt="You are a Python test engineer. Write comprehensive tests and ensure code quality.",
)

result = agent.run_task(
    goal="Add unit tests for the authentication module and ensure all tests pass.",
    files=["./src/auth.py"]
)
```

### Multi-Step Workflow with Verification

```python
from claude_agent_sdk import Agent, FileTool, BashTool
from claude_agent_sdk.verification import SemanticVerifier

# Create agent with verification
agent = Agent(
    tools=[FileTool(), BashTool()],
    verifier=SemanticVerifier(),
    max_iterations=5
)

# Define complex task with verification criteria
result = agent.run_task(
    goal="Implement user registration endpoint with validation, database integration, and error handling.",
    verification_criteria=[
        "Endpoint accepts POST requests with user data",
        "Email validation is implemented",
        "Passwords are hashed before storage",
        "Duplicate email detection works",
        "Error responses follow API spec"
    ],
    files=["./src/api/users.py", "./src/models/user.py"]
)

if result['verified']:
    print("Task completed successfully")
else:
    print(f"Verification failed: {result['verification_errors']}")
```

### Agent with MCP Tool Integration

```python
from claude_agent_sdk import Agent, MCPClient

# Connect to MCP server
mcp_client = MCPClient(
    server_config={
        "command": "uv",
        "args": ["--directory", "/path/to/mcp-server", "run", "server.py"]
    }
)

# Create agent with MCP tools
agent = Agent(
    tools=[mcp_client],
    system_prompt="You are a data analyst with access to company databases."
)

result = agent.run_task(
    goal="Generate quarterly sales report with charts and insights."
)
```

### TypeScript Example

```typescript
import { Agent, FileTool, BashTool } from "@anthropic/agent-sdk";

const agent = new Agent({
    tools: [new FileTool(), new BashTool()],
    systemPrompt: "You are a TypeScript refactoring expert.",
    model: "claude-sonnet-4-5"
});

const result = await agent.runTask({
    goal: "Convert JavaScript files to TypeScript with proper types.",
    files: ["./src/**/*.js"]
});

console.log(result.summary);
```

## Key Features and Capabilities

### File and Directory Manipulation

- Read/write/edit across project trees
- Path restrictions for security
- Binary file handling
- Glob pattern support for bulk operations

### Shell/CLI Execution

- Run permitted commands in sandbox
- Environment variable management
- Stdout/stderr capture
- Exit code handling

### Code Generation and Refactoring

- Multi-file context-aware changes
- Preserve behavior while restructuring
- Follow language-specific best practices
- Maintain code style and conventions

### Persistent Cross-Session Memory

- Store agent state in CLAUDE.md
- Accumulate project knowledge
- Track decisions and rationale
- Resume from prior sessions

### Streaming and Batch Modes

**Streaming** - Interactive, low-latency for UX-focused applications.

**Batch** - Deterministic, cost-optimized for background jobs.

### Custom Tools via MCP

- Register proprietary integrations
- Connect to APIs, databases, services
- Standardized tool discovery and invocation
- Security boundaries and permission controls

### Error Handling and Verification

**Semantic validation** - Use Claude to check output correctness.

**Rule-based checks** - Regex, schema validation, type checking.

**Recovery on failures** - Retry with different approaches.

**Human-in-the-loop** - Escalate ambiguous cases for approval.

### Observability

- Structured logs for debugging
- Diagnostics for failure analysis
- Audit trails for compliance
- Performance metrics (latency, token usage, iterations)

### Security-First Design

- Fine-grained tool permissions
- Resource quotas and timeouts
- Sandboxed execution
- Credential management via environment variables

## When to Use Agent SDK vs. Alternatives

| Approach | Use When | Avoid When |
|----------|----------|------------|
| **Agent SDK** | Building autonomous agents that interact with files, run code, manage workflows, integrate tools | Simple stateless queries, basic chatbots, single-shot completions |
| **Direct API Calls** | Simple LLM completion, basic chatbots, stateless queries where you don't need file/command access | Multi-step workflows, file operations, external tool integration |
| **Claude Code (CLI/IDE)** | Local interactive development, one-off coding tasks, IDE-style assistance with human in loop | Programmatic orchestration, production automation, headless agent systems |

### Decision Matrix

**Choose Agent SDK when:**
- Task requires multiple steps with verification loops
- Agent needs file system or command execution access
- Workflow must run autonomously without human per-step intervention
- Context persistence across sessions is critical
- Integration with external tools via MCP is required
- Production reliability (error handling, retry, logging) is essential

**Choose Direct API when:**
- Single completion or chat turn is sufficient
- No file/command access needed
- Stateless operation is acceptable
- Integration complexity not justified for use case

**Choose Claude Code when:**
- Human developer wants interactive AI coding assistant
- Working locally in terminal or IDE
- Task requires iterative human feedback per step
- Exploring codebase interactively rather than automating

## Common Use Cases

### Autonomous Coding Agents

- Multi-file refactoring projects
- Codebase analysis and documentation generation
- Project scaffolding and boilerplate creation
- Automated bug fixing from issue descriptions

### Data Analysis and Processing

- Pull data from APIs or databases
- Run custom transformation scripts
- Generate reports with charts and insights
- Summarize results programmatically

### Enterprise Process Automation

- File handling workflows (CSV processing, PDF generation)
- Scheduled report generation
- Integration with internal tools via MCP
- Compliance and audit automation

### Security and Assurance

- Automated code scanning for vulnerabilities
- Compliance checks against policies
- Secure file transformation and redaction
- Audit log analysis

### Research Assistants

- Literature review and synthesis
- Data aggregation from multiple sources
- Context-enriched content generation
- Cross-reference validation

## Best Practices and Patterns

### Three-Step Loop: Action → Verification → Correction

Always incorporate explicit validation on critical tasks. Use human-in-the-loop or LLM semantic verification for high-stakes operations.

```python
result = agent.run_task(
    goal="Implement payment processing endpoint",
    verification_criteria=[
        "Transaction validation is correct",
        "Error handling covers edge cases",
        "Security best practices followed"
    ],
    require_human_approval=True  # Escalate for review
)
```

### Minimize Context Spills

Use automatic compaction and keep prompts/files focused to avoid LLM context limits. Load context selectively rather than dumping entire codebase.

```python
agent = Agent(
    context_strategy="selective",  # Only load relevant files
    max_context_tokens=100000,
    auto_compact=True
)
```

### Tool Permission Principle

Explicitly declare required tool access for each agent. Avoid global allow-all settings.

```python
agent = Agent(
    tools=[
        FileTool(allowed_paths=["./src", "./tests"]),
        BashTool(allowed_commands=["pytest", "black"])
        # Only what's needed, nothing more
    ]
)
```

### External System Integration via MCP

Use MCP for robust, standardized external tool interfaces. Don't build custom integrations when MCP provides standard protocol.

```python
# Good: Use MCP for external tools
mcp_client = MCPClient(server_config=jira_server_config)
agent = Agent(tools=[mcp_client])

# Bad: Custom API integration in agent code
# agent.custom_jira_integration(...)  # Avoid this
```

### CI/CD and Testing

Maintain agent configs in source control. Run verification suites for agent logic to ensure reliability.

```python
# test_agent.py
def test_refactoring_agent():
    agent = Agent(tools=[FileTool()])
    result = agent.run_task(
        goal="Refactor test file",
        files=["test_sample.py"]
    )
    assert result['verified']
    assert len(result['files_modified']) > 0
```

### Structured File Layout

Store prompts, configs, and persistent context in designated directory.

```
project/
├── .claude/
│   ├── config.yaml          # Agent configuration
│   ├── CLAUDE.md           # Persistent context
│   └── prompts/            # System prompts
├── agents/
│   ├── refactoring_agent.py
│   ├── test_agent.py
│   └── docs_agent.py
└── src/
```

## Limitations and Trade-offs

### Sandbox Boundaries

Agents are limited to defined directories and commands. Cannot access full system by default without explicit permission configuration.

**Mitigation**: Carefully define allowed paths and commands during agent setup.

### Latency and Cost

Autonomous agent loops with multi-step LLM use and verification incur higher inference costs and longer latency vs. single LLM calls.

**Mitigation**: Use batch mode for background jobs. Optimize context to reduce token usage. Consider Claude Sonnet 4.5 for best cost/performance balance.

### Determinism

LLM-driven iteration and context handling can produce non-deterministic outcomes without strict constraints.

**Mitigation**: Use explicit verification criteria. Implement rule-based validation. Set iteration limits.

### Learning Curve

Requires more configuration (permissions, MCP integration, system prompts) compared to plug-and-play API chatbots.

**Mitigation**: Start with examples and templates. Build incrementally from simple to complex agents.

### Security Burden

Poor tool permission configuration can introduce risks. Best practice is least-privilege isolation.

**Mitigation**: Follow principle of least privilege. Audit tool permissions. Use sandboxed execution. Review agent logs.

## Current State (2025)

**Active maintenance** - SDKs for TypeScript and Python with feature parity as of October 2025.

**Enterprise adoption** - Used in production by major organizations (Bridgewater, Asana, Ramp) for workflow automation.

**Ecosystem integration** - Supports Bedrock, Vertex, and custom on-premise deployments via MCP.

**Cloud and self-hosted** - Available as Anthropic-hosted service and downloadable runtime for regulated industries.

**Recommended model** - Claude Sonnet 4.5 provides best balance of memory, execution accuracy, and context handling for coding agents.

**MCP maturity** - Model Context Protocol is stable and widely adopted for tool integration.

**Active development** - Continuous improvements to autonomy, error handling, observability, and performance.

## Agent SDK vs. Claude Code: Architectural Differences

Understanding the distinction between Agent SDK and Claude Code is critical:

| Aspect | Agent SDK | Claude Code |
|--------|-----------|-------------|
| **Interface** | Programmatic (Python/TypeScript APIs) | Interactive (CLI/IDE extension) |
| **Execution** | Autonomous, runs without human per-step | Interactive, human-guided per-step |
| **Use Case** | Production automation, headless agents | Local development, coding assistance |
| **Context** | Managed in code, persistent via files | Managed by Claude Code, session-based |
| **Deployment** | Servers, CI/CD, scheduled jobs | Developer workstations, IDEs |
| **Human Interaction** | Escalate only when needed | Continuous human oversight |

**Agent SDK** is for building production agent systems. **Claude Code** is for augmenting human developers interactively.

Both can coexist: Use Claude Code for prototyping and interactive development, then build production agents with Agent SDK for deployment.

## Summary: When Agent SDK is the Right Tool

Ask these questions:

1. **Autonomous execution?** - Does the agent need to run without human per-step intervention?
2. **Multi-step workflows?** - Does the task require multiple actions with verification?
3. **File/command access?** - Does the agent need to manipulate files or run commands?
4. **Production reliability?** - Do you need error handling, retry, and logging for production?
5. **Tool integration?** - Does the agent need to integrate with external systems via MCP?

If yes to most of these, Agent SDK is likely the right choice.

## Related Concepts

### Prerequisites

- [[llm_agents]] - Understanding AI agent architecture is essential before using Agent SDK
- [[mcp_overview]] - Agent SDK uses MCP for tool integration

### Related Topics

- [[claude_code]] - Claude Code is the interactive IDE counterpart to Agent SDK
- [[claude_code_agents]] - Claude Code subagents are related but different from Agent SDK agents
- [[python_mcp_sdk]] - MCP SDK enables custom tool development for Agent SDK
- [[agent_mcp_apis]] - Understanding MCP tool architecture enhances Agent SDK usage
- [[claude_code_skills]] - Skills provide similar modularity but for Claude Code, not Agent SDK

### Extended By

- [[claude_agent_sdk_production]] - Production deployment patterns and observability for Agent SDK

### Extends

- [[llm_agents]] - Agent SDK is a specific implementation of AI agents for production use

## References

[1] https://artechway.com/blog/claude-agent-sdk-the-complete-developer-guide-to-building-powerful-autonomous-ai-agents-in-2025 - Complete developer guide
[2] https://www.datacamp.com/tutorial/how-to-use-claude-agent-sdk - DataCamp tutorial
[3] https://www.youtube.com/watch?v=i6N8oQQ0tUE - Video walkthrough
[4] https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk - Official engineering blog
[5] https://docs.claude.com/en/api/agent-sdk/overview - Official SDK documentation
[6] https://blog.promptlayer.com/building-agents-with-claude-codes-sdk/ - PromptLayer guide
[7] https://www.anthropic.com/news/claude-sonnet-4-5 - Model recommendation
[8] https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/ - Best practices guide
