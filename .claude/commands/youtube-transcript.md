# YouTube Transcript and Create Note

Get transcript from a YouTube video, summarize it, and create a knowledge graph note.

## Usage

`/youtube-transcript <youtube_url> [note_filename]`

## Process

1. **Extract video metadata**
   - Use `mcp__firecrawl__firecrawl_scrape` to get video title, description
   - Extract video ID from URL

2. **Get transcript**
   - Use `mcp__firecrawl__firecrawl_scrape` with appropriate format
   - If transcript unavailable, inform user and suggest alternatives

3. **Analyze and summarize**
   - Identify key concepts and main points
   - Create structured summary
   - Extract actionable insights
   - Determine appropriate tags

4. **Generate note filename** (if not provided)
   - Based on video topic
   - Use lowercase with underscores
   - Format: `topic_from_video.md`

5. **Create structured note** with:
   - YAML frontmatter (tags, source URL, video title)
   - Brief summary paragraph
   - Key Points section
   - Main Content (synthesized insights)
   - Related Concepts section
   - References section (YouTube link)

## Note Structure

```markdown
---
tags: [domain, topic, content-type]
source: <youtube_url>
video_title: "<title>"
date_added: <ISO_date>
---

# Note Title

Brief summary of the video's main thesis.

## Key Points

- Point 1
- Point 2
- Point 3

## Main Content

Detailed synthesis of concepts and insights from the video.

## Related Concepts

### Prerequisites
- [[prerequisite]] - Why needed first

### Related Topics
- [[related]] - Connection explanation

## References

- [Video Title](<youtube_url>) - Brief description
- Transcript accessed: <date>
```

## Tools to Use

- `mcp__firecrawl__firecrawl_scrape` - Get video metadata and transcript
- `Grep` - Find related notes
- `Write` - Create new note
- `Edit` - Update related notes for bidirectionality
