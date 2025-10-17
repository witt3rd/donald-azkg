---
tags: [claude-code, extensibility, tools, workflow, automation]
---
# Claude Code Skills: Modular, Context-Aware Capability Extensions

**Claude Code Skills** are modular, project-local capability bundles that package instructions, scripts, templates, and resources to enable tailored workflow automation and deterministic tool execution. Skills are designed for intelligent, context-aware invocation—Claude automatically loads and executes the appropriate Skill based on user intent, task type, and metadata, without requiring explicit commands.

## What Skills Are

Skills are folder-based extensions that combine AI instructions with deterministic code execution, offering a middle ground between simple prompts and full plugin systems.

### Core Architecture

**Folder Structure**:
```
my-skill/
├── SKILL.md              # YAML frontmatter + instructions
├── scripts/              # Python, Bash, or shell scripts
│   └── process.py
├── templates/            # Output templates (Markdown, docx, etc.)
│   └── report_template.md
└── docs/                 # Optional documentation
```

**SKILL.md Format**:
```markdown
---
name: Image Editor
description: Crop, rotate, and enhance images. Use when editing images.
allowed-tools: [Pillow, Read, Write]
---

# Image Editor Skill

When invoked, analyze the image at the provided path and apply the requested transformations.

## Steps

1. Load image using Pillow
2. Apply transformations (crop, rotate, filters)
3. Save result to output path
4. Report changes made

Use scripts/edit.py for processing.
```

### Key Characteristics

**Context-Aware Activation**: Skills may be triggered automatically if their description field matches user requests or context, without explicit invocation. Claude's Skill selector relies on SKILL.md metadata (description, file path) to determine relevance.

**Progressive Context Management**: When triggered, Claude loads only the necessary Skill metadata and instructions, avoiding context bloat by referencing files on demand rather than injecting entire Skill content into the prompt context window.

**Deterministic Execution**: Workflows (parsing PDFs, generating reports, image processing) are executed via bundled scripts—typically Python, Bash, or shell commands—enabling functional augmentation beyond prompt-token operations.

**Project-Local Scoping**: Skills are discoverable by Claude when present in either per-user (`~/.claude/skills/`) or per-project (`.claude/skills/`) locations. Project-level scoping controls which Skills are available for specific codebases or repo tasks, enhancing reproducibility and auditability.

**Safe, Repeatable Execution**: Skill scripts are run deterministically by Claude, with input/output managed via safe file reads/writes or restricted tool permissions using the `allowed-tools` field.

## How Skills Work

### Execution Flow

1. **User requests task**: "Summarize code changes since last week"
2. **Claude detects relevant Skill**: Matches description to `report-generation` Skill
3. **Load instructions**: Reads SKILL.md and discovers available scripts
4. **Run script**: Executes Python script to parse `git log` using GitPython
5. **Generate output**: Produces Markdown, docx, or other format using templates
6. **Return to user**: Presents completed work in chat

### Discovery and Invocation

Skills are automatically discovered from designated directories:
- **Project Skills**: `.claude/skills/` (versioned, shared with team)
- **User Skills**: `~/.claude/skills/` (personal, not versioned)

**Automatic invocation**: Claude analyzes user intent and Skill descriptions to select appropriate Skill without explicit naming.

**Manual invocation**: Use Skill name directly if needed (though this is less common).

**Guardrails**: Ambiguous metadata or broken paths can prevent activation. Clear, specific descriptions are critical.

## Creating Custom Skills

### Step-by-Step Process

**1. Initiate Skill creation**: Request from Claude chat: "Create an image editor Skill" or manually create folder structure.

**2. Define SKILL.md**: Write clear YAML metadata with specific, actionable descriptions:
```yaml
---
name: Report Generator
description: Generate comprehensive project reports from git history and code metrics. Use for project summaries and status updates.
allowed-tools: [Read, Write, Bash, GitPython]
---
```

**3. Add supporting scripts**: Place executable code in `/scripts`:
```python
# scripts/report.py
import git
import json
from datetime import datetime, timedelta

def generate_report(repo_path, days=7):
    repo = git.Repo(repo_path)
    since = datetime.now() - timedelta(days=days)
    commits = list(repo.iter_commits(since=since))

    report = {
        'period': f'Last {days} days',
        'total_commits': len(commits),
        'authors': list(set(c.author.name for c in commits)),
        'files_changed': sum(len(c.stats.files) for c in commits)
    }
    return report
```

**4. Create templates**: Add reusable output formats in `/templates`:
```markdown
# templates/summary.md
# Project Report: {{period}}

**Generated**: {{timestamp}}

## Summary
- Total commits: {{total_commits}}
- Active contributors: {{authors}}
- Files modified: {{files_changed}}

## Details
{{commit_details}}
```

