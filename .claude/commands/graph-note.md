# Graph Note

Show detailed information about a specific note, including all relationships and backlinks.

## Task

Display:
- Note title, tags, and summary (from YAML frontmatter and heading)
- All relationships from "Related Concepts" section
- Backlinks (other notes that reference this note)

## Input

User provides filename: `/graph-note agents.md` or `/graph-note agents`

## Execution Steps

### 1. Normalize Filename

Ensure filename has `.md` extension.

### 2. Verify Note Exists

Use Glob to check if note exists:
```bash
Glob "agents.md"
```

If not found, report error.

### 3. Read Note Content

Use Read tool to get full note content.

### 4. Extract Metadata

From the note content:
- **Title**: First `# Heading` after YAML frontmatter
- **Tags**: From `tags:` field in YAML frontmatter
- **Summary**: First paragraph after title (before `##` sections)

### 5. Parse "Related Concepts" Section

From note content, extract all relationships:
- Prerequisites
- Related Topics
- Extends
- Extended By
- Alternatives
- Examples

For each relationship, capture the target note and "why" explanation.

### 6. Find Backlinks

Use Grep to find all notes that reference this note:
```bash
# Find all wikilinks to this note
Grep "\[\[agents\]\]" --glob="*.md" --output_mode="files_with_matches"
```

Count and list the files that link to this note.

## Output Format

```
Note: agents.md
============================================================

## Metadata
Title: AI Agents
Tags: #agents, #ai, #llm, #architecture
Summary: AI agents are autonomous systems powered by LLMs that can perceive,
decide, and act to achieve goals.

## Relationships (Total: 8)

### Prerequisites (0)
(None)

### Related Topics (3)
- [[semantic_routing]] - Enables intelligent model selection for agent tasks
- [[llm_self_talk_optimization]] - Token-efficient communication between agents
- [[react_agent_pattern]] - UI pattern for building agent interfaces

### Extends (0)
(None)

### Extended By (2)
- [[claude_code]] - Implements agentic coding assistant
- [[alita]] - Example implementation of AI agent system

### Alternatives (0)
(None)

### Examples (3)
- [[alita]] - Production AI agent implementation
- [[claude_code]] - Agentic coding assistant
- [[another_example]] - Another implementation

## Backlinks (12 notes reference this)

Files that link to [[agents]]:
- semantic_routing.md
- react_agent_pattern.md
- mcp_overview.md
- claude_code.md
- agents_moc.md
- ...

============================================================
💡 Next Steps:
• Use `/expand-graph agents.md` to discover more relationships
• Review backlinks to understand how this note is used
• Check if "Extended By" relationships should be in "Examples" instead
```

## Use Cases

- **Understand connections**: See how a note fits into the knowledge graph
- **Find usage**: See where a concept is referenced (backlinks)
- **Verify relationships**: Check if relationships are accurate and complete
- **Discover gaps**: Find missing prerequisite or extension relationships

## Tools Used

- **Glob** - Verify note exists
- **Read** - Get full note content
- **Grep** - Find backlinks (wikilinks to this note)
- **Parse logic** - Extract YAML, title, summary, relationships

## Present Results

- Show clear breakdown of relationship types
- Highlight if note has no prerequisites (might be foundational)
- Highlight if note has many Extended By (indicates it's a base concept)
- Show backlink count to indicate note importance/usage
- Suggest using `/expand-graph` if relationship count seems low
