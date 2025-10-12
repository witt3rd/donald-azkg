# Add Relationship

Manually add a relationship between two existing notes in the knowledge graph.

## Task

Execute the `add_relationship.py` script to establish a typed relationship between two notes with explanation.

## Input

User provides:
1. **Source note filename** (e.g., "note_a.md")
2. **Target note filename** (e.g., "note_b.md")
3. **Relationship type** (one of: prerequisites, related_concepts, extends, extended_by, alternatives, examples)
4. **Why explanation** (clear reason for the relationship)
5. **Optional: Bidirectional flag** (automatically create inverse relationship)

## Relationship Types

- **prerequisites** - Target must be understood before source
- **related_concepts** - Connected ideas at same level
- **extends** - Source builds upon target concept
- **extended_by** - Target builds upon source (inverse of extends)
- **alternatives** - Different approaches to same problem
- **examples** - Target is concrete implementation of source

## Execution

**Simple relationship:**
```bash
python .claude/scripts/add_relationship.py \
  "source.md" \
  "target.md" \
  "extends" \
  "Builds upon the base concept"
```

**Bidirectional relationship:**
```bash
python .claude/scripts/add_relationship.py \
  "source.md" \
  "target.md" \
  "extends" \
  "Builds upon the base concept" \
  --bidirectional \
  --inverse-type "extended_by"
```

## Common Bidirectional Patterns

**Extends/Extended By:**
- Source extends target → Target automatically gets extended_by source
```bash
--bidirectional --inverse-type "extended_by"
```

**Examples:**
- Source has example target → Target automatically gets extended_by source
```bash
--bidirectional --inverse-type "extended_by"
```

## Validation

Before adding, verify:
1. Both notes exist in the knowledge graph
2. Relationship type is valid
3. "Why" explanation is clear and specific
4. Relationship makes semantic sense
5. Not creating duplicate relationship

After adding:
- Run `/graph-validate` to ensure graph integrity
- Consider viewing both notes with `/graph-note` to verify

## Output

Success:
```
Successfully added relationship:
  source.md
    --extends--> target.md
  target.md
    --extended_by--> source.md
```

## Use Cases

- Manually correct missing relationships discovered during review
- Add relationships after creating new note
- Establish connections identified during research
- Fix bidirectional inconsistencies
- Add alternative relationships between competing approaches

## Notes

- Script automatically updates metadata timestamp
- Does NOT increment version (minor change)
- Relationship is immediately reflected in graph
- If relationship exists, script reports and exits without error
