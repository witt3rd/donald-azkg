---
tags: [claude-code, plugins, zettelkasten, knowledge-graph, project]
---

# Zettelkasten Claude Code Plugin: Implementation Guide

**A Claude Code plugin** that brings the Obsidian-based Zettelkasten knowledge graph system into Claude Code as a first-class development tool. This plugin would provide agents, slash commands, hooks, and MCP servers for intelligent knowledge management during software development.

## Vision

Transform the standalone knowledge graph management system into an integrated Claude Code plugin that enables developers to:
- Query and navigate knowledge graphs during coding sessions
- Create and link notes without leaving the development environment
- Leverage specialized agents for research, documentation, and learning path generation
- Automate knowledge capture through hooks triggered by development events

## Plugin Architecture

### Four Extension Points

**Slash Commands** (User-facing knowledge operations):
- `/create-note [topic]` - Create atomic notes with automatic relationship discovery
- `/search-notes [query]` - Semantic search across knowledge base
- `/graph-note [filename]` - View note relationships and metadata
- `/learning-path [target]` - Generate prerequisite learning sequences
- `/expand-graph [note]` - Discover missing relationships
- `/conform-note [filename]` - Restructure notes to standard format

**Subagents** (Specialized knowledge workers):
- **Research Agent**: Conduct multi-source research and create comprehensive notes
- **Relationship Discovery Agent**: Analyze codebase and knowledge graph to suggest connections
- **Documentation Agent**: Generate technical documentation with automatic knowledge graph linking
- **Learning Path Agent**: Create personalized learning sequences based on prerequisites

**MCP Server** (Knowledge graph as a service):
- Expose knowledge graph operations as MCP resources and tools
- Enable ANY Claude Code agent to query domain knowledge contextually
- Use JSON-RPC 2.0 protocol with standard MCP methods
- Provide authentication and caching for team environments

**Hooks** (Automatic knowledge capture):
- **Post-commit hook**: Extract concepts from commit messages and link to knowledge base
- **Documentation update hook**: Sync code documentation with knowledge graph notes
- **Learning trigger hook**: Suggest relevant notes when encountering unfamiliar APIs
- **Research capture hook**: Auto-create notes from investigation sessions

## Technical Implementation

### MCP Resources and Tools

**Critical Feature**: Expose the knowledge graph as MCP resources and tools that ANY agent can query during development, not just custom plugin agents. This enables all Claude Code agents to access domain knowledge contextually.

MCP uses **JSON-RPC 2.0 protocol** with `resources/list`, `resources/read`, `tools/list`, and `tools/call` methods.

#### MCP Resources (Read-Only Knowledge Access)

Resources provide discoverable, read-only access to knowledge graph data using URI-based access patterns.

**Available Resource URIs:**

- `kg://notes` - List all notes with metadata (filename, title, summary, tags)
  - Query parameters: `?tags=python,mcp` for filtering by tags
  - Query parameters: `?batch=Core+AI/Agents` for filtering by batch

- `kg://note/{filename}` - Retrieve specific note with full content
  - Returns: Complete markdown content plus metadata
  - Example: `kg://note/mcp_overview.md`

- `kg://relationships/{filename}` - Navigate relationship graph from a note
  - Query parameters: `?type=prerequisites` to filter relationship types
  - Query parameters: `?depth=2` to include related notes of related notes
  - Returns: Typed relationships (prerequisites, extends, related_concepts, etc.)

- `kg://learning-path/{filename}` - Generate prerequisite chain for a topic
  - Traverses prerequisite relationships to build ordered learning sequence
  - Returns: Ordered list of notes to study before target topic
  - Example: `kg://learning-path/react_agent_pattern.md` → [agents.md, react_framework.md, react_agent_pattern.md]

**Resource Response Format:**
```json
{
  "uri": "kg://note/agents.md",
  "mimeType": "text/markdown",
  "content": "Full markdown content...",
  "metadata": {
    "title": "AI Agents",
    "tags": ["ai", "agents", "llm"],
    "summary": "Brief description..."
  }
}
```

#### MCP Tools (Agent Actions)

Tools are actions that agents can invoke to search, discover, and navigate the knowledge graph.

**Available Tools:**

