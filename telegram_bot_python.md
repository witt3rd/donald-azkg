---
tags: [python, telegram, bot, api, sdk, guide]
---
# Telegram Bot API and Python SDK

Complete guide to setting up Telegram Bot API keys and using Python SDKs to build bots and clients for the Telegram messaging platform.

## API Types and Use Cases

Telegram provides two distinct API approaches with different capabilities:

### Bot API (HTTPS/RESTful)
- **Purpose:** Building automated bot accounts that respond to user messages
- **Protocol:** HTTPS RESTful interface
- **Authentication:** Single bot token from BotFather
- **Use cases:** Chatbots, group moderation, notifications, automation, customer support
- **Limitations:** Cannot act as regular user accounts, restricted to bot-specific features
- **Python SDKs:** python-telegram-bot, aiogram

### TDLib/MTProto (Binary Protocol)
- **Purpose:** Full Telegram client functionality including user actions
- **Protocol:** MTProto binary protocol
- **Authentication:** api_id and api_hash from Telegram
- **Use cases:** Custom clients, userbots, advanced automation, data collection
- **Capabilities:** Send messages as user, make calls, access full Telegram features
- **Python SDKs:** telethon, pyrogram
- **Note:** Stricter terms of service compliance required

## Obtaining Bot API Keys

### Create Bot with BotFather

BotFather is Telegram's official bot for managing bot accounts:

1. Open Telegram and search for `@BotFather`
2. Start conversation and send `/newbot` command
3. Choose **display name** (can contain spaces): `Example Bot`
4. Choose **unique username** (must end with `bot`): `example_bot`
5. BotFather replies with bot token: `123456789:AAHfiqksKZ8WmR2zSjiQ7_v4TMAKdiHm9T0`

**Token format:** `{bot_id}:{random_string}`

### Obtaining TDLib/MTProto Credentials

For full client access (telethon/pyrogram):

1. Visit https://my.telegram.org/auth
2. Log in with phone number
3. Navigate to "API development tools"
4. Create application to receive `api_id` and `api_hash`

## Python SDK Options

### python-telegram-bot (Synchronous/Async)

Feature-rich library wrapping Bot API with strong community support:

```python
from telegram import Bot
from telegram.ext import Application, CommandHandler

API_TOKEN = "YOUR_BOT_TOKEN"

async def start(update, context):
    await update.message.reply_text("Hello, I am your bot!")

def main():
    app = Application.builder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    main()
```

**Features:**
- Modern async/await support (v20+)
- Comprehensive Bot API coverage
- Built-in handlers for commands, messages, callbacks
- Job queue for scheduled tasks
- Extensive documentation

### aiogram (Async-First)

High-performance async framework designed for concurrent operations:

```python
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm built with aiogram.")

if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling(bot))
```

**Features:**
- Native asyncio implementation
- Excellent performance under high load
- FSM (Finite State Machine) for conversation flows
- Modern Python 3.12+ syntax
- Middleware support for request processing

### telethon (MTProto Client)

Full Telegram client library for user and bot accounts:

```python
from telethon import TelegramClient

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start()
    await client.send_message('username', 'Hello from Telethon!')

with client:
    client.loop.run_until_complete(main())
```

**Features:**
- Full MTProto protocol implementation
- Act as user or bot
- Access to all Telegram features (channels, calls, etc.)
- Session management with automatic reconnection
- Event-driven architecture

### pyrogram (Hybrid Bot/Client)

Modern MTProto library supporting both bot and user modes:

```python
from pyrogram import Client

app = Client(
    "my_bot",
    api_id="YOUR_API_ID",
    api_hash="YOUR_API_HASH",
    bot_token="YOUR_BOT_TOKEN"
)

@app.on_message()
async def hello(client, message):
    await message.reply("Hello from Pyrogram!")

app.run()
```

**Features:**
- Simplified API compared to telethon
- Supports both bot tokens and user sessions
- Built-in file handling and media processing
- Plugin system for modular code
- Smart session management

## Secure Credential Management

### Environment Variables with python-dotenv

