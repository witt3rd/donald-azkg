# Donald's Agentic-ZKG

**Welcome to my personal knowledge base** - an instance of an [[agentic_zkg]] powered by [[claude_plugin_azkg|Claude Code]].

This is not traditional documentation. This is a **living, agent-maintained knowledge network** that grows through conversation with Claude. Think of it as my second brain, but one that maintains itself.

## What's In This Knowledge Base

**98+ interconnected notes** covering:
- **AI & Agents** (23 notes) - LLMs, agentic systems, Claude Code, semantic routing
- **MCP Protocol** (10 notes) - Model Context Protocol implementation across languages
- **Python Stack** (12 notes) - Python development, async patterns, best practices
- **Rust** (8 notes) - Rust programming, ownership, async, tooling
- **TypeScript & React** (9 notes) - Full-stack development, frameworks, patterns
- **Writing & Communication** (7 notes) - Technical writing, prompting, storytelling
- **Systems & Tools** (15 notes) - Obsidian, git workflows, Windows dev, architecture
- **Meta** (14 notes) - This system itself, workflows, tag catalogs

## How This Works

This knowledge base implements the [[agentic_zkg]] paradigm using the [[claude_plugin_azkg]] implementation.

**Plugin Installation:**
```bash
# Add the marketplace
/plugin marketplace add witt3rd/claude-plugins

# Install AZKG plugin
/plugin install azkg@witt3rd

# Restart Claude Code to load the plugin
```

**Once installed, the plugin provides 11 slash commands** for automated knowledge management.

**I (human) provide direction:**
- "Create a note about X"
- "Find relationships between Y and Z"
- "What should I learn before studying A?"

**Claude (agent) maintains everything:**
- Researches topics via Perplexity
- Discovers relationships automatically
- Validates graph integrity
- Handles bulk operations (renames, migrations, conformance)
- Suggests improvements

**The result:** A knowledge base that grows and evolves through conversation, not manual curation.

## Key Statistics

- **Total notes**: 98
- **Relationship types**: 6 (prerequisites, extends, related_concepts, alternatives, examples, extended_by)
- **Tags**: 60+ across 6 dimensions
- **MOCs** (navigation hubs): 8
- **Bidirectional links**: All relationships work both ways
- **Automated operations**: 10+ slash commands

## What Makes This Different

**Not Obsidian alone:**
- Obsidian is my GUI for visual exploration
- Claude is my agent for automated maintenance
- Best of both: Human intuition + AI automation

**Not a wiki or documentation:**
- Notes are atomic - one complete idea each
- Structure emerges from links, not folders
- Knowledge forms a network, not a hierarchy
- Designed for AI agent consumption (LLM context)

**Not manually maintained:**
- Agent discovers relationships
- Agent validates integrity
- Agent handles migrations
- Agent suggests connections I'd miss

## Navigating This Knowledge Base

**Start with MOCs (Maps of Content):**
- `agents_moc.md` - AI agents and agentic systems
- `mcp_moc.md` - Model Context Protocol
- `python_moc.md` - Python development
- `rust_moc.md` - Rust programming
- `typescript_moc.md` - TypeScript and React
- `windows_moc.md` - Windows development
- `writing_moc.md` - Writing and communication
- `csharp_moc.md` - C# development

**Or search by tag:**
- `#agents` - AI agent architectures and patterns
- `#mcp` - Model Context Protocol across all languages
- `#python` + `#llm` - Python LLM integration
- `#pattern` - Design patterns across domains
- `#guide` - Step-by-step implementation guides

**Or ask Claude:**
- `/graph-note [filename]` - See all relationships for a note
- `/search-notes [query]` - Semantic search
- `/learning-path [target]` - Generate prerequisite chain

## Note Organization Principles

My notes follow three patterns (see [[agentic_zkg]] for the theory):

**1. Reference Notes** - Complete documentation
- `python_mcp_sdk.md` - Full guide to Python MCP SDK and FastMCP
- `rust_best_practices.md` - Comprehensive Rust coding standards
- `agent_mcp_apis.md` - Complete MCP API reference for agents

