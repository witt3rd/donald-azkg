# Expand Graph

You are tasked with discovering missing relationships between a note and the rest of the knowledge graph through multi-strategy analysis.

## 1. Parse Input and Load Note

**Input format:** User provides:
- A note name: `/expand-graph mcp_security.md`
- Or just the topic: `/expand-graph mcp_security`

**Normalize and validate:**
- Add `.md` extension if missing
- Verify the target note exists
- If not found, suggest similar notes using Glob

**Read the target note:**
- Use Read tool to get full content
- Extract YAML tags
- Extract main concepts and topics
- Note current relationships from knowledge_graph_full.json

## 2. Extract Key Concepts

**Analyze note content for:**

**Technical terms:**
- Technologies mentioned (Python, Rust, MCP, OAuth, etc.)
- Frameworks and tools (FastMCP, React, etc.)
- Protocols and standards (HTTP, JWT, RFC 8707, etc.)

**Domain concepts:**
- Core ideas discussed (authentication, security, agents, etc.)
- Patterns mentioned (observer, factory, reactive, etc.)
- Problem domains (enterprise, web, async, etc.)

**Wikilinks:**
- Existing wikilinks in content `[[note]]`
- Are these also in relationships? If not, why?

**Tags:**
- YAML frontmatter tags provide high-level domains

**Output concept extraction:**
```
📖 Analyzing mcp_security.md...

🔍 Key concepts identified:
   Technologies: OAuth, JWT, SAML, Active Directory
   Domains: security, authentication, authorization, privacy
   Protocols: RFC 8707, Resource Indicators, OAuth flows
   Patterns: least privilege, defense in depth, audit logging
   Tags: #mcp #protocol #security #authentication #authorization

📊 Current relationships:
   ✅ Prerequisites: 2 (mcp_overview, mcp_architecture)
   ✅ Related concepts: 3
   ✅ Extends: 1
   ✅ Examples: 0
   ✅ Alternatives: 0
```

## 3. Multi-Strategy Relationship Discovery

**Strategy 1: Content-Based Search (Grep)**

For each key concept, search other notes:
```
Searching for "OAuth" across knowledge base...
Found in:
- oauth_fundamentals.md (15 mentions)
- api_security.md (8 mentions)
- enterprise_auth.md (12 mentions)

Searching for "authentication" across knowledge base...
Found in:
- fastmcp_auth.md (20 mentions)
- api_security.md (18 mentions)
- enterprise_auth.md (25 mentions)
```

**Filter out:**
- The target note itself
- Notes already in relationships
- Low-relevance matches (1-2 mentions)

**Strategy 2: Tag-Based Discovery**

```
Target has tags: #mcp #security #authentication

Finding notes with overlapping tags...
- #mcp + #security: mcp_implementation.md, mcp_tools.md
- #security + #authentication: api_security.md, zero_trust.md
- #mcp (any): 12 other MCP-related notes
```

**Strategy 3: Wikilink Analysis**

```
Checking wikilinks in content vs relationships...

Found in content but NOT in relationships:
- [[mcp_overview]] - mentioned in text but not in prerequisites
- [[oauth_fundamentals]] - referenced but not linked formally

Found in other notes' relationships pointing here:
- fastmcp_auth.md lists this as "related" (we should reciprocate)
```

**Strategy 4: Research with Perplexity**

Ask targeted questions:
```
Query 1: "What foundational knowledge is required to understand [main topic of note]?"
Query 2: "What concepts are commonly related to [main topic] in practice?"
Query 3: "What are concrete examples or implementations of [main topic]?"
Query 4: "What are alternative approaches to [main topic]?"
```

Use Perplexity responses to:
- Discover conceptual prerequisites
- Find related domains
- Identify common patterns
- Suggest examples and alternatives

## 4. Classify and Score Relationships

**For each discovered note, determine:**

### Relationship Type

**Prerequisites:** Does target need this first?
- Contains foundational concepts mentioned in target
- Target assumes knowledge from this note
- Complexity: This note is simpler/more basic
- Example: mcp_overview → mcp_security

**Related concepts:** Parallel/complementary topics?
- Same level of complexity
- Different but connected domain
- Solve similar problems differently
- Example: api_security ↔ mcp_security

