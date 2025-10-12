---
tags: [mcp, protocol, prompts, templates, workflows]
---

# MCP Prompts

Prompts provide reusable templates and workflows that codify best practices for combining resources and tools to accomplish specific tasks.

## What are Prompts?

**Prompts** represent pre-defined templates and workflows that optimize the utilization of tools and resources for specific use cases[2][13]. This component enables developers to codify best practices and domain expertise into reusable templates that users can invoke to achieve common objectives[2].

Prompts serve as a bridge between user intent and technical implementation, providing structured approaches to complex multi-step workflows[2].

### Core Purpose

**Codify Best Practices**
- Capture domain expertise in templates
- Standardize approaches to common tasks
- Reduce learning curve for new users
- Ensure consistent outcomes

**Enable Workflows**
- Combine multiple tools and resources
- Define multi-step processes
- Coordinate complex operations
- Provide guided experiences

**Parameterization Support**
- Customize templates for specific contexts
- Maintain underlying structure
- Enable user-specific variations
- Balance flexibility with guidance[2]

## Prompt Structure

### Basic Prompt Definition

```json
{
  "name": "analyze_sales_data",
  "description": "Analyzes sales data for a specified time period and generates a summary report",
  "arguments": [
    {
      "name": "time_period",
      "description": "Time period to analyze (e.g., 'last_quarter', 'last_year')",
      "required": true
    },
    {
      "name": "region",
      "description": "Geographic region to focus on (optional)",
      "required": false
    }
  ]
}
```

### Prompt Components

**Name**
- Unique identifier for the prompt
- Should describe the goal/task
- Use verb phrases: `analyze_`, `generate_`, `review_`

**Description**
- Explains what the prompt does
- Describes expected outcomes
- Lists prerequisites or requirements
- Indicates when to use this prompt

**Arguments**
- Parameterize the prompt for different contexts
- Include required and optional parameters
- Provide clear parameter descriptions
- Specify valid values or formats

**Template Content**
- The actual prompt text with placeholders
- Instructions for the AI model
- Context about tools and resources available
- Expected output format

## Prompt Discovery

Prompts support dynamic discovery like tools and resources:

### Discovery Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "prompts/list",
  "params": {}
}
```

### Discovery Response

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "prompts": [
      {
        "name": "analyze_sales_data",
        "description": "Analyzes sales data for a specified time period and generates a summary report",
        "arguments": [
          {
            "name": "time_period",
            "description": "Time period to analyze",
            "required": true
          },
          {
            "name": "region",
            "description": "Geographic region",
            "required": false
          }
        ]
      },
      {
        "name": "debug_application_error",
        "description": "Investigates and diagnoses application errors using logs and system state",
        "arguments": [
          {
            "name": "error_id",
            "description": "Error identifier or stack trace",
            "required": true
          }
        ]
      }
    ]
  }
}
```

## Prompt Invocation

### Getting a Prompt

Request a prompt with specific arguments:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "prompts/get",
  "params": {
    "name": "analyze_sales_data",
    "arguments": {
      "time_period": "Q3_2025",
      "region": "North America"
    }
  }
}
```

### Prompt Response

Server returns the rendered prompt:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Analyze sales data for Q3 2025 in the North America region. Use the following workflow:\n\n1. Retrieve sales data using the `db://sales/by-period` resource with time_period='Q3_2025' and region='North America'\n2. Calculate key metrics: total revenue, number of transactions, average transaction value\n3. Compare to previous quarter (Q2_2025) for the same region\n4. Identify top 5 products by revenue\n5. Generate a summary report with insights and recommendations\n\nFormat the final report with clear sections for metrics, comparisons, and recommendations."
        }
      }
    ]
  }
}
```

## Workflow Design Patterns

### Sequential Workflow

Steps executed in order:

```text
Prompt: Code Review Workflow
1. Read the code file using resource
2. Check code style using tool
3. Run static analysis using tool
4. Generate review report combining findings
```

### Conditional Workflow

Steps depend on previous results:

```text
Prompt: Customer Support Workflow
1. Search customer database using tool
2. IF customer found:
   - Retrieve customer history using resource
   - Check for open tickets using tool
3. IF customer not found:
   - Suggest creating new customer record
4. Generate support response based on context
```

### Parallel Workflow

Independent steps executed concurrently:

```text
Prompt: System Health Check
1. In parallel:
   - Check database status using tool
   - Check API endpoint health using tool
   - Check disk space using resource
   - Check memory usage using resource
2. Aggregate results
3. Generate health report with any issues flagged
```

### Iterative Workflow

Steps repeated with refinement:

```text
Prompt: Document Generation
1. Generate initial draft using tools
2. Review draft for completeness
3. IF incomplete:
   - Identify missing sections
   - Generate additional content
   - GOTO step 2
