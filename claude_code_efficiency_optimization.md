---
tags: [claude-code, optimization, performance, tools, guide, mcp]
---
# Claude Code Efficiency Optimization

Comprehensive techniques and strategies for maximizing Claude Code performance through optimized search operations, smart tool selection, LLM routing, and cost-effective workflow patterns.

## Overview

Claude Code efficiency optimization focuses on reducing latency, minimizing token consumption, and accelerating development workflows through strategic tool integration, intelligent search patterns, and workflow design. Performance gains of 30-40% latency reduction and significant cost savings are achievable through systematic application of these techniques.

## Search and Grep Optimization

### AST-Grep Integration

**Syntax-aware code search** using Abstract Syntax Trees for language-aware pattern matching:

- **When to use**: Refactoring tasks, type-safe code changes, complex bug patterns requiring structural awareness
- **Performance**: Orders of magnitude faster than text search for code structure queries; subsecond on 1M+ LOC codebases
- **Why it's faster**: Matches on code structure, not text patterns; eliminates false positives from comments/strings
- **Implementation**: Integrate via MCP server or direct CLI invocation

**Pattern examples**:
```bash
# Find all function calls with specific signature
ast-grep --pattern 'function $NAME($$$ARGS) { $$$ }'

# Locate class methods by pattern
ast-grep --pattern 'class $CLASS { $METHOD() { $$$ } }'
```

**Key advantage**: Precision eliminates noise, dramatically reducing iteration time on large codebases.

### Ripgrep (rg) Acceleration

**Ultra-fast recursive search** using Rust's regex engine:

- **Performance**: 5-30x faster than grep/ack due to parallel file reads and aggressive filtering
- **Default optimizations**: Automatically ignores binary files, respects .gitignore, skips hidden files
- **Scale**: Handles millions of files efficiently
- **MCP integration**: mcp-ripgrep server provides distributed search with async streaming

**Usage patterns**:
```bash
# Basic fast search
rg "pattern" --type rust

# Multi-pattern search with context
rg -e "pattern1" -e "pattern2" -A 3 -B 3

# Performance: file type filtering is critical
rg "TODO" --type-add 'docs:*.{md,txt}' --type docs
```

**MCP-ripgrep architecture**:
- Worker pools with dedicated ripgrep runners per project
- Async result streaming (Claude can start generating before search completes)
- Linear scaling with shard count
- Up to 70% latency reduction vs synchronous single-process grep

**Routing strategy**: Use local rg for lightweight queries; escalate to mcp-ripgrep clusters for heavy/distributed searches.

### Semantic Search Tools

**Embedding-based code search** for conceptual queries:

- **Tools**: semtools, Sourcegraph Code Search, cody
- **Performance characteristics**:
  - Higher latency (10-100ms per query) vs text search
  - **400x faster than dense embeddings** (semtools specific optimization)
  - Enables queries like "find all sorting implementations" or "locate security validation"
- **When to use**: Text/structure search fails; need conceptual understanding; cross-language patterns

**Implementation best practices**:
1. **Precompute embeddings**: Batch updates, not per-query computation
2. **Aggressive indexing**: Index entire codebase upfront for sub-100ms queries
3. **Cache popular queries**: Template common searches
4. **Chain with grep/cat**: semtools → grep refinement → cat specific files

**Cost-effectiveness**: Semantic search is expensive; use as escalation path, not first resort.

### Hybrid Search Strategy

**Optimal workflow** for code search:

1. **Start local**: ripgrep or ast-grep (fastest, cheapest)
2. **Escalate to semantic**: Only when exact text/structure fails
3. **MCP integration**: Remote clusters for large-scale operations

**Decision tree**:
```
Need structural pattern? → ast-grep
Need fast text search? → ripgrep (local)
Need semantic understanding? → semtools/semantic search
Need distributed scale? → mcp-ripgrep (remote)
```

## LLM Routing for Speed

### Groq Acceleration

**GPU inference platform** for ultra-low latency:

- **Performance**: 5-20ms per prompt (2-6x speed boost for bulk routing)
- **Use cases**:
  - First-pass filtering
  - Boilerplate generation
  - Simple codegen tasks
  - Syntax validation
- **Routing strategy**: Groq for low-complexity/high-volume → Premium models (Claude 3.5, GPT-4) for complex/contextual

**When to route to Groq**:
- Routine code completion
- Format conversion
- Simple refactoring
- Test boilerplate generation

**When to use premium models**:
- Architecture decisions
- Complex debugging
- Nuanced refactoring
- Context-heavy tasks

### Haiku Filtering