**Extends:** Does target build on this?
- Target is specialized version
- Adds capabilities to base concept
- Target assumes this as foundation
- Example: mcp_security extends mcp_architecture

**Examples:** Is this a concrete implementation?
- Shows practical application of target concepts
- Code/pattern implementing target ideas
- Case study of target in practice
- Example: fastmcp_auth is example of mcp_security

**Alternatives:** Different approach to same problem?
- Solves same problem differently
- Competing technology or pattern
- Different paradigm
- Example: zero_trust vs traditional_security

### Confidence Score

**High (★★★★★):**
- Many shared concepts (10+)
- Strong semantic relationship
- Confirmed by Perplexity research
- Explicitly mentioned in content
- Example: OAuth fundamentals for OAuth-heavy security note

**Medium (★★★☆☆):**
- Moderate overlap (5-9 concepts)
- Reasonable semantic connection
- Supported by tag overlap
- Mentioned indirectly
- Example: General API security for MCP security

**Low (★★☆☆☆):**
- Minimal overlap (2-4 concepts)
- Weak semantic connection
- Speculative relationship
- Not mentioned in content
- Example: Zero trust model for MCP (valid but tangential)

### Evidence Collection

**For each relationship, capture:**
- **Frequency:** How many concept matches?
- **Quotes:** Specific text showing connection
- **Location:** Where in note is this relevant?
- **Research:** What did Perplexity say?
- **Reasoning:** Why should these be linked?

## 5. Present Suggestions

**Format as organized report:**

```markdown
# Graph Expansion: mcp_security.md

Found **12 potential relationships** across 8 notes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📚 Suggested Prerequisites (2)

### 1. [[mcp_overview]] → prerequisite
**Confidence:** ★★★★★ High

**Evidence:**
- Mentioned 3 times in target note
- Target references "MCP fundamentals" and "protocol basics"
- Research confirms: "Understanding MCP basics required before security"

**Reasoning:** Can't understand MCP security without knowing what MCP is.
The security model builds directly on protocol concepts.

**Current status:** Referenced in content but missing from relationships

---

### 2. [[oauth_fundamentals]] → prerequisite
**Confidence:** ★★★★★ High

**Evidence:**
- 15 mentions of "OAuth" in target note
- Entire section dedicated to "OAuth Flows"
- Tags overlap: #authentication, #security
- Research confirms: "OAuth knowledge essential for MCP auth"

**Reasoning:** OAuth is the primary authentication mechanism. Deep understanding
needed before tackling MCP-specific OAuth implementation.

**Current status:** Not currently linked

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔗 Suggested Related Concepts (4)

### 3. [[enterprise_architecture]] → related
**Confidence:** ★★★☆☆ Medium

**Evidence:**
- Both discuss: VNet integration, DLP, enterprise deployment
- 8 shared concepts
- Tags overlap: #enterprise

**Reasoning:** Both address enterprise concerns at similar abstraction level.
MCP security is part of broader enterprise architecture.

**Current status:** Not currently linked

---

### 4. [[api_security_best_practices]] → related
**Confidence:** ★★★☆☆ Medium

**Evidence:**
- MCP is API protocol
- 12 security best practices mentioned in both
- Research: "General API security principles apply to MCP"

**Reasoning:** MCP security inherits from general API security principles.
Provides broader context for MCP-specific patterns.

**Current status:** Not currently linked

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🏗️ Suggested "Extends" (1)

### 5. mcp_security extends [[mcp_architecture]]
**Confidence:** ★★★★★ High

**Evidence:**
- Security is explicit layer on architecture diagram
- Target states: "Security model built on top of MCP architecture"
- Architecture defines components, security defines protections

**Reasoning:** Security adds protection layer to architectural components.
Cannot exist without the architecture it secures.

**Current status:** Architecture listed as prerequisite, should be "extends"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 💡 Suggested Examples (3)

### 6. [[fastmcp_authentication]] → example
**Confidence:** ★★★★★ High

**Evidence:**
- Python implementation of MCP auth patterns
- Shows OAuth flow implementation
- Research: "FastMCP demonstrates MCP security in practice"

**Reasoning:** Concrete Python code implementing concepts discussed in target.
Shows theory in action.

**Current status:** Not currently linked

---

### 7. [[csharp_mcp_auth]] → example
**Confidence:** ★★★★☆ High

**Evidence:**
- C# implementation of same patterns
- Demonstrates enterprise auth integration
- Tags: #csharp, #mcp, #authentication

**Reasoning:** Alternative language implementation showing same concepts.
Useful for enterprise/.NET developers.

**Current status:** Not currently linked

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔄 Suggested Alternatives (2)

### 8. [[zero_trust_security_model]] → alternative
**Confidence:** ★★☆☆☆ Low

**Evidence:**
- Different security paradigm
- Both address: authentication, authorization, least privilege
- Research: "Zero trust can be applied to MCP deployments"

**Reasoning:** Alternative security philosophy applicable to MCP.
Different approach to similar goals.

**Current status:** Not currently linked

---

## 📊 Discovery Statistics

- **Total candidates examined:** 93 notes
- **Content matches found:** 23 notes
- **Tag overlaps found:** 15 notes
- **After filtering:** 12 high-quality suggestions
- **Confidence breakdown:**
  - High (★★★★★): 5 suggestions
  - Medium (★★★☆☆): 5 suggestions
  - Low (★★☆☆☆): 2 suggestions

## 💡 Insights

**Critical missing prerequisite:** oauth_fundamentals
This note is heavily referenced but not formally linked. High priority addition.

**Weak example coverage:** Only 0 examples currently
Consider adding fastmcp_authentication and csharp_mcp_auth to show practical application.

**Architecture relationship:** Currently listed as prerequisite
Should be "extends" relationship - security is layer on architecture.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 6. User Review and Approval

**Offer interaction modes:**

```
How would you like to proceed?

