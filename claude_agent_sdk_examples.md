---
tags: [agents, examples, code, reference, claude-code]
---
# Claude Agent SDK: Real Production Examples

This note contains real, production-tested code examples from the ottomator-agents repository demonstrating practical Agent SDK implementations. All code is battle-tested and actively used in production.

## Repository Reference

**Source**: [coleam00/ottomator-agents](https://github.com/coleam00/ottomator-agents/tree/main/claude-agent-sdk-demos)

**Key implementations**:
- `quickstart/` - Basic examples for learning
- `telegram_integration/` - Full Telegram bot with session management
- `obsidian_integration/` - OpenAI-compatible API for Obsidian

## Example 1: Simple Interactive CLI

**Source**: `quickstart/simple_cli.py`

A clean, minimal CLI demonstrating core Agent SDK patterns.

**Key features**:
- Session persistence (resume conversations)
- Streaming response display
- Tool usage indicators
- Color-coded output

**Complete implementation**:

```python
import asyncio
import json
import os
from pathlib import Path
from typing import Optional

from colorama import init, Fore, Style, Back
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage
)

# Initialize colorama for colors
init(autoreset=True)

# Session storage
SESSIONS_DIR = Path("sessions")
CURRENT_SESSION_FILE = SESSIONS_DIR / "current_session.json"

def save_session(session_id: str):
    """Save session ID for resuming later."""
    SESSIONS_DIR.mkdir(exist_ok=True)
    with open(CURRENT_SESSION_FILE, "w") as f:
        json.dump({"session_id": session_id}, f)

def load_session() -> Optional[str]:
    """Load last session ID."""
    if CURRENT_SESSION_FILE.exists():
        with open(CURRENT_SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("session_id")
    return None

async def chat_loop(resume_session: bool = False):
    """Main chat loop."""

    # Load session if resuming
    session_id = None
    if resume_session:
        session_id = load_session()
        if session_id:
            print(f"{Fore.CYAN}📂 Resuming previous conversation\n")

    # Configure agent
    options_dict = {
        "cwd": os.getcwd(),
        "system_prompt": "You are a helpful AI assistant.",
        "allowed_tools": ["Read", "Write", "Bash"],
    }

    if session_id:
        options_dict["resume"] = session_id

    options = ClaudeAgentOptions(**options_dict)

    print(f"\n{Fore.MAGENTA}{'=' * 60}")
    print(f"{Fore.MAGENTA}  Claude Agent SDK - Terminal Chat")
    print(f"{Fore.MAGENTA}{'=' * 60}")
    print(f"{Style.DIM}Type 'exit' or 'quit' to end\n")

    # Create client and chat
    async with ClaudeSDKClient(options=options) as client:
        while True:
            try:
                user_input = input(f"{Fore.CYAN}You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Fore.YELLOW}👋 Goodbye!")
                break

            if not user_input or user_input.lower() in ["exit", "quit"]:
                break

            # Send query
            await client.query(user_input)

            print(f"\n{Fore.GREEN}Claude: ", end="", flush=True)

            # Stream response
            current_session_id = None
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"{Fore.GREEN}{block.text}", end="", flush=True)
                        elif isinstance(block, ToolUseBlock):
                            print(f"\n{Back.MAGENTA}{Fore.WHITE} 🔧 {block.name.upper()} ", flush=True)

                elif isinstance(message, ResultMessage):
                    current_session_id = message.session_id
                    print("\n")

            # Save session
            if current_session_id:
                save_session(current_session_id)

def main():
    import sys
    resume = "--continue" in sys.argv

    try:
        asyncio.run(chat_loop(resume_session=resume))
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Goodbye!")

if __name__ == "__main__":
    main()
```

**Usage**:
```bash
# Start new conversation
python simple_cli.py

# Resume last conversation
python simple_cli.py --continue
```

**Key patterns demonstrated**:
- `ClaudeSDKClient` context manager for connection handling
- `receive_response()` for streaming complete responses
- Session persistence across runs
- Tool use detection and display

## Example 2: Telegram Bot with Per-User Sessions

**Source**: `telegram_integration/telegram_bot.py`

Production Telegram bot with advanced session management.

**Architecture**:
- Per-user session isolation
- Per-user working directory configuration
- Persistent conversation context
- Command-based directory management

**Session management implementation**:

```python
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

SESSIONS_DIR = Path("telegram_sessions")
SESSIONS_DIR.mkdir(exist_ok=True)

def save_user_session(user_id: int, session_id: str, cwd: Optional[str] = None):
    """Save session data for a Telegram user."""
    session_file = SESSIONS_DIR / f"{user_id}.json"

    # Load existing to preserve fields
    existing_data = {}
    if session_file.exists():
        with open(session_file, "r") as f:
            existing_data = json.load(f)

    # Update session data
    session_data = {
        "session_id": session_id,
        "cwd": cwd or existing_data.get("cwd"),
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }

    # Preserve created_at
    if "created_at" in existing_data:
        session_data["created_at"] = existing_data["created_at"]
    else:
        session_data["created_at"] = session_data["last_updated"]

    with open(session_file, "w") as f:
        json.dump(session_data, f, indent=2)

def load_user_session(user_id: int) -> Optional[Tuple[str, str]]:
    """Load session data for a user."""
    session_file = SESSIONS_DIR / f"{user_id}.json"

    if not session_file.exists():
        return None

    with open(session_file, "r") as f:
        data = json.load(f)
        session_id = data.get("session_id")
        cwd = data.get("cwd")
        return (session_id, cwd) if session_id else None

def clear_user_session(user_id: int):
    """Clear session but keep cwd configuration."""
    session_file = SESSIONS_DIR / f"{user_id}.json"

    if session_file.exists():
        with open(session_file, "r") as f:
            data = json.load(f)

        # Keep only cwd
        new_data = {
            "cwd": data.get("cwd"),
            "created_at": data.get("created_at"),
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }

        with open(session_file, "w") as f:
            json.dump(new_data, f, indent=2)
```

**Message handler with Agent SDK**:

```python
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages from Telegram users."""
    user_id = update.effective_user.id
    user_message = update.message.text

    # Load user's session and working directory
    session_data = load_user_session(user_id)
    session_id = None
    cwd = None

    if session_data:
        session_id, cwd = session_data

    if not cwd:
        cwd = os.getenv("WORKING_DIRECTORY", os.getcwd())

    # Configure agent with user's settings
    options_dict = {
        "cwd": cwd,
        "system_prompt": "You are Claude Code, a helpful AI assistant.",
        "allowed_tools": ["Read", "Write", "Bash", "Edit"],
    }

    if session_id:
        options_dict["resume"] = session_id

    options = ClaudeAgentOptions(**options_dict)

    # Send typing indicator
    await update.message.chat.send_action("typing")

    # Initialize collectors
    response_parts = []
    tool_uses = []
    new_session_id = None

    # Query agent
    async with ClaudeSDKClient(options=options) as client:
        await client.query(user_message)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_parts.append(block.text)
                    elif isinstance(block, ToolUseBlock):
                        tool_uses.append(f"🔧 {block.name.upper()}")

            elif isinstance(message, ResultMessage):
                new_session_id = message.session_id

    # Build response
    full_response = "".join(response_parts)

    if tool_uses:
        full_response += "\n\n" + " ".join(tool_uses)

    # Send to user
    await send_long_message(update.message.chat_id, full_response, context)

    # Save session
    if new_session_id:
        save_user_session(user_id, new_session_id, cwd)
```

**Handling Telegram message length limits**:

```python
MAX_TELEGRAM_MESSAGE_LENGTH = 4096

async def send_long_message(chat_id: int, text: str, context: ContextTypes.DEFAULT_TYPE):
    """Send long messages, splitting if necessary."""
    if len(text) <= MAX_TELEGRAM_MESSAGE_LENGTH:
        await context.bot.send_message(chat_id=chat_id, text=text)
    else:
        # Split by lines to avoid breaking mid-sentence
        chunks = []
        current_chunk = ""

        for line in text.split("\n"):
            if len(current_chunk) + len(line) + 1 > MAX_TELEGRAM_MESSAGE_LENGTH - 100:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = line
            else:
                current_chunk += "\n" + line if current_chunk else line

        if current_chunk:
            chunks.append(current_chunk)

        # Send all chunks
        for i, chunk in enumerate(chunks):
            if i > 0:
                chunk = f"(continued {i+1}/{len(chunks)})\n\n{chunk}"
            await context.bot.send_message(chat_id=chat_id, text=chunk)
```

**Command handlers**:

```python
async def setcwd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set working directory for user."""
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a directory path.\n"
            "Usage: /setcwd <path>"
        )
        return

    path = " ".join(context.args)

    if not os.path.exists(path) or not os.path.isdir(path):
        await update.message.reply_text(f"❌ Invalid directory: {path}")
        return

    abs_path = os.path.abspath(path)
    set_user_cwd(user_id, abs_path)

    await update.message.reply_text(
        f"✅ Working directory set to:\n{abs_path}"
    )

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear conversation but keep working directory."""
    user_id = update.effective_user.id
    clear_user_session(user_id)

    await update.message.reply_text(
        "🔄 Conversation cleared!\n"
        "Your working directory setting has been preserved."
    )
```

**Bot initialization**:

```python
def main():
    """Start the Telegram bot."""
    bot_token = os.getenv("TELEGRAM_BOT_API_KEY")

    application = ApplicationBuilder().token(bot_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("setcwd", setcwd_command))
    application.add_handler(CommandHandler("getcwd", getcwd_command))
    application.add_handler(CommandHandler("reset", reset_command))

    # Message handler for regular text
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.run_polling()
```

## Example 3: OpenAI-Compatible API Server

**Source**: `obsidian_integration/api_server.py`

FastAPI server providing OpenAI-compatible endpoints for integration with tools like Obsidian Copilot.

**Complete API server**:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import time
from pathlib import Path

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, ResultMessage

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = None

class ChatCompletionRequest(BaseModel):
    model: str = "claude-sonnet-4"
    messages: List[ChatMessage]
    stream: bool = False

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[dict]
    usage: dict

# Session management
SESSIONS_DIR = Path("api_sessions")
SESSIONS_DIR.mkdir(exist_ok=True)

def save_session(conversation_id: str, session_id: str):
    session_file = SESSIONS_DIR / f"{conversation_id}.json"
    with open(session_file, "w") as f:
        json.dump({"session_id": session_id}, f)

def load_session(conversation_id: str) -> Optional[str]:
    session_file = SESSIONS_DIR / f"{conversation_id}.json"
    if session_file.exists():
        with open(session_file, "r") as f:
            return json.load(f).get("session_id")
    return None

def is_continuing_conversation(messages: List[ChatMessage]) -> bool:
    """Check if this is a multi-turn conversation."""
    user_message_count = sum(1 for msg in messages if msg.role == "user")
    return user_message_count > 1

# FastAPI app
app = FastAPI(
    title="Claude Agent SDK API",
    description="OpenAI-compatible API powered by Claude Agent SDK"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """OpenAI-compatible chat completions endpoint."""

    # Extract latest user message
    user_query = ""
    for msg in reversed(request.messages):
        if msg.role == "user" and msg.content:
            user_query = msg.content
            break

    if not user_query:
        raise HTTPException(status_code=400, detail="No user message found")

    # Check if continuing conversation
    is_continuation = is_continuing_conversation(request.messages)
    session_id = None

    if is_continuation:
        session_id = load_session("current")
        if session_id:
            print(f"📂 Resuming session: {session_id}")

    # Configure agent
    options_dict = {
        "cwd": os.getenv("WORKING_DIRECTORY", os.getcwd()),
        "system_prompt": "You are a helpful AI assistant.",
        "allowed_tools": ["Read", "Write", "Bash", "Edit"],
        "mcp_servers": {
            "sequential-thinking": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
            }
        }
    }

    if session_id:
        options_dict["resume"] = session_id

    options = ClaudeAgentOptions(**options_dict)

    # Handle streaming
    if request.stream:
        async def stream_response():
            new_session_id = None

            async with ClaudeSDKClient(options=options) as client:
                await client.query(user_query)

                async for chunk, captured_session_id in convert_sdk_to_openai_stream(
                    client.receive_messages(),
                    model_name=request.model
                ):
                    yield chunk
                    if captured_session_id:
                        new_session_id = captured_session_id

            if new_session_id:
                save_session("current", new_session_id)

        return StreamingResponse(
            stream_response(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

    # Non-streaming response
    else:
        new_session_id = None
        messages = []

        async with ClaudeSDKClient(options=options) as client:
            await client.query(user_query)

            async for message in client.receive_response():
                messages.append(message)
                if isinstance(message, ResultMessage):
                    new_session_id = message.session_id

        full_response = extract_full_response_text(messages)

        if new_session_id:
            save_session("current", new_session_id)

        response = ChatCompletionResponse(
            id=f"chatcmpl-{int(time.time())}",
            created=int(time.time()),
            model=request.model,
            choices=[{
                "index": 0,
                "message": {"role": "assistant", "content": full_response},
                "finish_reason": "stop"
            }],
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        )

        return JSONResponse(content=response.model_dump())

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "claude-agent-sdk-api"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))

    print("=" * 60)
    print("Claude Agent SDK API Server")
    print("=" * 60)
    print(f"Starting server on http://0.0.0.0:{port}")
    print(f"Documentation: http://localhost:{port}/docs")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=port)
