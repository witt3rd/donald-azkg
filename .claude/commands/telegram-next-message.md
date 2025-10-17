# Telegram: Get Next Unprocessed Message

Retrieve the next unprocessed message from Telegram Saved Messages and present options for handling it.

## Process

1. Read `.telegram_state.json` to get the last processed message info
2. If no messages processed yet, start from 2020-01-01
3. Fetch next message after the last processed one (limit: 1)
4. Display the message content with context (date, message ID)
5. Present options:
   - Create a note from this message
   - Skip/ignore this message
   - Stop processing

## After User Decision

**If creating a note:**
- Detect message type (URL, YouTube, PDF, text, etc.)
- Suggest appropriate handler command
- Wait for user to confirm

**If skipping:**
- Update `.telegram_state.json` with this message's ID and date
- Ask if user wants to continue to next message

**If stopping:**
- Do not update state
- Exit workflow

## State Management

Always update `.telegram_state.json` after processing each message:
```json
{
  "last_processed_message_id": <message_id>,
  "last_processed_date": "<ISO_date>",
  "saved_messages_dialog_id": 264837327
}
```

## Commands to Use

- `mcp__plugin_telegram_telegram__read_messages` - Fetch messages
- `Read` - Read state file
- `Write` - Update state file
