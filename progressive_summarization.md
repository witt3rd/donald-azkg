---
tags: [knowledge-management, method, zettelkasten, note-taking, information-processing]
---

# Progressive Summarization

A note-taking technique developed by Tiago Forte that compresses information through multiple layers of highlighting applied opportunistically over time, optimizing for future discoverability rather than upfront organization.

## Core Methodology

Progressive Summarization operates on **opportunistic compression** - you add layers of summarization each time you naturally encounter a note while working, rather than following a scheduled processing workflow. This "summarize every time you touch it" rule organically creates a collection where summarization depth corresponds directly to how integral that note is to your actual work.

### The Five Layers

**Layer 0: Original Source**

- The complete, full-length source material in its original form
- Unprocessed external content (article, book chapter, video transcript)
- Serves as reference but too dense for quick retrieval

**Layer 1: Initial Notes**

- Content captured from the source that feels insightful, interesting, or useful
- Brought into your note-taking system without rigid selection criteria
- Forms your base working material
- **Compression**: Reduces source to personally relevant passages

**Layer 2: Bold Passages**

- Most important sections within Layer 1 notes are bolded
- **Compression ratio**: Typically reduces content to ~50% of Layer 1 length
- Serves as visual anchor for faster scanning
- Enables immediate recognition of key concepts without reading every word

**Layer 3: Highlighted Excerpts**

- "Best of the best" portions from bolded Layer 2 content
- **Compression ratio**: In Forte's example, 373 words (Layer 1) → 181 words (Layer 2) → 60 words (Layer 3)
- **Speed improvement**: 6-12x faster consumption than original Layer 1
- Can be scanned in 10-20 seconds vs. 2 minutes for full notes

**Layer 4: Summary/Remix** (Optional)

- Original synthesis that transforms excerpts into your own expression
- Executive summary, outline, or remix of core ideas
- Fully internalized knowledge in your voice
- Suitable for sharing or direct use in writing

## Design Philosophy

### Discoverability as Primary Goal

The compression creates visual hierarchies that allow you to assess a note's importance at a glance without reading words - simply by observing how many formatting layers it contains. Notes that prove repeatedly useful naturally accumulate more layers, while less relevant material remains at Layer 1 or 2.

### General Purpose Summarization

The technique addresses a fundamental challenge: **how to make information discoverable without knowing what your future self will need**. You prepare notes without predetermined use cases, creating an "archipelago of islands" that reveals your personal information landscape rather than a "dense jungle" where insights remain hidden.

### Alliance Between Present and Future Self

Your present self pays forward insights by compressing them into easily retrievable forms, while your future self capitalizes on this prepared ammunition when needed. This pulls time-consuming but risk-free activities (reading, highlighting, summarizing) as early in time as possible, while pushing quick but risky activities (execution, decision-making, delivery) toward the future.

## Practical Implementation

### The Compression Workflow

1. **Capture** (Layer 1): Save relevant passages from source without overthinking
2. **First encounter**: Bold the most important passages (Layer 2)
3. **Second encounter**: Highlight the "best of the best" from bolded content (Layer 3)
4. **Optional synthesis**: Create executive summary in your own words (Layer 4)

Each layer is added **only when you naturally touch the note** while working on projects or searching for information - not as scheduled busywork.

### Visual Hierarchy

The formatting creates scannable structure:

- Plain text = captured but not yet prioritized
- **Bold text** = important passages
- ==Highlighted bold== = critical insights
- Dedicated summary section = fully synthesized

You can quickly scan Layer 3 highlights across multiple notes to identify relevant material, then drill down into Layer 2 or Layer 1 details only when necessary.

### Judgment Calls

Effectiveness depends on making sound decisions about what constitutes "key points" and "best of the best" content during compression. Poor highlighting choices could obscure rather than surface important insights. The technique rewards developing taste for what matters.

## Strategic Advantages

### Low Upfront Cost, High Future Value

Delivers benefits of planning and organization without significant upfront time investment. When projects fail or change direction, you retain valuable summarized notes rather than losing effort invested in elaborate organizational schemes.

### Scalable Discoverability

As your note collection grows, the multi-layered structure prevents information overload by surfacing the most compressed, highest-signal content first. The compression ratios (6-12x faster consumption) compound as your knowledge base expands.

### Technology Resilience

Unlike systems that depend on specific software features or organizational schemes, Progressive Summarization's core mechanic (layered highlighting in markdown) survives platform changes and remains readable in any text environment.

