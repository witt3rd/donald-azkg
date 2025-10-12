---
tags: [mcp, protocol, tools, function-execution, api]
---
# MCP Tools

Tools enable AI models to perform actions and execute functions in external systems, providing controlled access to operations with side effects.

## What are Tools?

**Tools** constitute the action-oriented component of MCP, enabling AI models to perform specific functions and operations within external systems[2][13]. Unlike resources (read-only), tools are designed for **model-controlled execution** and can have side effects, modify system state, or trigger complex workflows[2].

### Core Characteristics

**Action-Oriented**
- Perform operations in external systems
- Execute functions based on AI decisions
- Trigger workflows and automations
- Modify state and data[2]

**Side Effects Allowed**
- Can modify external systems
- May trigger irreversible actions
- State changes expected and intended
- Requires careful security controls[2]

**Model-Controlled**
- AI decides when to invoke tools
- Parameters determined by model reasoning
- Execution based on natural language intent
- Tool selection through capability matching

## Tool Definition

Tools must include comprehensive metadata to help AI models understand proper usage:

### Tool Schema

```json
{
  "name": "send_email",
  "description": "Sends an email to specified recipients",
  "inputSchema": {
    "type": "object",
    "properties": {
      "to": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Email addresses of recipients"
      },
      "subject": {
        "type": "string",
        "description": "Email subject line"
      },
      "body": {
        "type": "string",
        "description": "Email body content in plain text"
      },
      "attachments": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Optional file paths for attachments"
      }
    },
    "required": ["to", "subject", "body"]
  }
}
```

### Required Metadata

**Name**
- Unique identifier for the tool
- Should be descriptive and verb-oriented
- Examples: `create_task`, `search_database`, `send_notification`

**Description**
- Clear explanation of what the tool does
- Include expected outcomes
- Mention side effects explicitly
- Describe when to use vs not use

**Input Schema**
- JSON Schema defining parameters
- Type information for each parameter
- Required vs optional fields
- Validation constraints
- Default values where appropriate
- Descriptions for each parameter[3]

### Description Best Practices

**Be specific and clear:**
```
✓ "Creates a new task in the project management system with title, description,
   assignee, and due date. Returns the created task ID."

✗ "Manages tasks in the system."
```

**Mention side effects:**
```
✓ "Sends an email immediately to all specified recipients. This action cannot
   be undone. Recipients will see the sender as system@company.com."

✗ "Sends email."
```

**Include usage guidance:**
```
✓ "Searches the customer database by email or phone number. Use this when the
   user asks about a specific customer. For general customer queries, use
   list_customers instead."

✗ "Searches customers."
```

## Tool Discovery

Like resources, tools support dynamic discovery:

### Discovery Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

### Discovery Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "create_task",
        "description": "Creates a new task in the project management system",
        "inputSchema": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string",
              "description": "Task title"
            },
            "assignee": {
              "type": "string",
              "description": "Username of person to assign task"
            }
          },
          "required": ["title"]
        }
      },
      {
        "name": "search_customers",
        "description": "Searches customer database by email or phone",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "Email address or phone number to search"
            }
          },
          "required": ["query"]
        }
      }
    ]
  }
}
```

## Tool Execution

### Execution Request

AI models invoke tools through the `tools/call` method:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "create_task",
    "arguments": {
      "title": "Review Q3 sales report",
      "assignee": "john.doe",
      "due_date": "2025-04-01"
    }
  }
}
```

### Execution Response

Tool execution returns results or errors:

**Success:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Task created successfully with ID: TASK-12345"
      }
    ]
  }
}
```

**Error:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32602,
    "message": "Invalid assignee",
    "data": {
      "parameter": "assignee",
      "value": "john.doe",
      "reason": "User not found in system"
    }
  }
}
```

## Tool Design Principles

### Goal-Oriented Design

Design tools for specific **user goals**, not as wrappers around entire APIs[3]:

**Good - Goal-oriented:**
```
- create_expense_report
- submit_timesheet
- approve_leave_request
```

**Less effective - API wrappers:**
```
- post_api_endpoint
- get_data
- update_record
```

The protocol encourages developers to design tools that are optimized for specific user goals and reliable outcomes, rather than creating wrapper interfaces around entire API schemas[3]. This approach improves model performance by providing focused, purpose-built tools.

### Reliability and Robustness

**Handle edge cases:**
- Validate inputs before execution
- Provide clear error messages
- Implement timeouts for long operations
- Support idempotency where possible

**Example: Idempotent tool design**
```json
{
  "name": "create_task",
  "description": "Creates a task. If a task with the same title and assignee already exists, returns the existing task ID instead of creating a duplicate.",
  "inputSchema": {
    "properties": {
      "idempotency_key": {
        "type": "string",
        "description": "Optional unique key to prevent duplicate task creation"
      }
    }
  }
}
```

### Parameter Design

