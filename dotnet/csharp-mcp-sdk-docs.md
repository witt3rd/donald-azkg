# Model Context Protocol C# SDK Documentation

## Configuring MCP Server in ASP.NET Core
Demonstrates how to configure and run an MCP server within an ASP.NET Core application. It shows adding the MCP server service, enabling HTTP transport, discovering tools from the assembly, mapping the MCP endpoint, and defining a simple EchoTool with an Echo method.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol.AspNetCore/README.md#_snippet_1
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

## Basic MCP Server Setup and Echo Tool (C#)
Demonstrates setting up a basic MCP server using the Host builder pattern and registering tools from the current assembly using `WithToolsFromAssembly()`. Includes a simple 'EchoTool' class with an 'Echo' method decorated with `McpServerTool` and `Description` attributes.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_4
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

## Create MCP Client and Interact with Tools (C#)
Demonstrates how to create an MCP client using McpClientFactory.CreateAsync, connect to a server via StdioClientTransport, list available tools, and call a specific tool ('echo') with parameters.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_1
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

## Integrate MCP Tools with AI Chat Client (C#)
Shows how to retrieve available MCP tools using client.ListToolsAsync() and pass them to an IChatClient instance to enable the chat client to use these tools.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_2
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

## Creating and Running MCP Server in C#
This snippet shows how to create and start an MCP server instance in C#. It uses `McpServerFactory` to create the server with a standard I/O transport and then runs it asynchronously.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_9
```csharp
await using IMcpServer server = McpServerFactory.Create(new StdioServerTransport("MyServer"), options);
await server.RunAsync();
```

---

## Tool Demonstrating Server and DI Injection (C#)
Illustrates how a tool method can receive the `IMcpServer` instance and other dependencies (like `HttpClient`) via method parameters using dependency injection. The example tool downloads content from a URL and uses the server's sampling chat client to summarize it.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_5
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

## Advanced MCP Server Configuration (C#)
Provides an example of configuring an MCP server with fine-grained control using `McpServerOptions`. Demonstrates setting server information, capabilities, and custom handlers for listing and calling tools, including defining tool schemas manually.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_7
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

## Define a Custom Prompt Type (C#)
Shows how to define a custom prompt type using the `McpServerPromptType` attribute on a class and `McpServerPrompt` on a static method within that class. The method generates a `ChatMessage` based on input parameters, which can be used by clients.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_6
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

## Handling MCP Tool Call in C#
This snippet demonstrates how to handle a tool call request within an MCP server implementation in C#. It shows returning a successful response for a known tool ('Echo') and throwing an exception for an unknown tool.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_8
```csharp
return Task.FromResult(new CallToolResponse()
{
    Content = [new Content() { Text = $"Echo: {message}", Type = "text" }]
});
}

throw new McpException($"Unknown tool: '{request.Params?.Name}'");
```

---

## Install MCP C# SDK NuGet Package
Installs the ModelContextProtocol NuGet package into a .NET project using the dotnet CLI. The --prerelease flag is used to include preview versions.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_0
```shell
dotnet add package ModelContextProtocol --prerelease
```

---

## Installing ModelContextProtocol.AspNetCore NuGet Package
Commands to create a new ASP.NET Core web project and add the ModelContextProtocol.AspNetCore NuGet package using the .NET CLI. This is the first step to integrate the SDK into a project.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol.AspNetCore/README.md#_snippet_0
```shell
dotnet new web
dotnet add package ModelContextProtocol.AspNetCore --prerelease
```

---

## Install ModelContextProtocol and Hosting Packages (Shell)
Installs the necessary ModelContextProtocol and Microsoft.Extensions.Hosting NuGet packages using the .NET CLI. These packages are required to build and run an MCP server application.
Source: https://github.com/modelcontextprotocol/csharp-sdk/blob/main/README.md#_snippet_3
```shell
dotnet add package ModelContextProtocol --prerelease
dotnet add package Microsoft.Extensions.Hosting