```

**OpenAI format converter helper** (conceptual):

```python
async def convert_sdk_to_openai_stream(messages, model_name: str):
    """Convert Claude SDK messages to OpenAI SSE format."""
    completion_id = f"chatcmpl-{int(time.time())}"

    async for message in messages:
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    chunk = {
                        "id": completion_id,
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": model_name,
                        "choices": [{
                            "index": 0,
                            "delta": {"content": block.text},
                            "finish_reason": None
                        }]
                    }
                    yield f"data: {json.dumps(chunk)}\n\n", None

        elif isinstance(message, ResultMessage):
            # Final chunk
            chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": model_name,
                "choices": [{
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop"
                }]
            }
            yield f"data: {json.dumps(chunk)}\n\n", message.session_id
            yield "data: [DONE]\n\n", None
```

## Key Patterns Demonstrated

### 1. Session Management Pattern

**File-based session storage**:
- One JSON file per user/conversation
- Preserve metadata (created_at, last_updated)
- Separate session ID from configuration (cwd)

**Benefits**:
- Simple, no database required
- Easy to inspect and debug
- Survives bot restarts

### 2. Context Manager Pattern

**Always use `async with` for ClaudeSDKClient**:

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query(user_message)
    async for message in client.receive_response():
        # Process messages
        pass
```

