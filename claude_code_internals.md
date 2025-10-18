---
tags: [claude-code, architecture, agents, implementation, reference, reverse-engineering]
---
# Claude Code Internals and Recreation Guide

Comprehensive technical analysis of Claude Code's internal architecture based on reverse-engineering efforts, providing a blueprint for recreating an agentic development assistant with similar capabilities.

## Overview

Claude Code operates as a **REPL-like agent loop** built on Node.js/TypeScript, emphasizing simplicity over complex orchestration. Its effectiveness stems from extensive prompt engineering, a focused set of 11-13 core tools, and layered memory management—not multi-agent swarms or elaborate frameworks. This architecture prioritizes debuggability, reliability, and direct local execution.

**Key architectural principle**: Minimal mediation between user and LLM—let the model reason agentically with strong prompts rather than heavy scaffolding.

## Primary Agent Loop

### Core REPL Structure

The main loop is a straightforward while loop that handles user inputs, constructs API requests, executes tools, and feeds results back until the LLM outputs pure text without tool calls.

**Loop phases**:

1. **Input processing**: Classify input (new topic detection via lightweight Haiku model)
2. **Prompt construction**: Build full message history with system prompts, environment info, tool definitions
3. **LLM API call**: Invoke Anthropic API (beta.messages.create) with Claude Sonnet/Opus
4. **Response handling**: Parse text responses vs tool invocations
5. **Tool execution**: Run tools, append results as system messages
6. **Iteration**: Loop back to step 3 if more tools needed
7. **Termination**: End when no tools called, display final response

**Pseudocode for recreation**:

```typescript
async function mainLoop(userInput: string, context: Message[]) {
  // Topic detection (lightweight LLM call with Haiku)
  const topic = await detectTopic(userInput);

  // Build full prompt
  const messages = [
    { role: 'system', content: systemWorkflowPrompt + envInfo },
    ...context,
    { role: 'user', content: userInput + reminderPrompt }
  ];

  while (true) {
    const response = await anthropic.messages.create({
      messages,
      tools,
      model: 'claude-sonnet-4-5'
    });

    if (response.type === 'text') {
      displayResponse(response.content);
      break;
    } else if (response.type === 'tool_use') {
      const toolResults = await executeTools(response.toolInvocations);
      messages.push({
        role: 'system',
        content: `Tool results: ${JSON.stringify(toolResults)}`
      });
    }
  }

  // Compact context if nearing limit (~92% threshold)
  if (estimateTokens(context) > threshold) {
    await compactContext(messages);
  }
}
```

### Termination Conditions

- **Explicit user command**: Exit, quit, done
- **Task completion**: LLM outputs "all done" or equivalent intent signal
- **Resource exhaustion**: Context token limit or memory constraints
- **Pure text response**: No tool_use blocks in LLM response

### Environment Context Injection

At loop start, inject static snapshot:

- Working directory tree (respecting .gitignore)
- Git status and recent commits
- Platform info (OS, Node version, etc.)
- Active todos from ~/.claude/todos/

**Note**: No dynamic updates during loop—tools must fetch fresh data.

## Core Tools Architecture

### Tool Registry Pattern

Tools are defined as JSON schemas in API calls with verbose descriptions including examples and usage guidelines.

```typescript
interface Tool {
  name: string;
  description: string;
  input_schema: JSONSchema;
  handler: (input: any) => Promise<ToolResult>;
  requiresPermission: boolean;
}

class ToolRegistry {
  private tools: Map<string, Tool> = new Map();

  register(tool: Tool) {
    this.tools.set(tool.name, tool);
  }

  async execute(toolName: string, input: any): Promise<ToolResult> {
    const tool = this.tools.get(toolName);
    if (tool.requiresPermission) {
      await requestUserPermission(toolName, input);
    }
    return tool.handler(input);
  }
}
```

### Tool Catalog

