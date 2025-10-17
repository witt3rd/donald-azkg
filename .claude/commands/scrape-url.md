# Scrape URL and Create Note

Scrape content from a URL and create a knowledge graph note from it.

## Usage

`/scrape-url <url> [note_filename]`

## Process

1. **Scrape the URL** using `mcp__firecrawl__firecrawl_scrape`
   - Format: markdown
   - Include main content only

2. **Analyze the content**
   - Extract key concepts
   - Identify domain/topic area
   - Determine appropriate tags

3. **Generate note filename** (if not provided)
   - Based on main topic
   - Use lowercase with underscores
   - Format: `topic_specific_concept.md`

4. **Create structured note** with:
   - YAML frontmatter (3-6 tags, source URL)
   - Brief summary paragraph
   - Main content (synthesized from scraped content)
   - Related Concepts section (suggest connections to existing notes)
   - References section (original URL)

5. **Identify relationships**
   - Search for related notes in repository
   - Suggest connections (prerequisites, related topics, etc.)
   - Ask user if they want to add bidirectional links

## Note Structure

```markdown
---
tags: [domain, technology, content-type]
source: <original_url>
date_added: <ISO_date>
---

# Note Title

Brief summary of the concept from the article.

## Main Content

Synthesized key points and insights.

## Related Concepts

### Prerequisites
- [[prerequisite]] - Why needed first

### Related Topics
- [[related]] - Connection explanation

## References

- [Original Article](<url>) - Brief description
```

## Tools to Use

- `mcp__firecrawl__firecrawl_scrape` - Scrape URL content
- `Grep` - Find related notes by tags/content
- `Write` - Create new note
- `Edit` - Update related notes for bidirectionality
