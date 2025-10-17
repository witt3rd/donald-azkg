---
tags: [api, prompting, python, development]
---
# The Case for Micro-Prompting with SLMs/SRMs

I’m optimistic about the potential of Small Language Models (SLMs) and Small Reasoning Models (SRMs) to transform how we design "agentic" programs through a technique I call **"micro-prompting."** Unlike Large Language Models (LLMs) and Large Reasoning Models (LRMs), which excel at processing large, complex prompts packed with instructions, guardrails, and context, SLMs and SRMs are better suited for the numerous discrete, modular steps that agentic workflows demand.

## Why SLMs/SRMs Shine in Agentic Workflows

Agentic programs often require breaking down tasks into smaller, logical steps—steps that traditional programming languages like C# or Python aren’t naturally equipped to handle, and that large models process inefficiently. Examples of such steps include:

- **Episodic Boundary Detection**: Is this new input related to the previous one, or is it a fresh topic?
- **Task Classification**: Is the request a question, command, or declaration?
- **Question Analysis**: If it’s a question, is it simple (single-step) or complex (multi-step)? Is it fact-based and durable (e.g., "What’s the capital of Washington?") or transient (e.g., "What’s the current weather?")?
- **Planning**: Do I have enough information to proceed?
- **Evaluation**: How good is the response? Should it be refined further?

Running these steps through cloud-based frontier models like LLMs/LRMs is high-latency and costly. Local SLMs/SRMs, however, offer a fast, cost-effective alternative, excelling at these micro-tasks while maintaining quality.

## Micro-Prompting: A New Programming Paradigm

Most current applications of LLMs/LRMs rely on massive prompts with extensive context. But the real opportunity lies in rethinking how we write programs. As Andrej Karpathy quipped, "English is the new programming language"—yet we haven’t fully embraced this shift. Micro-prompting bridges that gap.

With micro-prompting, we decompose problems into functional blocks, just as we do in traditional coding. But instead of writing functions in code, we craft **prompts**. The arguments become context, and the SLM/SRM serves as the execution engine. For instance:

- Traditional Code: `function classifyTask(input) { ... }`
- Micro-Prompting: A prompt like "Classify this input as a question, command, or declaration," executed by an SLM.

By leveraging SLMs/SRMs for each step, we improve efficiency and modularity, ultimately enhancing the overall quality of the result.

## Toward an AI-Native Future

This approach isn’t just an optimization—it’s a paradigm shift. Micro-prompting with SLMs/SRMs paves the way for a truly **AI-native operating system or platform**, where natural language drives development. It’s a natural evolution that makes AI more accessible and integral to how we build intelligent systems, aligning with the vision of language as the future of programming.

In short, SLMs/SRMs, through micro-prompting, unlock a more efficient, modular, and innovative way to create agentic programs—heralding a new era of AI-driven development.

## Related Concepts

### Related Topics

- [[llm_agents]] - Micro-prompting is designed for agentic workflows described in agents.md
- [[json_prompting]] - Both are structured approaches to prompt engineering
- [[react_agent_pattern]] - ReAct agents can use micro-prompting for decomposed reasoning steps
- [[spr]] - Both focus on efficiency in prompting - SPR via compression, micro-prompting via decomposition
- [[nvidia_small]] - Micro-prompting with SLMs for decomposed task execution

### Alternatives

- [[json_prompting]] - JSON prompting offers structured control while micro-prompting focuses on decomposition
