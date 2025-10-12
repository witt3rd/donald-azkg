# Rename Note Command

Rename a note file and update all wikilink references throughout the knowledge base.

## Task

1. Rename the physical markdown file (using Bash mv)
2. Update all wikilinks `[[old_filename]]` → `[[new_filename]]` in all markdown files (using Grep + Edit)
3. Update MOC files if needed (using Edit)

## Input

User provides:
- Old filename (e.g., "mcp_sdk.md" or just "mcp_sdk")
- New filename (e.g., "python_mcp_sdk.md" or just "python_mcp_sdk")

## Execution Steps

### 1. Normalize Filenames

Ensure both filenames have `.md` extension:
```
old_filename = "mcp_sdk" → "mcp_sdk.md"
new_filename = "python_mcp_sdk" → "python_mcp_sdk.md"
```

### 2. Verify Old File Exists

Use Glob to check if old file exists:
```bash
# Check if file exists
Glob mcp_sdk.md
```

If not found, report error to user.

### 3. Check New Filename Not In Use

Use Glob to ensure new filename doesn't already exist:
```bash
# Check if new filename is available
Glob python_mcp_sdk.md
```

If exists, report error to user.

### 4. Find All Wikilinks to Old Note

Use Grep to find all markdown files containing wikilinks to the old note:
```bash
# Find all files with wikilinks to old note
Grep "\[\[mcp_sdk\]\]" --glob="*.md" --output_mode="files_with_matches"
```

Store list of files that need updating.

### 5. Rename the Physical File

Use Bash to rename the file:
```bash
# Rename the file
mv "mcp_sdk.md" "python_mcp_sdk.md"
```

### 6. Update Wikilinks in All Files

For each file found in step 4, use Edit tool to replace wikilinks:

```markdown
# Old wikilink
[[mcp_sdk]]

# New wikilink
[[python_mcp_sdk]]
```

Use Edit tool for each file:
- old_string: `[[mcp_sdk]]`
- new_string: `[[python_mcp_sdk]]`
- replace_all: true (to catch all occurrences in the file)

Track how many files were updated.

### 7. Update MOC Files

Check if any MOC files were updated in step 6. If so, verify the context around the wikilink makes sense with the new name.

## Output Format

Report to user:
```
============================================================
Renamed Note: mcp_sdk.md → python_mcp_sdk.md
============================================================

📝 Physical file renamed
   ✓ mcp_sdk.md → python_mcp_sdk.md

📄 Updated wikilinks in N files:
   ✓ file1.md: X reference(s)
   ✓ file2.md: Y reference(s)
   ✓ file3.md: Z reference(s)

============================================================
✅ Rename Complete!
============================================================

📋 Summary:
   • File renamed: mcp_sdk.md → python_mcp_sdk.md
   • Markdown files updated: N
   • Total wikilink updates: M

💡 Next steps:
   • Review changes with git diff
   • Update note title if needed to match new filename
   • Update note tags if needed
   • Verify MOC entries make sense with new name
```

## Validation

After renaming:
- Old file no longer exists (verify with Glob)
- New file exists (verify with Glob)
- No remaining wikilinks to old filename (verify with Grep)
- All "Related Concepts" sections still valid (Read a few files to spot check)

## Safety Features

- Check old file exists before renaming
- Check new filename not in use before renaming
- Use replace_all to catch all wikilinks in each file
- Report which files were updated for transparency
- All changes visible in git diff

## Use Cases

- **Clarify naming**: Rename `mcp_sdk.md` → `python_mcp_sdk.md` to be more specific
- **Fix typos**: Rename `agnet.md` → `agent.md`
- **Reorganize**: Rename `notes.md` → `note_taking_systems.md` for better descriptiveness
- **Language consistency**: Ensure all filenames follow `language_topic.md` pattern

## Present Results

After renaming:
- Show summary of changes made
- Highlight number of files and references updated
- Suggest reviewing MOC files to ensure context still makes sense
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

## Tools Used

- **Glob** - Check if files exist
- **Grep** - Find all wikilinks to old filename
- **Bash** - Rename the physical file (mv command)
- **Edit** - Update wikilinks in each markdown file
- **Read** - Spot check updated files for correctness
