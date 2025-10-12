# Search Notes

You are tasked with searching across all notes in the Zettelkasten for a specific phrase or pattern, showing context for each match.

## 1. Parse Search Input

**Input format:** User provides either:
- A simple phrase: `/search-notes "semantic routing"`
- A regex pattern: `/search-notes "async.*await"`
- Multiple terms: `/search-notes "MCP security authentication"`

**Extract:**
- Search pattern (the phrase or regex)
- Optional flags (case-sensitive, whole word, etc.)

## 2. Execute Search with Context

**Use Grep tool to search all markdown files:**

```
pattern: <user's search term>
glob: "*.md"
output_mode: "content"
-n: true  (show line numbers)
-C: 2     (show 2 lines of context before and after)
-i: true  (case insensitive by default)
```

**Search strategy:**
- Search all `.md` files in repository root
- Include line numbers for reference
- Show 2 lines context before and after each match
- Case-insensitive by default (unless user specifies otherwise)

## 3. Format Results

**Group results by file and present clearly:**

```
Found <N> matches across <M> notes:

## note_name.md (X matches)

Match 1 (line 45):
43: context before
44: more context
45: **matching line with PATTERN highlighted**
46: context after
47: more context

Match 2 (line 120):
118: context before
119: more context
120: **matching line with PATTERN highlighted**
121: context after
122: more context

---

## another_note.md (Y matches)

Match 1 (line 78):
...
```

**Formatting guidelines:**
- Use `##` headers for each file
- Show match count per file
- Include line numbers for easy navigation
- Bold or highlight the matching text
- Separate files with `---`
- Show total stats at top

## 4. Analyze Results

**Provide insights:**

**Thematic clustering:**
- Which tags/domains show up most?
- Are matches concentrated in certain batches?
- Example: "Most matches in MCP Protocol notes (5 files)"

**Related concepts:**
- Which notes frequently appear together in results?
- Suggest wikilinks between related notes if not already linked

**Coverage assessment:**
- Is this concept well-covered or sparse?
- Suggest potential new notes or expansions

## 5. Suggest Next Actions

**Based on search results, suggest:**

**If many matches (>10):**
- "This concept is well-covered. Consider creating a MOC for [topic]"
- "Consider using `/generate-moc` for this theme"

**If few matches (1-3):**
- "Limited coverage found. Consider `/create-note` for deeper treatment"
- "Consider `/expand-graph` on existing notes to add related content"

**If related concepts found:**
- "Found related notes that aren't linked. Consider `/link-notes`"
- List specific note pairs that should be connected

**If search term in multiple contexts:**
- "This term appears in different contexts: [list domains]"
- "Consider creating separate atomic notes for each context"

## 6. Advanced Search Options

**Support optional flags:**

**Case-sensitive search:**
- User specifies: `/search-notes --case-sensitive "Python"`
- Set `-i: false` in Grep

**Whole word only:**
- User specifies: `/search-notes --whole-word "test"`
- Adjust pattern to: `\btest\b`

**Regex mode:**
- User specifies: `/search-notes --regex "mcp.*server"`
- Pass pattern directly to Grep

**More context:**
- User specifies: `/search-notes --context 5 "pattern"`
- Set `-C: 5` for 5 lines of context

**Files only (no content):**
- User specifies: `/search-notes --files-only "pattern"`
- Set `output_mode: "files_with_matches"`

## 7. Output Summary

**Provide concise summary:**

```
Search Summary for "<search-pattern>"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Statistics:
- Total matches: <N>
- Files with matches: <M>
- Most matches: <filename> (<X> matches)

📁 Distribution by batch:
- MCP Protocol: 5 notes
- Python Stack: 3 notes
- Core AI/Agents: 2 notes

🏷️  Common tags in results:
#mcp, #python, #security, #api

💡 Suggestions:
- [Specific actionable next step based on results]
- [Another suggestion]

🔗 Potentially missing links:
- [[note_a]] ↔ [[note_b]] - both discuss same concept
```

## 8. Special Search Patterns

**Recognize common search needs:**

**Tag search:**
- Input: `/search-notes "#mcp"`
- Search in YAML frontmatter tags specifically
- List all notes with that tag

**Broken wikilinks:**
- Input: `/search-notes --broken-links`
- Find `[[wikilinks]]` that don't point to existing files
- Report with locations

**TODOs and incomplete sections:**
- Input: `/search-notes --todos`
- Find `TODO`, `FIXME`, `[placeholder]`, etc.
- Report what needs completion

**Missing related concepts:**
- Input: `/search-notes --no-relationships`
- Find notes with empty "Related Concepts" sections
- Suggest running `/expand-graph` on them

## Usage Examples

**Simple search:**
```
/search-notes "semantic routing"
```

**Regex search:**
```
/search-notes --regex "async.*(await|runtime)"
```

**Case-sensitive search:**
```
/search-notes --case-sensitive "Python"
```

**Find all notes about a technology:**
```
/search-notes --context 3 "FastMCP"
```

**Tag search:**
```
/search-notes "#agents"
```

**Find broken links:**
```
/search-notes --broken-links
```

**Find incomplete notes:**
```
/search-notes --todos
```

## Important Notes

**Performance:**
- Grep is fast even across 93+ notes
- Results should return quickly
- If >100 matches, consider limiting output or grouping

**Formatting:**
- Keep results scannable
- Use consistent formatting
- Include enough context to understand match
- Link to line numbers for easy navigation: `note.md:45`

**Accuracy:**
- Match user's search term exactly as specified
- Don't modify regex patterns unless clarifying with user
- Report if pattern yields no results

Execute the search for the pattern provided by the user.
