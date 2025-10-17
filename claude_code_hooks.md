---
tags: [claude-code, automation, lifecycle, extensibility, workflow]
---
# Claude Code Hooks: Lifecycle Event System

**Claude Code hooks** are a lifecycle event system that enables developers to inject custom shell commands or scripts at specific stages of Claude Code workflows, providing deterministic automation and seamless integration with existing development processes. Unlike AI-driven behaviors which are probabilistic, hooks guarantee that specified actions execute reliably at designated lifecycle points.

## What Hooks Are

Hooks are user-defined shell commands or scripts bound to key Claude Code workflow events. When a defined event occurs (such as before running a tool, after generating code, or when submitting a prompt), the associated hook executes automatically, enabling:

- Deterministic, repeatable automation regardless of AI variability
- Integration with existing development toolchains (linters, formatters, test runners)
- Enforcement of team standards and policies
- Custom notifications and workflow triggers
- Background process orchestration

Hooks complement Claude Code's AI capabilities by providing predictable, script-based actions that always run at the right moment in the development workflow.

## Available Hook Types

Claude Code supports multiple lifecycle events where hooks can be attached:

### Core Hook Events

**PreToolUse**:
- Triggers before Claude Code executes any tool (file operations, shell commands, etc.)
- Use cases: Argument validation, blocking risky operations, configuration checks
- Example: Prevent destructive commands like `rm -rf` in production directories

**PostToolUse**:
- Triggers after a tool successfully completes execution
- Use cases: Auto-formatting, running tests, action logging, side effects
- Example: Run `prettier` after code generation, execute test suite after changes

**UserPromptSubmit**:
- Triggers when user submits a prompt, before AI processes the request
- Use cases: Inject additional context, validate input, pre-process requests
- Example: Append recent git changes to user's prompt for better context

**SessionStart**:
- Triggers at the beginning of each Claude Code session
- Use cases: Environment setup, loading project state, initialization
- Example: Pull latest git changes, fetch active Jira tickets, load secrets

**Notification**:
- Triggers when Claude Code sends a notification (permission requests, alerts)
- Use cases: Custom desktop notifications, team alerts, logging
- Example: Send Slack message when Claude requests sensitive operation approval

**Stop**:
- Triggers after Claude Code completes its overall response
- Use cases: Summarization, completion signals, cleanup
- Example: Generate change summary, update project dashboard

### Specialized Hooks

Some integrations (like GitButler) provide additional hooks:

**pre-commit**: Before git commits
**post-generation**: After code generation completes

## Configuration and Setup

### Installation

1. **Install Claude Code CLI**:
```bash
npm install -g @anthropic-ai/claude-code
```

2. **Authenticate** Claude Code to your environment

3. **Enable hooks module** in Claude Code configuration:
```json
{
  "features": ["hooks"]
}
```

### Configuration Files

Hooks are configured in `.claude/settings.json` in your project root:

```json
{
  "hooks": {
    "PreToolUse": "scripts/validate.sh",
    "PostToolUse": "scripts/format.sh",
    "SessionStart": "scripts/init.sh",
    "UserPromptSubmit": "scripts/context.sh"
  }
}
```

### File Structure

Recommended project organization:

```
project-root/
├── .claude/
│   └── settings.json        # Hook configuration
├── scripts/
│   ├── validate.sh          # PreToolUse hook
│   ├── format.sh            # PostToolUse hook
│   ├── init.sh              # SessionStart hook
│   └── context.sh           # UserPromptSubmit hook
└── hooks/                   # Alternative location
    └── ...
```

### CLI Management

Hooks can be managed via CLI commands:

**Register a hook**:
```bash
claude-code hook register PostToolUse scripts/format.sh
```

**List configured hooks**:
```bash
claude-code hook list
```

**Unregister a hook**:
```bash
claude-code hook unregister <hook-id>
```

## Execution Model

### How Hooks Execute

- Hooks run as **shell commands** or **scripts** under the user's environment
- Execute at **exact lifecycle moment** they're bound to
- Receive **event payloads** with context about the triggering action
- Run **synchronously** by default (blocking workflow until completion)
- Return **exit codes** to signal success/failure

### Event Payloads

Hooks receive structured event data they can inspect and use for logic:

