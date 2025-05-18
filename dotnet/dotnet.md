# Getting Started

Replace "ContosoAgent" with the name of your solution and project as needed.

## Creating the Solution

```pwsh
dotnet new sln -n ContosoAgent
```

## Creating the Project

```pwsh
dotnet new console -n src/ContosoAgent
```

## Adding the Project to the Solution

```pwsh
dotnet sln ContosoAgent.sln add src/ContosoAgent/ContosoAgent.csproj
```

## Installing Dependencies

```pwsh
dotnet add src/ContosoAgent/ContosoAgent.csproj package Microsoft.Extensions.Logging
```

## Building the Solution

```pwsh
dotnet build ContosoAgent.sln
```

## Running the Project

```pwsh
dotnet run --project src/ContosoAgent/ContosoAgent.csproj
```

## Best Practices for Microsoft.Extensions.AI and Microsoft.Extensions.AI.OpenAI

Based on the provided code and general best practices for these libraries, consider the following when integrating with MCP and OpenTelemetry:

### Unified AI Abstraction Layer

- **Model portability**: Use `IChatClient` and builder patterns (`AsBuilder()`, `Build()`) to create a service-agnostic AI client interface. This allows switching between different AI services (like Azure OpenAI, OpenAI API, or local models) without significant code changes.
- **Standardized tooling**: Provides a consistent interface for capabilities like function invocation (`UseFunctionInvocation()`).
- **Middleware integration**: Enables clean implementation of cross-cutting concerns such as telemetry, logging, and error handling.

### OpenTelemetry Observability

- **Centralized instrumentation**: Integrate with OpenTelemetry exporters (like OTLP) for collecting logs, metrics, and traces related to AI interactions.
- **Sensitive data handling**: Be cautious with enabling sensitive data (`EnableSensitiveData = true`). This should typically only be enabled in development environments for debugging purposes.
- **HTTP client monitoring**: Ensure HTTP client instrumentation (`AddHttpClientInstrumentation()`) is configured to track calls made to AI services.
- **Context propagation**: Leverage OpenTelemetry's capabilities to ensure trace correlation between your application logic, MCP interactions, and AI service calls.

### MCP Integration Patterns

- **Capability-based design**: When building MCP servers or clients, explicitly declare and utilize capabilities (e.g., `SamplingHandler`) for clear communication and feature negotiation.
- **Tool discovery**: Use patterns like `ListToolsAsync()` to dynamically discover tools available from an MCP server, making your client adaptable.
- **Streaming interaction**: Design your application to handle streaming responses from chat clients and MCP tools efficiently, especially for long-running operations or continuous conversations.
- **Protocol decoupling**: Abstract the underlying transport mechanism (like `StdioClientTransport`) to decouple your application logic from the specifics of how it communicates with the MCP server.

### Security & Configuration

- **Environment variables**: Store sensitive information like API keys (`OPENAI_API_KEY`) using environment variables or secure configuration providers, rather than hardcoding them.
- **Async initialization**: Use asynchronous patterns (`McpClientFactory.CreateAsync`) for initializing clients and connections to avoid blocking the main thread.
- **Transport isolation**: Consider the security implications of the transport used for MCP communication (e.g., Stdio vs HTTP) and ensure appropriate isolation and authentication mechanisms are in place if necessary.

### Error Handling & Diagnostics

- **Structured logging**: Utilize structured logging integrated with your observability backend (like OpenTelemetry) to capture detailed information about AI interactions and potential issues.
- **Robust response handling**: Implement robust error handling and retry logic for interactions with AI services and MCP servers, as these external dependencies can be subject to network issues or service unavailability.
- **Disposable resources**: Ensure that disposable resources, such as `IChatClient` instances and `McpClient` instances, are properly disposed of using `using` declarations or similar patterns.

For production deployments, consider implementing additional best practices such as retry policies, rate limiting, caching, and integrating prompt/content safety filters, potentially using the middleware extensibility points provided by the Microsoft.Extensions.AI libraries.

## Official .NET Documentation for AI Extensions and OpenAI

Here are official documentation references for `Microsoft.Extensions.AI` and related libraries like `Microsoft.Extensions.AI.OpenAI`:

- [Introduction to Microsoft.Extensions.AI](https://learn.microsoft.com/en-us/dotnet/ai/microsoft-extensions-ai)
- [GitHub Architecture Overview](https://github.com/dotnet/docs/blob/main/docs/ai/ai-extensions.md)
- [.NET AI Ecosystem Tools](https://learn.microsoft.com/en-us/dotnet/ai/dotnet-ai-ecosystem)

---

Not necessarily. To update all outdated NuGet packages automatically in a .NET solution or project without manually updating each one:

1. **Navigate to the solution/project directory**:
   ```bash
   cd path/to/your/solution
   ```

2. **Use `dotnet-outdated` tool** (recommended for automation):
   - Install the tool globally:
     ```bash
     dotnet tool install -g dotnet-outdated-tool
     ```
   - Run to update all packages to the latest version:
     ```bash
     dotnet outdated -u
     ```

3. **Alternative: Manual bulk update**:
   - List outdated packages:
     ```bash
     dotnet list package --outdated
     ```
   - Update all packages in a project using a script or command loop (e.g., in PowerShell):
     ```powershell
     dotnet list package --outdated | ForEach-Object { if ($_ -match '>\s+(\S+)\s+') { dotnet add package $matches[1] } }
     ```

4. **Verify**:
   ```bash
   dotnet build
   ```

**Note**: Install `dotnet-outdated-tool` for the easiest approach. Backup your project before updating. Some packages may require specific versions due to compatibility.