1. **`search_knowledge`** - Semantic search across knowledge base
   - Parameters:
     - `query` (string, required): Search query
     - `tags` (array of strings, optional): Filter by tags
     - `limit` (integer, optional, default: 10): Max results
   - Returns: Ranked list of matching notes with relevance scores
   - Use case: Agent searches for "async timeout handling" to help debug

2. **`find_related`** - Discover concepts related to a topic
   - Parameters:
     - `topic` (string, required): Topic to explore
     - `relationship_types` (array of strings, optional): Filter by relationship type
   - Returns: Notes connected via specified relationships
   - Use case: Agent explores what extends or relates to "semantic routing"

3. **`get_learning_path`** - Generate ordered prerequisite chain
   - Parameters:
     - `target` (string, required): Target note filename
   - Returns: Ordered sequence of prerequisites leading to target
   - Use case: Agent determines what to learn before implementing a pattern

**Tool Response Format:**
```json
{
  "tool": "search_knowledge",
  "results": [
    {
      "filename": "async_patterns.md",
      "title": "Async Patterns in Python",
      "summary": "...",
      "relevance_score": 0.89
    }
  ]
}
```

#### Agent Use Case Scenarios

**Scenario 1: Agent encounters unfamiliar API**
```
Context: Agent is working with MCP code and doesn't have full context

1. Agent requests resource: kg://note/mcp_overview.md
   → Receives full MCP overview note with summary

2. Agent requests resource: kg://relationships/mcp_overview.md?type=extends
   → Receives notes that extend MCP (python_mcp_sdk.md, typescript_mcp_sdk.md)

3. Agent reads relevant SDK notes to build context

Result: Agent has comprehensive MCP knowledge for the task
```

**Scenario 2: Agent builds prerequisite learning path**
```
Context: User wants to implement React agent pattern

1. Agent requests resource: kg://learning-path/react_agent_pattern.md
   → Receives ordered list:
      1. agents.md (understand AI agents)
      2. react_framework.md (understand React)
      3. react_agent_pattern.md (target topic)

2. Agent retrieves content for each note in sequence

Result: Agent learns concepts in proper dependency order
```

**Scenario 3: Agent searches during debugging**
```
Context: Code failing with async timeout error

1. Agent calls tool: search_knowledge
   Parameters: {
     "query": "async timeout error handling",
     "tags": ["python", "async"],
     "limit": 5
   }
   → Receives ranked list of relevant notes

2. Agent retrieves top 3 most relevant notes

Result: Agent has contextual knowledge to help debug
```

**Scenario 4: Agent discovers related concepts**
```
Context: User mentions "semantic routing" in requirements

1. Agent calls tool: find_related
   Parameters: {
     "topic": "semantic routing",
     "relationship_types": ["related_concepts", "examples"]
   }
   → Receives related concepts (agents.md, llm routing patterns)
   → Receives examples (specific routing implementations)

Result: Agent understands broader context and related patterns
```

### Plugin Manifest

```json
{
  "name": "zettelkasten-knowledge-graph",
  "version": "1.0.0",
  "description": "Obsidian-based Zettelkasten knowledge management for Claude Code",
  "author": "Your Name",
  "repository": "https://github.com/your-org/claude-code-zettelkasten",
  "extensions": {
    "commands": [
      "create-note",
      "search-notes",
      "graph-note",
      "learning-path",
      "expand-graph",
      "conform-note"
    ],
    "agents": [
      "research-agent",
      "relationship-discovery",
      "documentation-agent",
      "learning-path-agent"
    ],
    "mcp_server": {
      "protocol": "json-rpc-2.0",
      "resources": [
        "kg://notes",
        "kg://note/{filename}",
        "kg://relationships/{filename}",
        "kg://learning-path/{filename}"
      ],
      "tools": [
        "search_knowledge",
        "find_related",
        "get_learning_path"
      ]
    },
    "hooks": [
      "post-commit",
      "documentation-update",
      "learning-trigger",
      "research-capture"
    ]
  }
}
```

### Directory Structure

