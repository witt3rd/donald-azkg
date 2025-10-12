Your Zettelkasten system has rich potential for automation. Here are high-value commands to consider:

  Core Creation & Expansion

  /create-note [topic] - ✅ IMPLEMENTED - Guided atomic note creation

- Check for duplicate concepts in existing notes
- Research topic via Perplexity
- Generate initial structured content
- Discover relationships to existing notes (auto-expansion!)
- Add to appropriate batch via `.claude/scripts/add_note.py`
- Auto-generate 3-6 tags using tag_system.md catalog
- Update relevant MOC files
- Auto-validates graph integrity after creation using `/graph-validate`

  /expand-graph [note.md] - ✅ IMPLEMENTED - Discover missing relationships

- Multi-strategy relationship discovery (content search, tags, wikilinks, Perplexity)
- Confidence scoring (high/medium/low with evidence)
- Classify relationships by type (prerequisites, related, extends, examples, alternatives)
- Interactive review mode with approval workflow
- Update knowledge_graph_full.json bidirectionally
- Sync to "Related Concepts" sections
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

- Renames physical markdown file
- Updates all references in knowledge_graph_full.json
- Updates all wikilinks `[[old]]` → `[[new]]` in markdown files
- Creates backup before making changes
- Validates graph integrity after completion
- Uses `.claude/scripts/rename_note.py`
- Reverts on failure

  Graph Operations

  /graph-validate - ✅ IMPLEMENTED - Run integrity checks

- Verify metadata counts match actual counts
- Check all batch references point to existing notes
- Validate all relationship targets exist
- Check bidirectionality consistency (extends ↔ extended_by)
- Uses `.claude/scripts/validate_graph.py`
- Exit code 0 (valid) or 1 (errors)

  /graph-stats - ✅ IMPLEMENTED - Display graph statistics

- Total notes and batches
- Relationship counts by type
- Unique tag count and top 10 tags
- Uses `.claude/scripts/query_graph.py stats`

  /graph-note [filename] - ✅ IMPLEMENTED - Show note details

- Display title, tags, summary
- Complete relationship breakdown with "why" explanations
- Uses `.claude/scripts/query_graph.py note`

  /graph-batch [name] - ✅ IMPLEMENTED - Show batch contents

- Display batch number, name, note count
- List all notes in batch with titles
- Uses `.claude/scripts/query_graph.py batch`

  /graph-add-relationship [source] [target] [type] [why] - ✅ IMPLEMENTED - Add relationships

- Establish typed relationship with explanation
- Optional bidirectional link (e.g., extends ↔ extended_by)
- Uses `.claude/scripts/add_relationship.py`
- Validates both notes exist and type is valid
- Updates metadata timestamp

  /update-note [filename] --title|--tags|--summary - ✅ IMPLEMENTED - Update note metadata

- Update note's title, tags, or summary in knowledge graph
- Can update one or multiple fields in a single command
- Uses `.claude/scripts/update_note.py`
- Increments version (minor bump: 18.0 → 18.1)
- Does NOT modify markdown file (use /conform-note to sync)

  /sync-graph - Force synchronization

- Rebuild all "Related Concepts" sections from JSON
- Ensure markdown matches knowledge_graph_full.json
- Fix any bidirectionality issues
- Update metadata (version, note count)

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

  Implemented Commands Summary

  ✅ /create-note - Create atomic notes with research and relationship discovery
  ✅ /expand-graph - Auto-discover missing relationships with multi-strategy analysis
  ✅ /conform-note - Restructure note to standard format
  ✅ /rename-note - Rename note and update all references throughout knowledge base
  ✅ /graph-validate - Check graph integrity
  ✅ /graph-stats - View graph statistics
  ✅ /graph-note - Inspect note details and relationships
  ✅ /graph-batch - View batch contents
  ✅ /graph-add-relationship - Manually add relationships
  ✅ /update-note - Update note metadata (title, tags, summary)

  High-Value Next Implementations

  1. /sync-graph - Rebuild "Related Concepts" sections from JSON
  2. /find-gaps - Identify missing knowledge areas
  3. /learning-path - Generate prerequisite learning sequences
  4. /generate-moc - Auto-generate Maps of Content by tag/domain
  5. /search-notes - Search with context across all notes
