---
description: Update a note's metadata in the knowledge graph
---

# Update Note Metadata

Update the metadata (title, tags, summary) for an existing note in the knowledge graph.

## Usage

Use the `update_note.py` script to modify note metadata:

```bash
python .claude/scripts/update_note.py <filename> [options]
```

## Options

- `--title TITLE` - Update the note's title
- `--tags TAG1,TAG2,...` - Update the note's tags (comma-separated)
- `--summary SUMMARY` - Update the note's summary

You can specify one or more options in a single command.

## Examples

**Update title only:**
```bash
python .claude/scripts/update_note.py "agents.md" \
    --title "AI Agents: Autonomous Intelligence Systems"
```

**Update tags only:**
```bash
python .claude/scripts/update_note.py "agents.md" \
    --tags "ai,agents,llm,architecture,autonomous-systems"
```

**Update summary only:**
```bash
python .claude/scripts/update_note.py "agents.md" \
    --summary "Autonomous AI entities capable of goal-directed action"
```

**Update multiple fields:**
```bash
python .claude/scripts/update_note.py "my_note.md" \
    --title "New Title" \
    --tags "tag1,tag2,tag3" \
    --summary "New summary"
```

## What It Does

1. Loads the knowledge graph
2. Finds the specified note
3. Updates the requested metadata fields
4. Increments the version number (minor version bump: 18.0 → 18.1)
5. Updates the graph's last_updated timestamp
6. Saves the updated graph
7. Displays before/after values for changed fields

## Notes

- This command only updates metadata in the knowledge graph JSON file
- It does NOT modify the markdown file itself
- Use this when you need to correct or update note metadata without changing relationships
- For relationship changes, use `/graph-add-relationship` command
- Always run `/graph-validate` after making changes to ensure integrity

## Related Commands

- `/create-note` - Create a new note
- `/graph-note` - View note information
- `/graph-add-relationship` - Add/modify relationships
- `/graph-validate` - Validate graph integrity
- `/conform-note` - Sync markdown file with graph data