## Limitations and Constraints

### Medium-Dependent

Works best for conceptual and informational content where key insights can be extracted through highlighting. Challenges include:

- **Technical material**: Highly interdependent formulas or code requiring context may not compress effectively
- **Narrative content**: Stories where surrounding details matter resist excerpt-based compression
- **Procedural knowledge**: Step-by-step processes lose coherence when compressed

### Requires Digital Tools

Assumes note-taking tools supporting formatting like bolding and highlighting. The visual hierarchy created through formatting layers forms the core mechanism for rapid scanning. Paper-based implementations face significant constraints, though analogous methods using colored pens could approximate the effect.

### Inconsistency Risk

The technique requires consistent application of the "summarize when you touch it" principle. Inconsistent practice produces uneven compression across your collection, undermining the discoverability advantage.

## Relationship to Agentic ZKG

Progressive Summarization operates at the **content level** (how to compress individual notes), while [[knowledge_capture_workflow]] operates at the **workflow level** (what to capture and when). The two are complementary:

### Mapping to Knowledge Representation Levels

The [[knowledge_capture_workflow]] defines four **representation states** (LoD levels) that knowledge passes through. Progressive Summarization's layers map to these states:

**Forte Layer 0** = **LoD Level 0: Raw Signal**

- Identical: Both represent the unprocessed original source material

**Forte Layers 1-3** = **LoD Level 1: Extracted Content**

- All three layers (initial notes, bold passages, highlighted excerpts) remain in the original author's framing
- They differ in **compression degree** (Layer 3 is 6-12x faster to scan than Layer 1)
- But the **representation state** is the same: extracted content, not yet synthesized

**Forte Layer 4** = **LoD Level 2: Synthesized Knowledge**

- First time content transforms into YOUR voice and mental model
- "Executive summary, outline, or remix of core ideas... in your voice"
- Represents internalized understanding, not just compressed excerpts

**Graph Integration** = **LoD Level 3: Integrated Context**

- Positioning synthesized knowledge within the knowledge graph
- Adding typed bidirectional relationships
- Making knowledge discoverable and composable for LLM tasks

### The Critical Insight

Progressive Summarization Layers 1-3 are **compression operations** (workflow), not changes in **knowledge representation** (LoD levels). They optimize extracted content for scanning but don't transform it from "someone else's thinking" to "your understanding."

That transformation happens at Layer 4, which is why it's optional in Forte's method but essential for Level 2 in the AZKG framework.

### Key Distinction

- **Progressive Summarization**: Optimizes extracted content for **human retrieval** through visual compression
- **Agentic ZKG**: Transforms knowledge through **synthesis and integration** for LLM-augmented thinking

### Complementary Strengths

- **Progressive Summarization**: Makes LoD Level 1 (extracted content) scannable and future-proof
- **Agentic ZKG**: Provides the framework for moving content through LoD Levels 2-3 (synthesis → integration)

## Best Practices

1. **Don't force it**: Only add layers when you naturally encounter the note, not on a schedule
2. **Trust future judgment**: Your present self doesn't need to predict all future uses - just highlight what stands out now
3. **Compress progressively**: Don't try to jump straight to Layer 3 on first read
4. **Use formatting consistently**: Establish clear visual distinction between layers
5. **Preserve context**: Ensure highlighted excerpts remain coherent enough to understand standalone
6. **Accept unevenness**: Not all notes will reach Layer 3 - that's intentional and reveals actual utility

## Related Concepts

### Related Topics

- [[knowledge_capture_workflow]] - Workflow-level decisions about what to process and when
- [[agentic_zkg]] - The paradigm for building LLM-ready knowledge graphs
- [[zettelkasten]] - Atomic note-taking methodology that inspired this approach

### Extends

- [[note_taking_methods]] - (future note) Broader context of note-taking approaches

### Alternatives

- [[cornell_method]] - (future note) Structured note-taking with cue column
- [[outline_method]] - (future note) Hierarchical organization

### Examples

- [[obsidian_highlighting_workflow]] - (future note) Implementation in Obsidian
- [[markdown_layer_formatting]] - (future note) Markdown conventions for layers

## References

[1] <https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/>
[2] <https://fortelabs.com/blog/progressive-summarization-ii-examples-and-metaphors/>
[3] <https://fortelabs.com/blog/progressive-summarization-iii-guidelines-and-principles/>
[4] <https://hackmd.io/@_6snqgesSRWI1ygKSv1TtA/prog-sum-doc>