4. Format final document
5. Return completed document
```

## Use Cases and Examples

### Code Review Prompt

**Purpose:** Standardize code review process

```json
{
  "name": "review_pull_request",
  "description": "Performs comprehensive code review of a pull request",
  "arguments": [
    {
      "name": "pr_number",
      "description": "Pull request number to review",
      "required": true
    },
    {
      "name": "focus_areas",
      "description": "Specific areas to focus on (e.g., 'security', 'performance')",
      "required": false
    }
  ]
}
```

**Workflow:**
1. Retrieve PR details and files changed
2. Review code for style consistency
3. Check for security vulnerabilities
4. Assess test coverage
5. Generate structured review with findings

### Data Analysis Prompt

**Purpose:** Guide consistent data analysis approach

```json
{
  "name": "analyze_user_behavior",
  "description": "Analyzes user behavior patterns from activity logs",
  "arguments": [
    {
      "name": "user_segment",
      "description": "User segment to analyze (e.g., 'free_users', 'premium_users')",
      "required": true
    },
    {
      "name": "date_range",
      "description": "Date range for analysis in format 'YYYY-MM-DD to YYYY-MM-DD'",
      "required": true
    }
  ]
}
```

**Workflow:**
1. Query user activity data for segment and date range
2. Calculate engagement metrics
3. Identify behavior patterns and trends
4. Compare to other segments
5. Generate insights and recommendations

### Troubleshooting Prompt

**Purpose:** Systematic approach to debugging

```json
{
  "name": "diagnose_application_issue",
  "description": "Systematically diagnoses application issues using logs and metrics",
  "arguments": [
    {
      "name": "issue_description",
      "description": "Description of the issue or error message",
      "required": true
    },
    {
      "name": "affected_users",
      "description": "Number of users affected (e.g., 'all', 'single_user')",
      "required": false
    }
  ]
}
```

**Workflow:**
1. Search application logs for related errors
2. Check system metrics (CPU, memory, network)
3. Review recent deployments or changes
4. Check external service status
5. Generate diagnostic report with likely root cause

### Content Generation Prompt

**Purpose:** Consistent content creation workflow

```json
{
  "name": "generate_blog_post",
  "description": "Generates a blog post on a specified topic with research and citations",
  "arguments": [
    {
      "name": "topic",
      "description": "Blog post topic or title",
      "required": true
    },
    {
      "name": "target_audience",
      "description": "Target audience (e.g., 'technical', 'business', 'general')",
      "required": true
    },
    {
      "name": "length",
      "description": "Target length (e.g., 'short', 'medium', 'long')",
      "required": false
    }
  ]
}
```

**Workflow:**
1. Research topic using web search or knowledge base resources
2. Outline key points and structure
3. Generate draft content for each section
4. Add relevant examples and citations
5. Review and refine for target audience
6. Format for publication

## Best Practices

### Prompt Design

**Clear Objectives**
- Define specific, measurable outcomes
- State prerequisites and assumptions
- Explain when to use this prompt vs alternatives

**Comprehensive Instructions**
- Step-by-step guidance for the AI
- Specify which tools and resources to use
- Include example outputs or formats
- Handle edge cases and errors

**Appropriate Parameterization**
- Balance flexibility with guidance
- Use sensible defaults
- Validate parameter values
- Provide parameter usage examples

### Workflow Design

**Logical Flow**
- Steps should follow natural sequence
- Dependencies clearly indicated
- Error handling at each step
- Clear success/failure criteria

**Resource Efficiency**
- Minimize redundant tool calls
- Cache intermediate results when appropriate
- Use parallel execution where possible
- Consider rate limits and quotas

**User Experience**
- Progress indication for long workflows
- Meaningful intermediate feedback
- Clear final outputs
- Actionable results

### Documentation

**For Users**
- Clear description of what prompt does
- Expected inputs and outputs
- Usage examples
- Prerequisites and requirements

**For Maintainers**
- Rationale for workflow design
- Assumptions and limitations
- Maintenance notes
- Version history

## Template Patterns

### Research and Report Pattern

```text
1. Define research questions
2. Gather data from multiple sources (resources)
3. Analyze and synthesize findings
4. Generate structured report
5. Include citations and references
```

### Action and Verify Pattern

```text
1. Perform action using tool
2. Verify action completed successfully
3. IF verification fails:
   - Retry action
   - OR report error
4. Log action and result
5. Return confirmation
```

### Request and Process Pattern

```text
1. Request data from resource
2. Transform or filter data as needed
3. Apply business logic
4. Format results
5. Return processed data
```

### Approval Workflow Pattern

```text
1. Gather information for decision
2. Present options to user
3. Wait for user approval
4. IF approved:
   - Execute approved action using tool
5. IF rejected:
   - Log rejection and reason
6. Return outcome
```

## Security and Governance

### Prompt Safety

**Validate Parameters**
- Type checking
- Range validation
- Injection prevention
- Sanitize user inputs

**Control Tool Access**
- Prompts should not bypass user consent for tools
- Clearly indicate when tools will be invoked
- Allow user to review before execution
- Support dry-run mode where appropriate

### Audit and Compliance

**Track Prompt Usage**
- Log which prompts are invoked
- Record parameters provided
- Track success/failure rates
- Monitor for misuse

**Version Control**
- Version prompt templates
- Track changes over time
- Allow rollback if needed
- Document changes in changelog

## Implementation Guidance

### Server-Side

Key responsibilities:
1. Register prompts during initialization
2. Store prompt templates and metadata
3. Handle parameter substitution
4. Validate parameters before rendering
5. Return rendered prompts with instructions

### Client-Side

Key responsibilities:
1. Discover available prompts
2. Present prompts to users
3. Collect parameter values
4. Request rendered prompt
5. Execute prompt workflow
6. Display results to user

### Testing Prompts

Verify prompt implementations:
1. **Parameter validation** - Invalid inputs handled
2. **Rendering** - Template substitution works correctly
3. **Workflow execution** - Steps complete as expected
4. **Error handling** - Failures handled gracefully
5. **User experience** - Clear feedback and results

## Related Concepts

### Prerequisites
- [[mcp_overview]] - Need to understand MCP fundamentals first
- [[mcp_architecture]] - Need to understand how prompts are delivered through architecture

### Related Topics
- [[mcp_resources]] - Prompts coordinate access to resources
- [[mcp_tools]] - Prompts orchestrate tool execution in workflows
- [[mcp_implementation]] - Implementation of prompt servers
- [[json_prompting]] - MCP prompts use structured formats similar to JSON prompting

### Extends
- [[mcp_overview]] - Implements the prompts capability of MCP