# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **knowledge graph repository** designed for LLM context management, not a traditional code project. It contains 93+ interconnected markdown notes implementing a Zettelkasten system optimized for AI agents.

**Core principle**: This is a knowledge base *for* LLMs, not documentation *about* LLMs. Notes are atomic, composable contexts designed to be fed to language models for specific tasks.

## Repository Architecture

### Knowledge Graph System

The repository maintains an automated, bidirectional knowledge graph in `knowledge_graph_full.json`:

**Structure**:
- **Metadata**: Version (16.0), total notes (93), completion status
- **Batches**: Notes organized into 12 thematic batches (Core AI/Agents, MCP Protocol, Python Stack, etc.)
- **Typed relationships**: Six relationship types for each note
- **Bidirectional mappings**: All relationships are inverse-mapped

**Relationship Types**:
1. **prerequisites** - Must understand first
2. **related_concepts** - Connected ideas at same level
3. **extends** - Builds upon another concept
4. **extended_by** - Others build upon this (inverse)
5. **alternatives** - Different approaches to same problem
6. **examples** - Concrete implementations

**Graph Construction Algorithm**:
- **Forward pass** (batched): Discovers outbound relationships from each note
- **Backward pass**: Establishes inverse relationships (extends → extended_by)
- **Synchronization**: Writes "Related Concepts" sections to all markdown files

### Note Structure

Every markdown note follows this pattern:

```markdown
---
tags: [domain, technology, content-type]
last_refresh: 2025-10-11  # Optional
---

# Note Title

Brief summary of concept.

## Main Content

Complete, self-contained explanation.

## Related Concepts

### Prerequisites
- [[prerequisite_note]] - Why it's needed first

### Related Topics
- [[related_note]] - Why it connects

### Extends
- [[base_note]] - What this builds upon

### Examples
- [[example_note]] - Concrete implementation

## References

External citations if applicable.
```

**Critical rules**:
- Wikilinks use format `[[note]]` NOT `[[note.md]]`
- "Related Concepts" section is auto-generated from knowledge graph
- Tags use lowercase with hyphens: `#first-principles`
- 3-6 tags per note mixing dimensions (technology + domain + content-type)

### Organization Philosophy

**Flat structure**: All notes in repository root (no deep folder hierarchies)
- Organization through links, backlinks, and tags
- MOC (Map of Content) notes act as navigation hubs
- Knowledge forms a flexible network, not a rigid tree
- Any concept can connect to any other concept

**Atomicity for LLMs**: A note is atomic if it provides complete, usable knowledge when attached to an LLM prompt independently.

**Three note types**:
1. **Reference Notes**: Complete documentation (e.g., `python_mcp_sdk.md`)
2. **Concept Notes**: Single focused idea (e.g., `mcp_server_lifecycle.md`)
3. **Synthesis Notes**: MOCs linking related concepts (e.g., `Python_MOC.md`)

## Working with This Repository

### Custom Commands

**`/refresh-topic`** - Refresh a topic page with latest information
- Location: `.claude/commands/refresh-topic.md`
- Usage: `/refresh-topic game_theory.md`
- Process:
  1. Reads topic file
  2. Formulates Perplexity query for recent updates
  3. Incorporates updates into appropriate sections
  4. Updates `last_refresh` in YAML frontmatter
- Uses: `mcp__perplexity-ask__perplexity_ask` tool
- Preserves existing content, citations, and relationship sections

**`/rename-note`** - Rename a note and update all references
- Location: `.claude/commands/rename-note.md`
- Script: `.claude/scripts/rename_note.py`
- Usage: `/rename-note old_filename new_filename`
- Process:
  1. Renames physical markdown file
  2. Updates all references in `knowledge_graph_full.json`
  3. Updates all wikilinks `[[old]]` → `[[new]]` in markdown files
  4. Creates timestamped backup before changes
  5. Validates graph integrity after completion
- Safety: Reverts file rename if knowledge graph update fails
- Use cases: Clarify naming (mcp_sdk → python_mcp_sdk), fix typos, reorganize

### Knowledge Graph Operations

**Reading the graph**:
```python
# Load via Read tool
knowledge_graph_full.json
```

**Graph structure** (JSON):
```json
{
  "metadata": {
    "version": "16.0",
    "total_notes": 93,
    "forward_pass_batches_complete": 12,
    "backward_pass_complete": true
  },
  "batches": [
    {
      "batch_number": 1,
      "name": "Core AI/Agents",
      "notes": ["agents.md", "alita.md", ...]
    }
  ],
  "notes": {
    "agents.md": {
      "relationships": {
        "prerequisites": [],
        "related_concepts": [
          {"note": "semantic_routing.md", "why": "..."}
        ],
        "extends": [],
        "extended_by": [...],
        "alternatives": [],
        "examples": [...]
      }
    }
  }
}
```