**5. Test and iterate**: Prompt with use cases; ensure correct activation and output. Verify Skill path, description specificity, and tool restrictions work as intended.

**6. Install locally**: Drop Skill folder under `.claude/skills/` in your repo; reload if necessary.

**7. Version control**: Commit Skills to repository for CI/testing and project reproducibility. Treat as code artifacts with review and testing.

### Best Practices

**Be specific in descriptions**: List capabilities and trigger context to aid Claude's matching. Vague descriptions prevent activation.

**Limit allowed-tools**: Restrict to only necessary code/files for safety and reliability. Follow principle of least privilege.

**Keep Skills project-local**: Avoid global installs unless standardized internally. No official global path exists yet.

**Test activation scenarios**: Use local and CI tests to confirm Skill selection and output correctness.

**Document instructions and examples**: Maintain clear SKILL.md content for onboarding and maintenance.

**Iterate with clear prompts**: Use Claude's chat interface or manual edits to evolve Skill functionality.

## Skills vs. Other Extension Mechanisms

| Mechanism | Format | Invocation | Complexity | Scope | Best For |
|-----------|--------|------------|------------|-------|----------|
| **Skills** | Folder+SKILL.md+scripts | Context-aware/automatic | Medium | Project/task-scoped | Repeatable task automation, context-aware extensions |
| **Slash Commands** | Markdown files | Manual (`/cmd`) | Simple prompts | Single task | Repeatable prompts, ad-hoc actions |
| **Hooks** | Code/config | Event-triggered | Scripts/automation | Event response | Automation on file changes, lifecycle events |
| **Agents** | Code/config | Manual/delegated | Multi-step workflows | Stateful process | Complex workflows, multi-agent coordination |
| **Plugins** | Bundled package | Various | Full extensions | Multiple features | Comprehensive tools, multiple extension points |
| **MCP Servers** | Persistent server/client | Networked endpoints | External process | System/service integration | Heavy computation, external system interop |

### Decision Guide

**Use Skills when:**
- Extending project-limited workflows
- Require deterministic script execution with AI orchestration
- Need context-aware triggering, not explicit commands
- Task is repeatable but requires AI judgment to coordinate
- Want to bundle related scripts, templates, and instructions together

**Use alternatives when:**
- **Simple prompts** → Slash commands (lighter weight)
- **Lifecycle automation** → Hooks (event-driven)
- **Complex stateful workflows** → Agents (multi-step reasoning)
- **Cross-project features** → Plugins (comprehensive extensions)
- **External system integration** → MCP servers (networked services)

## Common Use Cases

### Code Analysis and Reporting

**Automated code reviews**:
- Skill parses recent diffs
- Checks style against project guidelines
- Outputs annotated reports with suggestions
- Uses templates for consistent formatting

**Project report generation**:
- Summarizes repo structure, dependencies, progress
- Pulls data from git, issue trackers, code metrics
- Outputs in Markdown or docx
- Scheduled or on-demand execution

### File Processing

**PDF extraction**:
- Python script using PyPDF2 or pdfplumber
- Extracts tables, forms, text
- Structures output for downstream processing
- Template-based formatting

**Image processing**:
- On-demand crop/rotate/filter of images
- Pillow for transformations
- Batch processing support
- Output for docs or assets

### Workflow Automation

**Test suite automation**:
- Scripted test runners
- Output parsing and result templating
- Coverage analysis
- Integration with CI/CD

**Documentation generation**:
- Creates custom READMEs, changelogs, onboarding guides
- Tailored to project changes via git analysis
- Template-based consistency
- Automatic updates on code changes

## Integration with Claude Code Ecosystem

### With Plugins