**PreToolUse event**:
```json
{
  "tool": "shell",
  "args": ["rm", "-rf", "temp/"],
  "workingDirectory": "/project/root",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**PostToolUse event**:
```json
{
  "tool": "edit",
  "result": "success",
  "filesModified": ["src/main.ts", "src/utils.ts"],
  "timestamp": "2025-01-15T10:30:05Z"
}
```

### Language Support

Hooks can be implemented in any language that can be executed as a shell command:

**Python example** (`scripts/validate.py`):
```python
#!/usr/bin/env python3
import sys
import json

def pre_tool_use(event):
    # Validate tool execution
    if event["tool"] == "shell" and "rm -rf" in " ".join(event["args"]):
        print("ERROR: Destructive operations not allowed", file=sys.stderr)
        sys.exit(1)
    return event

if __name__ == "__main__":
    event = json.loads(sys.stdin.read())
    pre_tool_use(event)
```

**TypeScript/Node example** (`scripts/format.js`):
```javascript
#!/usr/bin/env node
const { execSync } = require('child_process');

async function postToolUse(event) {
    if (event.filesModified) {
        for (const file of event.filesModified) {
            if (file.endsWith('.ts') || file.endsWith('.js')) {
                execSync(`prettier --write ${file}`);
            }
        }
    }
}

const event = JSON.parse(require('fs').readFileSync(0, 'utf-8'));
postToolUse(event).then(() => process.exit(0)).catch(err => {
    console.error(err);
    process.exit(1);
});
```

### API Integration

Hooks can be registered programmatically using Claude Code SDKs:

**Python SDK**:
```python
from anthropic.claude_code import ClaudeCode

def pre_tool_use_handler(event):
    # Custom validation logic
    if "dangerous" in str(event.get("args", [])):
        raise Exception("Operation blocked by policy")
    return event

def post_tool_use_handler(event):
    # Logging and formatting
    print(f"Tool {event['tool']} completed successfully")
    return event

client = ClaudeCode(
    api_key="YOUR_KEY",
    hooks={
        "PreToolUse": pre_tool_use_handler,
        "PostToolUse": post_tool_use_handler
    }
)
```

**TypeScript SDK**:
```typescript
import { ClaudeCode, HookEvent } from "@anthropic-ai/claude-code";

const client = new ClaudeCode({
    apiKey: "YOUR_KEY",
    hooks: {
        PreToolUse: async (event: HookEvent) => {
            // Validation logic
            if (event.tool === "shell" && event.args.includes("rm")) {
                throw new Error("Destructive operation blocked");
            }
        },
        PostToolUse: async (event: HookEvent) => {
            // Auto-format modified files
            console.log(`Completed: ${event.tool}`);
        }
    }
});
```

## When to Use Hooks

### Hooks vs. Other Extension Mechanisms

| Mechanism | Best For | Execution Model |
|-----------|----------|-----------------|
| **Hooks** | Deterministic automation at lifecycle points | Automatic, background |
| **Slash Commands** | User-initiated actions, manual triggers | Interactive, on-demand |
| **Subagents** | Complex AI-powered workflows | Autonomous, multi-step |
| **MCP Servers** | External service integration | Request/response |

### Ideal Use Cases for Hooks

**Use hooks when you need**:
- Guaranteed execution at specific workflow moments
- Background automation without user intervention
- Integration with existing CLI tools and scripts
- Policy enforcement and validation
- Side effects after AI actions

**Avoid hooks for**:
- Complex multi-step reasoning (use subagents)
- User-facing interactive features (use slash commands)
- Stateful external service integration (use MCP servers)

## Practical Use Cases

### Code Quality Enforcement

**Auto-formatting after edits** (PostToolUse):
```bash
#!/bin/bash
# scripts/format.sh
prettier --write "**/*.{ts,js,json,md}"
eslint --fix "**/*.{ts,js}"
```

**Prevent risky operations** (PreToolUse):
```python
#!/usr/bin/env python3
import sys, json
event = json.loads(sys.stdin.read())
if event["tool"] == "shell":
    args = " ".join(event["args"])
    if any(danger in args for danger in ["rm -rf /", "DROP DATABASE", "> /dev/sda"]):
        print("BLOCKED: Dangerous operation detected", file=sys.stderr)
        sys.exit(1)
