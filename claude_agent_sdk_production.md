---
tags: [agents, deployment, observability, production, monitoring, claude-code]
---
# Claude Agent SDK: Production Deployment and Observability

Production deployment of Claude Agent SDK requires careful consideration of architecture patterns, monitoring strategies, error handling, and operational excellence. This note covers real-world patterns for building reliable, observable agent systems.

## Production Architecture Patterns

### 1. API Wrapper Pattern

Wrap the Agent SDK with a standard API interface (OpenAI-compatible or custom) to enable integration with existing tools and services.

**Why this pattern:**

- Existing tools expect OpenAI-compatible endpoints
- Enables drop-in replacement for other LLM APIs
- Provides abstraction layer for future SDK changes
- Allows middleware injection (auth, rate limiting, logging)

**Implementation:**

```python
from fastapi import FastAPI, HTTPException
from claude_agent_sdk import Agent, query
from pydantic import BaseModel
import asyncio

app = FastAPI(title="Claude Agent API")

class ChatRequest(BaseModel):
    messages: list[dict[str, str]]
    model: str = "claude-sonnet-4-5"
    stream: bool = False

class ChatResponse(BaseModel):
    choices: list[dict]
    usage: dict

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """OpenAI-compatible endpoint for Claude Agent SDK"""

    # Convert OpenAI format to Agent SDK format
    conversation = format_openai_to_claude(request.messages)

    # Configure agent options
    options = {
        "model": request.model,
        "system_prompt": extract_system_prompt(request.messages),
        "allowed_tools": ["read", "write", "bash"],
        "current_working_directory": "/workspace"
    }

    # Query agent
    messages = []
    total_tokens = 0

    for message in query(conversation, options):
        messages.append(convert_message_to_openai(message))
        total_tokens += estimate_tokens(message)

    # Return OpenAI-compatible response
    return ChatResponse(
        choices=[{
            "message": messages[-1],
            "finish_reason": "stop"
        }],
        usage={
            "prompt_tokens": total_tokens // 2,
            "completion_tokens": total_tokens // 2,
            "total_tokens": total_tokens
        }
    )

def format_openai_to_claude(messages: list[dict]) -> str:
    """Convert OpenAI message format to Claude conversation"""
    return "\n\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in messages
    ])

def convert_message_to_openai(claude_message) -> dict:
    """Convert Claude SDK message to OpenAI format"""
    return {
        "role": "assistant",
        "content": extract_content(claude_message)
    }
```

**Real-world example**: The video demonstrates wrapping Agent SDK for Obsidian's Copilot plugin, which expects OpenAI-compatible endpoints.

### 2. Messaging Platform Integration Pattern

Integrate Agent SDK with messaging platforms (Telegram, Slack, Discord) for remote agent control.

**Why this pattern:**

- Enables mobile access to agents
- Asynchronous communication model
- Built-in user authentication
- Rich formatting support
- Notification capabilities

**Implementation (Telegram Bot):**

```python
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes
from claude_agent_sdk import Agent
import os

class ClaudeAgentBot:
    def __init__(self, token: str):
        self.app = Application.builder().token(token).build()
        self.working_directory = os.getcwd()

        # Register handlers
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        self.app.add_handler(CommandHandler("setdir", self.set_directory))
        self.app.add_handler(CommandHandler("status", self.get_status))

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages as agent queries"""
        user_message = update.message.text
        chat_id = update.effective_chat.id

        # Send "typing" indicator
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        try:
            # Configure agent
            options = {
                "current_working_directory": self.working_directory,
                "system_prompt": "You are a helpful coding assistant accessible via Telegram.",
                "allowed_tools": ["read", "write", "bash", "glob", "grep"],
                "mcp_servers": self.get_mcp_config()
            }

            # Query agent and collect responses
            responses = []
            tool_calls = []

            for message in query(user_message, options):
                if message.type == "text":
                    responses.append(message.content)
                elif message.type == "tool_use":
                    tool_calls.append(f"🔧 {message.tool_name}: {message.args}")

            # Send tool usage summary
            if tool_calls:
                await update.message.reply_text(
                    "**Tools used:**\n" + "\n".join(tool_calls)
                )

            # Send agent response
            full_response = "\n\n".join(responses)
            await update.message.reply_text(full_response)

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

    async def set_directory(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Change agent's working directory remotely"""
        if not context.args:
            await update.message.reply_text("Usage: /setdir <path>")
            return

        new_dir = " ".join(context.args)
        if os.path.isdir(new_dir):
            self.working_directory = new_dir
            await update.message.reply_text(f"✅ Working directory set to: {new_dir}")
        else:
            await update.message.reply_text(f"❌ Invalid directory: {new_dir}")

    async def get_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get current agent configuration"""
        status = f"""
**Agent Status**
📁 Working Directory: `{self.working_directory}`
🛠️ MCP Servers: {len(self.get_mcp_config())}
"""
        await update.message.reply_text(status)

    def get_mcp_config(self) -> list:
        """Load MCP server configuration"""
        # Load from config file or environment
        return []

    def run(self):
        """Start the bot"""
        self.app.run_polling()

# Usage
if __name__ == "__main__":
    bot = ClaudeAgentBot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    bot.run()
```

