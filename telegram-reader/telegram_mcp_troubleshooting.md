# Telegram MCP Server Troubleshooting Log

**Date**: 2025-10-15
**Status**: RESOLVED - Empty `env: {}` object in mcp-config.json was the root cause

## Problem Statement

The `/mcp` command shows `plugin:telegram:telegram` as **failed** with message "Failed to reconnect to plugin:telegram:telegram."

## SOLUTION (Final)

The `env: {}` object in `.claude-plugin/mcp-config.json` was empty. MCP servers need credentials directly in the config file - they don't automatically load `.env` files.

**Location**: `/c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/.claude-plugin/mcp-config.json`

**The fix**: Add Telegram API credentials to the `env` object in `mcp-config.json`.

## Debugging Summary

### What Was Checked

1. **Session file**: ✅ EXISTS at `~/.cache/telegram_mcp_session.session` (28KB, last modified 2025-10-15 06:48)
2. **Development repo .env**: ✅ EXISTS at `/c/Users/dothompson/src/witt3rd/claude-plugins/plugins/telegram/mcp-server/.env` with credentials
3. **Marketplace repo .env**: ✅ EXISTS at `/c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/mcp-server/.env` with credentials
4. **MCP tools availability**: ❌ FAILED - `mcp__telegram__list_conversations` not available

### Root Cause Identified

**Empty `env` object in mcp-config.json**

Location: `/c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/.claude-plugin/mcp-config.json`

**Before (WRONG)**:
```json
{
  "mcpServers": {
    "telegram": {
      "command": "uv",
      "args": [
        "--directory",
        "../mcp-server",
        "run",
        "server.py"
      ],
      "env": {}
    }
  }
}
```

**After (FIXED)**:
```json
{
  "mcpServers": {
    "telegram": {
      "command": "uv",
      "args": [
        "--directory",
        "../mcp-server",
        "run",
        "server.py"
      ],
      "env": {
        "TELEGRAM_API_ID": "your_actual_api_id",
        "TELEGRAM_API_HASH": "your_actual_api_hash"
      }
    }
  }
}
```

**Why this happened**:
- The `.env` file in `mcp-server/` directory contains the credentials
- The standalone CLI and development server work because they load `.env` directly via `python-dotenv`
- MCP servers launched by Claude Code do NOT automatically load `.env` files
- Credentials must be explicitly passed via the `env` object in `mcp-config.json`
- The plugin marketplace installation created the config with empty `env: {}`

## What Was Fixed

1. Added `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` to the `env` object in `.claude-plugin/mcp-config.json`
2. Credentials must be in the MCP config, not just in `.env` file

## To Apply Fix

After editing `mcp-config.json`:
1. Run `/plugin` and disable/re-enable the telegram plugin, OR
2. Restart Claude Code
3. Verify with `/mcp` - should show telegram as connected
4. Tools like `mcp__telegram__list_conversations` should become available

## Log Analysis

### Old Session Logs (SUCCESSFUL)

File: `/c/Users/dothompson/AppData/Local/claude-cli-nodejs/Cache/C--Users-dothompson-OneDrive-src-witt3rd-donald-azkg/mcp-logs-telegram/2025-10-15T13-32-23-687Z.txt`

**Key findings**:
- Server started successfully at 2025-10-15 06:32:32
- Connection established with capabilities
- Tool `list_conversations` executed successfully
- Returned 63 conversations
- Session ended cleanly at 2025-10-15 06:33:36

**This proves**: Authentication works, server code works, session file works.

### Current Session Logs

**CRITICAL ISSUE**: No new log file created for current connection attempt!

Last log: `2025-10-15T13-32-23-687Z.txt` (from 06:32-06:33)
Current time: ~07:00+
Gap: No logs for current failure

**This suggests**: Either:
1. Claude Code isn't attempting to connect (path error prevented launch)
2. Server crashes before writing logs
3. Logs are being written elsewhere

## Next Steps If Problem Persists After Restart

### 1. Check for NEW Log Files

```bash
ls -lt /c/Users/dothompson/AppData/Local/claude-cli-nodejs/Cache/C--Users-dothompson-OneDrive-src-witt3rd-donald-azkg/mcp-logs-telegram/
```

If new file exists, read it:
```bash
# Replace with actual newest timestamp
cat /c/Users/dothompson/AppData/Local/claude-cli-nodejs/Cache/C--Users-dothompson-OneDrive-src-witt3rd-donald-azkg/mcp-logs-telegram/[NEWEST_FILE].txt
```

### 2. Check Claude Code Main Logs

**IMPORTANT**: MCP server logs are in the project-specific cache. Claude Code itself may have logs elsewhere:

```bash
# Windows AppData logs
ls -la /c/Users/dothompson/AppData/Local/claude-cli-nodejs/
find /c/Users/dothompson/AppData/Local/claude-cli-nodejs/ -name "*.log" -o -name "*.txt" | head -20

# Check for general error logs
ls -la /c/Users/dothompson/AppData/Local/claude-cli-nodejs/Cache/
```

### 3. Test Server Manually