```

### Testing and Validation

**Run tests after code changes** (PostToolUse):
```bash
#!/bin/bash
# scripts/test.sh
if [[ "$FILES_MODIFIED" =~ \.test\. ]] || [[ "$FILES_MODIFIED" =~ src/ ]]; then
    npm test
    if [ $? -ne 0 ]; then
        echo "Tests failed! Please fix before continuing."
        exit 1
    fi
fi
```

### Environment and Context Management

**Load project context at session start** (SessionStart):
```bash
#!/bin/bash
# scripts/init.sh
echo "Loading project context..."
git fetch origin
git log --oneline -5 > .claude/recent_commits.txt
# Fetch active issues from Jira
curl -u $JIRA_USER:$JIRA_TOKEN "$JIRA_API/search?jql=assignee=$USER+AND+status=InProgress" \
  > .claude/active_issues.json
```

**Inject context into prompts** (UserPromptSubmit):
```python
#!/usr/bin/env python3
import sys, json, subprocess
# Get recent git changes
git_log = subprocess.check_output(["git", "log", "--oneline", "-3"]).decode()
print(f"\n[Recent commits: {git_log}]", file=sys.stderr)
```

### Notifications and Integration

**Send team notifications** (Notification):
```bash
#!/bin/bash
# scripts/notify.sh
MESSAGE="Claude Code: $NOTIFICATION_MESSAGE"
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK/URL \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"$MESSAGE\"}"
```

**Generate completion summary** (Stop):
```bash
#!/bin/bash
# scripts/summarize.sh
echo "Session completed at $(date)" >> .claude/session_log.txt
git diff --stat >> .claude/session_log.txt
```

### Security and Compliance

**Audit logging** (PreToolUse & PostToolUse):
```python
#!/usr/bin/env python3
import sys, json, datetime
event = json.loads(sys.stdin.read())
log_entry = {
    "timestamp": datetime.datetime.now().isoformat(),
    "tool": event["tool"],
    "args": event.get("args", []),
    "user": os.environ.get("USER")
}
with open(".claude/audit.log", "a") as f:
    f.write(json.dumps(log_entry) + "\n")
```

## Limitations and Constraints

### Technical Limitations

**Shell-based execution**:
- Hooks are primarily terminal/CLI-focused
- Limited support for GUI interactions
- Must be executable in user's shell environment

**Synchronous blocking**:
- Hooks block workflow until completion
- Long-running hooks degrade user experience
- No built-in timeout mechanism (must implement in script)

**Error handling**:
- Failed hooks (non-zero exit code) can block workflow
- Debugging hook failures can be challenging
- Limited error reporting to user

**Platform dependencies**:
- Hooks must be cross-platform or environment-specific
- Path differences between Windows/Unix
- Shell availability (bash, zsh, PowerShell)

### Security Considerations

**Arbitrary code execution**:
- Hooks execute with full user permissions
- Can access local resources and network
- Shared configurations may introduce malicious hooks

**Best practices**:
- Always review hook scripts before use
- Restrict hook execution context where possible
- Audit and version control all hooks
- Use signed/verified hooks in team environments

### Configuration Complexity

**Setup overhead**:
- Requires technical expertise to configure properly
- Maintaining multiple hooks increases complexity
- Hook interactions can be difficult to reason about

**No visual management UI**:
- CLI and file-based configuration only
- No graphical hook manager (as of 2025)
- Difficult to discover what hooks are active

## Creative Advanced Uses

### Multi-Stage Pipelines

Chain hooks to create sophisticated workflows:

**PostToolUse → dependency audit → vulnerability scan → changelog update**:
```bash
#!/bin/bash
npm audit --audit-level=moderate
snyk test --severity-threshold=high
conventional-changelog -p angular -i CHANGELOG.md -s
```

### External System Integration

**Trigger CI/CD pipelines**:
```bash
#!/bin/bash
# Hook into GitHub Actions via webhook
curl -X POST https://api.github.com/repos/owner/repo/actions/workflows/build.yml/dispatches \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"ref": "main"}'
```

**Sync with project management**:
```python
#!/usr/bin/env python3
# Update Jira ticket status based on code changes
import jira
jira_client = jira.JIRA(server='https://company.atlassian.net', token=JIRA_TOKEN)
issue = jira_client.issue('PROJ-123')
issue.update(fields={'status': {'name': 'In Review'}})
```

### Context-Aware Automation

**Dynamic test selection based on changed files**:
```bash
#!/bin/bash
CHANGED_FILES=$(git diff --name-only HEAD~1)
if echo "$CHANGED_FILES" | grep -q "^api/"; then
    pytest tests/api/
