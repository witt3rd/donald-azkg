---
tags: [writing, style-guide, technical-writing, citations, methodology, best-practices]
---

# Writing Style Guide

## Core Philosophy: Question Orientation (Planning Framework)

**IMPORTANT: This is a structural planning strategy only. Never explicitly state questions in the actual text.**

Knowledge is the correct answer to a question. A book imparts knowledge by answering questions. Therefore, structure the entire book as an implicit hierarchy of questions and answers:

- **Book Question**: What overarching problem does this book solve? (The book is the answer)
- **Chapter Questions**: What specific aspects support the book's answer? (Each chapter answers one)
- **Section Questions**: What details support the chapter's answer? (Each section answers one)
- **Paragraph Questions**: What evidence or examples support the section's answer?

Every piece of content should answer a clear question that readers have or should have. If you cannot identify the question a paragraph answers, rewrite or remove it. However, the questions remain implicit—they guide your planning and ensure focused content, but are never written in the text.

**Paul Graham's style naturally embodies this approach**: He answers questions so directly and completely that readers understand both the question and answer without either being explicitly stated. This is the ideal implementation of question orientation.

## Writing Principles

**Engagement Through Implicit Questions**
Hook readers by presenting scenarios that naturally raise questions in their minds. Instead of asking "How do you build an AI agent that adapts to new models?", start with "Every time OpenAI releases a new model, thousands of developers scramble to rewrite their orchestration code." The question is implicit but urgent and personal.

**Precision Over Padding**
Write like _Clean Code_: "Functions should do one thing." Avoid overused phrases ("delve into," "crucial," "key takeaway"). Every sentence must serve the question being answered. Cut ruthlessly.

**Show, Don't Just Tell**
Balance concepts with minimal, pointed examples. Use short code snippets or pseudocode that reinforce the answer. Reference full implementations in the codebase rather than including long listings. Production-ready examples with error handling demonstrate real-world application.

**Explain the Why**
Answer not just "what" but "why." _Clean Code_ doesn't just say "use meaningful names"—it explains how poor names create bugs and confusion. Context makes advice compelling and memorable.

**Conversational Authority**
Write with the confidence of _The Pragmatic Programmer_ but avoid academic dryness. Use metaphors ("broken windows") and analogies that stick. Inject personality without losing professionalism.

**Author's Voice and Personality (Paul Graham Style)**
Write in Paul Graham's distinctive style: conversational but precise, building arguments through clear reasoning, never afraid to challenge conventional wisdom. Start with a strong, declarative statement that frames the problem. Present options systematically, dismissing the broken ones with clear reasoning. Use concrete analogies that illuminate rather than decorate ("like buying a flying car in 1950"). State strong opinions as facts when backed by evidence. Build to a clear solution without unnecessary transitions or hedging.

**Example Transformation:**
Raw information:

- Teaching LLMs has limited methods with various tradeoffs
- Initial training is expensive but foundational
- Finetuning struggles with retrieval
- Online learning's future is uncertain
- In-context learning is the practical path
- RAG retrieves too much data, clogging context windows

Paul Graham style:
"If you want to teach an LLM something, you have exactly four options, and three of them are broken. Initial training works but costs millions. Finetuning sort of works but can't reliably retrieve what you taught it. Online learning might work someday, but betting on it now is like buying a flying car in 1950. That leaves in-context learning. This is the only method that consistently works, which is why everyone uses it. The standard approach is RAG—you store information in a database and retrieve it when needed. Sounds reasonable, right? Wrong. RAG systems are dumb. They retrieve everything that might be relevant, filling your limited context window with noise."

## References and Citations

**MANDATORY REQUIREMENT**: All research must be conducted using official, original, primary sources only. Secondary sources, aggregated content, and interpretive articles are prohibited unless the interpretation itself is the subject of study.

**Format**: Use IEEE-style numbered citations for technical credibility while maintaining readability.

**Organization**: Per-chapter references work best for technical books—readers can easily find sources relevant to specific topics without scrolling through a massive bibliography.

**Acceptable Source Types and Standards**:

- **Academic Papers**: Peer-reviewed journals, conference proceedings, arXiv preprints with full IEEE format and DOI
- **Official Documentation**: Framework docs, API references, official guides from the creating organization
- **Primary Research Reports**: Company research papers, official technical reports, whitepapers from source organizations
- **Official GitHub Repositories**: Original repositories with specific commit hashes or release tags
- **Official Company Announcements**: Press releases, blog posts from official company channels
- **Government/Standards Body Publications**: Technical standards, regulatory documents, official statistics

**PROHIBITED Sources**:

- Secondary analysis or interpretation articles (unless analyzing the interpretation itself)
- Aggregated statistics without primary source attribution
- "Best of" lists or comparison articles
- Tutorial or "how-to" content that interprets original sources
- Wikipedia or other crowd-sourced content
- News articles reporting on technical developments (cite the original source instead)

**Citation Style Examples**:

- Academic: [1] J. Smith, "Large Language Model Scaling Laws," _Nature Machine Intelligence_, vol. 4, pp. 123-135, 2024. DOI: 10.1038/s42256-024-0123-4
- Official Documentation: [2] OpenAI, "GPT-4 API Reference," OpenAI Documentation, v1.2.3, Dec. 2024. [Online]. Available: <https://platform.openai.com/docs/api-reference>
- Repository: [3] Microsoft, "AutoGen Framework," GitHub repository, commit a1b2c3d, 2024. [Online]. Available: <https://github.com/microsoft/autogen/tree/a1b2c3d>
- Company Report: [4] OpenAI, "GPT-4 Technical Report," OpenAI Research, Mar. 2024, pp. 15-23. [Online]. Available: <https://openai.com/research/gpt-4>

