# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **knowledge graph repository** designed for LLM context management, not a traditional code project. It contains 93+ interconnected markdown notes implementing a Zettelkasten system optimized for AI agents.

**Core principle**: This is a knowledge base *for* LLMs, not documentation *about* LLMs. Notes are atomic, composable contexts designed to be fed to language models for specific tasks.

## Repository Architecture

### Markdown-First Knowledge Graph

The repository implements a **markdown-first** knowledge graph - the graph lives entirely in markdown files:

**Graph Elements**:
- **Wikilinks** in content → implicit relationships
- **YAML frontmatter** → metadata (tags, title, last_refresh)
- **"Related Concepts" sections** → explicit typed relationships with "why" explanations
- **MOC files** → thematic organization (Core AI/Agents, MCP Protocol, Python Stack, etc.)

**Relationship Types** (in "Related Concepts" sections):
1. **Prerequisites** - Must understand first
2. **Related Topics** - Connected ideas at same level
3. **Extends** - Builds upon another concept
4. **Extended By** - Others build upon this (inverse)
5. **Alternatives** - Different approaches to same problem
6. **Examples** - Concrete implementations

**All relationships are bidirectional** - if A extends B, then B's "Extended By" section includes A

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
- "Related Concepts" sections are the source of truth for relationships
- Tags use lowercase with hyphens: `#first-principles`
- 3-6 tags per note mixing dimensions (technology + domain + content-type)
- No JSON graph file - markdown is the graph

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

#### Telegram Message Processing Workflow

**`/telegram:next-message`** - Get next unprocessed Telegram Saved Message
- Location: `.claude/commands/telegram-next-message.md`
- Usage: `/telegram:next-message`
- State tracking: `.telegram_state.json` tracks last processed message
- Process:
  1. Reads state file to get last processed message
  2. Fetches next message from Saved Messages
  3. Presents message with options: create note, skip, or stop
  4. Updates state after processing
- Uses: `mcp__plugin_telegram_telegram__read_messages`, Read, Write tools
- Interactive: User decides how to handle each message

#### Content Handler Commands (Generic)

**`/scrape-url`** - Scrape URL and create knowledge graph note
- Location: `.claude/commands/scrape-url.md`
- Usage: `/scrape-url <url> [note_filename]`
- Process:
  1. Scrapes URL using Firecrawl
  2. Analyzes content and extracts key concepts
  3. Generates structured note with proper frontmatter
  4. Identifies relationships to existing notes
  5. Adds bidirectional links
- Uses: `mcp__firecrawl__firecrawl_scrape`, Grep, Write, Edit tools
- Generic: Can be used with any URL source (not Telegram-specific)

**`/youtube-transcript`** - Get YouTube transcript and create note
- Location: `.claude/commands/youtube-transcript.md`
- Usage: `/youtube-transcript <youtube_url> [note_filename]`
- Process:
  1. Extracts video metadata and transcript
  2. Summarizes key points and insights
  3. Creates structured note with Key Points section
  4. Links to related concepts
- Uses: `mcp__firecrawl__firecrawl_scrape`, Grep, Write, Edit tools
- Generic: Can be used with any YouTube video (not Telegram-specific)

**`/process-pdf`** - Extract PDF content and create note
- Location: `.claude/commands/process-pdf.md`
- Usage: `/process-pdf <pdf_url_or_path> [note_filename]`
- Process:
  1. Extracts content from PDF (URL or local file)
  2. Analyzes document structure and key concepts
  3. Creates structured note with appropriate sections
  4. Preserves document metadata (title, authors)
- Uses: `mcp__firecrawl__firecrawl_scrape` (URLs), Read (local), Write, Edit tools
- Generic: Can be used with any PDF source (not Telegram-specific)

#### Knowledge Graph Maintenance

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
- Usage: `/rename-note old_filename new_filename`
- Process:
  1. Renames physical markdown file (Bash mv)
  2. Finds all wikilinks to old name (Grep)
  3. Updates all wikilinks `[[old]]` → `[[new]]` in markdown files (Edit tool)
  4. Updates MOC files if needed (Edit tool)
- Uses: Built-in tools (Grep, Edit, Bash) - no Python scripts
- Use cases: Clarify naming (mcp_sdk → python_mcp_sdk), fix typos, reorganize

### Knowledge Graph Operations

