# Graph Batch

Display information about a specific batch in the knowledge graph.

## Task

Execute the `query_graph.py batch` command to show:
- Batch number and name
- Total note count
- List of all notes in the batch with titles

## Input

User provides the batch name (e.g., "Core AI/Agents", "MCP Protocol", "Python Stack")

Common batch names:
- Core AI/Agents
- MCP Protocol
- Python Stack
- Rust Stack
- TypeScript Stack
- Windows Platform
- Writing & Strategy
- React/Frontend
- Build Tools
- Development Roles
- Architecture Patterns

## Execution

Use Bash tool to run the query script:

```bash
python .claude/scripts/query_graph.py batch "<batch-name>"
```

## Output Format

The script displays:
```
Batch N: Batch Name
============================================================
Total notes: X

Notes:
  - note1.md: Note Title
  - note2.md: Note Title
  ...
```

## Use Cases

- Review batch contents before adding new note
- Ensure thematic coherence within batch
- Find related notes in same domain
- Verify note is in correct batch
- Understand batch organization

## Present Results

After displaying batch information:
- Assess batch size (small/medium/large)
- Comment on thematic coherence
- Suggest if batch is getting too large (might need splitting)
- Identify potential organization improvements
