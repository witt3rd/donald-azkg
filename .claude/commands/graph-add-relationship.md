# Graph Add Relationship

Manually add a typed relationship between two notes with bidirectional update.

## Input

User provides:
- Source note: `agents.md`
- Target note: `semantic_routing.md`
- Relationship type: `related_topics` (or `prerequisites`, `extends`, `alternatives`, `examples`)
- Why: "Semantic routing enables intelligent model selection for agent tasks"

Example: `/graph-add-relationship agents semantic_routing related_topics "Enables model selection"`

## Valid Relationship Types

- `prerequisites` - Target must be understood first
- `related_topics` - Connected ideas at same level
- `extends` - Source builds upon target
- `alternatives` - Different approaches to same problem
- `examples` - Target is concrete implementation of source

## Execution Steps

### 1. Normalize Filenames

Ensure both filenames have `.md` extension.

### 2. Verify Both Notes Exist

Use Glob to verify both files exist:
```bash
Glob "agents.md"
Glob "semantic_routing.md"
```

### 3. Read Source Note

Use Read tool to get source note content, including current "Related Concepts" section.

### 4. Update Source Note

Use Edit tool to add relationship to appropriate section in source note:

```markdown
## Related Concepts

### Related Topics
- [[existing_note]] - Existing relationship
- [[semantic_routing]] - Enables intelligent model selection for agent tasks
```

### 5. Read Target Note

Use Read tool to get target note content, including current "Related Concepts" section.

### 6. Add Inverse Relationship

Determine inverse relationship type:
- `prerequisites` in A → add A to `related_topics` or `extended_by` in B (depending on context)
- `related_topics` in A → add A to `related_topics` in B
- `extends` in A → add A to `extended_by` in B
- `alternatives` in A → add A to `alternatives` in B
- `examples` in A → add A to `extended_by` or `related_topics` in B

Use Edit tool to add inverse relationship to target note.

### 7. Report Success

Show what was added to both files.

## Output Format

```
Added Relationship
============================================================

✓ Forward relationship:
  agents.md → semantic_routing.md
  Type: related_topics
  Why: Enables intelligent model selection for agent tasks

✓ Inverse relationship:
  semantic_routing.md → agents.md
  Type: related_topics
  Why: Agents use semantic routing for task delegation

============================================================
✅ Relationship Added!
============================================================

Updated files:
• agents.md - Added to "Related Topics" section
• semantic_routing.md - Added to "Related Topics" section

💡 Next steps:
• Review both notes to verify relationships make sense
• Use `/graph-note agents.md` to see all relationships
• Use `/graph-validate` to check bidirectionality
```

## Validation

Before adding:
- Both notes must exist
- Relationship type must be valid
- "Why" explanation should be provided (required for quality)

After adding:
- Both notes should have matching inverse relationships
- No duplicate relationships in either file

## Inverse Relationship Rules

| Forward Type | Inverse Type | Notes |
|--------------|--------------|-------|
| prerequisites | related_topics or extended_by | Context dependent |
| related_topics | related_topics | Symmetric |
| extends | extended_by | Clear inverse |
| alternatives | alternatives | Symmetric |
| examples | extended_by | Examples extend the concept |

## Use Cases

- **Fill gaps**: Add relationships discovered through usage
- **Manual correction**: Fix missing inverse relationships
- **Connect new notes**: Link newly created note to existing ones
- **Cross-domain links**: Connect concepts from different areas

## Tools Used

- **Glob** - Verify notes exist
- **Read** - Get current note content
- **Edit** - Update "Related Concepts" sections in both notes
- **Logic** - Determine inverse relationship type

## Important Notes

- Always provide meaningful "why" explanation
- Use consistent relationship types (follow conventions)
- Check both notes after adding to verify correctness
- Run `/graph-validate` if unsure about bidirectionality