elif echo "$CHANGED_FILES" | grep -q "^frontend/"; then
    npm run test:frontend
fi
```

**Adaptive documentation generation**:
```bash
#!/bin/bash
# Generate docs only for modified modules
for file in $FILES_MODIFIED; do
    if [[ $file =~ \.py$ ]]; then
        pdoc --html --force $file
    fi
done
```

## Best Practices

### Hook Development

**Keep hooks simple and focused**:
- Each hook should do one thing well
- Avoid complex logic in shell scripts
- Extract reusable functions to libraries

**Fast execution**:
- Hooks should complete in seconds, not minutes
- Use background processes for long-running tasks
- Implement timeouts to prevent hangs

**Defensive programming**:
- Validate all inputs and environment variables
- Handle errors gracefully with meaningful messages
- Use exit codes correctly (0 = success, non-zero = failure)

**Logging and debugging**:
- Log hook execution for troubleshooting
- Include timestamps and context in logs
- Use `set -x` in bash for debug tracing

### Organization and Maintenance

**Version control hooks**:
- Keep all hooks in project repository
- Document hook purpose and usage
- Review hook changes through code review

**Isolate hook scripts**:
- Place in dedicated `scripts/` or `hooks/` directory
- Use clear, descriptive filenames
- Include README documenting each hook

**Testing hooks**:
- Test hooks independently of Claude Code
- Create test fixtures for various scenarios
- Validate cross-platform compatibility

### Security and Permissions

**Principle of least privilege**:
- Limit hook permissions to minimum necessary
- Avoid running hooks as root/admin
- Use service accounts for external integrations

**Audit regularly**:
- Review active hooks periodically
- Remove unused or obsolete hooks
- Monitor hook execution logs for anomalies

**Validate external inputs**:
- Never trust event data blindly
- Sanitize file paths and shell arguments
- Prevent injection attacks

## Current State (2025)

**Maturity**: Hooks are stable and widely deployed in production workflows. The API is established but continues to evolve with new hook types and capabilities.

**Ecosystem**: Strong community around hook development, with shared libraries and example repositories. Third-party tools (GitButler, etc.) provide specialized hook integrations.

**Tooling**: Primarily CLI and file-based configuration. No official GUI management tool yet, though community tools are emerging.

**Documentation**: Comprehensive official docs with examples. Active discussion in community forums and GitHub.

**Future directions**:
- Async/non-blocking hook execution
- Richer event payloads with more context
- Hook marketplace for sharing common hooks
- Better debugging and monitoring tools

Claude Code hooks provide precision automation within AI-augmented workflows, enabling teams to enforce standards, integrate existing tools, and create deterministic, reproducible development processes that complement Claude's probabilistic AI capabilities.

## Related Concepts

### Prerequisites
- [[claude_code]] - Understanding Claude Code platform is essential for using hooks

### Related Topics
- [[claude_code_plugins]] - Hooks are a plugin component for event-driven automation
- [[claude_code_slash_commands]] - Slash commands provide complementary manual workflow triggers
- [[claude_code_agents]] - Agents handle complex workflows beyond simple hook automation
- [[claude_code_skills]] - Skills provide context-aware task execution while hooks provide event-driven automation

## References

[1] https://www.eesel.ai/blog/hooks-in-claude-code
[2] https://www.cometapi.com/claude-code-hooks-what-is-and-how-to-use-it/
[3] https://www.anthropic.com/news/claude-code-plugins
[4] https://anthropic.com/news/enabling-claude-code-to-work-more-autonomously
[5] https://www.siddharthbharath.com/claude-code-the-complete-guide/
[6] https://docs.gitbutler.com/features/ai-integration/claude-code-hooks
[7] https://www.anthropic.com/engineering/claude-code-best-practices
[8] https://www.builder.io/blog/claude-code
[9] https://docs.claude.com/en/docs/claude-code/hooks-guide
