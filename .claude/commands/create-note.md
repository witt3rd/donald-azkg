# Create Note

You are tasked with creating a new atomic note in the Zettelkasten knowledge graph. Follow these steps systematically:

## 1. Parse Input and Check for Duplicates

**Input format:** User provides either:
- A topic name: `/create-note semantic_routing`
- A descriptive phrase: `/create-note "Rust async runtime comparison"`

**Duplicate detection:**
- Search existing notes using Glob for similar filenames
- Search content using Grep for similar concepts
- If potential duplicate found, ask user:
  - "Found existing note `similar_note.md`. Would you like to:
    - Expand/refresh that note instead?
    - Create a new distinct note (explain the difference)?
    - Cancel?"

## 2. Generate Filename

**Naming convention:**
- `topic_specific_concept.md` - lowercase with underscores
- Descriptive, not generic: `python_mcp_sdk.md` NOT `sdk.md`
- No folder prefixes in filename
- All notes go in repository root

**Examples:**
- Input: "semantic routing" → `semantic_routing.md`
- Input: "Rust async runtime comparison" → `rust_async_runtime_comparison.md`
- Input: "First principles thinking" → `first_principles_thinking.md`

## 3. Research the Topic

**Use Perplexity for comprehensive research:**
- Formulate focused query: "Provide comprehensive, technical information about [TOPIC] including: definition, key concepts, how it works, common use cases, best practices, related technologies, and current state as of 2025. Focus on technical accuracy and concrete details."
- Use `mcp__perplexity-ask__perplexity_ask` tool
- Gather sufficient material for complete, self-contained note
- Capture citation sources for references section

**Research depth:**
- Note should be atomic (one concept) but complete
- Include enough context to be standalone
- Technical and specific, not superficial

## 4. Discover Relationships

**Analyze against existing knowledge graph using Grep and Read:**

**Prerequisites:** What must be understood first?
- Grep for foundational concepts this topic mentions
- Check existing notes for topics that should come before this
- Example: `mcp_security.md` requires `mcp_overview.md` first

**Related concepts:** What connects at the same level?
- Find complementary or adjacent topics via tag search
- Technologies that integrate or compare
- Example: `semantic_routing.md` relates to `agents.md`

**Extends:** What does this build upon?
- Specific notes this concept directly extends
- Base concepts or patterns this implements
- Example: `python_mcp_sdk.md` extends `mcp_overview.md`

**Examples:** What concrete implementations exist?
- Look for specific tool/framework notes
- Implementation patterns
- Example: `agents.md` has examples like `alita.md`

**Alternatives:** Different approaches to same problem?
- Competing technologies or patterns
- Different paradigms for same goal

## 5. Generate Tag Recommendations

**Read `tag_system.md` for complete tag catalog**

**Select 3-6 tags across multiple dimensions:**
1. **Technology/Language:** `#python`, `#rust`, `#typescript`, etc.
2. **Framework/Tool:** `#react`, `#mcp`, `#fastmcp`, etc.
3. **Domain/Discipline:** `#agents`, `#llm`, `#security`, etc.
4. **Content Type:** `#api`, `#guide`, `#pattern`, `#reference`, etc.
5. **Cross-cutting Themes:** `#async`, `#optimization`, `#testing`, etc.
6. **Method/Thinking:** `#first-principles`, `#systems-thinking`, etc.

**Tag format:** lowercase with hyphens in YAML array
```yaml
tags: [python, mcp, agents, sdk, api]
```

## 6. Write the Note

**Use Write tool to create the file with this structure:**

```markdown
---
tags: [tag1, tag2, tag3, tag4, tag5]
---
# Note Title

Brief 1-2 sentence summary of the concept.

## Main Content

Complete, self-contained explanation organized into logical sections.

### Section 1: Overview
[Core concept explanation]

### Section 2: How It Works
[Technical details]

### Section 3: Use Cases
[When and why to use this]

### Section 4: Best Practices
[Practical guidance]

## Related Concepts

### Prerequisites
- [[prerequisite_note]] - Why it's needed first

### Related Topics
- [[related_note]] - Connection explanation

### Extends
- [[base_note]] - What this builds upon

## References

[If research provided citations, include them here]
[1] Source URL
[2] Source URL
```

**Content guidelines:**
- Write for LLM context consumption, not just human reading
- Complete enough to stand alone when attached to prompt
- Technical and specific, avoid vague generalities
- No hyperbolic language or marketing claims
- Use wikilinks `[[note]]` to reference existing notes
- Code examples where appropriate
- Concrete, actionable information

## 7. Add Bidirectional Relationships

**Update connected notes using Edit tool:**

For each relationship discovered:
1. **Read the target note** to find its "Related Concepts" section
2. **Add inverse relationship:**
   - If new note extends X → Add new note to X's "Extended By" section
   - If new note has prerequisite X → Add new note to X's "Extended By" or "Related Topics"
   - If new note relates to X → Add new note to X's "Related Topics"

**Example:**
```markdown
# In agents.md - add to "Related Topics" section:
- [[semantic_routing]] - Enables intelligent model selection for agent tasks
```

## 8. Update MOC Files

**Identify relevant MOC files using Glob:**
- Check tags to determine which MOCs apply
- Common MOCs: `agents_moc.md`, `mcp_moc.md`, `rust_moc.md`, `typescript_moc.md`, `python_moc.md`, `writing_moc.md`

**For each relevant MOC:**
- Read the MOC file
- Find appropriate section to add link
- Add wikilink with brief context: `- [[new_note]] - Brief description`
- Maintain MOC organization and structure
- Use Edit tool for surgical updates

## 9. Provide Summary

**Report to user:**
```
Created new note: `new_note.md`

**Tags:** tag1, tag2, tag3, tag4, tag5

**Relationships established:**
- Prerequisites: 2 notes
- Related concepts: 3 notes
- Extends: 1 note
- Examples: 2 notes

**Bidirectional links updated:**
- Updated 5 notes with inverse relationships

**MOCs updated:**
- moc_name_moc.md (added to "Section Name")
- other_moc.md (added to "Other Section")

**Next steps:**
- Review the note at `new_note.md`
- Use `/graph-note new_note.md` to verify relationships
- Use `/expand-graph new_note.md` to discover additional connections
```

## Important Constraints

**Critical rules:**
- ALWAYS use wikilink format `[[note]]` not `[[note.md]]`
- MAINTAIN bidirectionality - update both notes in every relationship
- ENSURE atomicity - one complete, usable concept per note
- NO hyperbolic language or marketing claims
- ALL notes go in repository root (no subdirectories)
- Use Write for new files, Edit for updating existing files
- Use Grep/Glob for discovery, Read for content analysis

**Tools to use:**
- **Write** - Create new markdown file
- **Edit** - Update existing notes (add relationships, update MOCs)
- **Read** - Read tag_system.md, MOC files, existing notes
- **Grep** - Search for similar concepts, find notes by tag
- **Glob** - Find MOC files, check for duplicates
- **mcp__perplexity-ask** - Research the topic

**Quality checks before writing:**
- Is this truly atomic (one concept)?
- Is it complete enough to stand alone?
- Are relationships meaningful and justified?
- Do tags span multiple dimensions?
- Is content technical and specific?

Execute these steps for the topic provided by the user.
