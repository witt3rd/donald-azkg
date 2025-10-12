---
tags: [csharp, mcp, sdk, dotnet, api, reference]
---
# Model Context Protocol C# SDK Documentation

## Overview

The Model Context Protocol (MCP) is an open protocol that standardizes integration between AI models and external tools. It provides a common mechanism to send context (documents, code, prompts) to AI models and receive structured responses, reducing fragmentation in AI/LLM integration scenarios.

### Key Benefits
- Connect any LLM/backend to various applications
- Expose tooling (like code actions) to editors and apps
- Ensure different products can reuse integrations
- Provide structured, context-rich information to AI models

## Prerequisites and Installation

### Requirements
- .NET 8.0 or newer
- For server-hosted scenarios: `Microsoft.Extensions.Hosting` package

### Installation

```shell
# Install core MCP SDK
dotnet add package ModelContextProtocol --prerelease

# For hosted applications
dotnet add package Microsoft.Extensions.Hosting

# For ASP.NET Core integration
dotnet add package ModelContextProtocol.AspNetCore --prerelease
```

## Core Concepts

### Architecture Components

| Component      | Role                                                          |
|---------------|---------------------------------------------------------------|
| MCP Server    | Receives tool/context requests from clients                   |
| MCP Client    | Initiates connections and sends requests to MCP servers       |
| Tools         | Pluggable actions or services registered with the server      |
| Resources     | Data streams or artifacts (documents, APIs, user data)        |
| Prompts       | Instructions or input sent to tools or models via MCP         |

### Transport Options

- **stdio**: Standard input/output for simple local or CLI integration
- **HTTP**: Network-based communication for distributed scenarios
- **Named Pipes**: Inter-process communication (Windows/Unix)

## Server Configuration Examples

### Configuring MCP Server in ASP.NET Core

Demonstrates how to configure and run an MCP server within an ASP.NET Core application with HTTP transport. This setup automatically discovers tools from the assembly and maps the MCP endpoint.

```csharp
// Program.cs
using ModelContextProtocol.Server;
using System.ComponentModel;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddMcpServer()
    .WithHttpTransport()
    .WithToolsFromAssembly();
var app = builder.Build();

app.MapMcp();

app.Run("http://localhost:3001");

[McpServerToolType]
public static class EchoTool
{
    [McpServerTool, Description("Echoes the message back to the client.")]
    public static string Echo(string message) => $"hello {message}";
}
```

---

### Basic Console Application Server

Setting up a basic MCP server using the Host builder pattern with stdio transport. This configuration automatically registers tools from the current assembly and configures logging to stderr.

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using ModelContextProtocol.Server;
using System.ComponentModel;

var builder = Host.CreateApplicationBuilder(args);
builder.Logging.AddConsole(consoleLogOptions =>
{
    // Configure all logs to go to stderr
    consoleLogOptions.LogToStandardErrorThreshold = LogLevel.Trace;
});
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();
await builder.Build().RunAsync();

[McpServerToolType]
public static class EchoTool
{
    [McpServerTool, Description("Echoes the message back to the client.")]
    public static string Echo(string message) => $"hello {message}";
}
```

---

## Client Implementation

### Creating MCP Client and Interacting with Tools

Demonstrates how to create an MCP client, connect to a server, list available tools, and execute tool calls. The client can connect to any MCP server regardless of implementation.

```csharp
var clientTransport = new StdioClientTransport(new StdioClientTransportOptions
{
    Name = "Everything",
    Command = "npx",
    Arguments = ["-y", "@modelcontextprotocol/server-everything"],
});

var client = await McpClientFactory.CreateAsync(clientTransport);

// Print the list of tools available from the server.
foreach (var tool in await client.ListToolsAsync())
{
    Console.WriteLine($"{tool.Name} ({tool.Description})");
}

// Execute a tool (this would normally be driven by LLM tool invocations).
var result = await client.CallToolAsync(
    "echo",
    new Dictionary<string, object?>() { ["message"] = "Hello MCP!" },
    cancellationToken:CancellationToken.None);