**Why**:
- Ensures proper connection cleanup
- Handles errors gracefully
- Resource management

### 3. Response Streaming Pattern

**Two methods available**:

```python
# Method 1: receive_response() - Waits for complete response
async for message in client.receive_response():
    # All messages until ResultMessage
    pass

# Method 2: receive_messages() - Incremental streaming
async for message in client.receive_messages():
    # Messages as they arrive, no automatic stopping
    pass
```

**Use `receive_response()` for**:
- Turn-based chat interfaces
- When you need the complete response
- Simpler code

**Use `receive_messages()` for**:
- Real-time streaming UIs
- Custom flow control
- Advanced use cases

### 4. Tool Usage Detection Pattern

```python
tool_uses = []

async for message in client.receive_response():
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                tool_uses.append(block.name)

# Display tool usage summary
if tool_uses:
    print(f"Tools used: {', '.join(tool_uses)}")
```

### 5. Error Handling Pattern

```python
try:
    async with ClaudeSDKClient(options=options) as client:
        await client.query(user_message)
        # ... process response
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    # Provide user-friendly error message
    await send_error_message(f"⚠️ Error: {str(e)}")
```

## Configuration Patterns

### Basic Configuration

```python
options = ClaudeAgentOptions(
    cwd="/path/to/workspace",
    system_prompt="You are a helpful assistant.",
    allowed_tools=["Read", "Write", "Bash"]
)
```

