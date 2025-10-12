# Graph Stats

Display comprehensive statistics about the knowledge graph.

## Task

Execute the `query_graph.py stats` command to show:
- Total notes and batches
- Relationship counts by type (prerequisites, related_concepts, extends, extended_by, alternatives, examples)
- Unique tag count
- Top 10 most-used tags

## Execution

Use Bash tool to run the query script:

```bash
python .claude/scripts/query_graph.py stats
```

## Output Format

The script displays:
```
Graph Statistics
============================================================
Total notes: N
Total batches: M

Relationship counts:
  prerequisites: X
  related_concepts: X
  extends: X
  extended_by: X
  alternatives: X
  examples: X

Unique tags: N
Top 10 tags:
  tag1: count
  tag2: count
  ...
```

## Use Cases

- Quick overview of graph size and complexity
- Monitor growth over time
- Identify most common tags for consistency
- Understand relationship distribution
- Spot imbalances (e.g., too many related_concepts vs prerequisites)

## Present Results

After displaying the raw statistics, provide a brief analysis:
- Graph size context (e.g., "93 notes across 11 thematic batches")
- Relationship health (balanced distribution vs heavily skewed)
- Tag usage patterns (diversity vs concentration)
- Any notable patterns or recommendations