**2. Concept Notes** - Single focused ideas
- `semantic_routing.md` - Model selection based on query semantics
- `llm_self_talk_optimization.md` - Token-efficient agent communication
- `react_agent_pattern.md` - Design pattern for agent UIs

**3. MOC Notes** - Navigation hubs
- `agents_moc.md` - Links all AI agent concepts
- `mcp_moc.md` - Links all MCP protocol notes
- `writing_moc.md` - Links writing strategies

All notes are **atomic for LLM context** - they provide complete, usable knowledge when attached to an AI prompt independently.

## Why Everything Is Flat

All 98 notes live in the repository root. No folders, no hierarchy.

**Why?**
- A note can connect to ANY other note (folders create silos)
- Tags provide multi-dimensional organization (better than folders)
- MOC notes create structure without boundaries
- "Is MCP a Python topic or an agents topic?" → BOTH (tags: `#python #mcp #agents`)

**Organization through:**
- **Links** - Wikilinks to related concepts
- **Tags** - Multi-dimensional classification (`#python #mcp #agents #guide`)
- **MOCs** - Navigation hubs for domains
- **Relationships** - Typed connections (prerequisites, extends, related, etc.)

This lets me find notes by:
- Domain (via MOCs)
- Technology (via tags)
- Relationship type (via Related Concepts sections)
- Content (via search)

## How Relationships Work

Relationships between notes are maintained in markdown "Related Concepts" sections using typed links:

```markdown
## Related Concepts

### Prerequisites
- [[mcp_overview]] - Need to understand protocol first

### Extends
- [[mcp_implementation]] - Python-specific implementation

### Related Topics
- [[agents]] - Agents use MCP for tool integration
```

Six relationship types:
- **Prerequisites** - Must understand first
- **Extends** - Builds upon this concept
- **Extended By** - Others build upon this (inverse of extends)
- **Related Concepts** - Connected ideas at same level
- **Alternatives** - Different approaches
- **Examples** - Concrete implementations

All relationships are **bidirectional** - if A extends B, then B has "extended_by: A".

### Markdown-First Architecture

**The graph lives entirely in markdown files** - no separate JSON, no Python scripts, no hidden state.

**How it works:**
- **Wikilinks** in content → implicit relationships
- **YAML frontmatter** → metadata (tags, title)
- **"Related Concepts" sections** → explicit typed relationships with "why" explanations
- **MOC files** → thematic organization

Claude parses markdown on-demand during sessions, builds an in-memory graph, and operates directly on markdown files using built-in tools (Read, Edit, Grep, Glob).

See [[claude_plugin_azkg]] for the full architecture.

### Relationship Types

Six types of semantic relationships in "Related Concepts" sections:

1. **Prerequisites** - Concepts you must understand first
   - Example: `[[type_theory]]` is a prerequisite for `[[dhcg]]`

2. **Related Concepts** - Connected ideas at the same conceptual level
   - Example: `[[agents]]` relates to `[[semantic_routing]]` because routing enables task delegation

3. **Extends** - This note builds upon another concept
   - Example: `[[agent_mcp_apis]]` extends `[[mcp_overview]]`

4. **Extended By** - Other notes that build upon this concept (inverse of extends)
   - Example: `[[agents]]` is extended by `[[react_agent_pattern]]`

5. **Alternatives** - Different approaches to the same problem
   - Example: `[[marker]]` is an alternative to `[[firecrawl]]` for content conversion

6. **Examples** - Concrete implementations of abstract concepts
   - Example: `[[alita]]` is an example implementation of `[[agents]]`

### How Relationships Are Maintained

**Direct markdown editing** - All relationships live in "Related Concepts" sections:

```markdown
## Related Concepts

### Prerequisites
- [[type_theory]] - Builds on homotopy type theory foundations

### Related Topics
- [[agents]] - Proposes better representations for agent reasoning

### Extends
- [[category_theory]] - Uses categorical structures for semantic meaning
```

**Bidirectional consistency** - When Claude adds a relationship, it updates both notes:
- If A extends B → Claude adds A to "Related Concepts" in A, AND adds A to "Extended By" in B
- No sync needed - the edits ARE the graph

