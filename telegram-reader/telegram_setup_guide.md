# Telegram Channel Reader - Setup Guide

Complete setup guide for the Telegram integration, covering both the standalone CLI script and the Claude Code MCP plugin.

## Overview

This project provides two ways to access Telegram:

1. **Standalone CLI Script** - Direct command-line access via `telegram_channel_reader.py`
2. **Claude Code MCP Plugin** - Natural language access to Telegram via Claude Code

Both share the same Telegram API credentials but have different setup requirements.

---

## Part 1: Standalone CLI Script Setup

### Prerequisites

- Python 3.12+
- Telegram account with phone number
- Internet connection

### Step 1: Install Dependencies

```bash
pip install telethon python-dotenv loguru click
```

Or with uv:

```bash
uv pip install telethon python-dotenv loguru click
```

### Step 2: Get Telegram API Credentials

1. Visit https://my.telegram.org/auth
2. Log in with your phone number and verification code
3. Navigate to **"API development tools"**
4. Fill in application details:
   - **App title:** My Channel Reader (or any name)
   - **Short name:** reader (or any name)
   - **Platform:** Desktop
   - **Description:** Personal channel reader script
5. Click **"Create application"**
6. Copy your **api_id** (number) and **api_hash** (long string)

### Step 3: Configure Environment Variables

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:

```bash
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abc123def456abc123def456abc123de
```

**Security:** Never commit `.env` to version control. It should already be in `.gitignore`.

### Step 4: Run the Script

#### List All Your Channels

```bash
python telegram_channel_reader.py list-my-channels
```

On first run, you'll be prompted to authenticate:
- Enter your phone number (with country code, e.g., +1234567890)
- Enter verification code sent to Telegram
- If 2FA enabled, enter your password

This creates `telegram_session.session` file for subsequent runs (no re-authentication needed).

#### Read Message from Channel

```bash
# Using channel username
python telegram_channel_reader.py read-message @channelname --since 2025-10-01

# Using channel ID (get from list-my-channels)
python telegram_channel_reader.py read-message -1001234567890 --since "2025-10-01T14:30:00"

# With verbose logging
python telegram_channel_reader.py -v read-message @channelname --since 2025-10-01
```

### Usage Examples

#### Example 1: List channels with output

```bash
$ python telegram_channel_reader.py list-my-channels

Your channels:
--------------------------------------------------------------------------------
  ID: -1001234567890 | @technews         | Tech News Daily
  ID: -1009876543210 | @pythondev        | Python Developers
  ID: -1001111222333 | (no username)     | Private Team Channel
--------------------------------------------------------------------------------

Total: 3 channels
```

#### Example 2: Read recent message

```bash
$ python telegram_channel_reader.py read-message @technews --since 2025-10-10

First message since 2025-10-10 00:00:00:
--------------------------------------------------------------------------------
Message ID: 12345
Date: 2025-10-10 08:30:15
Sender: 987654321

Content:
Breaking: New Python 3.14 release includes major performance improvements
Read more: https://example.com/python314
--------------------------------------------------------------------------------
```

### Date Format Options

The `--since` parameter accepts ISO 8601 format:

```bash
# Date only (time defaults to 00:00:00)
--since 2025-10-01

# Date and time
--since "2025-10-01T14:30:00"

# With timezone (if needed)
--since "2025-10-01T14:30:00+00:00"
```

---

## Part 2: Claude Code MCP Plugin Setup

The MCP (Model Context Protocol) plugin enables Claude Code to access your Telegram channels via natural language queries.

### Prerequisites

- Telegram API credentials (from Part 1, Step 2)
- Claude Code with plugin support
- `uv` package manager

### Step 1: Install the Plugin

```bash
# From Claude Code
/plugin install witt3rd-claude-plugins/telegram
```

Or manually clone the plugin repository to your plugins directory.

### Step 2: Configure MCP Server Credentials

**CRITICAL:** The MCP server needs your Telegram API credentials in its configuration.

1. Navigate to the plugin directory:
```bash
cd <plugin-install-path>/telegram/.claude-plugin/
```

