# Process PDF and Create Note

Extract content from a PDF (URL or local file) and create a knowledge graph note.

## Usage

`/process-pdf <pdf_url_or_path> [note_filename]`

## Process

1. **Access PDF content**
   - If URL: Use `mcp__firecrawl__firecrawl_scrape` with PDF parser
   - If local file: Use `Read` tool (supports PDF)
   - Extract text, structure, and key information

2. **Analyze content**
   - Identify document type (academic paper, guide, report, etc.)
   - Extract key concepts and main arguments
   - Identify domain/topic area
   - Determine appropriate tags

3. **Generate note filename** (if not provided)
   - Based on document topic
   - Use lowercase with underscores
   - Format: `topic_from_document.md`

4. **Create structured note** with:
   - YAML frontmatter (tags, source, document metadata)
   - Brief summary paragraph
   - Main sections based on document structure
   - Related Concepts section
   - References section (PDF link/path)

## Note Structure

```markdown
---
tags: [domain, topic, content-type]
source: <pdf_url_or_path>
document_title: "<title>"
authors: "<authors if applicable>"
date_added: <ISO_date>
---

# Note Title

Brief summary of the document's main thesis or purpose.

## Key Concepts

Main ideas and concepts from the document.

## Main Content

Structured synthesis of the document's content, organized by sections or themes.

## Related Concepts

### Prerequisites
- [[prerequisite]] - Why needed first

### Related Topics
- [[related]] - Connection explanation

## References

- [Document Title](<source>) - Brief description
- Accessed: <date>
```

## Tools to Use

- `mcp__firecrawl__firecrawl_scrape` - For PDF URLs (with parser)
- `Read` - For local PDF files
- `Grep` - Find related notes
- `Write` - Create new note
- `Edit` - Update related notes for bidirectionality