**Key features from video:**

- Dynamic working directory changes via `/setdir` command
- Agent can modify its own configuration files
- Tool usage displayed in chat
- Mobile access for remote task triggering

### 3. Knowledge Management Integration Pattern

Integrate Agent SDK with knowledge management tools (Obsidian, Notion, Roam) for intelligent note-taking and content management.

**Why this pattern:**

- Leverage agent's file manipulation capabilities
- Context-aware note creation and linking
- Automated knowledge graph maintenance
- Content generation and summarization

**Implementation (Obsidian Integration):**

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from claude_agent_sdk import Agent, query
import json

app = FastAPI()

@app.post("/v1/chat/completions")
async def obsidian_chat(request: Request):
    """Endpoint for Obsidian Copilot plugin"""

    data = await request.json()
    messages = data.get("messages", [])
    stream = data.get("stream", False)

    # Extract vault path from config
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "/path/to/vault")

    # Configure agent for knowledge management
    options = {
        "current_working_directory": vault_path,
        "system_prompt": """You are an expert knowledge management assistant for Obsidian.

Your tasks:
- Help organize and link notes
- Summarize content and extract key insights
- Create new notes with proper frontmatter
- Maintain consistent formatting
- Suggest related notes and connections
- Generate content outlines and templates

Always use wikilink format [[note]] for internal links.
Add appropriate tags in YAML frontmatter.
""",
        "allowed_tools": ["read", "write", "glob", "grep", "edit"],
        "mcp_servers": [{
            "sequential_thinking": {
                "command": "uvx",
                "args": ["mcp-server-sequential-thinking"]
            }
        }]
    }

    # Process query
    if stream:
        return StreamingResponse(
            stream_agent_response(messages, options),
            media_type="text/event-stream"
        )
    else:
        return await get_complete_response(messages, options)

async def stream_agent_response(messages, options):
    """Stream agent responses in SSE format"""
    for message in query(format_messages(messages), options):
        chunk = format_sse_chunk(message)
        yield f"data: {json.dumps(chunk)}\n\n"

    # Send done signal
    yield "data: [DONE]\n\n"

def format_sse_chunk(message):
    """Format message as SSE chunk"""
    return {
        "id": message.id,
        "object": "chat.completion.chunk",
        "choices": [{
            "delta": {"content": extract_content(message)},
            "finish_reason": None if not message.is_final else "stop"
        }]
    }
```

**Real-world usage from video:**

- "Add bullet points to my script" - Agent finds file, edits it
- "Make my list shorter" - Agent reads, condenses, updates
- Operates on markdown files with wikilinks
- Maintains vault structure and conventions

## Observability and Monitoring

### 1. Sentry Integration for Agent Tracing

**Why Sentry:**

- Distributed tracing for agent workflows
- Tool call visibility
- Token usage tracking
- Error tracking and alerting
- Performance metrics

**Implementation:**

```python
import sentry_sdk
from sentry_sdk.integrations.anthropic import AnthropicIntegration
from claude_agent_sdk import Agent, query

