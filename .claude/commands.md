# AZKG Command Rationalization

## Current State (2025-10-12)

**13 Commands Implemented:**
1. ✅ /create-note - Research + create with auto-linking
2. ✅ /search-notes - Find notes by keyword/semantic search
3. ✅ /expand-graph - Multi-strategy relationship discovery
4. ✅ /learning-path - Generate prerequisite learning sequence
5. ✅ /conform-note - Restructure to standard format
6. ✅ /rename-note - Rename + update all wikilinks
7. ✅ /refresh-topic - Update note with latest Perplexity info
8. ✅ /graph-validate - Check integrity (wikilinks, bidirectionality)
9. ✅ /graph-stats - Count notes, relationships, tags
10. ✅ /graph-note - View note's relationships & metadata
11. ✅ /graph-moc - View MOC navigation hub (renamed from /graph-batch)
12. ✅ /graph-add-relationship - Manually add typed relationships
13. ✅ /update-note - Update YAML frontmatter metadata

## Rationalization Assessment

### Tier 1: Core Workflows (Essential - Use Daily)
- **Keep:** `/create-note`, `/search-notes`, `/expand-graph`, `/learning-path`, `/graph-note`, `/refresh-topic`
- **Why:** These provide agent-differentiated value - automation you can't easily do manually
- **Usage:** Creating knowledge, finding context, discovering connections, generating learning paths, staying current

### Tier 2: Maintenance (Important - Use Weekly)
- **Keep:** `/conform-note`, `/rename-note`, `/graph-validate`
- **Why:** Essential for quality, but periodic rather than daily
- **Usage:** Cleanup, refactoring, integrity checks

### Tier 3: Analysis (Useful - Use Monthly)
- **Keep:** `/graph-stats`
- **Reconsider:** `/graph-moc` - Do you just `Read` MOC files directly instead?
- **Why:** Informational rather than operational
- **Usage:** Understanding growth, finding patterns

### Tier 4: Granular Operations (Low Value - Rarely Used?)
- **Reconsider:** `/graph-add-relationship` - Isn't `/expand-graph` better for this?
- **Reconsider:** `/update-note` - Why not just use Edit tool directly on YAML?
- **Why:** Too manual, overlaps with better commands
- **Recommendation:** Consider removing if unused

## Missing High-Value Commands

Based on vision docs (agentic_zkg.md, claude_plugin_azkg.md), this is mentioned but NOT implemented:

1. **`/find-gaps`** - Identify missing knowledge areas
   - Would need: Broken wikilink detection + domain coverage analysis
   - Value: Medium - helps identify missing knowledge areas
   - Priority: Lower than maintaining/improving existing commands

## Recommendations

### Immediate Actions:
1. **Update documentation** - `/refresh-topic`, `/search-notes`, `/learning-path` are implemented but not listed in README.md
2. **Remove or justify Tier 4** - Test if you actually use `/graph-add-relationship` and `/update-note`
3. **Command naming is consistent** - All graph commands use `graph-` prefix, core operations don't (good distinction)
4. **✅ Renamed** - `/graph-batch` → `/graph-moc` to match MOC terminology

### Focus on Quality:
- All 13 core commands are implemented
- Focus should be on making these excellent rather than adding more
- Consider removing rarely-used commands to reduce maintenance

### Commands to Consider Removing:
- `/update-note` - Too granular, overlaps with Edit tool
- `/graph-add-relationship` - Overlaps with `/expand-graph` interactive mode
- `/graph-moc` - May overlap with just reading MOC files directly

### Advanced Commands (Defer):
- `/generate-moc`, `/merge-notes`, `/split-note`, `/visualize-graph` are interesting but not essential
- Focus on making the core 11 commands excellent first

---

Your Zettelkasten system has rich potential for automation. Here are high-value commands to consider:

  Core Creation & Expansion

  /create-note [topic] - ✅ IMPLEMENTED - Guided atomic note creation

