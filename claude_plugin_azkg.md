---
tags: [claude-code, plugins, zettelkasten, knowledge-graph, implementation, agentic-zkg]
---

# Claude Code Plugin for Agentic-ZKG

**A Claude Code plugin implementing the [[agentic_zkg]] paradigm** - providing conversational, agent-maintained knowledge management through slash commands, MCP servers, specialized subagents, and workflow hooks.

## Overview

This plugin is a **specific implementation** of the agentic-ZKG paradigm using Claude Code as the agent. It transforms the theoretical concept of agent-maintained knowledge graphs into a practical, installable tool.

**What it provides:**
- Slash commands for conversational knowledge operations
- MCP server exposing knowledge graph to ALL agents (not just this plugin)
- Specialized subagents for research, relationship discovery, documentation
- Workflow hooks for automatic knowledge capture
- Obsidian-compatible markdown format

**What it enables:**
Anyone can install this plugin and create their own agentic-ZKG instance - a personal knowledge base maintained through conversation with Claude.

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

### Architectural Decision: Markdown-First, No JSON Graph

**Critical Design Choice:** The MCP server does NOT maintain a separate JSON knowledge graph file. Instead, **markdown files are the single source of truth**.

#### Why Eliminate the JSON Graph?

The original prototype used `knowledge_graph_full.json` to track relationships, but this creates redundancy and overhead:

**The Problem with Dual Storage:**
- **Duplication**: Relationships exist in BOTH JSON and markdown "Related Concepts" sections
- **Sync overhead**: Every change must propagate JSON → markdown
- **Drift potential**: JSON and markdown can desynchronize
- **Coordination bottleneck**: JSON is a single file requiring atomic updates and locking
- **Information already exists**: The graph IS the markdown files

**What's Already in Markdown:**
1. **Wikilinks** in content body → implicit edges
2. **Tags** in YAML frontmatter → clustering/grouping
3. **Related Concepts sections** → explicit typed relationships WITH "why" explanations

Example:
```markdown
## Related Concepts

### Prerequisites
- [[mcp_overview]] - Need to understand protocol first

### Extends
- [[mcp_implementation]] - Python-specific implementation
```

**The graph exists in the markdown.** The JSON was just an index/cache.

#### Markdown-First Architecture

**MCP Server Implementation:**

1. **Parse on demand** - Read markdown files when needed (extremely fast with grep)
2. **Build in-memory graph** - Construct graph representation from markdown during session
3. **Cache during session** - Keep parsed graph in memory for fast queries
4. **Direct markdown updates** - Write changes directly to markdown files
5. **No JSON to maintain** - Eliminate sync overhead entirely

**Benefits:**
- ✅ **Single source of truth** - Markdown only
- ✅ **No sync overhead** - Changes go directly to markdown
- ✅ **Parallel updates** - Individual files can be processed independently (no global lock)
- ✅ **More transparent** - Everything visible in markdown
- ✅ **Obsidian-native** - True compatibility, no hidden state
- ✅ **Git-friendly** - Better merge handling with separate files
- ✅ **Simpler** - Eliminate entire JSON maintenance layer

**Performance:**
- Parsing 98 markdown files: **milliseconds**
- Grep for targeted searches: **instant**
- Semantic search if needed: ChromaDB/vector index (optional)
- Cache in-memory during agent session: **negligible overhead**

**Where Batches Live:**
MOC notes serve as batch/theme organizers:
- `Core_AI_MOC.md` - Links to all Core AI/Agents notes
- `MCP_MOC.md` - Links to all MCP Protocol notes
- `Python_Stack_MOC.md` - Links to all Python notes

This is **more Zettelkasten-aligned** than artificial JSON batches.

**No Python Scripts for Operations:**
Claude Code's slash commands use built-in tools (Read, Write, Edit, Grep, Glob, Bash) directly:
- `/create-note` → Write + Edit markdown files
- `/rename-note` → Grep for wikilinks + Edit each file
- `/graph-validate` → Grep + Glob to verify wikilinks exist
- `/graph-stats` → Grep + Glob to count notes/relationships

No need for intermediate Python scripts to manipulate a JSON graph - Claude operates directly on markdown.

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
│   ├── markdown_parser.py       # Parse markdown files to build graph
│   ├── graph_builder.py         # In-memory graph construction
│   ├── requirements.txt
│   └── config.json              # Path to markdown vault, cache settings
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
1. Implement markdown parser that extracts:
   - YAML frontmatter (tags, title, summary)
   - Wikilinks in content body
   - Related Concepts sections with typed relationships
2. Build in-memory graph representation from parsed markdown
3. Implement JSON-RPC 2.0 server with MCP protocol
4. Create resource handlers for kg:// URIs (query in-memory graph)
5. Implement tool handlers (search, find_related, get_learning_path)
6. Add caching layer for session performance
7. Deploy locally and test with Claude Code

**Deliverables**:
- Markdown parser library
- In-memory graph builder
- Working MCP server with resources and tools (no JSON file needed)
- API documentation with examples
- Integration tests

**Key principle**: Markdown is the single source of truth. JSON is never written, only derived in-memory.

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