**Mandatory Source Verification Requirements**:

- **Every quantitative claim** must cite the original data source, not secondary reporting
- **Framework capabilities** must reference official documentation, not third-party tutorials
- **Performance benchmarks** must cite the original benchmark study or official evaluation
- **Industry statistics** must cite primary research organizations, government sources, or company reports
- **Version numbers and features** must reference official changelogs, documentation, or release notes
- **Code examples** must reference specific commits or releases in official repositories

**Chapter Reference Format - FINAL SECTION REQUIREMENT**:
Every chapter MUST end with a "References" section as the absolute final section. This section lists all citations in IEEE numbered format. Keep URLs current and prefer permanent links (DOIs, archived versions, specific commit hashes) when possible. No content may appear after the References section.

## What to Avoid

- Bullet lists and marketing speak ("revolutionary," "game-changing")
- Vague advice without specifics ("use good design principles")
- Long code listings that duplicate the codebase
- Hype, superlatives, and sensationalism
- Academic prose disconnected from practice
- **Title case in subheadings**: All subheadings (h2+) must use sentence case, not title case with every word capitalized
- **Unsupported claims**: Every statistic, framework capability, or performance metric needs a citation to original, official sources
- **Secondary sources**: Never cite interpretive articles, tutorials, or aggregated content when primary sources are available

## Structure Template

Each chapter follows this implicit question-answering structure (remember: never state the questions explicitly):

1. **Opening Hook**: Start with a scenario or statement that implicitly poses the chapter's question
2. **Publisher Learning Objectives**: End the chapter introduction with a "In this chapter, you'll..." section that accurately reflects what the reader will learn and accomplish (this is a structural requirement of the publisher)
3. **Conceptual Framework**: Provide the theoretical foundation needed to understand the answer
4. **Practical Answer**: Demonstrate the solution through implementation
5. **Deep Exploration**: Address complexities and edge cases
6. **Exercises**: Hands-on activities that confirm understanding
7. **Chapter Summary**: Summarize what was accomplished (the implicit answer) and implicitly bridge to the next chapter
8. **References**: IEEE-style numbered citations for all sources used in the chapter

**CRITICAL Structure Requirements:**

- Exercises always come before the chapter summary
- Chapter summary comes before references
- **References MUST be the absolute final section of every chapter—no exceptions**
- The bridge to the next chapter is implicit within the summary—never use explicit "Bridge to Chapter X" headings
- The summary should naturally raise interest in the next chapter's topic without forced transitions
- **Every quantitative claim, framework version, or performance metric must cite original, official sources**
- **All research must be conducted using primary sources only**

## Examples from Top Books

- **_Clean Code_**: "How do you write maintainable code?" Answers with specific practices and before/after examples.
- **_Design Patterns_**: "How do you solve recurring design problems?" Answers with structured pattern solutions.
- **_The Pragmatic Programmer_**: "How do you become a better developer?" Answers with practical tips and memorable metaphors.

Each book succeeds because it clearly answers important questions that practitioners face.

## Quality Check

Before publishing any section, ask:

1. What question does this answer?
2. Is this the most direct answer possible?
3. Does this support the larger question hierarchy?
4. Would a busy practitioner find this immediately useful?

If any answer is unclear, revise until the question-answer relationship is obvious.

## Chapter Scaffolding Process

**From Notes to Research-Ready Scaffold**

The progression from book-level planning to chapter-level scaffolding follows a systematic question-oriented approach:

### Step 1: Extract the Chapter Question

From chapter notes, identify the core question the chapter must answer. For Chapter 1:

- **Note**: "Why do current frameworks fail at scale?"
- **Scaffold Purpose**: Demonstrate the orchestration trap through real failure cases

### Step 2: Map Question-Answer Structure

Transform the implicit question into the seven-part structure:

1. **Opening Hook**: Create scenario that raises the question (GPT-5 scramble)
2. **Context**: Theoretical foundation (evolution mismatch)
3. **Answer**: Concrete demonstration (anatomy of framework failure)
4. **Exploration**: Complexities and real costs
5. **Exercises**: Activities to confirm understanding
6. **Chapter Summary**: What was accomplished and implicit bridge to next chapter's question territory
7. **References**: IEEE-style citations for all quantitative claims and sources

### Step 3: Insert Research Markers

Clearly mark where specific research is needed before writing, with emphasis on primary source requirements:

- `[Research: Specific examples of framework breaks with major model releases - requires official changelogs and release notes]`
- `[Research: Timeline of LLM capability evolution vs framework design assumptions - requires original research papers and official announcements]`
- `[Research: Framework version churn statistics and migration costs - requires official repository data and primary survey research]`

This approach separates scaffold creation from content research, allowing focused work on structure first, then targeted information gathering from official, primary sources only.

### Step 4: Maintain Paul Graham Style Framework

Ensure each section answers its implicit question with:

- Strong declarative openings
- Clear reasoning progression
- Concrete examples over abstract concepts
- Dismissal of broken approaches with evidence
- Building toward clear solutions

### Step 5: Include Practical Elements

For technical books, add:

- Development environment setup (first chapter)
- Hands-on exercises that reinforce concepts
- Code examples that support the answer
- Bridge sections that naturally raise the next question

**Result**: A complete scaffolding that transforms chapter notes into a research-ready structure. Each section knows exactly what question it answers, what research it needs, and how it supports the larger chapter argument.

**Meta-Learning**: This process scales from chapter level to section level to paragraph level. The question-oriented approach provides consistent structure at every granularity, ensuring focused, useful content throughout.


## Related Concepts

### Related Topics

- [[role_technical_author]] - Style guide supports technical author role
- [[strategy_first_principles]] - Both emphasize reasoning from fundamentals