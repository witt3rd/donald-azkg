# Telegram MCP Plugin Setup Process

**Date**: 2025-10-15
**Purpose**: Document the setup process for deploying the Telegram MCP plugin to the Claude Code marketplace

## Overview

This directory (`telegram-reader/`) was used as a development workspace to create and test the Telegram session before deploying the MCP plugin to the Claude Code marketplace. The key files (`.env` and session file) needed to be generated here first, then copied to the marketplace plugin location.

## Setup Steps

### 1. Create Development Environment

Created `telegram-reader/` directory with Python project structure:

```bash
cd telegram-reader/
uv init  # Initialize Python project with uv
```

Files created:
- `pyproject.toml` - Python dependencies (telethon, python-dotenv)
- `.env` - Telegram API credentials
- `.env.example` - Template for credentials
- `.gitignore` - Protect sensitive files

### 2. Obtain Telegram API Credentials

1. Visited https://my.telegram.org/auth
2. Logged in with phone number
3. Navigated to "API development tools"
4. Created application to get:
   - `TELEGRAM_API_ID` (integer)
   - `TELEGRAM_API_HASH` (32-character hex string)

### 3. Configure Environment File

Created `.env` file with credentials:

```env
# Telegram API Credentials
TELEGRAM_API_ID=29780514
TELEGRAM_API_HASH=54ef7ab93e78e7e05f48cb1239edd6fa
```

### 4. Generate Telegram Session

The session file authenticates the Telegram client without requiring repeated logins. Generated using initial connection:

1. Ran Telegram client initialization (first time):
   ```bash
   cd telegram-reader/
   # Client code prompts for phone number and verification code
   ```

2. Session file created: `telegram_session.session` (28KB binary file)
   - Contains encrypted authentication tokens
   - Allows persistent connection without re-authentication
   - Must be kept secure (git-ignored)

### 5. Deploy to Marketplace Plugin

Copied files to Claude Code marketplace plugin location:

**Target structure:**
```
/c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/
└── plugins/
    └── telegram/
        └── mcp-server/
            ├── .env                          # API credentials
            ├── server.py                     # MCP server
            ├── telegram_core.py              # Telegram client logic
            └── pyproject.toml                # Dependencies
```

**Session file location (system cache):**
```
/c/Users/dothompson/.cache/
└── telegram_mcp_session.session              # Persistent session
```

### 6. File Deployments

**`.env` file:**
- Source: `telegram-reader/.env`
- Target: `/c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/mcp-server/.env`
- Status: Copied and verified

**Session file:**
- Source: `telegram-reader/telegram_session.session`
- Target: `/c/Users/dothompson/.cache/telegram_mcp_session.session`
- Status: Already in place (generated during testing)
- Note: Session file in cache was actually NEWER (Oct 15 06:48) than development copy (Oct 14 15:16)

## File Locations Summary

### Development Files (telegram-reader/)
```
telegram-reader/
├── .env                           # Development credentials (original)
├── .env.example                   # Template
├── telegram_session.session       # Development session (older)
├── pyproject.toml                 # Dev dependencies
└── src/
    └── telegram_reader/           # Development CLI code
```

### Production Files (Marketplace Plugin)
```
~/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/mcp-server/
├── .env                           # Production credentials (copied)
├── server.py                      # MCP server
├── telegram_core.py               # Core client
└── pyproject.toml                 # Production dependencies

~/.cache/
└── telegram_mcp_session.session   # Shared session file (28KB)
```

## Key Insights

### Why Separate Session Generation?

The Telegram session file requires **interactive authentication**:
1. User enters phone number
2. Telegram sends verification code via SMS/app
3. User enters verification code
4. Session file created with auth tokens

**This cannot be automated during plugin installation**, so the session must be pre-generated.

### Session File Sharing

The session file location (`~/.cache/telegram_mcp_session.session`) is:
- **Shared** between development and production
- **System-wide** cache location
- **Binary format** (SQLite database)
- **Persistent** across plugin updates

### Security Considerations

**Git-ignored files:**
- `.env` (contains API credentials)
- `telegram_session.session` (contains auth tokens)
- `*.session-journal` (SQLite journal files)

**What's committed:**
- `.env.example` (template only)
- `telegram_setup_guide.md` (setup instructions)
- Source code without credentials

## Verification

Files verified in production locations:

```bash
# Check .env file
ls -la /c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/mcp-server/.env
# Result: ✅ 274 bytes

# Check session file
ls -lh /c/Users/dothompson/.cache/telegram_mcp_session.session
# Result: ✅ 28KB, modified Oct 15 06:48
```

## Testing Results

**Old successful logs** (Oct 15 06:32-06:33):
- Server started successfully
- Connection established with Telegram
- Tool `list_conversations` executed
- Returned 63 conversations
- Session ended cleanly

This confirms all components work correctly when properly configured.

## MCP Configuration

The marketplace plugin uses this `mcp-config.json`:

```json
{
  "mcpServers": {
    "telegram": {
      "command": "uv",
      "args": [
        "--directory",
        "/c/Users/dothompson/.claude/plugins/marketplaces/witt3rd-claude-plugins/plugins/telegram/mcp-server",
        "run",
        "server.py"
      ],
      "env": {}
    }
  }
}
```

**Key points:**
- Uses `uv run` to execute server.py
- Points to marketplace plugin location (not development repo)
- Environment variables loaded from `.env` file
- Session file loaded from `~/.cache/` (hardcoded in telegram_core.py)

## Future Setup for New Users

For other users installing this plugin:

1. Obtain Telegram API credentials from https://my.telegram.org
2. Create `.env` file in plugin's mcp-server directory
3. Run session generation script (requires interactive auth)
4. Move session file to `~/.cache/telegram_mcp_session.session`
5. Restart Claude Code to load plugin

**TODO**: Create automated setup script that guides users through this process.

## Related Documentation

- `telegram_setup_guide.md` - Initial setup instructions
- `telegram_mcp_troubleshooting.md` - Debugging connection issues
- `README.md` - Project overview

## Status

✅ Development environment configured
✅ API credentials obtained
✅ Session file generated
✅ Files deployed to marketplace plugin
✅ Plugin configuration verified
⏳ Awaiting Claude Code restart for final testing