### Official Anthropic Pattern: Marketplace Repository

**Claude Code uses a decentralized plugin distribution model.** There is no centralized Anthropic-operated marketplace. Instead, plugin developers create **marketplace repositories** - Git repos containing multiple plugins and a marketplace manifest that Claude Code reads directly[1].

### Multi-Plugin Marketplace Repository

**Recommended structure for hosting multiple plugins (including AZKG):**

```
witt3rd-claude-plugins/              # GitHub repository
├── .claude-plugin/
│   └── marketplace.json             # Marketplace manifest (lists all plugins)
├── plugins/
│   ├── azkg/                        # AZKG plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json          # Plugin metadata
│   │   ├── commands/
│   │   │   ├── create-note.md
│   │   │   ├── search-notes.md
│   │   │   ├── expand-graph.md
│   │   │   ├── learning-path.md
│   │   │   └── ... (all 13 commands)
│   │   ├── agents/
│   │   │   ├── research-agent.md
│   │   │   └── relationship-discovery.md
│   │   ├── mcp-server/
│   │   │   ├── server.py
│   │   │   ├── resources.py
│   │   │   ├── tools.py
│   │   │   └── requirements.txt
│   │   ├── hooks/
│   │   │   └── post-commit.sh
│   │   ├── README.md                # AZKG plugin docs
│   │   └── docs/
│   ├── plugin-2/                    # Future plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── ...
│   └── plugin-3/                    # Future plugin
├── shared/                          # Optional: shared utilities
│   └── utils.py
├── docs/
│   ├── getting-started.md
│   └── plugin-development.md
├── README.md                        # Marketplace hero page
├── CONTRIBUTING.md
└── LICENSE
```

### Marketplace Manifest

**`.claude-plugin/marketplace.json`** - Catalog of all plugins in this repository:

```json
{
  "version": "1.0.0",
  "name": "witt3rd-claude-plugins",
  "description": "Professional-grade Claude Code plugins for knowledge management and development workflows",
  "author": "Donald Thompson",
  "repository": "https://github.com/witt3rd/claude-plugins",
  "plugins": [
    {
      "name": "azkg",
      "displayName": "Agentic Zettelkasten Knowledge Graph",
      "description": "Agent-maintained knowledge management with MCP server, specialized agents, and workflow hooks",
      "version": "1.0.0",
      "path": "./plugins/azkg",
      "tags": ["knowledge-management", "zettelkasten", "mcp", "research"],
      "author": "Donald Thompson",
      "homepage": "https://github.com/witt3rd/claude-plugins/tree/main/plugins/azkg"
    }
    // Additional plugins added here as developed
  ]
}
```

### Plugin Metadata

**`plugins/azkg/.claude-plugin/plugin.json`** - Individual plugin manifest:

```json
{
  "name": "azkg",
  "version": "1.0.0",
  "displayName": "Agentic-ZKG",
  "description": "Agent-maintained Zettelkasten knowledge graph",
  "author": "Donald Thompson",
  "license": "MIT",
  "repository": "https://github.com/witt3rd/claude-plugins",
  "commands": [
    "create-note",
    "search-notes",
    "expand-graph",
    "learning-path",
    "graph-note",
    "conform-note",
    "rename-note",
    "refresh-topic",
    "graph-validate",
    "graph-stats",
    "graph-moc"
  ],
  "agents": [
    "research-agent",
    "relationship-discovery"
  ],
  "hooks": [
    "post-commit"
  ],
  "mcp": {
    "enabled": true,
    "server": "./mcp-server/server.py"
  }
}
```

### Installation Flow

**Users install via native Claude Code commands:**

```bash
# 1. Add the marketplace repository
/plugin marketplace add witt3rd/claude-plugins

# 2. Browse available plugins in the marketplace
/plugin

# 3. Install the AZKG plugin
/plugin install azkg@witt3rd

# 4. Use the plugin commands
/create-note "neural networks"
/search-notes "MCP protocol"
/learning-path "react_agent_pattern.md"
```

### Marketplace README

**Repository hero page showcasing all plugins:**

```markdown
# witt3rd Claude Code Plugins

> Professional-grade plugins for Claude Code: knowledge management, development workflows, and AI-powered productivity

## 🚀 Quick Start

```bash
# Add this marketplace to Claude Code
/plugin marketplace add witt3rd/claude-plugins

# Install any plugin
/plugin install azkg@witt3rd
```

## 📦 Available Plugins

### 🧠 Agentic-ZKG
**Agent-maintained Zettelkasten knowledge management**

Transform Claude Code into a knowledge management powerhouse with:
- 🧠 Create atomic notes with automatic relationship discovery
- 🔍 Semantic search across your knowledge base
- 🤖 Specialized agents for research and documentation
- 🔗 MCP server exposing knowledge to all agents
- 📊 Learning path generation from prerequisites

**Install:** `/plugin install azkg@witt3rd`
**Version:** 1.0.0
**Docs:** [AZKG Plugin Guide](./plugins/azkg/README.md)

---

### 🔧 [Future Plugin 2]
Brief description...

**Install:** `/plugin install plugin2@witt3rd`
**Version:** 0.5.0

---

## 📚 Documentation

- [Getting Started](./docs/getting-started.md)
- [Plugin Development Guide](./docs/plugin-development.md)
- [Contributing](./CONTRIBUTING.md)

## 🤝 Contributing

Want to contribute? See our [Contributing Guide](./CONTRIBUTING.md)

## 📄 License

MIT License - See [LICENSE](./LICENSE)
```