// echo always returns one and only one text content object
Console.WriteLine(result.Content.First(c => c.Type == "text").Text);
```

---

### Integrating MCP Tools with AI Chat Client

Shows how to bridge MCP tools with Microsoft.Extensions.AI chat clients, enabling AI models to use tools exposed by MCP servers.

```csharp
// Get available functions.
IList<McpClientTool> tools = await client.ListToolsAsync();

// Call the chat client using the tools.
IChatClient chatClient = ...;
var response = await chatClient.GetResponseAsync(
    "your prompt here",
    new() { Tools = [.. tools] },

```

---

### Manual Server Creation

For scenarios requiring fine-grained control, you can manually create and configure an MCP server instance:

```csharp
await using IMcpServer server = McpServerFactory.Create(new StdioServerTransport("MyServer"), options);
await server.RunAsync();
```

---

## Tools and Dependency Injection

### Tool with Dependency Injection

Tools can receive dependencies via method parameters, including the server instance itself and any registered services. This example demonstrates a tool that uses HttpClient and the server's sampling capabilities:

```csharp
[McpServerTool(Name = "SummarizeContentFromUrl"), Description("Summarizes content downloaded from a specific URI")]
public static async Task<string> SummarizeDownloadedContent(
    IMcpServer thisServer,
    HttpClient httpClient,
    [Description("The url from which to download the content to summarize")] string url,
    CancellationToken cancellationToken)
{
    string content = await httpClient.GetStringAsync(url);

    ChatMessage[] messages =
    [
        new(ChatRole.User, "Briefly summarize the following downloaded content:"),
        new(ChatRole.User, content),
    ];

    ChatOptions options = new()
    {
        MaxOutputTokens = 256,
        Temperature = 0.3f,
    };

    return $"Summary: {await thisServer.AsSamplingChatClient().GetResponseAsync(messages, options, cancellationToken)}";
}
```

---

### Advanced Server Configuration

For complex scenarios, you can configure an MCP server with custom handlers and manually defined tool schemas:

```csharp
using ModelContextProtocol.Protocol.Transport;
using ModelContextProtocol.Protocol.Types;
using ModelContextProtocol.Server;
using System.Text.Json;

McpServerOptions options = new()
{
    ServerInfo = new Implementation() { Name = "MyServer", Version = "1.0.0" },
    Capabilities = new ServerCapabilities()
    {
        Tools = new ToolsCapability()
        {
            ListToolsHandler = (request, cancellationToken) =>
                Task.FromResult(new ListToolsResult()
                {
                    Tools =
                    [
                        new Tool()
                        {
                            Name = "echo",
                            Description = "Echoes the input back to the client.",
                            InputSchema = JsonSerializer.Deserialize<JsonElement>("""
                                {
                                    "type": "object",
                                    "properties": {
                                      "message": {
                                        "type": "string",
                                        "description": "The input to echo back"
                                      }
                                    },
                                    "required": ["message"]
                                }
                                """),
                        }
                    ]
                }),

            CallToolHandler = (request, cancellationToken) =>
            {
                if (request.Params?.Name == "echo")
                {
                    if (request.Params.Arguments?.TryGetValue("message", out var message) is not true)
                    {
                        throw new McpException("Missing required argument 'message'");
                    }

```

---

## Prompts and Resources

### Defining Custom Prompts

Prompts provide reusable templates for generating AI model inputs. Define them using attributes on static methods:

```csharp
[McpServerPromptType]
public static class MyPrompts
{
    [McpServerPrompt, Description("Creates a prompt to summarize the provided message.")]
    public static ChatMessage Summarize([Description("The content to summarize")] string content) =>
        new(ChatRole.User, $"Please summarize this content into a single sentence: {content}");
}
```

---

### Handling Tool Calls

When implementing custom tool handlers, return appropriate responses or throw exceptions for unknown tools:

```csharp
return Task.FromResult(new CallToolResponse()
{
    Content = [new Content() { Text = $"Echo: {message}", Type = "text" }]
});
}

throw new McpException($"Unknown tool: '{request.Params?.Name}'");
```

---

## Error Handling and Best Practices

### Error Handling

- **McpException**: Thrown on protocol errors (malformed requests, unsupported tools)
- **McpErrorCode**: Standardized error codes for robust error handling

### Best Practices

1. **Validate Input**: Always validate incoming context and resource requests
2. **Graceful Degradation**: Handle edge cases and protocol negotiation gracefully
3. **Logging**: Log requests and errors for diagnostics
4. **Discovery**: Clearly define capabilities and expose via MCP discovery endpoints
5. **Security**: Never expose sensitive data through tools or resources
6. **Async Operations**: Use async/await patterns for all I/O operations
7. **Cancellation**: Respect cancellation tokens in all operations

## Advanced Scenarios

### Streaming Responses

For real-time updates or progressive generation:

```csharp
public class StreamingTool : IMcpTool
{
    public async Task ExecuteAsync(
        McpToolContext context, 
        IProgress<McpToolResult> progress, 
        CancellationToken ct)
    {
        for (int i = 0; i < 10; i++)
        {
            progress.Report(new McpToolResult 
            { 
                Content = $"Progress: {i * 10}%" 
            });
            await Task.Delay(1000, ct);
        }
    }
}
```

### Custom Resources

Implement complex resources like file systems or databases:

```csharp
[McpResource("filesystem")]
public class FileSystemResource : IMcpResource
{
    public async Task<ResourceContent> GetAsync(
        string path, 
        CancellationToken ct)
    {
        var content = await File.ReadAllTextAsync(path, ct);
        return new ResourceContent 
        { 
            Data = content, 
            MimeType = "text/plain" 
        };
    }
}
```

### Multi-Tool Servers

Register multiple tools with different capabilities:

```csharp
builder.Services
    .AddMcpServer()
    .WithToolsFromAssembly()
    .WithTool<CodeFormatterTool>()
    .WithTool<DatabaseQueryTool>()
    .WithTool<FileSearchTool>()
    .WithResource<FileSystemResource>();
```

## Transport Configuration

### stdio Transport

```csharp
// Server
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport();

// Client
var transport = new StdioClientTransport(new StdioClientTransportOptions
{
    Command = "dotnet",
    Arguments = ["run", "--project", "MyMcpServer.csproj"]
});
```

### HTTP Transport

```csharp
// Server (ASP.NET Core)
app.MapMcp("/mcp");

// Client
var transport = new HttpClientTransport(
    new Uri("http://localhost:5000/mcp"));
```

## Status and Updates

**Current Status**: The MCP C# SDK is in preview. APIs may evolve with breaking changes as protocol standards expand.

**Recent Updates**:
- Integration with Microsoft.Extensions.AI
- Improved resource management
- Enhanced IDE integration support
- Streaming response capabilities

## References

- [Official Documentation](https://learn.microsoft.com/en-us/dotnet/ai/get-started-mcp)
- [API Reference](https://modelcontextprotocol.github.io/csharp-sdk/api/ModelContextProtocol.html)
- [GitHub Repository](https://github.com/modelcontextprotocol/csharp-sdk)
- [MCP Specification](https://modelcontextprotocol.io/specification)

## Related Concepts

### Prerequisites
- [[mcp_implementation]] - Need general implementation knowledge before C#-specific SDK
- [[dotnet]] - .NET foundation required for C# MCP SDK

### Related Topics
- [[mcp_sdk]] - Alternative language SDK for MCP
- [[dotnet]] - .NET is the foundation for C# MCP SDK

### Extends
- [[mcp_implementation]] - C#-specific implementation of MCP SDK

### Alternatives
- [[mcp_sdk]] - Use Python instead of C# for MCP development