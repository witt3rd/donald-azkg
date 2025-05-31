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

## What to Avoid

- Bullet lists and marketing speak ("revolutionary," "game-changing")
- Vague advice without specifics ("use good design principles")
- Long code listings that duplicate the codebase
- Hype, superlatives, and sensationalism
- Academic prose disconnected from practice

## Structure Template

Each chapter follows this implicit question-answering structure (remember: never state the questions explicitly):

1. **Opening Hook**: Start with a scenario or statement that implicitly poses the chapter's question
2. **Conceptual Framework**: Provide the theoretical foundation needed to understand the answer
3. **Practical Answer**: Demonstrate the solution through implementation
4. **Deep Exploration**: Address complexities and edge cases
5. **Verification**: Exercises that confirm understanding
6. **Resolution**: Summarize what was accomplished (the implicit answer)
7. **Bridge**: Connect to the next chapter's territory

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
