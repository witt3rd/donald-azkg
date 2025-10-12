# Validate Graph

Run validation checks on the knowledge graph to ensure integrity.

## Task

Check markdown files for:
- All wikilinks point to existing notes (no broken links)
- "Related Concepts" sections are well-formed
- Bidirectional relationships are consistent
- YAML frontmatter is valid

## Execution Steps

### 1. Find All Wikilinks

Use Grep to extract all wikilinks from all markdown files:
```bash
# Find all wikilinks in the format [[note_name]]
Grep "\[\[([^\]]+)\]\]" --glob="*.md" --output_mode="content" -n
```

Extract unique note names from results.

### 2. Verify All Wikilinks Point to Existing Files

For each unique wikilink target found:
- Use Glob to check if `target.md` exists in repository root
- Record any broken links (wikilink but no corresponding file)

### 3. Check Bidirectional Consistency

For notes with "Related Concepts" sections:
- Read notes with "Extends" relationships
- Verify target notes have "Extended By" back-reference
- Read notes with "Prerequisites" relationships
- Verify reasonable consistency (prerequisites should be foundational)

### 4. Validate YAML Frontmatter

Use Read tool to check a sample of notes:
- YAML frontmatter starts with `---` and ends with `---`
- `tags:` field is present and is an array
- Tags use lowercase-with-hyphens format

### 5. Check for Common Issues

- Notes without any "Related Concepts" section (orphaned notes)
- Notes with empty tags array
- Duplicate note filenames (shouldn't happen but check)
- MOC files that reference non-existent notes

## Output Format

**Success:**
```
Graph Validation
============================================================
[OK] Knowledge graph is valid

All checks passed:
  ✓ All wikilinks point to existing notes (N wikilinks checked)
  ✓ No broken links found
  ✓ Bidirectional relationships are consistent
  ✓ YAML frontmatter is well-formed
  ✓ No orphaned notes detected

Statistics:
  • Total notes: N
  • Total wikilinks: M
  • Total relationships: X
  • MOC files: Y
```

**Failure:**
```
Graph Validation
============================================================
[ERROR] Found N issue(s):

1. Broken wikilink: file1.md:42 references [[non_existent_note]]
2. Broken wikilink: file2.md:18 references [[another_missing]]
3. Missing inverse: agents.md extends [[semantic_routing]] but inverse not found
4. Orphaned note: lonely_note.md has no "Related Concepts" section
5. Invalid YAML: broken_note.md frontmatter is malformed

Recommendations:
  • Fix or remove broken wikilinks
  • Add "Extended By" section to semantic_routing.md
  • Consider adding relationships to lonely_note.md
  • Fix YAML frontmatter in broken_note.md
```

## Validation Rules

**Wikilink validation:**
- Every `[[note_name]]` must have corresponding `note_name.md` file
- Case-sensitive matching
- Should NOT include `.md` in wikilink (use `[[note]]` not `[[note.md]]`)

**Bidirectional validation:**
- If A extends B, then B should have "Extended By" section mentioning A
- If A is prerequisite for B, then B should mention A in "Prerequisites"
- Not always perfectly symmetric, but should be logically consistent

**YAML validation:**
- Well-formed YAML with proper delimiters
- Tags field exists and is array
- Tags follow naming convention (lowercase-with-hyphens)

**Structural validation:**
- Notes should have "Related Concepts" section (unless intentionally standalone)
- MOC files should only reference existing notes
- No circular dependencies in prerequisite chains (optional advanced check)

## If Validation Fails

For each error type, suggest fixes:

**Broken wikilinks:**
```
File: example.md:42
Issue: References [[missing_note]]
Fixes:
  • Create the missing note
  • Remove the wikilink
  • Change to reference an existing note
```

**Missing inverse relationships:**
```
File: agents.md
Issue: Extends [[semantic_routing]] but inverse not found
Fix:
  • Add to semantic_routing.md "Related Concepts" section:
    ### Extended By
    - [[agents]] - Uses routing for agent task selection
```

**Orphaned notes:**
```
File: lonely_note.md
Issue: No "Related Concepts" section
Fix:
  • Add "Related Concepts" section with at least one relationship
  • Link to appropriate MOC
  • Use /expand-graph to discover relationships
```

## Tools Used

- **Grep** - Find all wikilinks across all markdown files
- **Glob** - Check if wikilink targets exist as files
- **Read** - Read notes to check "Related Concepts" sections and YAML frontmatter
- **Parse logic** - Extract wikilinks, validate YAML, check consistency

## Success Criteria

- All wikilinks resolve to existing files
- No malformed YAML frontmatter
- Bidirectional relationships are logically consistent
- Minimal orphaned notes

## When to Run

- After creating new notes (check new relationships valid)
- After renaming notes (check wikilinks updated correctly)
- After bulk operations (check graph still consistent)
- Periodically (ensure graph health over time)
