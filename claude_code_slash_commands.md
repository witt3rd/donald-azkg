---
tags: [claude-code, tools, extensibility, guide, cli]
---
# Claude Code Slash Commands

Custom slash commands in Claude Code are user-defined shortcuts stored as markdown files that allow developers to invoke frequently-used tasks with a simple `/command-name` syntax. They streamline workflows by executing pre-defined, repeatable prompts with optional argument interpolation, providing a lightweight extensibility mechanism between one-off prompts and full plugin systems.

## What Are Slash Commands?

Slash commands are chat shortcuts beginning with `/` that execute static or parameterized prompts. Instead of re-typing instructions, a command file defines the task and can accept arguments for flexibility. Claude Code's agentic environment parses the command, interpolates any arguments, and sends the resulting directive to the Claude model for execution.

**Key characteristics:**
- Simplest Claude Code extensibility mechanism
- Single markdown file per command
- Invoked directly via `/` in chat or terminal
- Discovered automatically from designated directories
- Can be project-specific (shared/versioned) or personal (private)

## File Structure and Format

### Directory Organization

**Project commands (shared/versioned):**
```
.claude/
  commands/
    optimize.md              # /optimize
    security-review.md       # /security-review
    posts/
      new.md                 # /posts:new
      publish.md             # /posts:publish
```

**Personal commands (private):**
```
~/.claude/
  commands/
    personal-utility.md      # Available in all projects
    quick-fix.md
```

### File Format

Commands are markdown files with optional YAML frontmatter:

```markdown
---
description: Short description of what this command does
---

# Command Instructions

Your prompt/instructions here. Use $ARGUMENTS or $1, $2, etc. for parameters.

## Additional Context

Optional: Add examples, constraints, or guidance for Claude.
```

### Argument Interpolation

**Positional arguments:**
- `$ARGUMENTS` - All arguments as single string
- `$1`, `$2`, `$3`, ... - Individual positional arguments

**Example command file** (`.claude/commands/fix-issue.md`):
```markdown
---
description: Fix bug described in GitHub issue
---

Review and fix the bug described in GitHub issue #$1.

1. Read the issue details
2. Locate the relevant code
3. Implement and test the fix
4. Suggest commit message
```

Invoked as: `/fix-issue 123` (substitutes `$1` with `123`)

### Namespace Support

Subdirectories create command namespaces:
- `.claude/commands/posts/new.md` → `/posts:new`
- `.claude/commands/deploy/staging.md` → `/deploy:staging`

Enables logical organization without name collisions.

## How They Work

### Execution Flow

1. **User invokes:** `/command-name arg1 arg2`
2. **Command discovery:** Claude Code matches command name to file
3. **Argument substitution:** Replaces `$ARGUMENTS`, `$1`, `$2` with provided values
4. **Prompt execution:** Sends interpolated content to Claude model
5. **Tool interaction:** Claude can invoke tools, read files, run bash commands as directed
6. **Result delivery:** Response returned to user in chat

### Discovery and Availability

- **Automatic scanning:** Claude Code discovers all `.md` files in command directories
- **Listing commands:** Use `/help` to see all available commands with descriptions
- **Precedence:** Project commands override personal commands with same name
- **Case sensitivity:** Command names are case-insensitive

## Use Cases

### Code Analysis and Review

```markdown
# .claude/commands/security-review.md
Review this code for security vulnerabilities and suggest fixes.
Focus on:
- Authentication and authorization
- Input validation and sanitization
- Dependency vulnerabilities
- Data exposure risks

File to review: $ARGUMENTS
```

### Workflow Automation

```markdown
# .claude/commands/deploy.md
Prepare deployment for $1 environment:

1. Run test suite
2. Check for uncommitted changes
3. Build production artifacts
4. Generate deployment checklist
5. Show recent commits since last deployment
```

### Content Management

```markdown
# .claude/commands/posts/new.md
Create new blog post with title "$ARGUMENTS":

1. Generate filename from title (lowercase, hyphens)
2. Create markdown file with frontmatter (date, title, tags)
3. Generate initial outline based on title
4. Suggest related topics to cover
```

### Team Processes

```markdown
# .claude/commands/review.md
Perform code review on $ARGUMENTS:

1. Check adherence to project style guide (see .claude/style-guide.md)
2. Identify potential bugs or edge cases
3. Suggest performance improvements
4. Verify test coverage
5. Rate code quality (1-10) with justification
```