Skills can be bundled as components within plugin packages:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json         # Declares skills, commands, agents, hooks
├── skills/
│   └── report-generator/
│       ├── SKILL.md
│       └── scripts/
├── commands/
└── agents/
```

Plugin manifest references Skills in the `skills` field.

### With Slash Commands

Slash commands can explicitly invoke Skills:
```markdown
# .claude/commands/generate-report.md
Use the report-generator Skill to create a project summary for the last $1 days.
```

### With Hooks

Hooks can trigger Skills at lifecycle events:
```json
{
  "hooks": {
    "PostToolUse": "Run report-generator Skill if files in src/ modified"
  }
}
```

### With Agents

Skills provide deterministic execution within agent workflows. Agents can invoke Skills for specialized tasks (image processing, PDF parsing) while maintaining overall orchestration.

### With MCP

Skills can leverage MCP servers for external data:
```markdown
# In SKILL.md
Use MCP Jira server to fetch active issues, then generate report combining git changes and issue status.
```

## Technical Considerations

### Context and Token Management

Skills enable efficient context usage:
- Only Skill metadata loaded initially
- Scripts and templates referenced on demand
- Prevents bloating main conversation context
- Summarized results returned, not full execution logs

This makes Skills particularly valuable for large codebases or complex multi-step tasks where preserving context is critical.

### Security Model

**Sandboxed execution**: Skills run in controlled environments with restricted permissions.

**Tool restrictions**: `allowed-tools` field limits what Skills can access (file system, network, specific libraries).

**Audit logging**: Skill invocations can be logged for security review.

**Code review**: Skills should be treated as code artifacts with proper review before use.

### Performance

**Lazy loading**: Skills loaded only when needed, not at startup.

**Caching**: Skill metadata cached for faster subsequent invocations.

**Async execution**: Long-running scripts can run in background while Claude continues conversation.

**Resource limits**: Skills can be configured with timeout and memory constraints.

## Current State (October 2025)

**Maturity**: Skills are stable and widely supported in Claude Code and Claude chat UI for Pro+ plans. Official templates and guides exist for common tasks, plus community examples for rapid prototyping.

**Adoption**: Most repo-level automation and intelligent file handling now leverages Skills over explicit commands/plugins for context-aware capability extension.

**Best Practices**: Scope Skills to project-specific needs, enforce guardrails via CLAUDE.md, use clear and specific Skill descriptions, and leverage version control and testing workflows for reliability and maintainability.

**Tooling**: Integrated across CLI, VS Code extension, and desktop applications. No graphical Skill manager yet, but command-line management is well-established.

**Ecosystem**: Growing collection of shared Skills in community repositories. Skill templates accelerate development of common patterns.

**Future Directions**: Enhanced parallelization, richer metadata schemas, Skill marketplace, better debugging and monitoring tools.

## Limitations and Trade-offs

### Complexity vs. Slash Commands

Skills require more setup than slash commands (folder structure, scripts, templates vs. single markdown file). Use slash commands for simple prompts; Skills for multi-file, script-driven workflows.

### Coordination vs. Agents

Skills provide deterministic execution but limited multi-step reasoning. For complex stateful workflows with branching logic, agents remain the better choice. Skills excel at well-defined, repeatable tasks.

### Discovery Ambiguity

If multiple Skills have similar descriptions, Claude may struggle to select the right one. Clear, distinct descriptions are critical. Consider namespacing or explicit invocation when needed.

### Platform Dependencies

Skills using platform-specific scripts (PowerShell on Windows, Bash on Linux) may not be portable. Test cross-platform compatibility or document platform requirements.

## Summary

Claude Code Skills represent a powerful middle ground in the extensibility spectrum:
- **Lighter than plugins** (no full package manifest, simpler distribution)
- **More structured than slash commands** (bundled scripts, templates, resources)
- **More deterministic than agents** (explicit script execution, predictable outputs)
- **More specialized than hooks** (task-focused, not lifecycle-event-driven)

Skills enable developers to create context-aware, reusable, project-scoped capabilities that combine AI orchestration with deterministic code execution. By packaging instructions, scripts, and templates together, Skills provide the right abstraction for repeatable automation tasks that benefit from Claude's intelligent coordination but require predictable, script-driven implementation.

When deciding whether to create a Skill, ask:
1. Is this task repeatable and well-defined?
2. Does it benefit from AI judgment in coordination or parameter extraction?
3. Does it require deterministic script execution (file processing, external API calls)?
4. Should it be project-scoped and version-controlled?

If yes to most of these, Skills are likely the right tool for the job.

## Related Concepts

### Prerequisites
- [[claude_code]] - Understanding Claude Code platform is essential before learning about Skills

### Related Topics
- [[claude_code_plugins]] - Skills can be bundled within plugin packages as one extension type
- [[claude_code_slash_commands]] - Slash commands are lighter-weight for simple prompts; Skills add scripts and templates
- [[claude_code_hooks]] - Hooks provide event-driven automation; Skills provide context-aware task execution
- [[claude_code_agents]] - Agents handle complex stateful workflows; Skills provide deterministic script-driven tasks
- [[claude_agent_sdk]] - Agent SDK builds production agents while Skills extend Claude Code interactively

### Extends
- [[claude_code]] - Skills extend Claude Code's capabilities through modular, context-aware automation

## References

[1] https://apidog.com/blog/claude-skills/ - Practical guide to Claude Skills
[2] https://skywork.ai/blog/how-to-use-skills-in-claude-code-install-path-project-scoping-testing/ - Project scoping and testing Skills
[3] https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills - Agent Skills architecture
[4] https://docs.claude.com/en/docs/claude-code/skills - Official Skills documentation
[5] https://www.anthropic.com/news/skills - Skills announcement
[6] https://docs.claude.com/en/api/skills-guide - Skills API guide
[7] https://simonwillison.net/2025/Oct/16/claude-skills/ - Simon Willison's analysis
