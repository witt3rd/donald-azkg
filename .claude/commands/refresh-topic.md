---
description: Refresh a topic page with latest information from Perplexity
---

# Refresh Topic

You are tasked with refreshing a topic page with the latest information. Follow these steps:

## 1. Read the Topic File
- The user will provide a filename (e.g., `agents.md` or just `agents`)
- Read the file from the current working directory
- Parse the YAML frontmatter and main content

## 2. Formulate Perplexity Query
- Analyze the topic content to understand the main subject
- Extract key concepts, technologies, or themes
- Create a focused query to find:
  - Recent developments (last 6-12 months)
  - New research or papers
  - Updated best practices
  - Emerging trends
  - Deprecated or outdated information

Example query format: "What are the latest developments, research, and best practices for [TOPIC] as of 2025? Include any significant changes, new tools, or deprecated approaches."

## 3. Query Perplexity
- Use the `mcp__perplexity-ask__perplexity_ask` tool
- Provide a clear, focused query based on the topic analysis
- Request comprehensive, up-to-date information

## 4. Incorporate Updates
- Review the Perplexity response carefully
- Identify genuinely new or updated information that should be added
- For each update:
  - Determine the appropriate section to update
  - Maintain the existing structure and format
  - Add new information without removing valuable existing content
  - Preserve all existing citations and references
  - Add new citations for updated information if provided

## 5. Update Metadata
- Add or update the YAML frontmatter with:
  ```yaml
  last_refresh: 2025-10-11  # Use today's date
  ```
- Preserve all existing YAML fields (tags, etc.)
- Maintain YAML formatting

## 6. Write Updated File
- Use the Edit tool to make surgical updates to specific sections
- OR use the Write tool if comprehensive rewrite is needed
- Ensure all formatting is preserved (markdown, wikilinks, etc.)

## 7. Summary
- Provide a brief summary of:
  - What updates were found
  - Which sections were modified
  - Any significant new information added
  - Any outdated information identified (but keep unless contradicted)

## Important Notes
- **Preserve existing content**: Only add or update, don't remove unless information is clearly outdated or contradicted
- **Maintain structure**: Keep the same section organization
- **Keep relationships**: Don't modify the "Related Concepts" section
- **Respect format**: Maintain wikilink format `[[note]]`, YAML format, etc.
- **Be conservative**: Only incorporate high-quality, verifiable updates
- **No hyperbole**: Don't add marketing language or grandiose claims

Execute these steps for the topic file provided by the user.