```
zettelkasten-plugin/
├── manifest.json                 # Plugin metadata and extension declarations
├── README.md                     # Installation and usage guide
├── commands/                     # Slash command implementations
│   ├── create-note.ts
│   ├── search-notes.ts
│   ├── graph-note.ts
│   ├── learning-path.ts
│   ├── expand-graph.ts
│   └── conform-note.ts
├── agents/                       # Subagent definitions
│   ├── research-agent.md
│   ├── relationship-discovery.md
│   ├── documentation-agent.md
│   └── learning-path-agent.md
├── mcp-server/                   # MCP server implementation
│   ├── server.py                # JSON-RPC 2.0 server
│   ├── resources.py             # Resource handlers (kg:// URIs)
│   ├── tools.py                 # Tool implementations
│   ├── requirements.txt
│   ├── graph_lib.py             # Reused from existing scripts
│   └── knowledge_graph_full.json # Graph data (or path config)
├── hooks/                        # Lifecycle hooks
│   ├── post-commit.ts
│   ├── documentation-update.ts
│   ├── learning-trigger.ts
│   └── research-capture.ts
└── tests/                        # Plugin tests
    ├── test_commands.py
    ├── test_mcp_server.py
    └── test_hooks.py
```

## Implementation Phases

### Phase 1: Core MCP Server
**Goal**: Expose knowledge graph operations as MCP resources and tools

**Tasks**:
1. Implement JSON-RPC 2.0 server with MCP protocol
2. Create resource handlers for kg:// URIs
3. Implement tool handlers (search, find_related, get_learning_path)
4. Add authentication and rate limiting
5. Deploy locally and test with Claude Code

**Deliverables**:
- Working MCP server with resources and tools
- API documentation with examples
- Integration tests

### Phase 2: Essential Slash Commands
**Goal**: Basic knowledge operations from Claude Code interface

**Commands to implement**:
1. `/create-note` - Create notes with Perplexity research
2. `/search-notes` - Find relevant knowledge
3. `/graph-note` - View relationships

**Deliverables**:
- TypeScript command implementations
- User documentation
- Demo video

### Phase 3: Specialized Agents
**Goal**: AI-powered knowledge workers

**Agents to build**:
1. **Research Agent** - Multi-source investigation with note creation
2. **Relationship Discovery** - Analyze connections between concepts
3. **Documentation Agent** - Auto-link code docs to knowledge base

**Deliverables**:
- Agent prompt templates (`.md` files)
- Example workflows
- Performance benchmarks

### Phase 4: Workflow Hooks
**Goal**: Automatic knowledge capture

**Hooks to implement**:
1. **Post-commit** - Extract concepts from development activity
2. **Documentation update** - Sync docs with knowledge graph
3. **Learning trigger** - Suggest notes for unfamiliar APIs

**Deliverables**:
- Hook implementations
- Configuration guide
- Privacy considerations documentation

### Phase 5: Plugin Marketplace Release
**Goal**: Public distribution and community building

**Tasks**:
1. Create GitHub repository with marketplace-ready structure
2. Write comprehensive README with screenshots
3. Add installation scripts and setup automation
4. Create example knowledge graphs for demo
5. Publish to plugin registry
6. Create community Discord/discussion forum

**Deliverables**:
- Public GitHub repo
- Marketplace listing
- Community channels

## Marketplace Strategy

### Repository Setup

**GitHub Repository Structure**:
```
github.com/your-org/claude-code-zettelkasten/
├── README.md                    # Hero section with screenshots
├── INSTALLATION.md              # Step-by-step setup
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # Open source license (MIT?)
├── docs/                        # Detailed documentation
│   ├── getting-started.md
│   ├── slash-commands.md
│   ├── agents.md
│   ├── mcp-api.md
│   └── hooks.md
├── examples/                    # Example knowledge graphs
│   ├── software-engineering/
│   ├── machine-learning/
│   └── systems-design/
└── plugin/                      # Actual plugin code
    └── (structure from above)
```

**README Hero Section**:
```markdown
# Zettelkasten Knowledge Graph for Claude Code

> Transform Claude Code into a knowledge management powerhouse with Obsidian-compatible Zettelkasten note-taking, automatic relationship discovery, and AI-powered research agents.

[🚀 Install Plugin] [📚 Documentation] [💬 Community]

## Features
- 🧠 Create atomic notes with automatic relationship discovery
- 🔍 Semantic search across your knowledge base
- 🤖 Specialized agents for research and documentation
- 🔗 Visual knowledge graph navigation
- ⚡ Lightning-fast MCP server architecture
- 📊 Learning path generation from prerequisites

[Demo GIF showing plugin in action]
```