| Tool Name | Purpose | Inputs | Permissions | Implementation Notes |
|-----------|---------|--------|-------------|----------------------|
| **Bash** | Execute shell commands in persistent session | Command string | Yes (execution) | Child process; prefix detection for injection; handles git/gh CLI |
| **Read/View** | Read file contents (text/binary) | Path, optional line range | Yes (outside project) | Up to 2000 lines; base64 for images |
| **Edit** | Replace string in file | Path, old_string, new_string | Yes | Requires uniqueness; for targeted changes |
| **Write** | Create or overwrite file | Path, content | Yes | Verifies directory exists via LS first |
| **GlobTool** | Pattern-based file matching | Glob pattern, optional dir | Yes (outside project) | Returns sorted by modification time |
| **GrepTool** | Regex search in files | Regex, file filters | Yes (outside project) | Filters by type; sorted by mod time |
| **LS** | List directory tree | Path, ignore patterns | Yes (outside project) | Tree-format output |
| **WebFetchTool** | Fetch URL, convert to markdown | URL, extraction prompt | Yes (external access) | Read-only, cached; user-mentioned URLs only |
| **TodoWrite** | Manage task list JSON | Action, tasks array | No | States: pending, in_progress (one max), completed |
| **ReadNotebook** | Read Jupyter notebook | .ipynb path | Yes (outside project) | Handles code/markdown cells |
| **NotebookEditCell** | Edit notebook cell | Path, cell index, content | Yes | Replace/insert/delete operations |
| **ThinkTool** | Log internal reasoning | Thought string | No | Debugging; no actions |
| **BatchTool** | Parallel tool execution | Array of invocations | Varies | Promise.all for independent ops |

### Security and Permissions

**Permission system**:

- Gated via user prompts for destructive/external operations
- Bash commands scanned for injection patterns
- File operations restricted to project scope by default
- WebFetch limited to user-mentioned URLs

**Sandboxing approach**:

- No VM isolation—runs under user's native permissions
- macOS Seatbelt or Docker optional for additional containment
- Prefix detection catches simple injection attempts

**Example permission check**:

```typescript
async function requestUserPermission(tool: string, input: any): Promise<boolean> {
  console.log(`\n⚠️  ${tool} wants to: ${summarize(input)}`);
  const response = await promptUser('Allow? (y/n): ');
  return response.toLowerCase() === 'y';
}
```

## Prompt Engineering Architecture

### System Prompts

Prompts are extensive (1800-2500 words), reiterated across sections to combat "forgetting", with explicit examples and rules.

**Key prompt components**:

1. **System Workflow Prompt**: Agent role, conciseness rules, tool guidelines
2. **Reminder Prompts**: Injected after tool use to reinforce behaviors
3. **Compact Prompt**: Context compression at threshold
4. **Security Prompts**: Injection detection for Bash
5. **Topic Detection Prompt**: JSON classification of new topics
6. **Init Prompt**: Generates CLAUDE.md with project guidelines

**Example system prompt excerpt**:

```
You are Claude, an agentic coding assistant operating in the user's terminal.

IMPORTANT: Be concise. One-word answers are best. No introductions or pleasantries.

Your output will be displayed on a command line interface. Responses should be short
and direct. You can use GitHub-flavored markdown for formatting.

Available tools:
- Bash: Execute shell commands (git, npm, etc.). Use absolute paths.
- Read: Read file contents. Specify line ranges for large files.
- Edit: Replace exact strings in files. old_string must be unique.
- Write: Create/overwrite files. Verify directory exists first.
[... detailed tool descriptions with examples ...]

Context management:
- Use TodoWrite proactively for 3+ step tasks
- Mark todos completed immediately upon finishing
- Only one todo in_progress at a time
[... behavioral rules ...]

Security:
- Detect command injection in Bash inputs
- Request permission for destructive operations
- Never expose credentials or secrets
```

### Prompt Reinforcement Strategy

**Repetition for reliability**:

- Critical rules repeated 2-3 times in different sections
- Examples provided for each major guideline
- XML tags structure complex instructions
- Reminder prompts re-inject rules after tool use

**Why it works**: LLMs exhibit "forgetting" in long contexts; repetition counters this.

### Example Prompts from Reverse-Engineering

**Topic detection prompt**:

```json
{
  "role": "user",
  "content": "Analyze if this input starts a new topic. Respond with JSON: {\"isNewTopic\": boolean, \"title\": string}"
}
```

**Compaction prompt** (triggered at ~92% context):