**Never hardcode API tokens in source files.** Use environment variables:

```python
import os
from dotenv import load_dotenv
from telegram.ext import Application

load_dotenv()  # Loads from .env file

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set")

app = Application.builder().token(API_TOKEN).build()
```

**.env file format:**
```bash
TELEGRAM_BOT_TOKEN=123456789:AAHfiqksKZ8WmR2zSjiQ7_v4TMAKdiHm9T0
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=1234567890abcdef1234567890abcdef
```

**Add to .gitignore:**
```
.env
*.session
*.session-journal
```

### Production Secrets Management

For cloud deployments:

- **AWS:** AWS Secrets Manager, Parameter Store
- **Azure:** Azure Key Vault
- **Google Cloud:** Secret Manager
- **Kubernetes:** Sealed Secrets, External Secrets Operator
- **Docker:** Docker secrets, environment injection

### Best Practices

1. **Separate tokens per environment** (development, staging, production)
2. **Rotate credentials periodically** and immediately if exposed
3. **Use dedicated bot accounts** - one bot per project
4. **Restrict token access** with least privilege principle
5. **Monitor token usage** through BotFather analytics
6. **Never log tokens** in application logs or error messages
7. **Revoke compromised tokens** immediately via BotFather

## Common Bot Patterns

### Command Handlers

```python
from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text("Welcome!")

async def help_command(update, context):
    await update.message.reply_text("Available commands:\n/start - Start bot\n/help - Show help")

app = Application.builder().token(API_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
```

### Inline Keyboards

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def show_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1')],
        [InlineKeyboardButton("Option 2", callback_data='2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose option:", reply_markup=reply_markup)

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"Selected: {query.data}")
```

### Conversation State Management (aiogram FSM)

```python
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    age = State()

@dp.message(Command("register"))
async def register_start(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("What's your name?")

@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("How old are you?")
```

### Notification Bot Pattern

```python
import asyncio
from telegram import Bot

async def send_notification(bot_token: str, chat_id: str, message: str):
    """Send notification from external system (CI/CD, monitoring, IoT)."""
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

# Use from any Python application
asyncio.run(send_notification(
    bot_token=os.getenv("BOT_TOKEN"),
    chat_id="@channel_name",
    message="Deployment completed successfully!"
))
```

## Current State (2025)

### Bot API Updates (v7.0+)

- **Stories support:** Bots can post and react to stories
- **Reactions:** Enhanced reaction types including custom emoji
- **Protected content:** No-forward and self-destruct message controls
- **Premium features:** Access to premium emoji and features
- **Media editing:** Edit images, videos in sent messages
- **Improved polls:** Quiz mode, multiple answer types
- **Business accounts:** Bot integration with Telegram Business

### SDK Maturity

- **python-telegram-bot v21+:** Python 3.12+ support, improved async patterns
- **aiogram v3+:** Complete rewrite with modern asyncio, FSM improvements
- **telethon v1.36+:** Multi-factor auth, enhanced session security
- **pyrogram v2+:** Unified bot/client API, improved file handling

### Rate Limits and Performance

- **Bot API:** 30 messages/second per bot, 20 messages/minute per chat group
- **Webhook mode:** Recommended for production (push vs polling)
- **File uploads:** 50MB via Bot API, 2GB via client libraries
- **Message length:** 4096 characters per message

## Related Concepts

### Prerequisites
- [[python_coding_standards]] - Python best practices for building reliable bots
- [[uv]] - Modern Python package manager for installing Telegram SDKs

### Related Topics
- [[openrouter_openai_python_sdk]] - Similar pattern of SDK configuration and API key management
- [[youtube_transcript_api]] - Another Python API integration example
- [[tenacity]] - Retry logic for handling Telegram API rate limits and network errors

### Extends
- [[python_coding_standards]] - Applies Python standards to bot development

## References

[1] https://core.telegram.org/bots/api - Official Telegram Bot API documentation
[2] https://core.telegram.org/bots/tutorial - Bot development tutorial
[3] https://docs.siteguarding.com/en/how-to-create-telegram-bot-api-token - BotFather setup guide