[A] Accept all high-confidence suggestions (★★★★★)
[R] Review each suggestion individually
[C] Custom selection (specify which to add)
[S] Save suggestions to file for later review
[Q] Quit without changes

Choice: █
```

**If user chooses [R] (Review):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Review 1 of 12

Add [[mcp_overview]] as prerequisite?

Confidence: ★★★★★ High
Evidence: Referenced 3 times, foundational concept
Reasoning: Must understand MCP basics before security

[Y] Yes, add this relationship
[N] No, skip this one
[E] Edit relationship type (suggest different type)
[?] Show full context from both notes
[S] Skip remaining and finish

Choice: █
```

**Track decisions:**
- Accepted relationships
- Rejected relationships (with reasons)
- Modified relationships (type changes)

## 7. Update Knowledge Graph

**For each accepted relationship:**

### Update JSON Structure

**Add forward relationship:**
```json
{
  "notes": {
    "mcp_security.md": {
      "relationships": {
        "prerequisites": [
          {"note": "mcp_overview.md", "why": "Must understand MCP basics first"},
          {"note": "oauth_fundamentals.md", "why": "OAuth is primary auth mechanism"}
        ]
      }
    }
  }
}
```

**Add bidirectional inverse:**
```json
{
  "notes": {
    "mcp_overview.md": {
      "relationships": {
        "extended_by": [
          {"note": "mcp_security.md", "why": "Security layer on MCP protocol"}
        ]
      }
    }
  }
}
```

**Update metadata:**
```json
{
  "metadata": {
    "version": "17.0",  // Increment
    "total_notes": 93,   // Same
    "last_expansion": "2025-10-11",
    "last_expansion_note": "mcp_security.md"
  }
}
```

### Sync to Markdown Files

**Update target note's "Related Concepts" section:**
- Read current section
- Add new relationships in proper subsections
- Maintain existing relationships
- Sort alphabetically within each subsection

**Update related notes' "Related Concepts" sections:**
- Add inverse relationships
- Maintain bidirectionality
- Don't duplicate existing entries

**Use Edit tool for surgical updates**

## 8. Provide Completion Report