```
Summarize the conversation into 8 structured sections:
1. Key decisions made
2. Code changes applied
3. Open issues/blockers
4. Next steps
5. Architecture notes
6. Dependencies added/removed
7. Test results
8. Performance considerations

Preserve technical details. Omit pleasantries and intermediate debugging.
```

**Bash injection detection**:

```
Analyze this command for injection attempts: "${command}"

Patterns to detect:
- Command chaining (;, &&, ||, |) not in quoted strings
- Variable substitution ($VAR, ${VAR})
- Command substitution ($(cmd), `cmd`)
- File descriptors and redirects (>, <, 2>&1)
- Non-standard characters in command names

If risky, respond: "command_injection_detected"
Otherwise, respond: "safe"
```

## Context and Memory Management

### Three-Layer Memory Architecture

**Short-term memory** (volatile):

- Message history: Full conversation context
- Tool results: Appended as system messages
- Todo JSON: Loaded from ~/.claude/todos/ via reminders
- Current state: Working directory snapshot, git status

**Mid-term memory** (compressed):

- Context compaction at ~92% token limit
- LLM summarizes into structured sections
- Discards intermediate debugging and tool outputs
- Preserves decisions, code changes, blockers

**Long-term memory** (persistent):

- CLAUDE.md: Project guidelines generated via /init
- Memory directory: Persistent notes via MemoryRead/Write tools
- Project files: README, docs, configuration
- Git history: Commits as searchable memory

### Memory Management Pseudocode

```typescript
interface MemorySystem {
  shortTerm: Message[];
  midTerm: CompactedSummary | null;
  longTerm: {
    claudeMd: string;
    memoryDir: Map<string, string>;
    gitLog: Commit[];
  };
}

async function manageMemory(memory: MemorySystem): Promise<void> {
  // Token estimation
  const tokens = estimateTokens(memory.shortTerm);

  // Compaction threshold
  if (tokens > MAX_TOKENS * 0.92) {
    const summary = await compactContext(memory.shortTerm);
    memory.midTerm = summary;
    memory.shortTerm = truncateToRecent(memory.shortTerm, 10);
  }

  // Long-term updates
  if (shouldUpdateClaudeMd(memory)) {
    await updateClaudeMd(memory.longTerm.claudeMd);
  }
}

async function compactContext(messages: Message[]): Promise<CompactedSummary> {
  const compactPrompt = buildCompactionPrompt(messages);
  const summary = await callLLM(compactPrompt);
  return parseStructuredSummary(summary);
}
```

### CLAUDE.md Structure

Generated via `/init` command, serves as project memory:

```markdown
# Project: [Name]

## Overview
[Brief description]

## Build Commands
```bash
npm run build
npm test
npm run lint
```

## Architecture

- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL

## Coding Standards

- Use TypeScript strict mode
- Prefer functional components
- Write tests for all features

## Known Issues

- [Issue 1]
- [Issue 2]

## Next Steps

- [ ] Task 1
- [ ] Task 2

```

### Sub-Agent Context Isolation

Sub-agents operate with isolated contexts to avoid polluting main conversation:
- Spawned via Task/DispatchAgent tools
- Receive subset of tools (often read-only: View, Glob, Grep)
- Extract task-specific context from main history
- Return only summary, discard intermediates
- Prevent "dirty" searches from bloating main context

**Sub-agent workflow**:

```typescript
async function dispatchSubAgent(task: string, context: Message[]): Promise<string> {
  // Extract relevant context
  const subContext = extractTaskContext(task, context);

  // Specialized system prompt
  const subPrompt = buildSubAgentPrompt(task);

  // Isolated execution
  const subMessages = [
    { role: 'system', content: subPrompt },
    ...subContext
  ];

  // Run sub-loop
  const result = await subAgentLoop(subMessages, readOnlyTools);

  // Return only summary
  return summarizeResult(result);
}
```

## Parallel Execution Architecture

### BatchTool Implementation

Parallelizes independent tool calls for efficiency (e.g., multiple Glob/Grep during /init):