### Distribution Model

**Decentralized, Git-based distribution:**

✅ **How it works:**
- Plugin marketplace is a Git repository (public or private)
- Users add marketplace URL to Claude Code
- Claude Code reads `marketplace.json` to discover plugins
- Plugins install directly from Git repository
- No centralized registry or approval process

✅ **Benefits:**
- **Full control** - You own the marketplace and distribution
- **No gatekeepers** - No approval process or waiting
- **Private or public** - Works with GitHub, GitLab, internal Git
- **Version control** - Git provides built-in versioning
- **Team-friendly** - Can host private marketplaces for internal teams

✅ **Community Discovery:**
- No official central directory (similar to pre-npm era)
- Community-curated lists like "awesome-claude-code"[2]
- Social sharing via GitHub, blogs, documentation
- Word-of-mouth and developer networks

### Scaling Strategy

**Start with monorepo marketplace (2-5 plugins):**
- Single repository
- Shared tooling and CI/CD
- Easy to add new plugins
- Clean organization with subdirectories

**Scale to multi-repo if needed (10+ plugins):**
- Split each plugin to separate repository
- Use Git submodules or meta-repository
- Marketplace repo contains only manifest + docs
- Better for community contributions

**This AZKG plugin is the first in the witt3rd-claude-plugins marketplace.**

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
- Support Obsidian wikilink syntax `[[note]]` (not `[[note.md]]`)
- Watch for file system changes from Obsidian (inotify/file watching)
- Refresh in-memory graph cache when markdown files change
- No hidden state - everything visible in markdown

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
1. **Create marketplace repository:** `witt3rd/claude-plugins` on GitHub
2. **Set up directory structure:** `.claude-plugin/`, `plugins/azkg/`, `shared/`, `docs/`
3. **Create marketplace manifest:** `.claude-plugin/marketplace.json` with AZKG entry
4. **Create plugin manifest:** `plugins/azkg/.claude-plugin/plugin.json`
5. **Write marketplace README:** Hero page with installation instructions

### Short Term (Month 1)
1. **Migrate AZKG commands:** Move 13 command implementations to `plugins/azkg/commands/`
2. **Implement MCP server:** JSON-RPC 2.0 server with resource and tool handlers
3. **Add agent definitions:** Research and relationship discovery agents
4. **Create plugin documentation:** `plugins/azkg/README.md` with usage guide
5. **Test installation flow:** `/plugin marketplace add witt3rd/claude-plugins`

### Medium Term (Quarter 1)
1. Complete all five implementation phases
2. Alpha testing with small user group
3. Create demo videos and documentation
4. Add to community-curated lists (e.g., awesome-claude-code)
5. Gather feedback and iterate

### Long Term (Year 1)
1. Grow user base to 1000+ active users
2. Establish contributor community
3. Develop advanced features based on feedback
4. Explore premium/enterprise offerings
5. Create ecosystem of compatible tools

## Summary

This Claude Code plugin provides a complete implementation of the [[agentic_zkg]] paradigm, enabling anyone to create and maintain their own agent-powered knowledge base.

**Key Architectural Principles:**

1. **Markdown-First** - No separate JSON graph. Markdown files are the single source of truth.
2. **In-Memory Graph** - Parse markdown on-demand, cache in-memory during session.
3. **MCP Protocol** - Expose knowledge graph as resources and tools for any agent.
4. **Obsidian-Compatible** - Full compatibility with Obsidian, no hidden state.
5. **Automated Maintenance** - Claude handles relationship discovery, validation, and evolution.

**Installation enables:**
- Create your own agentic-ZKG instance
- Conversational knowledge management through slash commands
- Automated relationship discovery and graph maintenance
- MCP server providing knowledge access to all Claude Code agents
- Obsidian compatibility for visual exploration

This plugin makes the agentic-ZKG paradigm practical and accessible, enabling developers to build personal knowledge graphs that grow alongside their codebases through intelligent, conversational interaction with Claude.

## Related Concepts

### Extends
- [[agentic_zkg]] - This plugin implements the agentic-ZKG paradigm using Claude Code

### Prerequisites
- [[claude_code_plugins]] - Understanding plugin architecture is essential for implementation
- [[mcp_overview]] - MCP protocol is the foundation for the knowledge graph server

### Related Topics
- [[claude_code]] - Platform that hosts this plugin
- [[claude_code_agents]] - Subagent system used by knowledge worker agents

## References

[1] Anthropic. "Claude Code Plugins Documentation." https://docs.claude.com/en/docs/claude-code/plugins

[2] hesreallyhim. "Awesome Claude Code - Curated list of Claude Code resources." https://github.com/hesreallyhim/awesome-claude-code
