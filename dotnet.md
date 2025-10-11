---
tags: [csharp, dotnet, reference, guide, api, best-practices]
---

# Getting Started with .NET Development

This guide provides essential .NET CLI commands and best practices for creating and managing .NET projects. Replace "ContosoAgent" with your actual project name.

## Creating Solutions and Projects

### Creating a Solution

```pwsh
# Create a new solution file
dotnet new sln -n ContosoAgent

# Create in a specific folder
dotnet new sln -n ContosoAgent -o solutions/ContosoAgent
```

### Creating a Console Project

```pwsh
# Create a console application
dotnet new console -n src/ContosoAgent

# With specific framework
dotnet new console -n src/ContosoAgent -f net9.0

# Using explicit Program.Main instead of top-level statements (NET 6+)
dotnet new console -n src/ContosoAgent --use-program-main
```

### Adding Projects to Solution

```pwsh
# Add project to solution
dotnet sln ContosoAgent.sln add src/ContosoAgent/ContosoAgent.csproj

# Add to solution folder
dotnet sln ContosoAgent.sln add src/ContosoAgent/ContosoAgent.csproj --solution-folder src

# List all projects in solution
dotnet sln list
```

## Managing NuGet Packages

### Installing Packages

```pwsh
# Add a package (latest version)
dotnet add src/ContosoAgent/ContosoAgent.csproj package Microsoft.Extensions.Logging

# Add specific version
dotnet add package Microsoft.Extensions.Logging --version 9.0.0

# Add prerelease version
dotnet add package Microsoft.Extensions.AI --prerelease

# Add with specific source
dotnet add package MyPackage -s https://api.nuget.org/v3/index.json
```

### Listing Packages

```pwsh
# List outdated packages
dotnet list package --outdated

# List all packages including transitive
dotnet list package --include-transitive
```

## Building Projects

```pwsh
# Build solution or project
dotnet build ContosoAgent.sln

# Build in Release configuration
dotnet build -c Release

# Build for specific runtime
dotnet build -r win-x64

# Build with specific architecture
dotnet build -a x64

# Build without restore
dotnet build --no-restore

# Build with custom output path (NET 8+)
dotnet build --artifacts-path ./artifacts
```

## Running Projects

```pwsh
# Run project
dotnet run --project src/ContosoAgent/ContosoAgent.csproj

# Run from current directory
dotnet run

# Run with arguments
dotnet run -- arg1 arg2

# Run without building
dotnet run --no-build

# Run with environment variables
dotnet run -e ASPNETCORE_ENVIRONMENT=Development

# Run with specific framework
dotnet run -f net9.0

# Run with specific configuration
dotnet run -c Release
```

## Microsoft.Extensions.AI and Microsoft.Extensions.AI.OpenAI

### Installation

```pwsh
# Install Microsoft.Extensions.AI (includes abstractions)
dotnet add package Microsoft.Extensions.AI --prerelease

# Install OpenAI implementation
dotnet add package Microsoft.Extensions.AI.OpenAI --prerelease

# Latest preview versions (as of August 2025)
# Microsoft.Extensions.AI: 9.8.0
# Microsoft.Extensions.AI.OpenAI: 9.7.1-preview.1.25365.4
```

### Key Features (2025)

- **Unified AI Abstractions**: IChatClient interface for consistent AI service integration
- **Provider Flexibility**: Easy switching between OpenAI, Azure OpenAI, Ollama, and other providers
- **Middleware Pipeline**: Layer components for logging, caching, telemetry, and function invocation
- **Function Calling**: Automatic function invocation with AIFunction and FunctionInvokingChatClient
- **Multi-modal Support**: Handle text, images, audio, and other content types

### Basic Usage Example

```csharp
using Microsoft.Extensions.AI;

// Create client with OpenAI
IChatClient client = new OpenAI.Chat.ChatClient(
    "gpt-4o-mini", 
    Environment.GetEnvironmentVariable("OPENAI_API_KEY")
).AsIChatClient();

// Add middleware layers
IChatClient enhancedClient = client
    .AsBuilder()
    .UseFunctionInvocation()
    .UseOpenTelemetry()
    .UseDistributedCache(cache)
    .Build();

// Send chat request
var response = await enhancedClient.GetResponseAsync("What is AI?");
```

### Best Practices for Production

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

## .NET AI Templates (Preview 2 - April 2025)

### Installation

```pwsh
# Install AI templates
dotnet new install Microsoft.Extensions.AI.Templates

# Create AI chat web app
dotnet new aichatweb -n MyAIChatApp

# List available AI templates
dotnet new list ai
```

### Template Features

- **AI Chat Web App**: Blazor-based chat application with RAG support
- **Data Ingestion**: Built-in data processing and caching
- **Vector Store Support**: Local storage by default, Qdrant in Preview 2
- **.NET Aspire Integration**: Cloud-native AI app development (Preview 2)
- **GitHub Models**: Default model provider for easy startup

### Coming Soon

- AI Console template
- Minimal API template  
- Semantic Kernel integration
- Azure AI Foundry support
- Default inclusion in .NET SDK

## Official Documentation References

### Microsoft.Extensions.AI
- [Microsoft.Extensions.AI Documentation](https://learn.microsoft.com/en-us/dotnet/ai/microsoft-extensions-ai)
- [Introducing Microsoft.Extensions.AI Preview](https://devblogs.microsoft.com/dotnet/introducing-microsoft-extensions-ai-preview/)
- [NuGet Package](https://www.nuget.org/packages/Microsoft.Extensions.AI)

### .NET AI Development
- [.NET AI Ecosystem Tools](https://learn.microsoft.com/en-us/dotnet/ai/dotnet-ai-ecosystem)
- [AI Template Quickstart](https://learn.microsoft.com/en-us/dotnet/ai/quickstarts/ai-templates)
- [Azure OpenAI with .NET](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai.openai-readme)

### .NET CLI References
- [dotnet new Command](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-new)
- [dotnet build Command](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build)
- [dotnet run Command](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-run)
- [dotnet add package Command](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-add-package)
- [dotnet sln Command](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-sln)

## Updating NuGet Packages in Bulk

To update all outdated NuGet packages efficiently:

### Using dotnet-outdated Tool (Recommended)

The `dotnet-outdated-tool` is actively maintained (last updated March 2025) and provides comprehensive bulk update capabilities.

```bash
# Install the tool
dotnet tool install -g dotnet-outdated-tool

# Update all packages automatically
dotnet outdated -u

# Interactive mode - prompts for each package
dotnet outdated -u:prompt

# Update only minor/patch versions (preserve major version)
dotnet outdated -u -vl:Major

# Update only patch versions (preserve minor version)  
dotnet outdated -u -vl:Minor

# Include pre-release packages
dotnet outdated -u -pre:Always

# Check specific project or solution
dotnet outdated path/to/project.csproj
```

### Using Built-in .NET CLI

```bash
# List outdated packages
dotnet list package --outdated

# List with sources
dotnet list package --outdated --include-transitive
```

### PowerShell Script for Bulk Updates

```powershell
# Parse and update each outdated package
dotnet list package --outdated --format json | 
    ConvertFrom-Json | 
    ForEach-Object { $_.projects } | 
    ForEach-Object { $_.frameworks } | 
    ForEach-Object { $_.topLevelPackages } | 
    ForEach-Object { dotnet add package $_.id }
```

**Best Practices**:
- Always backup or commit your code before bulk updates
- Test thoroughly after updates
- Consider using version locking (-vl) to prevent breaking changes
- Review update changes before applying in production
