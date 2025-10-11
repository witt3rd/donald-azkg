---
tags: [meta, system, reference]
---

# Tag System Catalog

This is the living reference for the tag system used throughout this repository. Tags enable multi-dimensional discovery across the knowledge network.

**Purpose:** Maintain a consistent, evolving taxonomy that enables powerful cross-domain discovery while avoiding tag proliferation.

**Maintenance:** When adding a new tag, add it here with description and examples. When a tag becomes obsolete or redundant, document the deprecation.

## Tag Dimensions

Our tagging system uses six dimensions that can be mixed to create rich, discoverable metadata.

### 1. Technology/Language

Primary programming languages and platforms.

| Tag | Description | Use When |
|-----|-------------|----------|
| `#python` | Python language and ecosystem | Python code, libraries, patterns |
| `#rust` | Rust language and ecosystem | Rust code, cargo, ownership patterns |
| `#typescript` | TypeScript/JavaScript | TS/JS code, Node.js, web development |
| `#javascript` | Pure JavaScript contexts | When specifically about JS not TS |
| `#cpp` | C++ language | C++ code, CMake, compilation |
| `#csharp` | C# language | C# code, .NET development |
| `#dotnet` | .NET platform | .NET framework, runtime, tooling |
| `#powershell` | PowerShell scripting | Windows automation, scripts |

### 2. Framework/Tool

Specific frameworks, libraries, and tools.

| Tag | Description | Use When |
|-----|-------------|----------|
| `#mcp` | Model Context Protocol | MCP servers, protocol, implementations |
| `#react` | React framework | React components, hooks, patterns |
| `#vite` | Vite build tool | Build configuration, dev server |
| `#tailwind` | Tailwind CSS | Styling, utility classes |
| `#burn` | Burn ML framework (Rust) | ML in Rust, tensor operations |
| `#cargo` | Rust package manager | Rust dependencies, builds |
| `#node` | Node.js runtime | Node-specific features, npm |
| `#obsidian` | Obsidian note-taking | Obsidian features, plugins, workflow |
| `#cmake` | CMake build system | C++ project configuration |
| `#onnx` | ONNX runtime/format | Model inference, cross-platform ML |

### 3. Domain/Discipline

What the note is fundamentally about.

| Tag | Description | Use When |
|-----|-------------|----------|
| `#agents` | AI agent systems | Agent architecture, reasoning, tools |
| `#llm` | Large Language Models | LLM APIs, prompting, inference |
| `#ml` | Machine Learning (general) | Training, models, algorithms |
| `#ai` | Artificial Intelligence (broad) | AI concepts, systems, applications |
| `#windows` | Windows platform | Windows-specific development, APIs |
| `#web` | Web development | Browsers, HTTP, web standards |
| `#cli` | Command-line interfaces | Terminal tools, CLI design |
| `#gpu` | GPU computing | GPU acceleration, CUDA, compute |
| `#math` | Mathematics | Mathematical concepts, theory |
| `#writing` | Writing and authoring | Technical writing, documentation |
| `#social-media` | Social media | Content strategies, platforms |

### 4. Content Type

How to use this note.

| Tag | Description | Use When |
|-----|-------------|----------|
| `#api` | API reference | API documentation, endpoints, methods |
| `#reference` | Reference documentation | Complete reference material |
| `#guide` | How-to guide | Step-by-step instructions |
| `#pattern` | Design pattern | Reusable solution pattern |
| `#strategy` | Strategic approach | High-level strategy, methodology |
| `#concept` | Conceptual explanation | Understanding a concept |
| `#framework` | Conceptual framework | Mental model, thinking tool |
| `#tutorial` | Tutorial/walkthrough | Learning-focused guide |
| `#specification` | Formal specification | Standards, protocols, specs |
| `#template` | Template/boilerplate | Reusable code or document template |

### 5. Cross-cutting Themes

Concepts that span multiple domains and technologies.

| Tag | Description | Use When |
|-----|-------------|----------|
| `#async` | Asynchronous programming | Async/await, promises, concurrency |
| `#optimization` | Performance optimization | Speed, efficiency, profiling |
| `#security` | Security concerns | Authentication, encryption, safety |
| `#testing` | Testing and QA | Tests, test patterns, quality |
| `#performance` | Performance topics | Benchmarking, speed, resource use |
| `#architecture` | System architecture | Design, structure, components |
| `#protocol` | Communication protocols | Standards, specifications, formats |
| `#embedding` | Vector embeddings | Semantic search, RAG, embeddings |
| `#prompting` | Prompt engineering | LLM prompts, prompt patterns |
| `#deployment` | Deployment and ops | Production, CI/CD, infrastructure |

