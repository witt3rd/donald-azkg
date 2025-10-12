# Knowledge Graph Scripts

Generic Python scripts for working with knowledge graph JSON files. All scripts are designed to be graph-agnostic and work with any knowledge graph instance following the standard Zettelkasten structure.

**Location:** `.claude/scripts/` - Keeps scripts with Claude Code configuration and hidden by default in Obsidian.

## Core Library

### `graph_lib.py`

Core library module with all graph operations. Import this in custom scripts or use the provided CLI tools.

**Key functions:**
- `load_graph(path)` - Load graph from JSON
- `save_graph(graph, path)` - Save graph to JSON
- `find_note(notes, filename)` - Find note by filename
- `find_batch(batches, name/number)` - Find batch
- `add_note(graph, note_entry)` - Add note to graph
- `add_relationship(graph, source, target, type, why, ...)` - Add relationship
- `establish_bidirectional_relationships(graph)` - Establish all inverse relationships
- `update_metadata(graph, ...)` - Update graph metadata
- `validate_graph(graph)` - Validate graph integrity
- `get_statistics(graph)` - Get graph statistics

## CLI Tools

### `add_note.py`

Add a new note to the knowledge graph.

**Usage:**
```bash
python .claude/scripts/add_note.py <filename> <title> <tags> <summary> <batch_name> [relationships_json]
```

**Example:**
```bash
python .claude/scripts/add_note.py "my_note.md" "My Note Title" "tag1,tag2,tag3" \
    "Brief summary of the note" "Core AI/Agents"
```

**With relationships:**
```bash
python .claude/scripts/add_note.py "my_note.md" "My Note" "tag1,tag2" "Summary" "Core AI/Agents" \
    '{"prerequisites": [{"note": "other.md", "why": "needs this first"}]}'
```

**What it does:**
1. Creates note entry with metadata
2. Adds to specified batch
3. Establishes bidirectional relationships
4. Updates metadata (version, count, timestamp)
5. Saves graph

---

### `add_relationship.py`

Add relationships between existing notes.

**Usage:**
```bash
python .claude/scripts/add_relationship.py <source> <target> <type> <why> [--bidirectional] [--inverse-type TYPE]
```

**Relationship types:**
- `prerequisites` - Must understand first
- `related_concepts` - Connected ideas at same level
- `extends` - Builds upon another concept
- `extended_by` - Others build upon this (inverse)
- `alternatives` - Different approaches
- `examples` - Concrete implementations

**Example:**
```bash
python .claude/scripts/add_relationship.py "note_a.md" "note_b.md" "extends" \
    "Builds upon concept B"
```

**Bidirectional example:**
```bash
python .claude/scripts/add_relationship.py "note_a.md" "note_b.md" "extends" \
    "Builds upon B" --bidirectional --inverse-type "extended_by"
```

---

### `query_graph.py`

Query and inspect the knowledge graph.

**Usage:**
```bash
python .claude/scripts/query_graph.py <command> [args]
```

**Commands:**

**Show statistics:**
```bash
python .claude/scripts/query_graph.py stats
```
Displays:
- Total notes and batches
- Relationship counts by type
- Tag distribution
- Top 10 tags

**Show note details:**
```bash
python .claude/scripts/query_graph.py note "agents.md"
```
Displays:
- Title, tags, summary
- All relationships with explanations

**Show batch contents:**
```bash
python .claude/scripts/query_graph.py batch "Core AI/Agents"
```
Displays:
- Batch number and name
- All notes in batch

**Show metadata:**
```bash
python .claude/scripts/query_graph.py metadata
```
Displays all metadata fields

**Validate graph:**
```bash
python .claude/scripts/query_graph.py validate
```
Runs validation checks

---

### `validate_graph.py`

Validate knowledge graph integrity (convenience wrapper).

**Usage:**
```bash
python .claude/scripts/validate_graph.py
```

**Checks performed:**
- Metadata counts match actual counts
- All batch references point to existing notes
- All relationship targets exist
- Bidirectional relationships are consistent (extends ↔ extended_by)

**Exit codes:**
- `0` - Graph is valid
- `1` - Graph has errors

---

## Using in Commands

The `/create-note` command and other graph-updating commands use these scripts instead of creating one-off Python code.

**Example usage in command:**
```python
import subprocess
import json

# Prepare relationships
relationships = {
    "prerequisites": [{"note": "other.md", "why": "reason"}],
    "related_concepts": [{"note": "related.md", "why": "reason"}]
}

# Call add_note.py (from repository root)
result = subprocess.run([
    "python", ".claude/scripts/add_note.py",
    "new_note.md",
    "New Note Title",
    "tag1,tag2,tag3",
    "Brief summary",
    "Core AI/Agents",
    json.dumps(relationships)
], capture_output=True, text=True)

print(result.stdout)
```

**Note:** All scripts automatically resolve the path to `knowledge_graph_full.json` in the repository root, regardless of where they're called from.

---

## Graph Structure

The scripts expect knowledge graph JSON with this structure:

```json
{
  "metadata": {
    "version": "X.0",
    "total_notes": N,
    "forward_pass_batches_complete": M,
    "backward_pass_complete": true,
    "last_updated": "YYYY-MM-DD"
  },
  "batches": [
    {
      "batch_number": 1,
      "name": "Batch Name",
      "notes": ["note1.md", "note2.md"]
    }
  ],
  "notes": [
    {
      "filename": "note.md",
      "title": "Note Title",
      "tags": ["tag1", "tag2"],
      "summary": "Brief summary",
      "relationships": {
        "prerequisites": [{"note": "other.md", "why": "reason"}],
        "related_concepts": [],
        "extends": [],
        "extended_by": [],
        "alternatives": [],
        "examples": []
      }
    }
  ]
}
```

---

## Error Handling

All scripts provide clear error messages and appropriate exit codes:
- `0` - Success
- `1` - Error (validation failure, note not found, etc.)

Use these exit codes in commands to handle errors appropriately.

---

## Future Enhancements

Potential additions:
- `sync_to_markdown.py` - Sync "Related Concepts" sections from JSON to markdown files
- `remove_note.py` - Remove note and clean up all references
- `batch_operations.py` - Batch add/update multiple notes
- `export_subgraph.py` - Export subset of graph for specific topic
- `merge_graphs.py` - Merge two knowledge graphs

---

## Development

To add new functionality:
1. Add core function to `graph_lib.py`
2. Write comprehensive docstring
3. Create CLI wrapper if needed
4. Update this README
5. Test thoroughly with validation

**Testing pattern:**
```bash
# Make changes
python .claude/scripts/add_note.py ...

# Validate
python .claude/scripts/validate_graph.py

# Inspect
python .claude/scripts/query_graph.py stats
```
