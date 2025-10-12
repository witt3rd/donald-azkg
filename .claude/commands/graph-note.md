# Graph Note

Display detailed information about a specific note from the knowledge graph.

## Task

Execute the `query_graph.py note` command to show:
- Note filename and title
- All tags
- Summary
- Complete relationship breakdown by type with "why" explanations

## Input

User provides the note filename (e.g., "agents.md" or "llm_self_talk_optimization.md")

## Execution

Use Bash tool to run the query script:

```bash
python .claude/scripts/query_graph.py note "<filename>"
```

## Output Format

The script displays:
```
Note: filename.md
============================================================
Title: Note Title
Tags: tag1, tag2, tag3
Summary: Brief summary of the note

Relationships:
  prerequisites: N
    - note.md: Why this is a prerequisite
    ...
  related_concepts: N
    - note.md: Why this is related
    ...
  extends: N
    - note.md: Why this extends that
    ...
  extended_by: N
    - note.md: Why that extends this
    ...
  alternatives: N
    - note.md: Why this is an alternative
    ...
  examples: N
    - note.md: Why this is an example
    ...
```

## Use Cases

- Understand a note's position in the knowledge graph
- Review all connections before editing
- Verify relationships are correctly established
- Find related notes to explore
- Check bidirectional consistency

## Present Results

After displaying the note information:
- Summarize the note's role (e.g., "foundational concept", "specific implementation", "comparative analysis")
- Highlight key connections
- Suggest exploration paths (e.g., "Prerequisites chain back to...", "Extended by 5 specialized notes...")