# Initialize Sentry with Anthropic integration
sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[
        AnthropicIntegration(
            include_prompts=True,  # Log full prompts
            include_completions=True  # Log full responses
        )
    ],
    traces_sample_rate=1.0,  # Capture 100% of traces
    profiles_sample_rate=1.0  # Enable profiling
)

def query_with_tracing(user_input: str, options: dict):
    """Query agent with Sentry tracing"""

    # Start transaction
    with sentry_sdk.start_transaction(op="agent.query", name="Claude Agent Query") as transaction:
        transaction.set_tag("working_directory", options.get("current_working_directory"))
        transaction.set_tag("model", options.get("model", "claude-sonnet-4-5"))

        try:
            responses = []
            tool_calls = []
            total_tokens = 0

            for message in query(user_input, options):
                # Track tool usage
                if message.type == "tool_use":
                    with sentry_sdk.start_span(op="tool.call", description=message.tool_name) as span:
                        span.set_data("tool_args", message.args)
                        tool_calls.append(message.tool_name)

                # Track tokens
                if hasattr(message, "usage"):
                    total_tokens += message.usage.total_tokens

                responses.append(message)

            # Set transaction data
            transaction.set_measurement("tokens.total", total_tokens)
            transaction.set_measurement("tools.count", len(tool_calls))
            transaction.set_tag("tools_used", ",".join(set(tool_calls)))

            return responses

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise

# Usage
options = {
    "current_working_directory": "/workspace",
    "system_prompt": "You are a helpful assistant.",
    "allowed_tools": ["read", "write", "bash"]
}

responses = query_with_tracing("Refactor main.py for readability", options)
```

**What you get in Sentry dashboard:**

- Every agent interaction as a trace
- Tool execution timeline
- Token usage per query
- Error rates and types
- Response time percentiles
- Tool call parameters and results

**Example from video:**
The presenter showed Sentry traces for:

- Sequential thinking MCP calls (multiple thinking steps)
- File edit operations (showing exact file paths)
- Token usage metrics per request
- Total execution time

### 2. Structured Logging Pattern

**Implementation:**

```python
import logging
import json
from datetime import datetime
from typing import Any

class AgentLogger:
    """Structured logger for agent operations"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.logger.setLevel(logging.INFO)

        # JSON formatter for structured logs
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

    def log_query_start(self, user_input: str, options: dict):
        """Log query initiation"""
        self._log({
            "event": "query.start",
            "user_input": user_input[:100],  # Truncate
            "working_directory": options.get("current_working_directory"),
            "model": options.get("model"),
            "tools_allowed": options.get("allowed_tools", [])
        })

    def log_tool_call(self, tool_name: str, args: dict, result: Any = None, error: str = None):
        """Log tool execution"""
        self._log({
            "event": "tool.call",
            "tool_name": tool_name,
            "args": args,
            "success": error is None,
            "error": error,
            "result_preview": str(result)[:200] if result else None
        })

    def log_token_usage(self, input_tokens: int, output_tokens: int, total_tokens: int):
        """Log token consumption"""
        self._log({
            "event": "tokens.usage",
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens
        })

    def log_query_complete(self, duration_ms: int, message_count: int, success: bool):
        """Log query completion"""
        self._log({
            "event": "query.complete",
            "duration_ms": duration_ms,
            "message_count": message_count,
            "success": success
        })

    def log_error(self, error: Exception, context: dict = None):
        """Log error with context"""
        self._log({
            "event": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {}
        })

    def _log(self, data: dict):
        """Internal structured log method"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": self.agent_id,
            **data
        }
        self.logger.info(json.dumps(log_entry))

# Usage in agent wrapper
class MonitoredAgent:
    def __init__(self, agent_id: str, options: dict):
        self.agent_id = agent_id
        self.options = options
        self.logger = AgentLogger(agent_id)

    def query(self, user_input: str):
        """Query with comprehensive logging"""
        start_time = datetime.now()
        self.logger.log_query_start(user_input, self.options)

        try:
            responses = []
            for message in query(user_input, self.options):

                # Log tool usage
                if message.type == "tool_use":
                    self.logger.log_tool_call(
                        message.tool_name,
                        message.args,
                        result=message.result if hasattr(message, 'result') else None
                    )

                # Log token usage
                if hasattr(message, "usage"):
                    self.logger.log_token_usage(
                        message.usage.input_tokens,
                        message.usage.output_tokens,
                        message.usage.total_tokens
                    )

                responses.append(message)

            # Log completion
            duration = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.log_query_complete(duration, len(responses), True)

            return responses

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.log_error(e, {"user_input": user_input})
            self.logger.log_query_complete(duration, 0, False)
            raise