**Updating relationships**:
1. Modify relationships in `knowledge_graph_full.json`
2. Ensure bidirectionality (if A extends B, B must have extended_by A)
3. Sync to markdown files (update "Related Concepts" sections)

### Creating New Notes

**Before creating**:
1. Search: Does this concept already exist?
2. Atomicity check: Is this one complete, usable idea?
3. Links: What existing notes does this connect to?

**Naming convention**:
- `topic_specific_concept.md` - lowercase with underscores
- Descriptive: `python_mcp_sdk.md` not `sdk.md`
- No folder prefixes in names

**After creating**:
1. Add YAML frontmatter with 3-6 tags
2. Add to appropriate batch in `knowledge_graph_full.json`
3. Run forward pass to discover relationships
4. Add to relevant MOC notes
5. Increment version in metadata

### Tag System

**Tag dimensions** (see `tag_system.md` for complete catalog):
1. Technology/Language (`#python`, `#rust`, `#typescript`)
2. Framework/Tool (`#react`, `#mcp`, `#obsidian`)
3. Domain/Discipline (`#agents`, `#llm`, `#writing`)
4. Content Type (`#api`, `#guide`, `#pattern`, `#reference`)
5. Cross-cutting Themes (`#async`, `#optimization`)
6. Method/Thinking (`#first-principles`, `#systems-thinking`)

**Discovery patterns**:
- `#mcp` finds all MCP content across languages
- `#python AND #llm` finds Python LLM integrations
- `#pattern` reveals patterns across all domains

### MOC (Map of Content) Notes

Navigation hubs for topic areas:
- `agents_moc.md` - AI agents concepts
- `mcp_moc.md` - Model Context Protocol
- `rust_moc.md` - Rust ecosystem
- `typescript_moc.md` - TypeScript stack
- `windows_moc.md` - Windows development
- `writing_moc.md` - Writing strategies

MOCs contain links and brief context, not content itself.

## Key Files

- **`knowledge_graph_full.json`** - Central graph data structure (source of truth)
- **`README.md`** - Philosophy and usage guide (comprehensive)
- **`tag_system.md`** - Complete tag catalog and guidelines
- **`*_moc.md`** - Navigation hub notes for topic areas

## Critical Constraints

**When working with notes**:
- NEVER modify "Related Concepts" sections manually - they're auto-generated from graph
- ALWAYS use wikilink format `[[note]]` not `[[note.md]]`
- PRESERVE existing content when updating - only add/enhance, rarely remove
- MAINTAIN bidirectionality in knowledge graph relationships
- NO hyperbolic language or marketing claims - demonstrate value, don't claim it

**When updating the knowledge graph**:
- Update metadata version when making structural changes
- Ensure forward and backward passes maintain consistency
- Sync changes to both JSON and markdown files
- Document relationship "why" explanations clearly

## Common Workflows

**Add new topic**:
1. Create `new_topic.md` with proper structure
2. Add to batch in `knowledge_graph_full.json`
3. Discover relationships (forward pass logic)
4. Establish inverse relationships (backward pass)
5. Sync to markdown "Related Concepts" section
6. Update relevant MOC notes

**Refresh existing topic**:
1. Use `/refresh-topic topic_name.md`
2. Review and verify Perplexity updates
3. Update `last_refresh` in YAML

**Rename a note**:
1. Use `/rename-note old_name new_name`
2. Script automatically handles file, graph, and wikilink updates
3. Review changes with git diff
4. Update note title/tags if needed to match new filename

**Explore concept relationships**:
1. Check `knowledge_graph_full.json` for typed relationships
2. Follow prerequisite chains for learning paths
3. Explore extended_by for advanced topics
4. Use alternatives for different approaches

**Find related content**:
1. Check "Related Concepts" section in markdown
2. Query `knowledge_graph_full.json` by relationship type
3. Search by tag combinations
4. Navigate via MOC notes
5. Use Obsidian graph view

## Obsidian Integration

This repository is designed for use with Obsidian:
- Wikilinks `[[note]]` create navigable connections
- Graph view visualizes knowledge network
- Tag search enables multi-dimensional discovery
- Backlinks show inverse relationships
- Daily notes and MOCs provide navigation

The knowledge graph JSON provides LLM-friendly structure, while markdown + Obsidian provides human-friendly navigation.