**Lightweight LLM pre-processing** for task triage:

- **Purpose**: Filter non-actionable prompts before expensive model calls
- **Deployment**: Microservice in front of Claude for maximum parallelism
- **Latency**: Sub-millisecond per call
- **Benefits**:
  - Reduces overload on premium models
  - Prevents costly long-context runs
  - Flags security-sensitive content early
  - Preclassifies for optimal model selection

**Filtering patterns**:
```
Input → Haiku triage → Simple task? → Groq
                     → Complex task? → Claude/GPT-4
                     → Security flag? → Human review
```

### Model Selection Matrix

| Task Type | Recommended Model | Latency | Cost |
|-----------|------------------|---------|------|
| Boilerplate generation | Groq | 5-20ms | Lowest |
| Simple refactoring | Groq/Haiku | 10-50ms | Low |
| Code review | Claude Sonnet | 200-500ms | Medium |
| Architecture design | Claude Opus | 500ms-2s | High |
| Complex debugging | Claude Opus | 500ms-2s | High |

## MCP Server Optimization

### Performance Characteristics

**MCP integration benefits**:
- Orchestrate remote/distributed CLI operations
- Async result streaming (parallel processing)
- Linear scaling with worker pools
- Up to 70% latency reduction vs synchronous execution

**Implementation patterns**:

**Worker pools**:
```python
# Dedicated ripgrep runners per project/service
mcp_server = MCPServer()
mcp_server.spawn_workers(count=4, tool="ripgrep")
```

**Async streaming**:
```python
# Claude starts generating before search completes
async for result in mcp_server.search_async(pattern):
    process_result(result)
```

**Query deduplication**:
```python
# Avoid redundant searches
cache = QueryCache()
result = cache.get_or_compute(query, mcp_server.search)
```

### Routing Strategy

**Local vs Remote MCP**:

| Query Type | Route | Reason |
|------------|-------|--------|
| Single file search | Local rg | No overhead |
| Multi-repo search | Remote MCP | Parallelism |
| Semantic queries | Remote MCP | Resource intensive |
| Lightweight grep | Local CLI | Fastest path |

## Cost-Effective Patterns

### Token Optimization

**Dynamic context loading**:
- Only load files/methods needed for current task
- Pipe via CLI to control exactly what enters context
- Avoid full codebase dumps

**Context management**:
```bash
# Bad: Load entire codebase
cat **/*.py | claude

# Good: Load specific context
rg -l "UserAuth" | head -5 | xargs cat | claude
```

**Helper scripts for context control**:
```bash
# claude-grep: Search + controlled context injection
#!/bin/bash
rg "$1" -l | head -n "${2:-3}" | xargs cat
```

### Caching Strategies

**Prompt template caching**:
- Template common tasks (lint, tests, onboarding)
- Cache responses for repeated operations
- Significant compute savings on routine tasks

**Session management**:
- Use `/clear` or `/init` to reset context between batches
- Prevents token bloat from accumulated history
- Maintain lean context for faster responses

### Workflow Modularization

**Atomic micro-workflows**:
- Split work into independent subtasks
- Enable parallel execution
- Simplify retry logic
- Reuse for similar tasks

**Benefits**:
- Scalable and fault-tolerant
- Token-efficient (each task has minimal context)
- 20-40% latency/token savings

## Helper Scripts and Automation

### Context Management CLI

**Common helpers**:

```bash
# claude-grep: Controlled search + context injection
claude-grep() {
    rg "$1" -l | head -n "${2:-5}" | xargs cat
}

# claude-reset: Clear context between tasks
claude-reset() {
    echo "/clear" | claude
}

# claude-compact: Trigger manual compaction
claude-compact() {
    echo "/compact" | claude
}
```

### Automated File Fetching

**Selective file injection**:
```bash
# Only relevant files, not entire codebase
relevant_files() {
    rg -l "$1" |
    grep -E "\.(py|rs|ts)$" |
    head -n 10 |
    xargs cat
}
```

### Token Pruning Utilities

**Minimize prompt size**:
```python
def prune_prompt(prompt: str, max_tokens: int) -> str:
    """Strip unnecessary context, preserve key info"""
    # Remove comments
    # Strip docstrings
    # Compress whitespace
    # Truncate to max_tokens
    pass
```

## Codebase Indexing Strategies

### Indexing Approaches

