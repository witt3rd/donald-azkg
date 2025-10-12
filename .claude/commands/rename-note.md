# Rename Note Command

Rename a note file and update all references throughout the knowledge base.

## Task

Execute the `rename_note.py` script to:
1. Rename the physical markdown file
2. Update all references in `knowledge_graph_full.json`
3. Update all wikilinks `[[old_filename]]` → `[[new_filename]]` in markdown files
4. Create backup before making changes
5. Validate graph integrity after changes

## Input

User provides:
- Old filename (e.g., "mcp_sdk.md" or just "mcp_sdk")
- New filename (e.g., "python_mcp_sdk.md" or just "python_mcp_sdk")

## Execution

Use Bash tool to run the rename script:

```bash
python .claude/scripts/rename_note.py "<old_filename>" "<new_filename>"
```

## Output Format

The script displays:
```
============================================================
Renaming Note: old.md → new.md
============================================================

📦 Creating backup of knowledge graph...
   ✓ Backup created: knowledge_graph_backup_YYYYMMDD_HHMMSS.json

📝 Renaming physical file...
   ✓ Renamed: old.md → new.md

🔗 Updating knowledge graph references...
   ✓ Updated N references in knowledge graph

📄 Updating wikilinks in markdown files...
   ✓ Updated wikilinks in M files:
      - file1.md: X reference(s)
      - file2.md: Y reference(s)
      ...

✅ Validating knowledge graph integrity...
   ✓ Graph validation passed

============================================================
✅ Rename Complete!
============================================================

📋 Summary:
   • File renamed: old.md → new.md
   • Knowledge graph references updated: N
   • Markdown files with wikilink updates: M
   • Backup created: knowledge_graph_backup_YYYYMMDD_HHMMSS.json

💡 Next steps:
   • Review changes with git diff
   • Update any MOC files that reference this note
   • Consider updating note title if needed
```

## Validation

The script performs these checks:
- Old file exists
- New filename not already in use
- All graph references updated correctly
- No broken relationships after rename
- Metadata counts still accurate

## Safety Features

- Creates timestamped backup before making changes
- Reverts file rename if knowledge graph update fails
- Reports any files that couldn't be updated
- Validates graph integrity after completion

## Use Cases

- **Clarify naming**: Rename `mcp_sdk.md` → `python_mcp_sdk.md` to be more specific
- **Fix typos**: Rename `agnet.md` → `agent.md`
- **Reorganize**: Rename `notes.md` → `note_taking_systems.md` for better descriptiveness
- **Language consistency**: Ensure all filenames follow `language_topic.md` pattern

## Present Results

After renaming:
- Show summary of changes made
- Highlight number of references updated
- Suggest reviewing MOC files that might need manual updates
- Recommend updating note title/tags if needed to match new filename

## Common Patterns

**Language-specific SDK notes:**
```
mcp_sdk.md → python_mcp_sdk.md
(leaves room for typescript_mcp_sdk.md, rust_mcp_sdk.md, etc.)
```

**Generic to specific:**
```
agents.md → ai_agents.md
deployment.md → docker_deployment.md
```

**Consistency with existing patterns:**
```
mcp-overview.md → mcp_overview.md  (underscore convention)
llm_agents.md → agents.md  (when already specific enough)
```