### With Session Resume

```python
options = ClaudeAgentOptions(
    cwd="/path/to/workspace",
    system_prompt="You are a helpful assistant.",
    allowed_tools=["Read", "Write", "Bash"],
    resume="session-uuid-here"  # Resume existing conversation
)
```

### With MCP Servers

```python
options = ClaudeAgentOptions(
    cwd="/path/to/workspace",
    system_prompt="You are a helpful assistant.",
    allowed_tools=["Read", "Write", "Bash"],
    mcp_servers={
        "sequential-thinking": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
        },
        "custom-tool": {
            "command": "uv",
            "args": ["--directory", "/path/to/server", "run", "server.py"]
        }
    }
)
```

## Deployment Considerations

### Environment Variables

```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-...          # Optional if using CLI OAuth
TELEGRAM_BOT_API_KEY=123456:ABC-...   # For Telegram bot
PORT=8003                              # API server port
WORKING_DIRECTORY=/path/to/workspace   # Default working directory
```

### Authentication

**Two options**:

1. **CLI OAuth** (Recommended for development):
```bash
claude auth login
```

2. **API Key** (For production):
```python
# SDK automatically uses ANTHROPIC_API_KEY environment variable
```

### Dependencies

```txt
# requirements.txt
claude-agent-sdk>=1.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
python-telegram-bot>=20.0
python-dotenv>=1.0.0
colorama>=0.4.6
```

