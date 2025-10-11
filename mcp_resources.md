---
tags: [mcp, protocol, resources, data-access, api]
---

# MCP Resources

Resources provide AI models with structured, read-only access to external data sources through a safe, discoverable interface.

## What are Resources?

**Resources** represent the foundational data access component of MCP, providing AI models with structured access to external information sources without performing computational operations or causing side effects[2][13]. Resources function similarly to GET endpoints in REST APIs, offering read-only access to various data formats while ensuring safe, predictable behavior[2].

### Core Characteristics

**Read-Only Access**
- Resources cannot modify external systems
- No side effects from resource reads
- Safe to access repeatedly
- Predictable, deterministic behavior[2]

**Multiple Data Formats**
- Plain text content
- Structured JSON objects
- Binary data (images, files)
- Streaming data support[2]

**Safe by Design**
- Cannot trigger unintended actions
- No state changes in external systems
- Auditable access patterns
- Transparent data access[2]

## Resource Discovery

The resource system supports **dynamic discovery**, allowing clients to enumerate available resources at runtime and access metadata about each resource[2].

### Discovery Process

1. **List Available Resources**
   - Client queries server for resource catalog
   - Server returns list of available resources
   - Each resource includes metadata and description

2. **Resource Metadata**
   - **Resource URI** - Unique identifier for the resource
   - **Content type** - MIME type of resource data
   - **Description** - Human-readable explanation
   - **Schema information** - Structure of resource data (for structured content)

3. **Runtime Enumeration**
   - No compile-time knowledge required
   - Dynamic resource lists
   - Supports changing resource availability
   - Enables adaptive AI behavior[2]

### Discovery Example

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list",
  "params": {}
}
```

Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resources": [
      {
        "uri": "file:///path/to/document.txt",
        "name": "Project Documentation",
        "description": "Main project documentation file",
        "mimeType": "text/plain"
      },
      {
        "uri": "db://customers/recent",
        "name": "Recent Customers",
        "description": "List of customers from last 30 days",
        "mimeType": "application/json"
      }
    ]
  }
}
```

## Resource Access Patterns

### Reading Resources

Resources are accessed via the `resources/read` method:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "resources/read",
  "params": {
    "uri": "file:///path/to/document.txt"
  }
}
```

Response:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "contents": [
      {
        "uri": "file:///path/to/document.txt",
        "mimeType": "text/plain",
        "text": "Resource content here..."
      }
    ]
  }
}
```

### Content Types

**Text Resources**
- Plain text files
- Markdown documents
- Source code
- Configuration files

**JSON Resources**
- Structured data objects
- API response data
- Database query results
- Configuration data

**Binary Resources**
- Images
- PDF documents
- Audio/video files
- Archive files

## Use Cases and Examples

### File System Access

**Use case:** Provide AI access to project files, documentation, or configuration files.

**Example implementations:**
- Local file system browser
- Project documentation access
- Configuration file reader
- Log file access

**Benefits:**
- AI can reference current file contents
- Stay synchronized with codebase
- Access documentation during conversations
- Read configuration for context

### Database Query Results

**Use case:** Expose database query results as resources for AI analysis.

**Example implementations:**
- Customer data access
- Sales report data
- Analytics results
- Audit logs

**Benefits:**
- AI can analyze current data
- Real-time insights
- Data-driven responses
- Context-aware recommendations

### API Response Data

**Use case:** Make external API data available to AI systems.

**Example implementations:**
- Weather data access
- Stock market information
- Social media feeds
- News aggregation

**Benefits:**
- Fresh external data
- Third-party service integration
- Real-time information access
- Broad knowledge base

### Knowledge Base Integration

**Use case:** Connect AI to organizational knowledge repositories.

**Example implementations:**
- Company wikis
- Document management systems
- Help desk knowledge bases
- Internal documentation

**Benefits:**
- Organization-specific context
- Accurate company information
- Reduced hallucination
- Consistent responses

## Resource Design Best Practices

### Naming and URIs