**How Claude discovers relationships:**
1. **Content analysis** - Semantic analysis of note content
2. **Tag analysis** - Notes with similar tags are often related
3. **Wikilink analysis** - Existing links suggest relationship types
4. **Perplexity research** - Query for domain connections
5. **Confidence scoring** - High/medium/low evidence for each suggestion

**Benefits of markdown-first:**
- ✅ **Single source of truth** - Markdown only, no JSON duplication
- ✅ **No sync overhead** - Relationships ARE the markdown edits
- ✅ **Obsidian-native** - Perfect compatibility, no hidden state
- ✅ **Git-friendly** - Better merge handling with separate files
- ✅ **Transparent** - See exactly what changed in git diff
- ✅ **Parallel updates** - Claude can edit multiple files simultaneously
- ✅ **LLM-friendly** - Claude parses markdown directly (Read/Grep tools)

The knowledge graph is a **living network** that both humans (via Obsidian) and AI agents (via Claude Code) can navigate and maintain.

## How to Work With This Repository

### Finding Context for a Task

**Method 1: Read "Related Concepts" sections**
- Open any note and scroll to "Related Concepts" section
- Follow prerequisite chains to understand dependencies
- Explore "Extended By" to find advanced topics
- Check "Related Topics" for connected ideas

**Method 2: Start with MOC notes**
- Look for `*_moc.md` files (e.g., `agents_moc.md`, `mcp_moc.md`)
- Follow links to relevant notes
- Compose the contexts you need

**Method 3: Use Obsidian search/graph**
- Search by topic or tag
- Explore the graph view to find connections
- Use backlinks to discover related concepts

**Method 4: Tag-based discovery**
- Every note has tags like `#python #mcp #agents`
- Search by tag combinations to find cross-cutting concepts
- See [[tag_system]] for the complete tag catalog and strategy

**Method 5: Ask Claude**
- `/graph-note [filename]` - Show all relationships for a note
- `/search-notes [query]` - Semantic search across all notes
- `/learning-path [target]` - Generate prerequisite learning sequence

### Creating New Notes

**Before Creating:**
1. Search: Does this note already exist?
2. Atomicity: Is this one complete, usable idea?
3. Links: What existing notes does this connect to?

**Note Structure:**
```markdown
---
tags: [python, mcp, api]
---

# Note Title

Brief one-line summary of what this note contains.

## Main Content

The complete, self-contained idea or reference.

## Related Concepts

Links to connected notes:
- [[related_note_1]] - why it connects
- [[related_note_2]] - why it connects

## References

External sources if applicable.
```

**Naming Convention:**
- `topic_specific_concept.md` - lowercase with underscores
- Descriptive: `python_mcp_sdk.md` not `sdk.md`
- No folders in name: `mcp_protocol.md` not `agents_mcp_protocol.md`

### Evolving the Repository

**Add a new concept:**
1. Create atomic note
2. Add relevant tags
3. Link from related notes
4. Add to appropriate MOC

**Refactor existing content:**
1. If a note covers multiple concepts, consider splitting
2. If concepts are duplicated, consolidate and link
3. Update MOCs when structure changes
4. Let connections emerge naturally

**Quality checks:**
- Can an LLM use this note independently?
- Is it focused on one topic/task?
- Are links meaningful (not just "related")?
- Do tags accurately describe cross-cutting themes?
## Organization Principles

- **Minimal folders**: Flat structure preferred, folders only for broad functional separation if needed
- **Descriptive filenames**: `python_mcp_sdk.md`, `rust_best_practices.md`
- **Rich tagging**: Multi-dimensional tags enable discovery across hierarchies
- **MOC notes**: Hub documents that link related contexts (e.g., `Python_MOC.md`)
- **Meaningful links**: Explain WHY notes connect, not just that they do
- **Living system**: The network grows and adapts continuously

### Tag Strategy

Tags are the primary organizational mechanism in this repository. A well-designed tag system enables multi-dimensional discovery that folders cannot provide.

**Tag Dimensions:**

