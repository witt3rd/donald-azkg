# Graph Stats

Display comprehensive statistics about the knowledge graph.

## Task

Use Grep and Glob to calculate:
- Total notes count
- Total MOC files count
- Relationship counts by type
- Unique tag count and top 10 tags
- Notes per MOC

## Execution Steps

### 1. Count Total Notes

Use Glob to count all markdown files (excluding MOCs):
```bash
# Count all .md files
Glob "*.md"
```

Filter out MOC files (files ending in `_moc.md`) for pure note count.

### 2. Count MOC Files

Use Glob to find MOC files:
```bash
# Find all MOC files
Glob "*_moc.md"
```

### 3. Count Relationships by Type

Use Grep to find each relationship type in "Related Concepts" sections:

```bash
# Count Prerequisites
Grep "### Prerequisites" --glob="*.md" --output_mode="count"

# Count Related Topics
Grep "### Related Topics" --glob="*.md" --output_mode="count"

# Count Extends
Grep "### Extends" --glob="*.md" --output_mode="count"

# Count Extended By
Grep "### Extended By" --glob="*.md" --output_mode="count"

# Count Alternatives
Grep "### Alternatives" --glob="*.md" --output_mode="count"

# Count Examples
Grep "### Examples" --glob="*.md" --output_mode="count"
```

For each type, also count individual relationship entries by counting lines starting with `- [[` within those sections.

### 4. Extract and Count Tags

Use Grep to find all tags in YAML frontmatter:
```bash
# Find all tags lines
Grep "^tags: \[" --glob="*.md" --output_mode="content"
```

Parse out individual tags, count occurrences, and sort by frequency.

### 5. Calculate Additional Metrics

- Average tags per note
- Average relationships per note
- Notes without "Related Concepts" section (orphaned)
- Most connected notes (top 5 by relationship count)

## Output Format

```
Graph Statistics
============================================================
Total notes: N
Total MOCs: M
Pure notes (excluding MOCs): X

Relationship counts:
  Prerequisites: X notes have prerequisites (Y total relationships)
  Related Topics: X notes have related topics (Y total relationships)
  Extends: X notes extend others (Y total relationships)
  Extended By: X notes are extended by others (Y total relationships)
  Alternatives: X notes have alternatives (Y total relationships)
  Examples: X notes have examples (Y total relationships)

Total relationships: Z

Tag Statistics:
  Unique tags: N
  Average tags per note: X.Y

Top 10 tags:
  #python: 25 notes
  #mcp: 18 notes
  #agents: 15 notes
  #rust: 12 notes
  #typescript: 10 notes
  ...

Graph Health:
  ✓ Well-connected notes: X (>3 relationships)
  ! Sparsely connected: Y (1-2 relationships)
  ⚠ Orphaned notes: Z (0 relationships)
```

## Analysis and Insights

After displaying stats, provide brief analysis:

**Good signs:**
- Balanced relationship distribution (no single type dominates)
- High average tags per note (3-6 ideal)
- Few orphaned notes (<5%)
- Diverse tag usage (no extreme tag concentration)

**Potential issues:**
- Many orphaned notes → Use `/expand-graph` to discover relationships
- Imbalanced relationships → Consider adding missing relationship types
- Tag concentration → Some notes may need more specific tags
- Low relationship count → Graph may not be well-connected

## Use Cases

- **Growth tracking**: Monitor note and relationship count over time
- **Health check**: Identify orphaned or poorly connected notes
- **Tag consistency**: Find most-used tags for standardization
- **Balance analysis**: Ensure relationship types are balanced
- **Discover trends**: See which domains are growing fastest

## Tools Used

- **Glob** - Count files (notes, MOCs)
- **Grep** - Find relationship sections, count relationships, extract tags
- **Parse logic** - Extract tags from YAML, calculate statistics, sort and rank

## Present Results

After displaying stats:
- Highlight any concerning metrics (too many orphaned notes, imbalanced relationships)
- Suggest actions (use `/expand-graph` on orphaned notes, add missing relationship types)
- Celebrate growth (if note count is increasing, congratulate user on knowledge expansion)