- Check for duplicate concepts in existing notes (Grep/Glob)
- Research topic via Perplexity
- Generate initial structured content
- Discover relationships to existing notes (auto-expansion!)
- Create markdown file with YAML frontmatter (Write tool)
- Auto-generate 3-6 tags using tag_system.md catalog
- Update relevant MOC files (Edit tool)
- No JSON graph - markdown is the source of truth

  /expand-graph [note.md] - ✅ IMPLEMENTED - Discover missing relationships

- Multi-strategy relationship discovery (content search, tags, wikilinks, Perplexity)
- Confidence scoring (high/medium/low with evidence)
- Classify relationships by type (prerequisites, related, extends, examples, alternatives)
- Interactive review mode with approval workflow
- Update "Related Concepts" sections directly in markdown (Edit tool)
- Ensure bidirectionality (if A extends B, update B's "Extended By" section)
- Comprehensive completion report with statistics

  Note Maintenance

  /conform-note [filename] - ✅ IMPLEMENTED - Restructure note to standard format

- Ensures proper YAML frontmatter structure
- Fixes title and summary sections
- Reorganizes content to match standard structure
- Converts "Citations:" to "## References" heading
- Removes extraneous separators and attribution lines
- Preserves all content and "Related Concepts" section
- Maintains wikilink format `[[note]]`

  /rename-note [old_filename] [new_filename] - ✅ IMPLEMENTED - Rename note and update references

- Renames physical markdown file (Bash mv)
- Finds all files with wikilinks to old name (Grep)
- Updates all wikilinks `[[old]]` → `[[new]]` in markdown files (Edit tool)
- Updates MOC files if needed (Edit tool)
- No JSON graph to update - markdown is the source of truth
- Uses built-in tools (Grep, Edit, Bash) - no Python scripts

  Graph Operations

  /graph-validate - ✅ IMPLEMENTED - Run integrity checks

- Find all wikilinks and verify target files exist (Grep + Glob)
- Check "Related Concepts" bidirectionality (Read + parse)
- Verify YAML frontmatter well-formed (Read + parse)
- Validate relationship consistency (if A extends B, B has "Extended By: A")
- Uses built-in tools (Grep, Glob, Read) - no Python scripts
- Report errors or confirm validity

  /graph-stats - ✅ IMPLEMENTED - Display graph statistics

- Total notes (Glob *.md | count)
- Relationship counts by type (Grep in "Related Concepts" sections)
- Unique tag count and top 10 tags (Grep in YAML frontmatter)
- MOC count (Glob *_moc.md)
- Uses built-in tools (Grep, Glob) - no Python scripts

  /graph-note [filename] - ✅ IMPLEMENTED - Show note details

- Display title, tags, summary from YAML frontmatter (Read tool)
- Complete relationship breakdown from "Related Concepts" section (Read + parse)
- Show backlinks (Grep for wikilinks to this note)
- Uses built-in tools (Read, Grep) - no Python scripts

  /graph-moc [name] - ✅ IMPLEMENTED - View MOC (Map of Content) navigation hub

**Note:** Replaces old "batches" concept - MOCs are thematic navigation hubs

- Read MOC file (e.g., agents_moc.md, mcp_moc.md, python_moc.md)
- Display all sections and wikilinks with descriptions
- Count notes per section and total
- Show MOC organization and coverage
- Suggest gaps or improvements
- Uses Read and Glob tools - no Python scripts

  /graph-add-relationship [source] [target] [type] [why] - ✅ IMPLEMENTED - Add relationships

- Establish typed relationship with explanation
- Update source note's "Related Concepts" section (Edit tool)
- Add bidirectional link in target note (Edit tool)
- Validates both notes exist (Glob)
- Uses built-in tools (Edit, Glob, Read) - no Python scripts

  /update-note [filename] --title|--tags|--summary - ✅ IMPLEMENTED - Update note metadata

- Update note's title, tags, or summary in YAML frontmatter
- Can update one or multiple fields in a single command
- Updates markdown file directly (Edit tool)
- No version tracking needed - markdown is source of truth
- Uses built-in Edit tool - no Python scripts

  /sync-graph - ELIMINATED (not needed)

**Note:** With markdown-first architecture, there is no JSON to sync.
Markdown files ARE the graph. No synchronization needed.

  Discovery & Analysis

  /find-gaps - Identify missing knowledge

- Analyze notes for referenced but non-existent concepts
- Find broken prerequisite chains
- Detect domains with thin coverage (few notes per tag)
- Use Perplexity to research what concepts should exist
- Generate suggested note titles to fill gaps

  /learning-path [target-note.md] - Generate learning sequence

- Trace prerequisite chains back to foundations
- Create ordered learning list
- Optionally generate MOC for the path
- Show estimated "depth" (prerequisite levels)

  /suggest-tags [note.md] - Intelligent tag recommendations

- Analyze note content
- Compare against tag_system.md catalog
- Suggest 3-6 tags across dimensions (tech + domain + type)
- Update YAML frontmatter

  Advanced Workflows

  /research-deep [topic] - Comprehensive research

- Multiple targeted Perplexity queries
- Find academic papers, tools, implementations
- Create new note OR expand existing
- Establish relationships to existing knowledge

  /generate-moc [tag OR domain] - Auto-generate Map of Content

- Collect all notes matching criteria
- Organize into logical sections
- Add brief contextual descriptions
- Link to all relevant notes
- Example: /generate-moc #rust creates comprehensive Rust MOC

  /merge-notes [note1.md] [note2.md] - Combine duplicate concepts

- Identify overlapping content
- Merge into single atomic note
- Update all incoming wikilinks
- Update knowledge graph relationships
- Remove duplicate from JSON

  /split-note [note.md] - Break non-atomic notes

- Detect multiple distinct concepts
- Create separate atomic notes
- Establish relationships between new notes
- Update wikilinks in other notes
- Update knowledge graph

## Implemented Commands Summary (Markdown-First Architecture)

### Core Operations (6 commands)
  ✅ /create-note - Create atomic notes with Perplexity research and auto-linking (Write, Edit, mcp__perplexity-ask)
  ✅ /search-notes - Find notes by keyword/semantic search (Grep, Read tools)
  ✅ /expand-graph - Auto-discover missing relationships with multi-strategy analysis (Edit, Grep, Read, mcp__perplexity-ask)
  ✅ /learning-path - Generate prerequisite learning sequence (Read, Grep tools)
  ✅ /graph-note - Inspect note details and relationships (Read, Grep tools)
  ✅ /refresh-topic - Update note with latest Perplexity info (mcp__perplexity-ask, Edit tools)

### Maintenance Operations (3 commands)
  ✅ /conform-note - Restructure note to standard format (Edit tool)
  ✅ /rename-note - Rename note and update all references throughout knowledge base (Grep, Edit, Bash)
  ✅ /graph-validate - Check graph integrity (Grep, Glob, Read tools)

### Analysis Operations (2 commands)
  ✅ /graph-stats - View graph statistics (Grep, Glob tools)
  ✅ /graph-moc - View MOC (Map of Content) navigation hubs (Read, Glob tools)

### Granular Operations (2 commands - consider removing)
  ✅ /graph-add-relationship - Manually add typed relationships (Edit, Read tools)
  ✅ /update-note - Update note metadata in YAML frontmatter (Edit tool)

  **All commands use Claude's built-in tools - NO Python scripts required**
  **Total: 13 commands implemented**

## Potential Future Commands (Lower Priority)

  1. /find-gaps - Identify missing knowledge areas (Grep for broken wikilinks, analyze tags)
  2. /generate-moc - Auto-generate Maps of Content by tag/domain (Grep, Read, Write tools)
  3. /visualize-graph - Generate graph visualization from markdown (Grep relationships, output DOT/Mermaid)
  4. /merge-notes - Combine duplicate concepts into atomic notes
  5. /split-note - Break non-atomic notes into focused concepts

**Recommendation:** Focus on improving existing 13 commands rather than adding more