## Best Practices

### Command Design Principles

**Naming:**
- Clear and descriptive: `/security-review` not `/check`
- Verb-first when possible: `/fix-issue`, `/generate-docs`
- Use namespaces for organization: `/project:command`, `/category:action`
- Consistent with team conventions

**Scope:**
- One command, one responsibility (atomicity)
- Keep prompts focused and specific
- Avoid "god commands" that bundle unrelated actions

**Documentation:**
- Include `description:` in frontmatter for discoverability
- Add usage examples in command file
- Document expected arguments and their formats

### Argument Handling

**Validation patterns:**
```markdown
Expected arguments: <issue-number> <severity: low|medium|high>

Validate:
- $1 must be numeric issue number
- $2 must be one of: low, medium, high

If invalid, explain correct usage and exit.
```

**Context injection:**
```markdown
Before analyzing $ARGUMENTS, gather context:
1. Run: git status
2. Run: git diff $ARGUMENTS
3. Read relevant test files
```

### When to Use Slash Commands

**Use slash commands when:**
- Task requires AI reasoning or judgment
- Prompt is reused frequently
- Arguments make prompt flexible
- Workflow benefits from discoverability
- Team needs standardized process

**Use alternatives when:**
- Task is deterministic/scriptable → Use hooks or bash scripts
- Workflow is complex/stateful → Use agents
- Multiple extension points needed → Use plugins
- One-off task → Just prompt directly

### Security Considerations

**Least privilege:**
```markdown
---
description: Deploy to staging (requires git and npm access)
allowed-tools: [git, npm, bash]
---
```

**Argument sanitization:**
```markdown
# Never do this:
Run: bash -c "deploy.sh $ARGUMENTS"

# Do this instead:
Validate $1 is valid environment (staging|production)
Then run: bash -c "deploy.sh --env $1"
```

**Permission boundaries:**
- Restrict commands that modify production systems
- Audit commands that access secrets or credentials
- Use environment-specific commands (staging vs production)

### Team Collaboration

**Shared commands:**
- Store in `.claude/commands/` (versioned)
- Peer review command additions/changes
- Document in `CLAUDE.md` or `README.md`
- Establish naming conventions

**Personal commands:**
- Store in `~/.claude/commands/` (not versioned)
- Useful for experimenting before proposing to team
- Customize workflows without impacting others

**Version control:**
- Commit all project command files
- Treat as code artifacts (review, test, refactor)
- Track changes for rollback capability

### Performance and Efficiency

**Keep prompts focused:**
```markdown
# Too verbose:
Analyze the file provided in the arguments. Look at each function carefully.
Check for bugs, performance issues, security problems, and style violations.
Generate a comprehensive report with detailed findings and suggestions.

# Better:
Analyze $ARGUMENTS for: bugs, performance, security, style.
Report issues with severity and suggested fixes.
```

**Reusable patterns:**
```markdown
# .claude/commands/analyze.md
Analyze $1 focusing on $2:
- $2=bugs: Logic errors, edge cases, error handling
- $2=perf: Bottlenecks, algorithmic complexity, resource usage
- $2=security: Vulnerabilities, input validation, auth issues
```

### Maintenance Strategies

**Testing:**
- Document expected behavior in comments
- Test with sample inputs periodically
- Update when tools or workflows change

**Refactoring:**
- Split complex commands into smaller ones
- Deprecate superseded versions
- Update documentation on changes

**Hygiene:**
- Remove obsolete commands
- Consolidate duplicates
- Keep command files short and focused

## Comparison to Other Mechanisms

| Feature | Slash Commands | Hooks | Agents | Plugins |
|---------|----------------|-------|--------|---------|
| **Format** | Markdown files | Code/config | Code/config | Bundled package |
| **Invocation** | Manual (`/cmd`) | Event-triggered | Manual/delegated | Various |
| **Complexity** | Simple prompts | Scripts/automation | Multi-step workflows | Full extensions |
| **Scope** | Single task | Event response | Stateful process | Multiple features |
| **Discovery** | `/help` menu | Config files | Manifest | Plugin manager |
| **Best for** | Repeatable prompts | Automation | Complex workflows | Comprehensive tools |

**Decision guide:**
- **Simple, repeatable AI task** → Slash command
- **Deterministic automation** → Hook
- **Complex, stateful workflow** → Agent
- **Multiple extension points** → Plugin

