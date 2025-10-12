---
tags: [claude, agents, configuration, deployment, tutorial, guide]
---
# Adding MCP Servers to Claude Code

## Overview

Claude Code supports Model Context Protocol (MCP) servers for extending functionality. This guide covers how to add and manage MCP servers using the Claude CLI.

## CLI Commands

### List MCP Servers

```bash
claude mcp list
```

Shows all configured MCP servers and their connection status.

### Add MCP Server (Basic)

```bash
claude mcp add [options] <name> <command> [args...]
```

Options:

- `-s, --scope <scope>`: Configuration scope (local, user, or project) - default: "local"
- `-t, --transport <transport>`: Transport type (stdio, sse, http) - default: "stdio"
- `-e, --env <env...>`: Set environment variables (e.g., `-e KEY=value`)
- `-H, --header <header...>`: Set WebSocket headers

### Add MCP Server with JSON

```bash
claude mcp add-json [options] <name> <json>
```

This is useful for complex configurations with multiple arguments or environment variables.

Example:

```bash
claude mcp add-json -s user perplexity-ask '{"command":"npx","args":["-y","server-perplexity-ask"],"env":{"PERPLEXITY_API_KEY":"your-key-here"}}'
```

### Remove MCP Server

```bash
claude mcp remove [options] <name>
```

### Get MCP Server Details

```bash
claude mcp get <name>
```

## Configuration Scopes

- **local**: Project-specific configuration
- **user**: User-wide configuration (recommended for personal API keys)
- **project**: Project configuration file (.mcp.json)

## Platform-Specific Considerations

### Windows

On Windows, when using npx or other node-based commands, you need to wrap them with `cmd /c`:

```bash
claude mcp add-json -s user perplexity-ask '{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "server-perplexity-ask"],
  "env": {
    "PERPLEXITY_API_KEY": "your-api-key"
  }
}'
```

### macOS/Linux

On Unix-based systems, you can use npx directly:

```bash
claude mcp add-json -s user perplexity-ask '{
  "command": "npx",
  "args": ["-y", "server-perplexity-ask"],
  "env": {
    "PERPLEXITY_API_KEY": "your-api-key"
  }
}'
```

## Common MCP Server Examples

### Perplexity (Web Search)

```bash
# Windows
claude mcp add-json -s user perplexity-ask '{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "server-perplexity-ask"],
  "env": {
    "PERPLEXITY_API_KEY": "your-api-key"
  }
}'

# macOS/Linux
claude mcp add-json -s user perplexity-ask '{
  "command": "npx",
  "args": ["-y", "server-perplexity-ask"],
  "env": {
    "PERPLEXITY_API_KEY": "your-api-key"
  }
}'
```

### Filesystem Access

```bash
# All platforms
claude mcp add -s user filesystem "npx" "-y" "@modelcontextprotocol/server-filesystem" "/path/to/allowed/directory"
```

### GitHub Integration

```bash
claude mcp add-json -s user github '{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_TOKEN": "your-github-token"
  }
}'
```

## Tips

1. Use `-s user` scope for servers with personal API keys
2. The `add-json` command is better for servers requiring multiple arguments
3. Always verify connection with `claude mcp list` after adding
4. Environment variables in the `-e` option must be in `KEY=value` format
5. Arguments with hyphens (like `-y`) should be passed as separate array elements in JSON

## Verification

After adding an MCP server, verify it's working:

1. List all servers and check status:

```bash
claude mcp list
```

2. Check specific server details:

```bash
claude mcp get <server-name>
```

3. Test in Claude Code:

```bash
claude
# Then try using the server's functionality
```

## Configuration Files

MCP server configurations are stored in JSON files:

- **User config**: `~/.claude.json` (or `%USERPROFILE%\.claude.json` on Windows)
- **Project config**: `.claude.json` in project root
- **MCP config**: `.mcp.json` in project root

Example user config structure:

```json
{
  "mcpServers": {
    "perplexity-ask": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "server-perplexity-ask"],
      "env": {
        "PERPLEXITY_API_KEY": "your-key"
      }
    }
  }
}
```

## Troubleshooting

### Windows-Specific Issues

- **"Windows requires 'cmd /c' wrapper"**: Always wrap npx commands with `cmd /c` on Windows
- **Path issues**: Use forward slashes or escaped backslashes in paths

### General Issues

- **Arguments starting with `-`**: Use the `add-json` command for complex argument structures
- **Server not connecting**: Check `claude mcp list` for connection status
- **Permission errors**: Ensure the server has access to required resources
- **API key issues**: Verify environment variables are set correctly

### Debugging

1. Check the doctor output:

```bash
claude doctor
```

2. View server logs:

```bash
claude mcp get <server-name>
```

3. Test with minimal configuration first, then add complexity

## Related Concepts

### Prerequisites
- [[mcp_overview]] - Need to understand MCP fundamentals before configuring servers
- [[mcp_architecture]] - Understanding MCP architecture helps with server configuration

### Related Topics
- [[agents]] - MCP servers extend agent capabilities in Claude Code
- [[mcp_implementation]] - Related to implementing MCP in practice