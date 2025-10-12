# Learning Path

Generate an optimal learning sequence for a target note by tracing prerequisite chains through the knowledge graph.

## 1. Parse Input

**Input format:** User provides:
- A note name: `/learning-path mcp_security.md`
- Or just the topic: `/learning-path mcp_security`

**Normalize input:**
- Add `.md` extension if missing
- Use Glob to verify the target note exists
- If not found, suggest similar notes using Glob

## 2. Load Target Note

**Read the target note:**
- Use Read tool to get full content
- Extract YAML tags and title
- Parse "Related Concepts" section to get prerequisites

**Example:**
```markdown
## Related Concepts

### Prerequisites
- [[mcp_overview]] - Must understand MCP basics first
- [[oauth_fundamentals]] - OAuth is primary auth mechanism

### Related Topics
- [[api_security]] - General API security principles
```

## 3. Trace Prerequisite Chains

**Algorithm: Depth-First Traversal**

Starting from the target note, recursively follow prerequisite relationships:

```
function buildPrerequisiteTree(note, visited = new Set()):
  if note in visited:
    return []  // Cycle detection

  visited.add(note)

  // Read the note and parse "Related Concepts" → "Prerequisites"
  prerequisites = readNote(note).prerequisites

  if prerequisites is empty:
    return [note]  // Foundation reached

  tree = []
  for prereq in prerequisites:
    subtree = buildPrerequisiteTree(prereq.note, visited)
    tree.extend(subtree)

  tree.append(note)
  return tree
```

**Implementation with tools:**
1. **Read** target note to get prerequisites
2. For each prerequisite, **Read** that note to get its prerequisites
3. Recursively traverse until reaching foundation notes (no prerequisites)
4. Track visited nodes to detect cycles

**Key features:**
- **Cycle detection:** Track visited nodes to prevent infinite loops
- **Multiple paths:** Handle notes with multiple prerequisites
- **Foundation detection:** Identify notes with no prerequisites
- **Depth tracking:** Calculate how many levels deep each note is

## 4. Build Learning Sequence

**Create ordered learning path:**

1. **Topological sort:** Order notes so prerequisites always come before dependents
2. **Remove duplicates:** Each note appears once, at earliest possible position
3. **Group by depth level:** Show conceptual layers

**Example structure:**
```
Level 0 (Foundations):
- note_a.md
- note_b.md

Level 1 (Builds on foundations):
- note_c.md (requires: note_a)
- note_d.md (requires: note_b)

Level 2 (Intermediate):
- note_e.md (requires: note_c, note_d)

Level 3 (Target):
- target_note.md (requires: note_e)
```

## 5. Read Note Summaries

**For each note in the learning path:**
- Use Read tool to get first 3-5 lines (the summary)
- Extract the brief description after the title
- This provides context for each step

**Example:**
```
## mcp_overview.md
"Introduction to Model Context Protocol, a standardized way for AI assistants to connect to data sources and tools."
```

## 6. Analyze Learning Path

**Calculate metrics:**

**Path statistics:**
- Total notes in sequence: `N`
- Depth levels: `M` (foundation to target)
- Estimated reading time: `N × 10 minutes = X minutes`
- Foundational notes: Count of level 0 notes
- Branching factor: Average prerequisites per note

**Complexity assessment:**
- **Simple path (1-3 notes):** "Quick learning path"
- **Moderate path (4-7 notes):** "Intermediate learning sequence"
- **Complex path (8+ notes):** "Comprehensive learning journey"

**Identify critical concepts:**
- Notes that multiple paths converge through
- "Bottleneck" concepts that are prerequisites for many others

## 7. Suggest Related Learning

**Enrich the path with optional content:**

**Parallel reading (Related Topics):**
- Read "Related Topics" sections from notes in path
- Notes at same level that provide additional context
- Not strictly required but enhance understanding

**Deeper dives (Extended By):**
- Read "Extended By" sections from notes in path
- Advanced topics that build on concepts in the path
- "After mastering this path, explore..."

**Alternative approaches (Alternatives):**
- Read "Alternatives" sections from notes in path
- Different ways to achieve similar understanding
- "For a different perspective, consider..."

**Practical examples (Examples):**
- Read "Examples" sections from notes in path
- Concrete implementations to solidify understanding
- "Apply these concepts with..."

## 8. Generate Output

**Format the learning path:**