```

**Log output example:**

```json
{"timestamp": "2025-10-17T10:30:00.000Z", "agent_id": "telegram-bot-1", "event": "query.start", "user_input": "Add sequential thinking MCP to my agent", "working_directory": "/workspace", "model": "claude-sonnet-4-5", "tools_allowed": ["read", "write", "glob"]}
{"timestamp": "2025-10-17T10:30:01.234Z", "agent_id": "telegram-bot-1", "event": "tool.call", "tool_name": "glob", "args": {"pattern": "**/*.py"}, "success": true}
{"timestamp": "2025-10-17T10:30:02.456Z", "agent_id": "telegram-bot-1", "event": "tool.call", "tool_name": "read", "args": {"file_path": "bot.py"}, "success": true}
{"timestamp": "2025-10-17T10:30:05.678Z", "agent_id": "telegram-bot-1", "event": "tool.call", "tool_name": "edit", "args": {"file_path": "bot.py", "changes": "..."}, "success": true}
{"timestamp": "2025-10-17T10:30:06.890Z", "agent_id": "telegram-bot-1", "event": "tokens.usage", "input_tokens": 1250, "output_tokens": 450, "total_tokens": 1700}
{"timestamp": "2025-10-17T10:30:07.000Z", "agent_id": "telegram-bot-1", "event": "query.complete", "duration_ms": 7000, "message_count": 8, "success": true}
```

### 3. Custom Metrics and Dashboards

**Implementation with Prometheus:**

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from functools import wraps
import time

# Define metrics
agent_queries_total = Counter(
    'agent_queries_total',
    'Total number of agent queries',
    ['agent_id', 'status']
)

agent_query_duration_seconds = Histogram(
    'agent_query_duration_seconds',
    'Agent query duration in seconds',
    ['agent_id']
)

agent_tokens_total = Counter(
    'agent_tokens_total',
    'Total tokens consumed',
    ['agent_id', 'token_type']
)

agent_tool_calls_total = Counter(
    'agent_tool_calls_total',
    'Total tool calls made',
    ['agent_id', 'tool_name', 'status']
)

agent_active_queries = Gauge(
    'agent_active_queries',
    'Number of currently active queries',
    ['agent_id']
)

def track_metrics(agent_id: str):
    """Decorator to track agent metrics"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Increment active queries
            agent_active_queries.labels(agent_id=agent_id).inc()

            # Track duration
            start_time = time.time()

            try:
                result = func(*args, **kwargs)

                # Record success
                agent_queries_total.labels(
                    agent_id=agent_id,
                    status='success'
                ).inc()

                return result

            except Exception as e:
                # Record failure
                agent_queries_total.labels(
                    agent_id=agent_id,
                    status='error'
                ).inc()
                raise

            finally:
                # Record duration
                duration = time.time() - start_time
                agent_query_duration_seconds.labels(
                    agent_id=agent_id
                ).observe(duration)

                # Decrement active queries
                agent_active_queries.labels(agent_id=agent_id).dec()

        return wrapper
    return decorator

# Usage
class MetricsAgent:
    def __init__(self, agent_id: str, options: dict):
        self.agent_id = agent_id
        self.options = options

    @track_metrics("my-agent")
    def query(self, user_input: str):
        """Query with metrics tracking"""
        responses = []

        for message in query(user_input, self.options):
            # Track tool calls
            if message.type == "tool_use":
                agent_tool_calls_total.labels(
                    agent_id=self.agent_id,
                    tool_name=message.tool_name,
                    status='success'
                ).inc()

            # Track tokens
            if hasattr(message, "usage"):
                agent_tokens_total.labels(
                    agent_id=self.agent_id,
                    token_type='input'
                ).inc(message.usage.input_tokens)

                agent_tokens_total.labels(
                    agent_id=self.agent_id,
                    token_type='output'
                ).inc(message.usage.output_tokens)

            responses.append(message)

        return responses

# Start metrics server
start_http_server(8000)
```