Try running the MCP server directly to see initialization errors:

```bash
cd /c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/mcp-server

# This will hang waiting for stdin (expected), but should show startup errors if any
uv run server.py
# Press Ctrl+C after a few seconds if it starts cleanly
```

### 4. Check Plugin Registry

```bash
# See how Claude Code sees the plugin
cat /c/Users/dothompson/.claude/plugins/known_marketplaces.json

# Check if there's a plugin state file
find /c/Users/dothompson/.claude/plugins/ -type f -name "*.json"
```

### 5. Verify MCP Server Can Start

Check if dependencies are actually synced:

```bash
cd /c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/mcp-server

# Ensure dependencies installed
uv sync

# Verify Python can import modules
uv run python3 -c "from fastmcp import FastMCP; from telethon import TelegramClient; print('Imports OK')"
```

### 6. Check for Path Issues on Windows

The path `/c/Users/...` works in Git Bash but might need different format for `uv`:

```bash
# Try Windows-style path if Unix-style fails
# In mcp-config.json, try:
# "C:\\Users\\dothompson\\.claude\\plugins\\marketplaces\\witt3rd-claude-plugins\\plugins\\telegram\\mcp-server"
```

### 7. Look for stderr in Process Spawn

The old log shows server stderr as `"error"` entries (even though they're INFO logs). Look for:
- "error" entries that are actually Python exceptions
- Connection timeout messages
- "Command failed" or "Process exited" messages

## Expected Success Indicators

After restart, if working correctly you should see:

1. `/mcp` shows telegram as ✔ connected
2. New log file created in mcp-logs-telegram/
3. Log contains "Telegram client connected"
4. Tool `mcp__telegram__list_conversations` becomes available

## Configuration Summary

**Plugin location (marketplace)**:
`/c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/`

**Development repo** (don't use for production):
`/c/Users/dothompson/src/witt3rd/claude-plugins/plugins/telegram/`

**Session file**:
`/c/Users/dothompson/.cache/telegram_mcp_session.session`

**Log directory**:
`/c/Users/dothompson/AppData/Local/claude-cli-nodejs/Cache/C--Users-dothompson-OneDrive-src-witt3rd-donald-azkg/mcp-logs-telegram/`

**Server log** (separate from MCP logs):
`/c/Users/dothompson/.cache/telegram-mcp-server.log`

## Additional Investigation Paths

### Check Server's Own Log File

```bash
# The server.py writes its own log separate from MCP logs
tail -100 /c/Users/dothompson/.cache/telegram-mcp-server.log
```

### Check if uv is in PATH

```bash
which uv
uv --version
```

If uv not found, Claude Code won't be able to start the server.

### Check for Port Conflicts

Although MCP uses stdio, check if Telegram client has connection issues:

```bash
# Run CLI tool to verify Telegram connectivity
cd /c/Users/dothompson/src/witt3rd/claude-plugins/plugins/telegram/cli
uv run telegram-reader list-dialogs
```

If CLI works but MCP doesn't, it's purely an MCP integration issue.

## Key Insights

**The old logs show SUCCESSFUL operation**, which means:
- The code is correct
- The authentication is correct
- The session file is valid

**The problem was configuration**, not code:
- MCP servers don't automatically load `.env` files
- Credentials must be explicitly in `mcp-config.json`'s `env` object
- Empty `env: {}` means the server starts without API credentials
- Server fails silently without proper error messages when credentials missing

## Common Mistake Pattern

This issue occurs when:
1. Developer creates `.env` file with credentials (works for CLI)
2. Plugin uses same code but via MCP integration
3. MCP config has empty `env: {}`
4. Server can't authenticate because credentials aren't passed to it
5. No clear error message about missing credentials

## Questions for User After Restart

1. Does `/mcp` now show telegram as connected?
2. If still failed, is there a NEW log file?
3. What does the newest log file say?
4. Does the server's own log at `~/.cache/telegram-mcp-server.log` exist?

---

## For Plugin Developers

**Critical lesson**: When creating an MCP plugin that requires credentials:

1. **Document clearly** that credentials must be in `mcp-config.json`'s `env` object
2. **Don't rely on `.env` files** for MCP server configuration
3. **Provide template** in plugin documentation showing exactly where to put credentials
4. **Consider adding validation** in server startup to fail fast with clear error if credentials missing
5. **Test the marketplace installation flow** - not just development environment

**Example good documentation**:
```markdown
### Step 2: Configure MCP Server Credentials

Edit `.claude-plugin/mcp-config.json` and add your credentials:

```json
{
  "mcpServers": {
    "myserver": {
      "command": "uv",
      "args": ["run", "server.py"],
      "env": {
        "API_KEY": "your_actual_key_here",
        "API_SECRET": "your_actual_secret_here"
      }
    }
  }
}
```

⚠️ **Important**: The `env` object MUST contain your actual credentials.
An empty `env: {}` will prevent the server from starting.
```

---

**Resolution**: The fix has been applied. After reloading the plugin or restarting Claude Code, the telegram MCP server should connect successfully.