**Keep parameters focused:**
- Include only essential parameters
- Use sensible defaults
- Group related parameters logically
- Avoid overly complex nested structures

**Example: Well-designed parameters**
```json
{
  "name": "schedule_meeting",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": { "type": "string" },
      "duration_minutes": {
        "type": "integer",
        "default": 30,
        "description": "Meeting duration in minutes (default: 30)"
      },
      "attendees": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Email addresses of attendees"
      },
      "start_time": {
        "type": "string",
        "format": "date-time",
        "description": "Meeting start time in ISO 8601 format"
      }
    },
    "required": ["title", "start_time", "attendees"]
  }
}
```

### Response Design

**Provide actionable results:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Task TASK-12345 created and assigned to John Doe. Due date: April 1, 2025. View at: https://tasks.example.com/TASK-12345"
    }
  ]
}
```

**Include context and next steps:**
- Confirmation of action taken
- Relevant identifiers or links
- Status information
- Suggestions for follow-up actions

## Use Cases and Examples

### Task Management

**Tools:**
- `create_task` - Create new tasks
- `update_task_status` - Change task status
- `assign_task` - Assign tasks to team members
- `add_task_comment` - Add comments to tasks

**Use case:** AI assistant helping manage project workflow based on natural language requests.

### Communication

**Tools:**
- `send_email` - Send emails
- `post_slack_message` - Post to Slack channels
- `schedule_meeting` - Schedule calendar events
- `send_sms` - Send text messages

**Use case:** AI handling communications on behalf of users with appropriate consent and control.

### Data Manipulation

**Tools:**
- `create_database_record` - Insert new records
- `update_database_record` - Modify existing records
- `delete_database_record` - Remove records
- `execute_sql_query` - Run parameterized queries

**Use case:** AI-powered database interactions through natural language interfaces.

### External API Integration

**Tools:**
- `github_create_issue` - Create GitHub issues
- `github_add_comment` - Comment on issues/PRs
- `stripe_create_invoice` - Generate invoices
- `twilio_send_sms` - Send SMS via Twilio

**Use case:** AI integrating with third-party services to perform automated actions.

## Security Considerations

### User Consent

**Always require explicit user consent before tool execution:**
- Display tool name and parameters to user
- Explain what action will be taken
- Allow user to approve or reject
- Enable undo/rollback when possible[2]

### Scope Limitation

**Design tools with narrow, specific purposes:**
- Avoid overly broad permissions
- Implement least privilege principle
- Separate read and write operations
- Limit blast radius of errors

### Audit Logging

**Log all tool executions:**
- Tool name and parameters
- User who authorized execution
- Timestamp and result
- Success/failure status

### Validation and Sanitization

**Validate all inputs:**
- Type checking
- Range validation
- Format verification
- SQL injection prevention
- Command injection prevention

## Error Handling

### Error Response Structure

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32602,
    "message": "Validation failed",
    "data": {
      "parameter": "email",
      "value": "invalid-email",
      "reason": "Must be a valid email address",
      "suggestion": "Use format: user@domain.com"
    }
  }
}
```

### Common Error Codes

- `-32602` - Invalid params
- `-32603` - Internal error
- `-32001` - Server error (custom)
- `-32002` - Permission denied (custom)
- `-32003` - Resource not found (custom)

### Error Messages

**Provide actionable error information:**
- What went wrong
- Why it went wrong
- How to fix it
- Alternative approaches if applicable

## Testing Tools

### Test Coverage

Verify tool implementations:
1. **Happy path testing** - Normal successful execution
2. **Parameter validation** - Invalid inputs handled correctly
3. **Error conditions** - Network failures, timeouts, etc.
4. **Permission checks** - Unauthorized access rejected
5. **Idempotency** - Duplicate requests handled correctly

### Integration Testing

Test in realistic scenarios:
- End-to-end workflows
- AI model invocation patterns
- Error recovery
- User consent flows

## Implementation Guidance

### Server-Side

Key responsibilities:
1. Register tools during initialization
2. Validate parameters before execution
3. Execute operations safely
4. Return meaningful results or errors
5. Log all executions for audit

### Client-Side

Key responsibilities:
1. Discover available tools
2. Present tools to AI model
3. Obtain user consent before execution
4. Display execution results to user
5. Handle errors gracefully

## Related Concepts

### Prerequisites
- [[mcp_overview]] - Need to understand MCP fundamentals first
- [[mcp_architecture]] - Need to understand how tools operate within MCP architecture

### Related Topics
- [[mcp_resources]] - Resources provide read capabilities while tools perform actions
- [[mcp_prompts]] - Prompts orchestrate tool usage in workflows
- [[agent_mcp_apis]] - Agents use MCP tools for task execution
- [[mcp_security]] - Critical security for tool execution and side effects
- [[mcp_implementation]] - Implementation of tool servers

### Extends
- [[mcp_overview]] - Implements the tools capability of MCP

### Extended By
- [[filesystem]] - Filesystem implements MCP tools