**Use descriptive URIs:**
```
✓ file:///project/docs/api-reference.md
✓ db://customers/by-region/north-america
✓ api://weather/current-conditions/seattle

✗ file:///doc1.txt
✗ db://table1
✗ api://data
```

**Include context in names:**
- Resource purpose should be clear
- Include relevant qualifiers (date ranges, filters)
- Use hierarchical structure when appropriate

### Metadata Quality

**Provide comprehensive descriptions:**
```json
{
  "uri": "db://sales/monthly-report",
  "name": "Monthly Sales Report",
  "description": "Aggregated sales data for the current month, updated daily at midnight UTC",
  "mimeType": "application/json"
}
```

**Include relevant metadata:**
- Last updated timestamp
- Data freshness indicators
- Source system information
- Access restrictions or limitations

### Performance Considerations

**Scope resources appropriately:**
- Avoid exposing entire large datasets as single resources
- Implement pagination for large data sets
- Use filters and parameters to limit data
- Consider caching for frequently accessed resources

**Example: Parameterized Resources**
```
db://sales/by-month?month=2025-03
db://customers/by-region?region=north-america&limit=100
```

### Error Handling

**Provide meaningful error messages:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32602,
    "message": "Resource not found",
    "data": {
      "uri": "file:///missing-file.txt",
      "reason": "File does not exist at specified path"
    }
  }
}
```

**Handle common scenarios:**
- Missing resources
- Permission denied
- Temporary unavailability
- Malformed URIs

## Security and Privacy

### Access Control

Resources should implement appropriate access controls:
- **User-based permissions** - Only expose resources user can access
- **Server-scoped access** - Limit server to specific resource domains
- **Audit logging** - Track resource access patterns
- **Consent requirements** - User approval before data access[2]

### Data Privacy

Protect sensitive information:
- **Filter sensitive data** - Remove PII when not needed
- **Redaction support** - Allow partial data exposure
- **Explicit consent** - Always obtain permission before access
- **Transparent disclosure** - Clear about what data is accessed[2]

### Rate Limiting

Prevent abuse and overuse:
- Implement request limits
- Throttle expensive operations
- Cache frequently accessed resources
- Monitor access patterns

## Resource Templates

Resources can be **templated** to support parameterization:

```json
{
  "uri": "db://customers/{region}",
  "name": "Customers by Region",
  "description": "Customer list filtered by geographic region",
  "parameters": {
    "region": {
      "type": "string",
      "description": "Geographic region (e.g., 'north-america', 'europe', 'asia')",
      "required": true
    }
  }
}
```

This enables:
- Dynamic resource access patterns
- User-specific data filtering
- Flexible query capabilities
- Reduced resource proliferation

## Implementation Guidance

### Server-Side Implementation

Key responsibilities:
1. **Register resources** during initialization
2. **Handle discovery requests** with complete metadata
3. **Implement read operations** efficiently
4. **Manage errors gracefully**
5. **Enforce access controls**

### Client-Side Implementation

Key responsibilities:
1. **Discover available resources** at connection time
2. **Cache resource metadata** to avoid repeated discovery
3. **Request resources** as needed for AI context
4. **Handle errors and unavailability**
5. **Respect rate limits**

### Testing Resources

Verify resource implementations:
- Test discovery endpoint
- Validate metadata completeness
- Check error handling
- Verify access controls
- Test performance with realistic data sizes

## Related Concepts

- [[mcp_overview]] - High-level introduction to MCP (prerequisite)
- [[mcp_architecture]] - How resources operate within MCP architecture
- [[mcp_tools]] - Comparison with tools (write operations vs read-only)
- [[mcp_prompts]] - How prompts can utilize resources
- [[mcp_security]] - Security considerations for resource access
- [[mcp_implementation]] - Practical implementation of resource servers

## References

[1] https://modelcontextprotocol.io/introduction
[2] https://modelcontextprotocol.io/specification/2025-03-26
[7] https://modelcontextprotocol.io/examples
[13] https://www.philschmid.de/mcp-introduction