### Distribution Channels

**Official Plugin Registry**:
- Submit to Anthropic's plugin marketplace (if available)
- Maintain compatibility with registry standards
- Regular updates and version management

**Community Platforms**:
- GitHub repository with issues and discussions
- Discord server for users and contributors
- Tutorial videos on YouTube
- Blog posts about knowledge management in development

**Documentation Site**:
- Hosted on GitHub Pages or Vercel
- Interactive examples
- API reference
- Video tutorials
- Community showcase

## Technical Challenges and Solutions

### Challenge 1: Graph Size and Performance
**Problem**: Large knowledge graphs (1000+ notes) may be slow to load

**Solutions**:
- Implement lazy loading for graph queries
- Add Redis caching layer for frequently accessed notes
- Use graph database (Neo4j) for complex relationship queries
- Implement pagination for search results

### Challenge 2: Multi-User Synchronization
**Problem**: Teams need shared access to knowledge graphs

**Solutions**:
- Implement locking mechanism for concurrent edits
- Add conflict resolution for simultaneous updates
- Use Git as version control backend
- Implement real-time sync via WebSockets

### Challenge 3: Obsidian Compatibility
**Problem**: Users want to use both Obsidian and Claude Code

**Solutions**:
- Maintain identical markdown format
- Support Obsidian wikilink syntax
- Watch for file system changes from Obsidian
- Sync graph JSON with markdown files bidirectionally

### Challenge 4: Agent Context Management
**Problem**: Agents need access to relevant notes without context overflow

**Solutions**:
- Implement retrieval-augmented generation (RAG)
- Use vector embeddings for semantic similarity
- Cache agent context between invocations
- Provide context compression utilities

## Business Model Considerations

### Open Source Strategy
- Core functionality: **Free and open source** (MIT License)
- Builds community and trust
- Enables contributions and extensions
- Increases adoption rate

### Premium Features (Optional)
- **Team plans**: Multi-user sync and collaboration
- **Cloud hosting**: Managed MCP server deployment
- **Advanced agents**: Specialized domain agents (medical, legal, etc.)
- **Enterprise support**: SLA, custom integrations, training

### Sustainability Model
- GitHub Sponsors for individual contributors
- Corporate sponsorships from companies using the plugin
- Optional paid hosting service
- Consulting for custom implementations

## Success Metrics

### Adoption Metrics
- GitHub stars and forks
- Plugin installations
- Active users (MAU)
- Community engagement (Discord members, issues, PRs)

### Usage Metrics
- Notes created per user
- Slash command usage frequency
- Agent invocations
- Graph size distribution

### Quality Metrics
- Bug reports and resolution time
- User satisfaction (surveys)
- Documentation completeness
- Test coverage

## Next Steps

### Immediate Actions (Week 1)
1. Set up GitHub repository with marketplace structure
2. Implement JSON-RPC 2.0 MCP server with resource and tool handlers
3. Implement core slash commands (`/create-note`, `/search-notes`)
4. Create plugin manifest and basic documentation

### Short Term (Month 1)
1. Complete Phase 1 and 2 implementation
2. Alpha testing with small user group
3. Create demo videos and documentation
4. Prepare marketplace submission

### Medium Term (Quarter 1)
1. Complete all five implementation phases
2. Public beta release
3. Build community channels
4. Gather feedback and iterate
5. Submit to official plugin registry

### Long Term (Year 1)
1. Grow user base to 1000+ active users
2. Establish contributor community
3. Develop advanced features based on feedback
4. Explore premium/enterprise offerings
5. Create ecosystem of compatible tools

This Zettelkasten Claude Code plugin represents the convergence of knowledge management and AI-assisted development, enabling developers to build personal knowledge graphs that grow alongside their codebases and accelerate learning through intelligent automation.

## Related Concepts

### Prerequisites
- [[claude_code_plugins]] - Understanding plugin architecture is essential for implementation
- [[mcp_overview]] - MCP protocol is the foundation for the knowledge graph server

### Related Topics
- [[claude_code]] - Platform that will host the plugin
- [[claude_code_agents]] - Subagent system used by knowledge worker agents

### Examples
- This note describes a concrete example of building a Claude Code plugin
