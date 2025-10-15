# Telegram Channel Reader - Setup Guide

Complete setup guide for `telegram_channel_reader.py` script.

## Prerequisites

- Python 3.12+
- Telegram account with phone number
- Internet connection

## Step 1: Install Dependencies

```bash
pip install telethon python-dotenv loguru click
```

Or with uv:

```bash
uv pip install telethon python-dotenv loguru click
```

## Step 2: Get Telegram API Credentials

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

## Step 3: Configure Environment Variables

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

## Step 4: Run the Script

### List All Your Channels

```bash
python telegram_channel_reader.py list-my-channels
```

On first run, you'll be prompted to authenticate:
- Enter your phone number (with country code, e.g., +1234567890)
- Enter verification code sent to Telegram
- If 2FA enabled, enter your password

This creates `telegram_session.session` file for subsequent runs (no re-authentication needed).

### Read Message from Channel

```bash
# Using channel username
python telegram_channel_reader.py read-message @channelname --since 2025-10-01

# Using channel ID (get from list-my-channels)
python telegram_channel_reader.py read-message -1001234567890 --since "2025-10-01T14:30:00"

# With verbose logging
python telegram_channel_reader.py -v read-message @channelname --since 2025-10-01
```

## Usage Examples

### Example 1: List channels with output

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

### Example 2: Read recent message

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

## Date Format Options

The `--since` parameter accepts ISO 8601 format:

```bash
# Date only (time defaults to 00:00:00)
--since 2025-10-01

# Date and time
--since "2025-10-01T14:30:00"

# With timezone (if needed)
--since "2025-10-01T14:30:00+00:00"
```

## Troubleshooting

### Error: "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set"

- Check that `.env` file exists in the same directory as the script
- Verify credentials are correctly copied (no extra spaces)
- Ensure TELEGRAM_API_ID is a number, not quoted

### Error: "Could not access channel"

- Verify channel username is correct (include @ symbol)
- Ensure you're a member of the channel
- For private channels, use channel ID instead of username
- Check that channel ID is correct (negative number for channels)

### Session Issues

If authentication fails:

```bash
# Delete session file and re-authenticate
rm telegram_session.session
python telegram_channel_reader.py list-my-channels
```

### Rate Limiting

Telegram has rate limits:
- If you get "FloodWaitError", wait the specified time
- Don't make too many requests in short time
- For bulk operations, add delays between requests

## Security Best Practices

1. **Keep credentials secure:**
   - Never share your api_id and api_hash
   - Never commit `.env` file to Git
   - Keep `telegram_session.session` private

2. **Session file:**
   - `telegram_session.session` stores authentication
   - Anyone with this file can access your Telegram account
   - Don't share or upload this file

3. **Revoke access:**
   - If credentials compromised, delete the app at https://my.telegram.org/auth
   - Log out of all sessions via Telegram app settings

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

## File Structure

```
your-project/
├── telegram_channel_reader.py    # Main script
├── .env                           # Your credentials (git-ignored)
├── .env.example                   # Template
├── telegram_setup_guide.md        # This file
└── telegram_session.session       # Created on first run (git-ignored)
```

## References

- Telethon documentation: https://docs.telethon.dev/
- Telegram API: https://core.telegram.org/api
- API credentials: https://my.telegram.org/auth
