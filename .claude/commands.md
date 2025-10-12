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

  /graph-batch [name] - REFACTORED to /graph-moc

**Note:** "Batches" are now MOC (Map of Content) files

- Read MOC file (e.g., agents_moc.md)
- Display all wikilinks and their context
- Count notes in MOC
- Uses Read tool - no Python scripts

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

  Implemented Commands Summary (Markdown-First Architecture)

  ✅ /create-note - Create atomic notes with research and relationship discovery (Write, Edit tools)
  ✅ /expand-graph - Auto-discover missing relationships with multi-strategy analysis (Edit, Grep, Read tools)
  ✅ /conform-note - Restructure note to standard format (Edit tool)
  ✅ /rename-note - Rename note and update all references throughout knowledge base (Grep, Edit, Bash)
  ✅ /graph-validate - Check graph integrity (Grep, Glob, Read tools)
  ✅ /graph-stats - View graph statistics (Grep, Glob tools)
  ✅ /graph-note - Inspect note details and relationships (Read, Grep tools)
  ✅ /graph-moc - View MOC (Map of Content) files (Read tool)
  ✅ /graph-add-relationship - Manually add relationships (Edit, Read tools)
  ✅ /update-note - Update note metadata (Edit tool)

  **All commands use Claude's built-in tools - NO Python scripts required**

  High-Value Next Implementations

  1. /find-gaps - Identify missing knowledge areas (Grep for broken wikilinks, analyze tags)
  2. /learning-path - Generate prerequisite learning sequences (Read + parse "Prerequisites" sections)
  3. /generate-moc - Auto-generate Maps of Content by tag/domain (Grep, Read, Write tools)
  4. /search-notes - Semantic search with context across all notes (Grep, Read tools)
  5. /visualize-graph - Generate graph visualization from markdown (Grep relationships, output DOT/Mermaid)
