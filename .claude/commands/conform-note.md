# Conform Note

Restructure a note to follow the standard repository format as defined in CLAUDE.md and README.md.

## Task

Transform the provided note to match this standard structure:

```markdown
---
tags: [domain, technology, content-type]
last_refresh: YYYY-MM-DD  # Optional, preserve if exists
---

# Note Title

Brief summary paragraph (1-3 sentences describing what this note contains).

## Main Content Sections

(Preserve existing section structure and content)

## Related Concepts

### Prerequisites
- [[note]] - Why it's needed first

### Related Topics
- [[note]] - Why it connects

### Extends
- [[note]] - What this builds upon

### Extended By
- [[note]] - What builds upon this

### Examples
- [[note]] - Concrete implementation

### Alternatives
- [[note]] - Different approach

## References

[1] <https://example.com>
[2] <https://example.com>
```

## Steps

### 1. Read and Analyze
- Read the specified note file
- Identify existing sections and their purpose
- Preserve all valuable content

### 2. Fix YAML Frontmatter
- Ensure proper YAML format with `tags: [tag1, tag2, tag3]`
- Preserve `last_refresh` if it exists
- Ensure tags follow conventions: lowercase with hyphens

### 3. Restructure Title and Summary
- Ensure single H1 title
- If the opening paragraph is already a good summary, keep it
- If opening is too long or mixed with introduction content, extract a 1-3 sentence summary

### 4. Organize Main Content
- Preserve existing section structure
- Keep all substantive content in appropriate sections
- Maintain proper heading hierarchy

### 5. Fix References Section
- Change "Citations:" to "## References"
- Remove any "---" separator lines between content and references
- Remove attribution lines like "Answer from Perplexity: pplx.ai/share"
- Keep all citation links properly formatted
- Ensure References section comes AFTER Related Concepts

### 6. Preserve Related Concepts
- The "## Related Concepts" section contains typed relationships - be careful when editing
- This section IS the knowledge graph - relationships live directly in markdown files
- Ensure it appears before References section
- When conforming structure, preserve all existing relationships exactly as they are

### 7. Final Structure Check

The final order should be:
1. YAML frontmatter
2. Title (H1)
3. Brief summary paragraph
4. Main content sections (H2)
5. ## Related Concepts (H2) - preserve existing relationships
6. ## References (H2)

## Execution

1. Use Read tool to load the note
2. Use Edit tool to make surgical changes OR Write tool if complete restructure needed
3. Preserve all wikilinks in format `[[note]]` NOT `[[note.md]]`
4. Maintain all existing content - only reorganize, don't remove substance

## Important Rules

- **Preserve content**: Only reorganize, don't delete valuable information
- **Preserve Related Concepts**: Keep all existing relationships exactly as written
- **Maintain wikilinks**: Use `[[note]]` format
- **Keep citations**: Transform format but preserve all references
- **Clean formatting**: Remove extraneous separators and attribution lines
- **Consistent headings**: Use H2 (##) for major sections

## Example Transformations

**Before:**
```markdown
# Some Note

Lots of intro text...

## Content

...

Citations:
[1] https://example.com

---

Answer from Perplexity: pplx.ai/share

## Related Concepts
...
```

**After:**
```markdown
---
tags: [relevant, tags]
---

# Some Note

Brief summary extracted from intro.

## Content

...

## Related Concepts
...

## References

[1] <https://example.com>
```

Execute this transformation for the note file specified by the user.