1. **Technology/Language** - The primary implementation language (`#python`, `#rust`, `#typescript`)
2. **Framework/Tool** - Specific tools and libraries (`#react`, `#mcp`, `#obsidian`)
3. **Domain/Discipline** - What the note is about (`#agents`, `#llm`, `#writing`, `#math`)
4. **Content Type** - How to use the note (`#api`, `#guide`, `#pattern`, `#reference`)
5. **Cross-cutting Themes** - Concepts that span multiple domains (`#async`, `#optimization`, `#security`)
6. **Method/Thinking** - Cognitive tools and approaches (`#first-principles`, `#systems-thinking`)

**Tagging Principles:**

- **3-6 tags per note** - Enough for discovery without dilution
- **Mix dimensions** - Combine technology + domain + content type for rich discovery
- **Lowercase with hyphens** - `#first-principles` not `#FirstPrinciples`
- **Specific over generic** - `#mcp` better than `#protocol`
- **Enable serendipity** - Tags reveal unexpected connections across domains
- **Evolve organically** - Add new tags as new domains emerge

**Tag Discovery:**

The power of multi-dimensional tagging:
- `#mcp` finds all MCP-related notes across Python, C#, TypeScript, and protocol specs
- `#python AND #llm` finds specifically Python LLM integration contexts
- `#pattern` reveals patterns across Rust, React, agents, and writing strategies
- `#api` surfaces all API references regardless of language

See [[tag_system]] for the complete, maintained catalog of tags with descriptions and usage guidelines.

## The Agentic Advantage

This system is **Obsidian-compatible** but **agent-enhanced**:

**You can use Obsidian** for:
- Visual graph exploration
- Manual note browsing
- Quick edits and reading
- Human-friendly navigation

**The agent handles** for you:
- Automated note creation with research (Write, Edit tools)
- Relationship discovery across the entire graph (Grep, Read, Edit tools)
- Maintaining graph integrity and bidirectionality (Read, Edit tools)
- Bulk operations (renames, conformance, validation) (Grep, Edit, Bash tools)
- Research and updates via Perplexity integration (mcp__perplexity-ask)
- Direct markdown editing - no Python scripts, no JSON synchronization

**Best of both worlds:** Human intuition + visual exploration (Obsidian) meets automated maintenance + intelligent operations (Agent).

## Agentic Operations

**Commands provided by the installed AZKG plugin** (`azkg@witt3rd`):

**Creation & Discovery:**
- `/create-note [topic]` - Research via Perplexity, create note, discover relationships
- `/expand-graph [note]` - Multi-strategy relationship discovery with confidence scoring
- `/search-notes [query]` - Semantic search across all notes
- `/learning-path [target]` - Generate prerequisite learning sequence

**Maintenance & Quality:**
- `/conform-note [file]` - Restructure notes to standard format
- `/rename-note [old] [new]` - Rename file + update all wikilinks

**Graph Operations:**
- `/graph-validate` - Check wikilinks, bidirectionality, YAML frontmatter
- `/graph-stats` - Count notes, relationships, tags
- `/graph-note [file]` - Show relationships and backlinks
- `/graph-moc [name]` - View MOC (Map of Content) files

**Research & Updates:**
- `/refresh-topic [file]` - Query Perplexity, update note with latest info

**All operations use Claude's built-in tools** - no Python scripts, no JSON files. Markdown is the graph.

See the [AZKG plugin repository](https://github.com/witt3rd/claude-plugins/tree/main/plugins/azkg) for complete command documentation.

## What This Is NOT

- ❌ Traditional hierarchical documentation
- ❌ A dump of external docs
- ❌ A GUI-based note-taking app (that's Obsidian)
- ❌ Static reference material
- ❌ Manually maintained

## What THIS Knowledge Base IS

- ✅ My **second brain** that maintains itself
- ✅ An implementation of the [[agentic_zkg]] paradigm
- ✅ 98+ atomic notes optimized for AI agent consumption
- ✅ A **living system** that evolves through conversation with Claude
- ✅ Obsidian-compatible but agent-enhanced
- ✅ Knowledge that explains itself through typed relationships

**The innovation:** This isn't documentation *about* AI. It's a knowledge base *for* AI - designed to be consumed by language models as context, maintained by an agent through conversation, and navigable by both humans and AI.

Want to understand how this works? See [[agentic_zkg]] (the concept) and [[claude_plugin_azkg]] (the implementation).