## Integration with Claude Code Ecosystem

### With Hooks

Commands can trigger or be triggered by hooks:
```markdown
# .claude/commands/pre-commit-review.md
Run before commit (invoked by pre-commit hook):
1. Analyze staged changes
2. Check style compliance
3. Suggest improvements or approve
```

### With Agents

Commands can delegate to specialized agents:
```markdown
# .claude/commands/refactor.md
Delegate large-scale refactoring to refactor-agent:
- Agent: /agents/refactor-agent
- Context: $ARGUMENTS
- Goal: Modernize code while preserving behavior
```

### With MCP Tools

Commands leverage MCP servers for external integrations:
```markdown
# .claude/commands/jira-sync.md
Sync code changes with Jira issue $1:
1. Read issue details via MCP Jira server
2. Analyze related code changes
3. Update issue status and comments
```

### With Plugins

Commands are a plugin component (bundled in plugin packages):
```
my-plugin/
  .claude-plugin/
    plugin.json          # Declares commands, agents, hooks
  commands/
    command1.md
    command2.md
  agents/
  hooks/
```

## Common Pitfalls and Anti-Patterns

**Over-engineering:**
- Creating commands for one-off tasks
- Building complex logic better suited for agents
- Duplicating functionality of existing tools

**Poor argument handling:**
- No validation or constraints
- Blindly interpolating into shell commands (injection risk)
- Unclear expected argument formats

**Monolithic commands:**
- Combining unrelated tasks
- Verbose, unfocused prompts
- Hard to maintain and understand

**Lack of version control:**
- Not committing project commands
- No peer review process
- Lost customizations when switching machines

**Documentation gaps:**
- Missing descriptions or examples
- Unclear usage patterns
- No team communication about new commands

## Advanced Patterns

### Context Block Automation

```markdown
# .claude/commands/analyze-pr.md
Analyze pull request $1:

<context_block>
Run: git diff main...$1
Run: git log main...$1 --oneline
Read: .github/PULL_REQUEST_TEMPLATE.md
</context_block>

Review changes against:
- PR template requirements
- Code style guidelines
- Breaking change impact
```

### Chained Workflows

```markdown
# .claude/commands/release.md
Prepare release $1:

1. Run: /run-tests
2. Run: /update-changelog $1
3. Run: /build-artifacts
4. Generate release notes
5. Run: /deploy staging

Wait for approval before production deployment.
```

### Environment-Aware Commands

```markdown
# .claude/commands/deploy.md
Deploy to $1 environment:

Validation:
- $1 must be: dev|staging|production
- For production, require confirmation

Environment-specific steps:
- dev: Skip tests, fast deployment
- staging: Run smoke tests
- production: Full test suite, manual approval, rollback plan
```

## Current State (2025)

**Maturity:** Well-established feature with stable API and extensive documentation

**Adoption:** Primary customization method for individual developers and teams

**Tooling:** Integrated across CLI, VS Code extension, and desktop applications

**Ecosystem:** Growing repository of shared community commands (GitHub, forums)

**Standards:** Anthropic-maintained best practices and conventions

Slash commands represent the most accessible entry point to Claude Code customization, balancing simplicity with power for everyday development workflows.

## Related Concepts

### Prerequisites
- [[claude_code]] - Understanding Claude Code platform is essential for using slash commands

### Related Topics
- [[claude_code_plugins]] - Slash commands are one component of the plugin system
- [[claude_code_hooks]] - Hooks provide event-driven automation complementary to commands
- [[claude_code_agents]] - Agents handle complex workflows beyond simple commands
- [[claude_code_skills]] - Skills provide more structured, script-driven automation than slash commands

### Extends
- [[claude_code]] - Slash commands extend Claude Code's base functionality through custom workflows

## References

[1] https://docs.claude.com/en/docs/claude-code/slash-commands - Official slash commands documentation
[2] https://www.anthropic.com/engineering/claude-code-best-practices - Best practices guide
[3] https://www.eesel.ai/blog/slash-commands-claude-code - Practical slash command guide
[4] https://cloudartisan.com/posts/2025-04-14-claude-code-tips-slash-commands/ - Advanced tips and patterns
[5] https://shipyard.build/blog/claude-code-cheat-sheet/ - Quick reference and examples