```typescript
interface BatchInvocation {
  tool_name: string;
  input: any;
}

async function executeBatch(invocations: BatchInvocation[]): Promise<ToolResult[]> {
  // Dependency analysis
  const { independent, sequential } = analyzeDependencies(invocations);

  // Parallel execution for independent
  const parallelResults = await Promise.all(
    independent.map(inv => executeToolSafe(inv.tool_name, inv.input))
  );

  // Sequential for dependent
  const sequentialResults = [];
  for (const inv of sequential) {
    const result = await executeToolSafe(inv.tool_name, inv.input);
    sequentialResults.push(result);
  }

  return [...parallelResults, ...sequentialResults];
}

function analyzeDependencies(invocations: BatchInvocation[]): { independent: BatchInvocation[], sequential: BatchInvocation[] } {
  // Detect conflicts (e.g., multiple writes to same file)
  // Classify as independent or sequential
}
```

### Sub-Agent Parallelism

Sub-agents enable pseudo-parallelism while main loop remains sequential:

- Background tasks (tests, searches) while main agent plans
- Multiple sub-agents for different codebases/modules
- Coordination via task scheduler

**Example parallel workflow**:

```typescript
async function parallelWorkflow(tasks: string[]) {
  const subAgentPromises = tasks.map(task =>
    dispatchSubAgent(task, getCurrentContext())
  );

  const results = await Promise.all(subAgentPromises);

  // Merge results into main context
  integrateSubAgentResults(results);
}

// Usage
await parallelWorkflow([
  'Analyze database schema',
  'Review API endpoints',
  'Check test coverage'
]);
```

## Implementation Stack

### Technology Choices

**Language**: Node.js with TypeScript

- Type safety for tool interfaces
- Async/await for streaming responses
- Native child_process for Bash tool
- Rich ecosystem for file operations

**API Integration**: Anthropic SDK

- beta.messages.create for streaming
- Tool definitions via JSON schemas
- Model selection (Sonnet for main, Haiku for lightweight)

**Security**: User-permission gates

- No VM—native user permissions
- Optional sandboxing (Seatbelt, Docker)
- Prefix detection for injection

### Project Structure

```
claude-code/
├── src/
│   ├── agent/
│   │   ├── main-loop.ts        # Core REPL
│   │   ├── sub-agent.ts        # Sub-agent spawning
│   │   └── context.ts          # Memory management
│   ├── tools/
│   │   ├── registry.ts         # Tool registration
│   │   ├── bash.ts             # Shell execution
│   │   ├── filesystem.ts       # Read/Write/Edit
│   │   ├── search.ts           # Glob/Grep
│   │   └── todo.ts             # TodoWrite
│   ├── prompts/
│   │   ├── system.ts           # System prompts
│   │   ├── compact.ts          # Compaction prompts
│   │   └── security.ts         # Injection detection
│   ├── api/
│   │   ├── anthropic.ts        # API client
│   │   └── streaming.ts        # Response streaming
│   └── permissions/
│       └── gate.ts             # Permission system
├── tests/
├── package.json
└── tsconfig.json
```

### Key Dependencies

```json
{
  "dependencies": {
    "@anthropic-ai/sdk": "^0.30.0",
    "typescript": "^5.0.0",
    "glob": "^10.0.0",
    "marked": "^12.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "vitest": "^1.0.0"
  }
}
```

## Recreation Blueprint

### Minimal Viable Implementation

**Phase 1: Core loop** (1-2 days)

1. Set up Node.js/TypeScript project
2. Implement basic REPL with Anthropic API
3. Add Read/Write tools
4. Test basic file operations

**Phase 2: Tool expansion** (3-5 days)
5. Implement Bash with permission gates
6. Add Glob/Grep for search
7. Implement Edit with uniqueness checks
8. Add TodoWrite for task tracking

**Phase 3: Memory system** (2-3 days)
9. Message history management
10. Context compaction at threshold
11. CLAUDE.md generation via /init

**Phase 4: Advanced features** (5-7 days)
12. Sub-agent spawning
13. BatchTool for parallelism
14. WebFetch for documentation
15. Enhanced security (injection detection)

### Testing Strategy

**Unit tests**:

- Tool handlers (mock file system)
- Prompt construction
- Token estimation
- Dependency analysis

**Integration tests**:

- Full agent loops on sample projects
- Sub-agent coordination
- Context compaction accuracy

