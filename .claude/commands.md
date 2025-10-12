Your Zettelkasten system has rich potential for automation. Here are high-value commands to consider:

  Core Creation & Expansion

  /create-note [topic] - Guided atomic note creation

- Check for duplicate concepts in existing notes
- Research topic via Perplexity
- Generate initial structured content
- Discover relationships to existing notes (auto-expansion!)
- Add to appropriate batch in knowledge_graph_full.json
- Auto-generate 3-6 tags using tag_system.md catalog
- Update relevant MOC files

  /expand-graph [note.md] - Discover missing relationships

- Analyze note content for implicit connections
- Search existing notes for unlinked related concepts
- Research (Perplexity) to discover prerequisite chains
- Suggest new typed relationships with "why" explanations
- Update knowledge_graph_full.json bidirectionally
- Sync to "Related Concepts" sections

  /link-notes [note1.md] [note2.md] [relationship-type] - Manual relationship creation

- Prompt for "why" explanation
- Establish bidirectional link (e.g., extends ↔ extended_by)
- Update JSON and both markdown files
- Validate relationship makes semantic sense

  Graph Integrity

  /validate-graph - Comprehensive integrity check

- Verify all wikilinks point to existing files
- Check bidirectionality consistency
- Detect orphaned notes (no incoming/outgoing links)
- Find circular dependencies in prerequisite chains
- Report notes in JSON but missing as files
- Validate relationship types are valid

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

  My Top 5 Recommendations

  1. /create-note - Most frequent operation, high automation value
  2. /expand-graph - Your exact use case, combines research + relationship discovery
  3. /validate-graph - Essential for maintaining graph integrity
  4. /find-gaps - Proactive knowledge discovery
  5. /learning-path - High user value, showcases graph power

  Want me to implement any of these? I'd suggest starting with /create-note and /expand-graph since they directly support your research and creation workflow.