## Testing Examples

### Unit Test for Session Management

```python
import pytest
from pathlib import Path
import json

def test_save_and_load_session(tmp_path):
    """Test session persistence."""
    # Use temporary directory
    global SESSIONS_DIR
    SESSIONS_DIR = tmp_path

    user_id = 12345
    session_id = "test-session-uuid"
    cwd = "/test/path"

    # Save session
    save_user_session(user_id, session_id, cwd)

    # Load session
    loaded_session_id, loaded_cwd = load_user_session(user_id)

    assert loaded_session_id == session_id
    assert loaded_cwd == cwd

    # Verify file structure
    session_file = tmp_path / f"{user_id}.json"
    assert session_file.exists()

    with open(session_file) as f:
        data = json.load(f)
        assert "created_at" in data
        assert "last_updated" in data
```

### Integration Test for Agent Query

```python
@pytest.mark.asyncio
async def test_agent_query():
    """Test basic agent query."""
    options = ClaudeAgentOptions(
        cwd=".",
        system_prompt="You are a test assistant.",
        allowed_tools=["Read"]
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("What is 2+2?")

        response_text = ""
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_text += block.text

        assert "4" in response_text.lower()
```

## Related Concepts

### Prerequisites
- [[claude_agent_sdk]] - Understanding SDK fundamentals before implementation examples

### Related Topics
- [[claude_agent_sdk_production]] - Production patterns and observability
- [[python_mcp_sdk]] - MCP server integration examples
- [[mcp_overview]] - MCP protocol used in examples

### Extends
- [[claude_agent_sdk]] - Real code examples extend conceptual understanding

## References

[1] https://github.com/coleam00/ottomator-agents/tree/main/claude-agent-sdk-demos - Source repository
[2] https://docs.claude.com/en/api/agent-sdk/python - Official Python SDK documentation