```markdown
✅ Graph Expansion Complete!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Changes Applied

### mcp_security.md

**Added relationships:**
✅ Prerequisites: 2
   - [[mcp_overview]] - Must understand MCP basics first
   - [[oauth_fundamentals]] - OAuth is primary auth mechanism

✅ Related concepts: 3
   - [[enterprise_architecture]] - Parallel enterprise concerns
   - [[api_security_best_practices]] - General API security principles
   - [[fastmcp_authentication]] - Moved from suggested examples

✅ Extends: 1 (modified)
   - [[mcp_architecture]] - Changed from prerequisite to extends

✅ Examples: 2
   - [[fastmcp_authentication]] - Python implementation
   - [[csharp_mcp_auth]] - C# implementation

**Rejected:**
❌ [[zero_trust_security_model]] - User declined (too tangential)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Bidirectional Updates

Updated 9 additional notes with inverse relationships:
- mcp_overview.md → added to extended_by
- oauth_fundamentals.md → added to extended_by
- enterprise_architecture.md → added to related_concepts
- api_security_best_practices.md → added to related_concepts
- mcp_architecture.md → moved to extended_by (from prerequisite inverse)
- fastmcp_authentication.md → added to extended_by
- csharp_mcp_auth.md → added to extended_by

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Knowledge Graph Stats

**Before expansion:**
- Version: 16.0
- Total relationships: 247

**After expansion:**
- Version: 17.0
- Total relationships: 263 (+16)
- Files modified: 10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Quality Improvements

🎯 **Closed gaps:**
   - Connected heavily-referenced OAuth concepts
   - Added missing example implementations
   - Corrected architecture relationship type

📈 **Coverage increase:**
   - Prerequisites: 2 → 4 (+100%)
   - Examples: 0 → 2 (new coverage)
   - Related: 3 → 6 (+100%)

🔗 **Network density:**
   - mcp_security.md now has 12 total relationships (was 6)
   - Better integrated into knowledge graph

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Next Steps

💡 **Suggestions:**
1. Run `/learning-path mcp_security` to see updated prerequisite chain
2. Run `/expand-graph oauth_fundamentals` to enrich that critical note
3. Run `/validate-graph` to verify all bidirectional links

🔄 **Consider expanding:**
- fastmcp_authentication.md (added as example, may need more connections)
- csharp_mcp_auth.md (added as example, may need more connections)

📊 **Graph health:**
✅ All relationships bidirectional
✅ No orphaned nodes created
✅ Relationship types semantically appropriate
```

## 9. Handle Edge Cases

**No new relationships found:**
```
✅ Graph Analysis Complete

No new high-confidence relationships discovered for mcp_security.md

**Current coverage:**
- Prerequisites: 3 (comprehensive)
- Related concepts: 5 (well-connected)
- Extends: 1 (appropriate)
- Examples: 2 (good coverage)
- Alternatives: 1 (adequate)

**Analysis:**
- 93 notes examined
- 0 high-confidence matches found
- This note appears well-integrated

💡 This is actually good news - the note is already well-connected!
```

**Conflicting relationships:**
```
⚠️ Potential Conflict Detected

[[mcp_architecture]] appears as both:
- Prerequisite (current)
- Should extend (suggested)

**Analysis:**
A note cannot both be a prerequisite AND be extended by the same note.

**Recommendation:**
Change to "extends" because:
- Security is specialized layer on architecture
- "extends" captures that security builds upon architecture
- Prerequisites should be for foundational knowledge

**Action:**
[Y] Accept recommendation (change to extends)
[N] Keep as prerequisite
[?] Explain difference between prerequisite and extends

Choice: █
```

**Circular dependency risk:**
```
⚠️ Circular Dependency Warning

Adding [[note_a]] as prerequisite would create cycle:
  mcp_security → oauth_fundamentals → mcp_implementation → mcp_security

**Options:**
1. Don't add this relationship
2. Add as "related" instead of "prerequisite"
3. Review and break the existing cycle

Recommended: Option 2 (related instead)

Choice: █
```

## 10. Important Notes

**Quality principles:**
- Evidence over guessing
- Confidence scoring for transparency
- User control over changes
- Bidirectional integrity always
- Clear reasoning for every suggestion

**Performance considerations:**
- Grep can search 93 notes quickly
- Perplexity queries in parallel where possible
- Cache concept extractions
- Filter aggressively before showing to user

**User experience:**
- Make suggestions actionable
- Provide escape hatches
- Allow customization
- Show clear before/after
- Celebrate improvements

Execute graph expansion for the note provided by the user.