**Grafana dashboard queries:**

```promql
# Query rate by agent
rate(agent_queries_total[5m])

# Average query duration
rate(agent_query_duration_seconds_sum[5m]) / rate(agent_query_duration_seconds_count[5m])

# Token consumption rate
rate(agent_tokens_total[5m])

# Tool call success rate
rate(agent_tool_calls_total{status="success"}[5m]) / rate(agent_tool_calls_total[5m])

# Active queries (current load)
agent_active_queries
```

## Error Handling and Resilience

### 1. Retry with Exponential Backoff

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    """Decorator for exponential backoff retry"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = base_delay

            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1

                    if retries >= max_retries:
                        raise

                    # Exponential backoff
                    wait_time = min(delay * (2 ** retries), max_delay)
                    print(f"Retry {retries}/{max_retries} after {wait_time}s due to: {e}")
                    time.sleep(wait_time)

        return wrapper
    return decorator

class ResilientAgent:
    def __init__(self, agent_id: str, options: dict):
        self.agent_id = agent_id
        self.options = options

    @retry_with_backoff(max_retries=3, base_delay=2)
    def query(self, user_input: str):
        """Query with automatic retry"""
        return list(query(user_input, self.options))
```

### 2. Graceful Degradation

```python
class GracefulAgent:
    """Agent with graceful degradation on tool failures"""

    def __init__(self, agent_id: str, options: dict):
        self.agent_id = agent_id
        self.options = options

    def query(self, user_input: str):
        """Query with fallback on tool failures"""
        responses = []
        failed_tools = set()

        for message in query(user_input, self.options):
            # Handle tool failures
            if message.type == "tool_use" and hasattr(message, "error"):
                tool_name = message.tool_name
                failed_tools.add(tool_name)

                # Log failure
                print(f"Tool {tool_name} failed: {message.error}")

                # Remove failed tool from allowed list
                if "allowed_tools" in self.options:
                    self.options["allowed_tools"] = [
                        t for t in self.options["allowed_tools"]
                        if t != tool_name
                    ]

                # Notify user
                responses.append({
                    "type": "warning",
                    "content": f"⚠️ Tool {tool_name} unavailable, continuing without it."
                })

            responses.append(message)

        # Log degraded state
        if failed_tools:
            print(f"Completed with degraded tools: {failed_tools}")

        return responses
```

### 3. Circuit Breaker Pattern

```python
from datetime import datetime, timedelta
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker for agent queries"""

    def __init__(self, failure_threshold=5, timeout_seconds=60):
        self.failure_threshold = failure_threshold
        self.timeout = timedelta(seconds=timeout_seconds)

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""

        # Check if circuit should transition to half-open
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                print("Circuit breaker: Attempting recovery (HALF_OPEN)")
            else:
                raise Exception("Circuit breaker OPEN - too many failures")

        try:
            result = func(*args, **kwargs)

            # Success - reset on closed or transition from half-open
            if self.state == CircuitState.HALF_OPEN:
                print("Circuit breaker: Recovery successful (CLOSED)")

            self.failure_count = 0
            self.state = CircuitState.CLOSED
            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            # Open circuit if threshold exceeded
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                print(f"Circuit breaker OPEN after {self.failure_count} failures")

            raise

class ProtectedAgent:
    """Agent with circuit breaker protection"""

    def __init__(self, agent_id: str, options: dict):
        self.agent_id = agent_id
        self.options = options
        self.circuit_breaker = CircuitBreaker(failure_threshold=3, timeout_seconds=30)

    def query(self, user_input: str):
        """Query with circuit breaker"""
        return self.circuit_breaker.call(
            self._do_query,
            user_input
        )

    def _do_query(self, user_input: str):
        """Internal query implementation"""
        return list(query(user_input, self.options))
```

## Production Best Practices

### 1. Configuration Management

```python
from pydantic import BaseModel, Field
from typing import Optional
import yaml