| Approach | Upfront Cost | Query Speed | Maintenance | Use Case |
|----------|-------------|-------------|-------------|----------|
| **File-based** (rg/ast-grep) | None | Fast | None | Small-medium codebases |
| **Static index** (ctags/cscope) | Medium | Instant | Periodic | Symbol lookups |
| **Semantic** (embeddings) | High | Sub-100ms | Continuous | Cross-language patterns |
| **Hybrid** | Medium | Variable | Moderate | Best of both worlds |

### Recommended Hybrid Approach

**Three-tier strategy**:
1. **Static index** (ctags): Day-to-day symbol navigation
2. **ripgrep/ast-grep**: Ad-hoc text/structure queries
3. **Semantic search**: Fallback for conceptual queries

**Workflow**:
```
Symbol lookup? → Static index (instant)
Pattern match? → ast-grep/ripgrep (subsecond)
Concept search? → Semantic embeddings (100ms)
```

## Performance Metrics and Benchmarks

### Measured Improvements

**Search operations**:
- ast-grep vs grep: **10-100x faster** for structural queries
- ripgrep vs grep: **5-30x faster** for text search
- mcp-ripgrep vs local: **70% latency reduction** with async streaming
- semtools vs dense embeddings: **400x faster**

**LLM routing**:
- Groq vs Claude: **2-6x speed boost** for simple tasks
- Haiku filtering: **Sub-ms overhead**, prevents expensive calls

**Workflow optimization**:
- Micro-workflows: **20-40% token reduction**
- Dynamic context loading: **30-50% token savings** vs full codebase
- Manual compaction: **Prevents degradation** from context bloat

### Benchmarking Strategy

**Key metrics to track**:
```python
metrics = {
    "search_latency": time_to_first_result,
    "token_consumption": total_tokens_per_task,
    "model_cost": inference_cost_usd,
    "time_to_completion": end_to_end_duration,
}
```

**A/B testing**:
- Baseline: Standard Claude Code workflow
- Optimized: Apply techniques systematically
- Measure: Before/after deltas on real tasks

## Best Practices Summary

### Search Optimization

1. **Start local, escalate strategically**: rg/ast-grep → mcp-ripgrep → semantic
2. **Use right tool for task**: Structure=ast-grep, Text=rg, Concept=semantic
3. **MCP for distribution**: Worker pools, async streaming, query deduplication
4. **Cache aggressively**: Popular queries, template responses

### LLM Routing

1. **Groq for simple tasks**: Boilerplate, format conversion, simple refactoring
2. **Haiku for triage**: Filter before expensive calls, security flagging
3. **Premium for complex**: Architecture, debugging, context-heavy operations
4. **Batch when possible**: Reduce per-call overhead

### Token Management

1. **Dynamic loading**: Only necessary files, not full codebase
2. **Manual compaction**: Strategic `/clear` and `/compact` usage
3. **Helper scripts**: Automate context control
4. **Micro-workflows**: Atomic tasks with minimal context

### Workflow Design

1. **Modularize**: Break into independent subtasks
2. **Parallelize**: Concurrent operations where possible
3. **Automate**: Scripts for repeated patterns
4. **Measure**: Benchmark before/after optimizations

## Related Concepts

### Prerequisites
- [[claude_code]] - Understanding Claude Code fundamentals is essential for optimization strategies

### Related Topics
- [[claude_code_agents]] - Subagents benefit from efficiency optimizations through parallel execution
- [[mcp_overview]] - MCP servers enable distributed tool integration for performance
- [[llm_self_talk_optimization]] - Complementary token reduction through prompt compression
- [[optimization]] - General optimization principles applicable to Claude Code workflows

### Extends
- [[claude_code]] - These optimization techniques build upon core Claude Code functionality

## References

[1] Sidetool - Advanced Claude Code Workflows (2025) - https://www.sidetool.co/post/advanced-claude-code-workflows-tips-and-tricks-for-power-users
[2] Siddharth Bharath - Claude Code Complete Guide (2025) - https://www.siddharthbharath.com/claude-code-the-complete-guide/
[3] Anthropic Engineering - Claude Code Best Practices (2025) - https://www.anthropic.com/engineering/claude-code-best-practices
[4] Collabnix - Advanced Command-Line AI Development (2025) - https://collabnix.com/claude-code-best-practices-advanced-command-line-ai-development-in-2025/
[5] Tembo - Mastering Claude Code Tips (2025) - https://tembo.io/blog/mastering-claude-code-tips
[6] ClaudeLog - Claude Code Performance FAQ (2025) - https://www.claudelog.com/faqs/claude-code-performance/
[7] GitHub - Claude Flow High Performance (2025) - https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-High-Performance
[8] AI Multiple - Agentic Coding Research (2025) - https://research.aimultiple.com/agentic-coding/