### 6. Method/Thinking

Cognitive tools and analytical approaches.

| Tag | Description | Use When |
|-----|-------------|----------|
| `#first-principles` | First principles thinking | Breaking down to fundamentals |
| `#systems-thinking` | Systems thinking approach | Holistic analysis, feedback loops |
| `#zettelkasten` | Zettelkasten method | Note-taking, knowledge management |
| `#question-decomposition` | Breaking down questions | Analysis through questioning |
| `#socratic` | Socratic method | Dialogue, critical questioning |
| `#meta` | Meta-level (about the system itself) | Documentation about documentation |

## Tagging Guidelines

### How Many Tags?

- **Minimum:** 3 tags (technology + domain + content type)
- **Optimal:** 4-5 tags (adds cross-cutting theme or method)
- **Maximum:** 6 tags (beyond this, tags lose discriminating power)

### Combining Dimensions

Good tagging mixes dimensions to enable rich discovery:

**Example: `python_mcp_sdk.md`**
```yaml
tags: [python, mcp, api, reference, agents, sdk]
```
- Technology: `#python`
- Framework: `#mcp`
- Content Type: `#api`, `#reference`
- Domain: `#agents`
- Tool: `#sdk`

**Example: `writing_strategy_first_principles.md`**
```yaml
tags: [writing, strategy, first-principles, guide, method]
```
- Domain: `#writing`
- Content Type: `#strategy`, `#guide`
- Method: `#first-principles`, `#method`

### Tag Naming Conventions

1. **Lowercase only** - `#python` not `#Python`
2. **Hyphens for multi-word** - `#first-principles` not `#firstprinciples` or `#first_principles`
3. **Singular form** - `#agent` not `#agents` (exception: when plural is the standard term)
4. **Specific over generic** - `#mcp` better than `#protocol` when appropriate
5. **No abbreviations** unless standard - `#api` ✅, `#ml` ✅, `#perf` ❌

## Evolution and Maintenance

### Adding New Tags

When a new topic area emerges:

1. **Check for existing tags** - Can an existing tag serve this purpose?
2. **Add to appropriate dimension** - Which dimension does it belong to?
3. **Document here** - Add description and use cases
4. **Apply consistently** - Update related notes with the new tag

### Deprecating Tags

When tags become redundant or unused:

1. **Mark as deprecated** - Add `[DEPRECATED]` prefix
2. **Provide migration path** - Which tag replaces it?
3. **Update notes** - Migrate old notes to new tags
4. **Remove after migration** - Clean up after all notes updated

### Tag Relationships

Some tags often appear together:

- `#mcp` commonly pairs with `#python`, `#csharp`, `#typescript`, `#agents`
- `#llm` commonly pairs with `#api`, `#prompting`, `#agents`
- `#writing` commonly pairs with `#strategy`, `#guide`, `#method`
- `#optimization` commonly pairs with technology tags and `#performance`

## Query Examples

Powerful queries enabled by multi-dimensional tagging:

| Query | Finds |
|-------|-------|
| `#mcp` | All MCP-related notes across languages and implementations |
| `#python AND #llm` | Python-specific LLM integration |
| `#pattern` | All patterns across Rust, React, writing, agents |
| `#api AND #reference` | Complete API references |
| `#guide AND #async` | Guides about asynchronous programming |
| `#writing AND #strategy` | Writing strategies and methodologies |
| `#first-principles` | All first principles analyses across domains |
| `#agents AND #architecture` | Agent system architectures |

## Meta Notes

- **Created:** 2025-10-11
- **Last Updated:** 2025-10-11
- **Status:** Living document - continuously evolving
- **Owner:** Repository maintainer

## Related Concepts

- [[README]] - Overall repository philosophy and organization
- [[obsidian_workflow]] - How to use Obsidian features with this tag system (future)

## References

- [Obsidian Tag Best Practices](https://help.obsidian.md/Editing+and+formatting/Tags)
- [Zettelkasten Tag Strategy](https://zettelkasten.de/introduction/)