2. Edit `mcp-config.json` to include your credentials:

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
        "TELEGRAM_API_ID": "12345678",
        "TELEGRAM_API_HASH": "abc123def456abc123def456abc123de"
      }
    }
  }
}
```

**Important:** The `env` object MUST contain your actual credentials. An empty `env: {}` will prevent the MCP server from starting.

### Step 3: Enable the Plugin

1. In Claude Code, run `/plugin`
2. Enable (check) the telegram plugin
3. Restart Claude Code or disable/re-enable the plugin to load the MCP server

### Step 4: Verify MCP Server is Running

```bash
# In Claude Code
/mcp
```

You should see "telegram" in the list of active MCP servers. If it's missing, see troubleshooting below.

### Step 5: Authenticate with Telegram (First Run)

The MCP server uses the same authentication as the CLI script:

1. On first use, you'll be prompted for:
   - Phone number (with country code)
   - Verification code from Telegram
   - 2FA password (if enabled)

2. A session file is created in the MCP server directory for subsequent runs

### Using the MCP Plugin

Once configured, you can query Telegram naturally in Claude Code:

```
"Show me recent messages from my tech news channel"
"List all my Telegram channels"
"What did the Python developers channel post since yesterday?"
```

Claude will use the MCP server to access your Telegram data and respond.

---

## Troubleshooting

### CLI Script Issues

#### Error: "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set"

- Check that `.env` file exists in the same directory as the script
- Verify credentials are correctly copied (no extra spaces)
- Ensure TELEGRAM_API_ID is a number, not quoted

#### Error: "Could not access channel"

- Verify channel username is correct (include @ symbol)
- Ensure you're a member of the channel
- For private channels, use channel ID instead of username
- Check that channel ID is correct (negative number for channels)

#### Session Issues

If authentication fails:

```bash
# Delete session file and re-authenticate
rm telegram_session.session
python telegram_channel_reader.py list-my-channels
```

### MCP Plugin Issues

#### MCP Server Not Appearing in `/mcp` List

**Symptoms:** Plugin shows as enabled in `/plugin` but doesn't appear in `/mcp`

**Common cause:** Empty or missing environment variables in `mcp-config.json`

**Solution:**
1. Check `.claude-plugin/mcp-config.json`
2. Verify the `env` object contains your credentials:
   ```json
   "env": {
     "TELEGRAM_API_ID": "your_actual_id",
     "TELEGRAM_API_HASH": "your_actual_hash"
   }
   ```
3. NOT an empty object: `"env": {}`
4. Disable and re-enable the plugin in `/plugin`
5. Or restart Claude Code

#### MCP Server Crashes on Startup

**Check:**
1. Credentials in `mcp-config.json` are correct
2. `uv` is installed and in PATH
3. Check MCP server logs (location varies by OS)
4. Verify Python dependencies in `../mcp-server/` are installed

#### Authentication Fails in MCP Server

The MCP server stores its session file separately from the CLI script:

```bash
# Delete MCP server session file
rm <plugin-path>/telegram/mcp-server/telegram_session.session
```

Then restart the MCP server (disable/enable plugin or restart Claude Code).

### Rate Limiting

Telegram has rate limits:
- If you get "FloodWaitError", wait the specified time
- Don't make too many requests in short time
- For bulk operations, add delays between requests

---

## Security Best Practices

1. **Keep credentials secure:**
   - Never share your api_id and api_hash
   - Never commit `.env` files to Git
   - Never commit `mcp-config.json` with credentials to public repos
   - Keep `telegram_session.session` files private

2. **Session files:**
   - Session files store authentication for your Telegram account
   - Anyone with these files can access your Telegram account
   - Don't share or upload session files
   - The CLI script and MCP server maintain separate session files

3. **Revoke access:**
   - If credentials compromised, delete the app at https://my.telegram.org/auth
   - Log out of all sessions via Telegram app settings

4. **MCP Plugin security:**
   - The `mcp-config.json` file contains credentials in plaintext
   - Store it securely
   - Use `.gitignore` if the plugin is in a Git repository
   - Consider using environment variables or a secrets manager for production use

---

## Advanced Usage

### Python API Usage

You can also import and use the functions in your own scripts:

```python
import asyncio
from telegram_channel_reader import get_credentials, list_channels, get_message_since
from telethon import TelegramClient
from datetime import datetime

async def my_script():
    api_id, api_hash = get_credentials()
    client = TelegramClient('my_session', api_id, api_hash)

    await client.start()

    channels = await list_channels(client)
    for channel in channels:
        print(f"Processing {channel['title']}")

        msg = await get_message_since(
            client,
            channel['id'],
            datetime(2025, 10, 1)
        )

        if msg:
            print(f"Latest: {msg['text'][:100]}")

    await client.disconnect()

asyncio.run(my_script())
```

---

## File Structure

### CLI Script Structure

```
telegram-reader/
├── telegram_channel_reader.py    # Main script
├── .env                           # Your credentials (git-ignored)
├── .env.example                   # Template
├── telegram_setup_guide.md        # This file
└── telegram_session.session       # Created on first run (git-ignored)
```

### MCP Plugin Structure

```
telegram/
├── .claude-plugin/
│   ├── plugin.json                # Plugin manifest
│   └── mcp-config.json            # MCP server config WITH credentials
├── mcp-server/
│   ├── server.py                  # MCP server implementation
│   ├── telegram_core.py           # Telegram logic
│   ├── .env                       # Optional: local credentials
│   ├── telegram_session.session   # MCP server session (git-ignored)
│   └── pyproject.toml             # Python dependencies
├── cli/
│   └── telegram_channel_reader.py # Optional CLI wrapper
└── README.md
```

---

## References

- Telethon documentation: https://docs.telethon.dev/
- Telegram API: https://core.telegram.org/api
- API credentials: https://my.telegram.org/auth
- Claude Code Plugins: https://docs.claude.com/en/docs/claude-code/plugins
- Model Context Protocol: https://modelcontextprotocol.io/
