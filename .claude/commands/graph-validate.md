# Validate Graph

Run validation checks on the knowledge graph to ensure integrity.

## Task

Execute the `validate_graph.py` script to check:
- Metadata counts match actual counts
- All batch references point to existing notes
- All relationship targets exist
- Bidirectional relationships are consistent (extends ↔ extended_by)

## Execution

Use Bash tool to run the validation script:

```bash
python .claude/scripts/validate_graph.py
```

## Output

The script will display:
- **[OK] Graph is valid** - If all checks pass
- **[ERROR] Graph has N error(s)** - If validation fails, with detailed error list

## Success Criteria

- Script exits with code 0 (success)
- All validation checks pass
- No errors reported

## If Validation Fails

If errors are found:
1. Report the specific errors to the user
2. Suggest the appropriate fix based on error type:
   - **Metadata count mismatch**: The count was off, but should now be correct
   - **Missing batch references**: Note exists in batch but not in notes list
   - **Missing relationship targets**: Relationship points to non-existent note
   - **Bidirectional inconsistency**: Missing inverse relationship (extends ↔ extended_by)

## Example Output

**Success:**
```
Graph Validation
============================================================
[OK] Graph is valid

All checks passed:
  [OK] Metadata counts match actual counts
  [OK] All batch references point to existing notes
  [OK] All relationship targets exist
  [OK] Bidirectional relationships are consistent
```

**Failure:**
```
Graph Validation
============================================================
[ERROR] Graph has 2 error(s):

1. Metadata total_notes (94) doesn't match actual count (93)
2. Note 'agents.md' extends 'semantic_routing.md' but inverse not found
```
