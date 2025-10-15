# Telegram Channel Reader

CLI tool to list your Telegram channels and read messages by date using the Telethon library.

## Features

- List all channels you have access to
- Read first message from a channel since a specified date/time
- Secure credential management with environment variables
- Session persistence (authenticate once)
- 2FA support

## Quick Start

### 1. Install with uv

```bash
cd telegram-reader
uv sync
```

### 2. Get Telegram API Credentials

1. Visit https://my.telegram.org/auth
2. Log in with your phone number
3. Go to "API development tools"
4. Create an application
5. Copy your `api_id` and `api_hash`

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your credentials
```

### 4. Run Commands

```bash
# List all your channels
uv run telegram-reader list-my-channels

# Read message from a channel
uv run telegram-reader read-message @channelname --since 2025-10-01

# With verbose logging
uv run telegram-reader -v read-message @channelname --since 2025-10-01
```

## Usage

### List Channels

```bash
uv run telegram-reader list-my-channels
```

Output:
```
Your channels:
--------------------------------------------------------------------------------
  ID: -1001234567890 | @technews         | Tech News Daily
  ID: -1009876543210 | @pythondev        | Python Developers
--------------------------------------------------------------------------------
Total: 2 channels
```

### Read Message

```bash
# By username
uv run telegram-reader read-message @channelname --since 2025-10-01

# By ID
uv run telegram-reader read-message -1001234567890 --since "2025-10-01T14:30:00"
```

## Date Formats

Accepts ISO 8601 format:
- `2025-10-01` (time defaults to 00:00:00)
- `2025-10-01T14:30:00` (date and time)
- `2025-10-01T14:30:00+00:00` (with timezone)

## Security

- Never commit `.env` file (git-ignored)
- Keep `*.session` files private (git-ignored)
- API credentials grant full account access

## Documentation

See `telegram_setup_guide.md` for complete setup instructions and troubleshooting.

## Dependencies

- Python 3.13+
- telethon - Telegram client library
- click - CLI framework
- python-dotenv - Environment variable management
- loguru - Logging

## License

MIT