class MCPServerConfig(BaseModel):
    command: str
    args: list[str] = []
    env: dict[str, str] = {}

class AgentConfig(BaseModel):
    """Type-safe agent configuration"""

    agent_id: str
    model: str = "claude-sonnet-4-5"
    current_working_directory: str
    system_prompt: str
    allowed_tools: list[str] = ["read", "write", "glob", "grep"]
    mcp_servers: dict[str, MCPServerConfig] = {}
    max_tokens: Optional[int] = None
    temperature: float = 1.0

    # Operational settings
    max_retries: int = 3
    timeout_seconds: int = 300
    enable_logging: bool = True
    enable_metrics: bool = True

    @classmethod
    def from_yaml(cls, path: str) -> "AgentConfig":
        """Load configuration from YAML file"""
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def to_agent_options(self) -> dict:
        """Convert to Agent SDK options format"""
        return {
            "model": self.model,
            "current_working_directory": self.current_working_directory,
            "system_prompt": self.system_prompt,
            "allowed_tools": self.allowed_tools,
            "mcp_servers": {
                name: config.dict()
                for name, config in self.mcp_servers.items()
            }
        }

# Example config file: agent_config.yaml
"""
agent_id: telegram-bot-1
model: claude-sonnet-4-5
current_working_directory: /workspace
system_prompt: |
  You are a helpful coding assistant accessible via Telegram.
  Focus on clear, concise responses.
allowed_tools:
  - read
  - write
  - bash
  - glob
mcp_servers:
  sequential_thinking:
    command: uvx
    args:
      - mcp-server-sequential-thinking
max_retries: 3
timeout_seconds: 300
enable_logging: true
enable_metrics: true
"""

# Usage
config = AgentConfig.from_yaml("agent_config.yaml")
agent = ResilientAgent(config.agent_id, config.to_agent_options())
```

### 2. Security Considerations

**API Key Management:**

```python
import os
from cryptography.fernet import Fernet

class SecureConfig:
    """Secure configuration with encrypted secrets"""

    def __init__(self, encryption_key: bytes = None):
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)

    def encrypt_secret(self, secret: str) -> str:
        """Encrypt sensitive value"""
        return self.cipher.encrypt(secret.encode()).decode()

    def decrypt_secret(self, encrypted: str) -> str:
        """Decrypt sensitive value"""
        return self.cipher.decrypt(encrypted.encode()).decode()

    @staticmethod
    def load_api_key() -> str:
        """Load API key securely from environment or secret manager"""
        # Prefer environment variable
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            # Fallback to secret manager (AWS Secrets Manager, etc.)
            api_key = load_from_secret_manager("anthropic-api-key")

        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        return api_key

def load_from_secret_manager(secret_name: str) -> str:
    """Load secret from cloud secret manager"""
    # AWS Secrets Manager example
    import boto3
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']
```

**Permission Isolation:**

```python
class IsolatedAgent:
    """Agent with strict permission boundaries"""

    SAFE_TOOLS = ["read", "glob", "grep"]
    DANGEROUS_TOOLS = ["write", "bash", "edit"]

    def __init__(self, agent_id: str, trust_level: str, options: dict):
        self.agent_id = agent_id
        self.trust_level = trust_level
        self.options = self._apply_security_policy(options, trust_level)

    def _apply_security_policy(self, options: dict, trust_level: str) -> dict:
        """Apply security policy based on trust level"""

        if trust_level == "read_only":
            # Only allow safe, read-only tools
            options["allowed_tools"] = self.SAFE_TOOLS

        elif trust_level == "standard":
            # Allow most tools but restrict dangerous operations
            options["allowed_tools"] = self.SAFE_TOOLS + ["write", "edit"]

        elif trust_level == "elevated":
            # Full access but with audit logging
            options["allowed_tools"] = self.SAFE_TOOLS + self.DANGEROUS_TOOLS
            print(f"⚠️ Agent {self.agent_id} running with ELEVATED permissions")

        # Restrict working directory
        if "current_working_directory" in options:
            cwd = options["current_working_directory"]
            if not self._is_safe_directory(cwd):
                raise ValueError(f"Unsafe working directory: {cwd}")

        return options

    def _is_safe_directory(self, path: str) -> bool:
        """Check if directory is within allowed boundaries"""
        safe_prefixes = ["/workspace", "/home/user/projects", "/tmp"]
        return any(path.startswith(prefix) for prefix in safe_prefixes)