**Evaluation benchmarks**:

- SWE-bench (code generation)
- Aider polyglot benchmark
- Custom task suites (refactoring, documentation)

### Common Pitfalls

**"Forgetting" in long contexts**:

- Solution: Repeat critical rules in prompts
- Use reminder prompts after tool execution

**Context explosion**:

- Solution: Aggressive compaction at 92% threshold
- Sub-agent isolation for "dirty" tasks

**Over-parallelism causing conflicts**:

- Solution: Dependency analysis in BatchTool
- Sequential fallback for writes

**Permission fatigue**:

- Solution: Batch permission requests
- Remember choices within session

**Injection vulnerabilities**:

- Solution: Prefix detection + regex scanning
- Allowlist for safe command patterns

## Performance Characteristics

### Measured Metrics

**Latency**:

- Simple queries: 200-500ms (Sonnet)
- Complex refactoring: 2-5s (Opus)
- Sub-agent dispatch: +500ms overhead
- Context compaction: 1-2s

**Token consumption**:

- System prompts: 1800-2500 tokens
- Tool definitions: ~1000 tokens
- Typical conversation: 10k-50k tokens
- Post-compaction: 3k-8k tokens

**Reliability**:

- Task completion: 85-90% (SWE-bench subset)
- Security: 95%+ injection detection
- Context coherence: Degrades after 50+ turns without compaction

### Optimization Opportunities

1. **Prompt compression**: Use [[llm_self_talk_optimization]] techniques
2. **Tool result filtering**: Haiku post-processing to reduce noise
3. **Caching**: Reuse embeddings for similar projects
4. **Model routing**: Groq for simple tasks, Claude for complex
5. **Lazy loading**: Fetch tool definitions only when needed

## Related Concepts

### Prerequisites

- [[llm_agents]] - Understanding AI agent fundamentals is essential
- [[claude_code]] - Knowledge of Claude Code features and capabilities

### Related Topics

- [[claude_code_agents]] - Sub-agent architecture extends this implementation pattern
- [[claude_code_efficiency_optimization]] - Performance optimization builds on these internals
- [[mcp_overview]] - MCP provides standardized tool integration that could replace custom tools
- [[llm_self_talk_optimization]] - Prompt compression techniques applicable to system prompts
- [[windows_agents_platform]] - OS-level platform architecture inspired by Claude Code capabilities

### Extends

- [[claude_code]] - These internals explain how Claude Code implements its features

## References

**Reverse-engineering sources**:
[1] GitHub - Yuyz0112/claude-code-reverse - <https://github.com/Yuyz0112/claude-code-reverse>
[2] Reverse engineering Claude Code - Kir Shatrov - <https://kirshatrov.com/posts/claude-code-internals>
[3] Reverse-Engineering Claude Code Using Sub Agents - <https://www.sabrina.dev/p/reverse-engineering-claude-code-using>
[4] Claude Code Feels Like a Senior Dev - Medium - <https://medium.com/@sampan090611/claude-code-feels-like-a-senior-dev-heres-what-actually-makes-it-different-and-what-the-49c02b456d9c>
[5] Inside Claude Code: Prompt Engineering Masterpiece - <https://beyondthehype.dev/p/inside-claude-code-prompt-engineering-masterpiece>
[6] Reverse engineering Claude Code - Reid Barber - <https://reidbarber.com/blog/reverse-engineering-claude-code>
[7] I Reverse-Engineered Claude Code (YouTube) - <https://www.youtube.com/watch?v=i0P56Pm1Q3U>

**Official documentation**:
[8] Understanding Claude Code Plan Mode - <https://lord.technology/2025/07/03/understanding-claude-code-plan-mode-and-the-architecture-of-intent.html>
[9] Claude Sonnet 4.5 Release - <https://www.anthropic.com/news/claude-sonnet-4-5>
[10] How Claude Code is Built - Pragmatic Engineer - <https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built>
[11] Claude Code Best Practices - Anthropic Engineering - <https://anthropic.com/engineering/claude-code-best-practices>
[12] Getting Good Results from Claude Code - <https://www.dzombak.com/blog/2025/08/getting-good-results-from-claude-code/>