**Reading note relationships**:
```bash
# Read a note's relationships (Read tool)
Read agents.md

# The "Related Concepts" section contains all relationships:
## Related Concepts

### Prerequisites
- [[prerequisite_note]] - Why needed first

### Related Topics
- [[related_note]] - Connection explanation

### Extends
- [[base_note]] - What this builds upon
```

**Finding all notes with a specific tag**:
```bash
# Grep for tags in YAML frontmatter
Grep "tags:.*agents" --glob="*.md"
```

**Finding all wikilinks to a note**:
```bash
# Find backlinks
Grep "\[\[note_name\]\]" --glob="*.md"
```

**Updating relationships**:
1. Edit source note's "Related Concepts" section (Edit tool)
2. Ensure bidirectionality (if A extends B, update B's "Extended By" section)
3. No JSON to sync - markdown is the source of truth

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
1. Add YAML frontmatter with 3-6 tags (Write tool includes this)
2. Add "Related Concepts" section with initial relationships (Edit tool)
3. Add to relevant MOC notes (Edit tool)
4. Ensure bidirectional relationships in connected notes (Edit tool)
5. No JSON to update - markdown is the source of truth

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

- **`README.md`** - Philosophy and usage guide (comprehensive)
- **`agentic_zkg.md`** - The paradigm definition (concept level)
- **`claude_plugin_azkg.md`** - Claude Code implementation (implementation level)
- **`tag_system.md`** - Complete tag catalog and guidelines
- **`*_moc.md`** - Navigation hub notes for topic areas (MOCs replace "batches")

## Critical Constraints

**When working with notes**:
- ALWAYS use wikilink format `[[note]]` not `[[note.md]]`
- PRESERVE existing content when updating - only add/enhance, rarely remove
- MAINTAIN bidirectionality when adding relationships (update both notes)
- NO hyperbolic language or marketing claims - demonstrate value, don't claim it
- "Related Concepts" sections can be edited - they ARE the graph

**When updating relationships**:
- Edit "Related Concepts" sections directly in markdown (Edit tool)
- Ensure bidirectionality (if A extends B, update B's "Extended By" section)
- Always include "why" explanations for each relationship
- No JSON to maintain - markdown is the source of truth

## Common Workflows

**Add new topic**:
1. Create `new_topic.md` with proper structure (Write tool)
2. Add "Related Concepts" section with initial relationships (Edit tool)
3. Update bidirectional relationships in connected notes (Edit tool)
4. Add to relevant MOC notes (Edit tool)
5. No JSON to update - markdown is the source of truth

**Process Telegram Saved Messages**:
1. Use `/telegram:next-message` to get next unprocessed message
2. Review message content and decide action:
   - Create note: Identify content type (URL, YouTube, PDF, text)
   - Skip: Move to next message
   - Stop: Exit workflow
3. For note creation, use appropriate handler:
   - `/scrape-url <url>` for web articles
   - `/youtube-transcript <url>` for videos
   - `/process-pdf <url>` for documents
4. State automatically tracks progress in `.telegram_state.json`

**Refresh existing topic**:
1. Use `/refresh-topic topic_name.md`
2. Review and verify Perplexity updates
3. Update `last_refresh` in YAML

**Rename a note**:
1. Use `/rename-note old_name new_name`
2. Command uses Grep + Edit to update all wikilinks
3. Review changes with git diff
4. Update note title/tags if needed to match new filename

**Explore concept relationships**:
1. Read note's "Related Concepts" section (Read tool)
2. Follow prerequisite chains for learning paths
3. Explore "Extended By" for advanced topics
4. Use alternatives for different approaches
5. Use Grep to find backlinks

**Find related content**:
1. Check "Related Concepts" section in markdown (Read tool)
2. Grep for wikilinks and tags (Grep tool)
3. Search by tag combinations (Grep in YAML frontmatter)
4. Navigate via MOC notes (Read MOC files)
5. Use Obsidian graph view

## Obsidian Integration

This repository is designed for use with Obsidian:
- Wikilinks `[[note]]` create navigable connections
- Graph view visualizes knowledge network
- Tag search enables multi-dimensional discovery
- Backlinks show inverse relationships
- Daily notes and MOCs provide navigation

**Markdown-first architecture** means perfect Obsidian compatibility - no hidden state, no JSON files, everything is visible and editable in Obsidian.