```

### 3. Performance Optimization

**Caching:**

```python
from functools import lru_cache
import hashlib

class CachedAgent:
    """Agent with response caching for repeated queries"""

    def __init__(self, agent_id: str, options: dict):
        self.agent_id = agent_id
        self.options = options
        self.cache = {}

    def query(self, user_input: str, use_cache: bool = True):
        """Query with optional caching"""

        if use_cache:
            cache_key = self._generate_cache_key(user_input)

            if cache_key in self.cache:
                print(f"Cache HIT for query: {user_input[:50]}...")
                return self.cache[cache_key]

        # Execute query
        responses = list(query(user_input, self.options))

        # Cache result
        if use_cache:
            self.cache[cache_key] = responses

        return responses

    def _generate_cache_key(self, user_input: str) -> str:
        """Generate cache key from query and options"""
        content = f"{user_input}:{self.options}"
        return hashlib.sha256(content.encode()).hexdigest()
```

**Batch Processing:**

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class BatchAgent:
    """Agent with batch query processing"""

    def __init__(self, agent_id: str, options: dict, max_workers: int = 5):
        self.agent_id = agent_id
        self.options = options
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def query_batch(self, queries: list[str]) -> list:
        """Process multiple queries in parallel"""

        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                self.executor,
                self._query_single,
                q
            )
            for q in queries
        ]

        return await asyncio.gather(*tasks)

    def _query_single(self, user_input: str):
        """Single query execution"""
        return list(query(user_input, self.options))
```

## Summary: Production Deployment Checklist

### Architecture

- [ ] Choose integration pattern (API wrapper, messaging, knowledge management)
- [ ] Implement OpenAI-compatible endpoints if needed
- [ ] Design configuration management strategy
- [ ] Plan for multi-tenancy if applicable

### Observability

- [ ] Integrate Sentry for distributed tracing
- [ ] Implement structured logging
- [ ] Set up Prometheus metrics
- [ ] Create Grafana dashboards
- [ ] Configure alerting thresholds

### Resilience

- [ ] Implement retry with exponential backoff
- [ ] Add circuit breaker pattern
- [ ] Design graceful degradation strategy
- [ ] Handle partial failures

### Security

- [ ] Secure API key management (environment variables, secret manager)
- [ ] Implement permission isolation by trust level
- [ ] Restrict working directory boundaries
- [ ] Audit dangerous tool usage
- [ ] Encrypt sensitive configuration

### Performance

- [ ] Cache repeated queries
- [ ] Implement batch processing for bulk operations
- [ ] Optimize context loading
- [ ] Monitor token usage and costs

### Operations

- [ ] Document deployment procedures
- [ ] Create runbooks for common issues
- [ ] Set up health checks and readiness probes
- [ ] Plan for zero-downtime updates
- [ ] Establish backup and recovery procedures

## Related Concepts

### Prerequisites

- [[claude_agent_sdk]] - Understanding Agent SDK fundamentals is essential before production deployment

### Related Topics

- [[mcp_overview]] - MCP servers are critical for extending agent capabilities
- [[python_mcp_sdk]] - Building custom MCP servers for production agents
- [[claude_code]] - Understanding Claude Code architecture informs Agent SDK patterns
- [[windows_agents_platform]] - OS-level platform architecture provides comparison for production patterns

### Extends

- [[claude_agent_sdk]] - Production deployment patterns extend basic Agent SDK usage

## References

[1] YouTube video demonstration: Telegram and Obsidian integrations with Claude Agent SDK
[2] <https://docs.sentry.io/platforms/python/integrations/anthropic/> - Sentry Anthropic integration
[3] <https://prometheus.io/docs/introduction/overview/> - Prometheus monitoring
[4] <https://grafana.com/docs/> - Grafana dashboards
[5] <https://docs.anthropic.com/en/api/agent-sdk/observability> - Agent SDK observability guide