```markdown
# Learning Path: [Target Note Title]

🎯 **Goal:** Understand [target topic]
📚 **Total Notes:** N notes across M levels
⏱️  **Estimated Time:** X minutes
🏗️  **Complexity:** [Simple|Moderate|Complex]

---

## Prerequisites Sequence

### Level 0: Foundations
Start here if you're new to this topic.

1. **[[note_a]]** (5 min read)
   Brief description from note.
   *Why it's needed:* Foundation for understanding [concept]

2. **[[note_b]]** (8 min read)
   Brief description from note.
   *Why it's needed:* Introduces core [concept]

### Level 1: Core Concepts
Once you understand the foundations, proceed here.

3. **[[note_c]]** (10 min read)
   Brief description from note.
   *Builds on:* note_a
   *Why it's needed:* Extends [concept] with [new idea]

4. **[[note_d]]** (7 min read)
   Brief description from note.
   *Builds on:* note_b
   *Why it's needed:* Applies [concept] to [domain]

### Level 2: Integration
Combining concepts from previous levels.

5. **[[note_e]]** (12 min read)
   Brief description from note.
   *Builds on:* note_c, note_d
   *Why it's needed:* Synthesizes [concepts] for [purpose]

### Level 3: Target Concept
Your destination!

6. **[[target_note]]** (15 min read)
   Brief description from note.
   *Builds on:* note_e
   *This is your goal:* Complete understanding of [target topic]

---

## Optional Enrichment

### Parallel Reading (Same Level)
Enhance understanding at each level:
- **[[related_a]]** - Provides additional context on [concept]
- **[[related_b]]** - Alternative perspective on [concept]

### Go Deeper (Beyond Target)
After mastering this path:
- **[[advanced_a]]** - Builds on target with [advanced concept]
- **[[advanced_b]]** - Applies target to [specific domain]

### Practical Applications
See these concepts in action:
- **[[example_a]]** - Real implementation of [concept]
- **[[example_b]]** - Case study using [concept]

### Alternative Paths
Different approaches to similar understanding:
- **[[alternative_a]]** - [Different approach] to achieving similar goals

---

## Critical Concepts

These notes are central to this learning path:
- **[[critical_note]]** - Required by X other notes in this path

---

## Visual Path

```
Foundations          Core Concepts        Integration         Target
─────────────        ─────────────        ───────────         ──────

note_a ──────────┐
                 ├──> note_c ────────┐
                 │                   │
note_b ──────────┴──> note_d ────────┴──> note_e ──> target_note
```

---

## Next Steps

1. **Start with Level 0** if concepts are new
2. **Skip familiar sections** if you have background knowledge
3. **Use `/graph-note`** to inspect relationships for each note
4. **Use `/expand-graph`** to discover more connections
5. **Review in Obsidian** for visual graph navigation

**Pro tip:** Open multiple notes in tabs and read through the sequence in order!
```

## 9. Handle Edge Cases

**No prerequisites:**
```
Learning Path: [Target Note]

✅ This note has no prerequisites!

This is a foundational concept that can be learned directly.
No background knowledge required.

**Estimated reading time:** X minutes

**What builds on this:**
After understanding this note, you can explore:
- [[note_x]] - Extends this concept
- [[note_y]] - Applies this concept
```

**Circular dependencies:**
```
⚠️ Circular Dependency Detected

The following notes form a dependency cycle:
- [[note_a]] requires [[note_b]]
- [[note_b]] requires [[note_c]]
- [[note_c]] requires [[note_a]]

**Suggested reading order:**
Read these notes together as an interconnected group:
1. [[note_a]] - Brief overview
2. [[note_b]] - Builds on understanding from note_a
3. [[note_c]] - Completes the cycle
4. Re-read all three for full understanding

**Action needed:** Consider refactoring these notes to break the cycle.
Use `/graph-validate` to check for more circular dependencies.
```

**Very long path (>15 notes):**
```
📚 Complex Learning Path Detected

This path contains N notes across M levels.

**Suggested approach:**
- Break into smaller milestones
- Focus on one level at a time
- Take breaks between levels
- Consider creating intermediate checkpoints

**Milestones:**
🎯 Milestone 1: Foundations (Notes 1-5)
🎯 Milestone 2: Core Concepts (Notes 6-10)
🎯 Milestone 3: Advanced Topics (Notes 11-15)
🎯 Milestone 4: Target Mastery (Notes 16-N)
```

## 10. Provide Summary Stats

**Output concise metrics:**

```
Learning Path Summary
━━━━━━━━━━━━━━━━━━━━━

📊 Path Metrics:
- Total notes: N
- Depth levels: M
- Estimated time: X minutes
- Foundation notes: Y
- Average prerequisites per note: Z

🎯 Complexity: [Simple|Moderate|Complex]

💡 Key Insight: [Most important observation about this path]

🔗 Critical Concept: [Note that appears most frequently as prerequisite]
```

## Tools Used

- **Read** - Get note content, parse "Related Concepts" sections, extract summaries
- **Glob** - Verify notes exist, find similar notes if target not found
- **Parse logic** - Traverse prerequisite chains, topological sort, depth calculation
- **Graph traversal** - Depth-first search with cycle detection

## Important Notes

**Quality guidelines:**
- Clear level progression
- Justify why each prerequisite is needed
- Provide time estimates (realistic reading + comprehension)
- Make path scannable with good formatting
- Include visual representation when helpful
- Handle edge cases gracefully

**User experience:**
- Make it easy to start learning immediately
- Show progress milestones
- Suggest checkpoints for complex paths
- Provide escape hatches (skip, alternative paths)
- Encourage practical application

**Graph integrity:**
- Report any issues found (cycles, broken links)
- Suggest graph improvements
- Validate prerequisite chains make semantic sense
- Use `/graph-validate` to check bidirectionality

Execute the learning path generation for the note provided by the user.
