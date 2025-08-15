# Windows Foundry Local with C#/.NET: Local AI Model Integration Guide

## Overview

Windows Foundry Local is Microsoft's official desktop runtime for serving AI models locally on Windows and macOS. It enables developers to run large language models directly on their hardware, providing privacy-preserving, low-latency AI inference without cloud dependencies.

### Key Benefits

- **Data Privacy**: All processing happens locally; no data leaves your machine
- **Low Latency**: Direct hardware inference without network roundtrips
- **Cost Effective**: No cloud inference fees or API usage charges
- **Offline Capable**: Works without internet connectivity
- **Hardware Optimized**: Automatically selects the best model variant for your hardware (CPU, GPU, NPU)

## Installation and Setup

### Installing Foundry Local

#### Windows
```powershell
# Using winget (recommended)
winget install Microsoft.FoundryLocal

# Or manually download and install
Add-AppxPackage .\FoundryLocal.msix -DependencyPath .\VcLibs.appx
```

#### macOS (Apple Silicon)
```bash
brew tap microsoft/foundrylocal
brew install foundrylocal
```

### Verify Installation
```bash
foundry --help
foundry model list
```

## Model Management

### Available Models

Foundry Local supports various models optimized for different hardware configurations:
- **phi-3.5-mini**: Microsoft's efficient language model
- **qwen2.5-coder-7b-instruct**: Specialized for code generation
- **mistral-7b**: General-purpose language model
- And more...

### Download and Load Models

```bash
# List available models
foundry model list

# Download a model (auto-selects best variant for your hardware)
foundry model download qwen2.5-coder-7b-instruct

# Load and run a model
foundry model run qwen2.5-coder-7b-instruct

# The service will start and display the endpoint URL
# Example: http://localhost:1234
```

## C#/.NET Integration

### NuGet Packages

```xml
<PackageReference Include="Microsoft.AI.Foundry.Local" Version="1.0.0" />
<PackageReference Include="OpenAI" Version="2.0.0" />
<PackageReference Include="Microsoft.Extensions.AI" Version="9.0.0-preview.9" />
```

### Programmatic Setup with FoundryLocalManager

The Foundry Local SDK provides `FoundryLocalManager` to programmatically manage the service and models:

```csharp
using Microsoft.AI.Foundry.Local;
using OpenAI;
using OpenAI.Chat;

// Method 1: Quick start with automatic service and model management
var manager = await FoundryLocalManager.StartModelAsync("qwen2.5-coder-7b-instruct");

// Method 2: Manual control over service and model lifecycle
var manager = new FoundryLocalManager();

// Start the Foundry Local service (if not already running)
await manager.StartServiceAsync();

// Download model if needed (automatic with StartModelAsync)
// This happens automatically when getting model info if not cached
var modelInfo = await manager.GetModelInfoAsync("qwen2.5-coder-7b-instruct");

// The manager provides the endpoint and API key
Console.WriteLine($"Service endpoint: {manager.Endpoint}"); // e.g., http://localhost:5001/v1
Console.WriteLine($"Service running: {manager.IsServiceRunning}");

// Configure OpenAI client with the programmatically managed endpoint
var client = new OpenAIClient(
    new ApiKeyCredential(manager.ApiKey), 
    new OpenAIClientOptions
    {
        Endpoint = manager.Endpoint
    });

// Get the chat client using the model ID from modelInfo
var chatClient = client.GetChatClient(modelInfo.ModelId);
```

### FoundryLocalManager API Reference

| Method/Property | Description |
|----------------|-------------|
| `ServiceUri` | Base URI of the local service |
| `Endpoint` | Full OpenAI-compatible API endpoint (`/v1`) |
| `ApiKey` | API key for authorization (default: "OPENAI_API_KEY") |
| `IsServiceRunning` | Boolean indicating if service is running |
| `StartServiceAsync()` | Starts the Foundry Local service |
| `StopServiceAsync()` | Stops the running service |
| `StartModelAsync(modelAlias)` | Starts service and loads model (downloads if needed) |
| `ListCatalogModelsAsync()` | Lists all available models in catalog |
| `GetModelInfoAsync(alias)` | Gets model information by alias or ID |
| `RefreshCatalog()` | Clears local model catalog cache |

### Complete Lifecycle Example

```csharp
public class FoundryLocalChatService : IDisposable
{
    private readonly FoundryLocalManager _manager;
    private readonly OpenAIClient _openAiClient;
    private ChatClient _chatClient;
    
    public async Task InitializeAsync(string modelAlias = "phi-3.5-mini")
    {
        // Initialize the manager
        _manager = new FoundryLocalManager();
        
        // Start the service if not running
        if (!_manager.IsServiceRunning)
        {
            await _manager.StartServiceAsync();
        }
        
        // Get or download the model
        var modelInfo = await _manager.GetModelInfoAsync(modelAlias);
        
        if (modelInfo == null)
        {
            // List available models if requested model not found
            var catalog = await _manager.ListCatalogModelsAsync();
            throw new InvalidOperationException(
                $"Model '{modelAlias}' not found. Available models: " +
                string.Join(", ", catalog.Select(m => m.Alias)));
        }
        
        // Create OpenAI client with Foundry endpoint
        _openAiClient = new OpenAIClient(
            new ApiKeyCredential(_manager.ApiKey),
            new OpenAIClientOptions { Endpoint = _manager.Endpoint }
        );
        
        // Get chat client for the specific model
        _chatClient = _openAiClient.GetChatClient(modelInfo.ModelId);
    }
    
    public async Task<string> ChatAsync(string message)
    {
        var completion = await _chatClient.CompleteChatAsync(
            [new UserChatMessage(message)]);
        
        return completion.Value.Content[0].Text;
    }
    
    public void Dispose()
    {
        // Optionally stop the service when done
        _manager?.StopServiceAsync().GetAwaiter().GetResult();
    }
}

// Usage
using var service = new FoundryLocalChatService();
await service.InitializeAsync("qwen2.5-coder-7b-instruct");
var response = await service.ChatAsync("Hello, how are you?");
Console.WriteLine(response);
```

## Structured Output Examples

### Simple Structured Output with Native OpenAI SDK

The OpenAI .NET SDK provides native support for structured outputs using JSON schema:

```csharp
using System.Text.Json;
using OpenAI.Chat;

// Define a simple structured output model
public record PowerShellScript(
    string Description,
    string Script
);

// Example: Generate a PowerShell script with structured output
public async Task<PowerShellScript> GeneratePowerShellScript(
    ChatClient chatClient, 
    string task)
{
    // Define the JSON schema for our output
    var jsonSchema = BinaryData.FromString("""
    {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Brief description of what the script does"
            },
            "script": {
                "type": "string",
                "description": "The PowerShell script code"
            }
        },
        "required": ["description", "script"],
        "additionalProperties": false
    }
    """);

    // Configure structured output format
    var responseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
        name: "powershell_script",
        jsonSchema: jsonSchema,
        description: "A PowerShell script with description"
    );

    // Create the chat completion request
    var options = new ChatCompletionOptions
    {
        ResponseFormat = responseFormat,
        Temperature = 0.2f, // Lower for more consistent output
        MaxOutputTokens = 500
    };

    // Make the request
    var completion = await chatClient.CompleteChatAsync(
        [
            new SystemChatMessage("You are a PowerShell expert. Generate scripts with clear descriptions."),
            new UserChatMessage($"Create a PowerShell script to: {task}")
        ],
        options
    );

    // Parse the structured response
    var jsonResponse = completion.Value.Content[0].Text;
    return JsonSerializer.Deserialize<PowerShellScript>(jsonResponse);
}

// Usage example
var script = await GeneratePowerShellScript(
    chatClient, 
    "list all files larger than 100MB in the current directory"
);

Console.WriteLine($"Description: {script.Description}");
Console.WriteLine($"Script:\n{script.Script}");
```

### Using Microsoft.Extensions.AI for Structured Output

Microsoft.Extensions.AI provides a more streamlined approach with automatic type handling:

```csharp
using Microsoft.Extensions.AI;

// Define your response models
public record CodeAnalysis(
    string Language,
    string Purpose,
    bool HasErrors,
    string[] Suggestions
);

// Convert OpenAI client to IChatClient
IChatClient aiClient = chatClient.AsIChatClient();

// Use generic CompleteAsync with type parameter
var analysis = await aiClient.CompleteAsync<CodeAnalysis>(
    "Analyze this code: def hello(): print('world')"
);

Console.WriteLine($"Language: {analysis.Language}");
Console.WriteLine($"Purpose: {analysis.Purpose}");
Console.WriteLine($"Has Errors: {analysis.HasErrors}");
```

### Advanced Structured Output with Complex Types

```csharp
// Define a more complex structured output
public record ApiDocumentation(
    string Endpoint,
    string Method,
    string Description,
    Parameter[] Parameters,
    Response Response
);

public record Parameter(
    string Name,
    string Type,
    bool Required,
    string Description
);

public record Response(
    int StatusCode,
    string ContentType,
    string Schema
);

// Generate API documentation
public async Task<ApiDocumentation> GenerateApiDocs(
    ChatClient chatClient,
    string codeSnippet)
{
    var jsonSchema = BinaryData.FromString("""
    {
        "type": "object",
        "properties": {
            "endpoint": { "type": "string" },
            "method": { "type": "string" },
            "description": { "type": "string" },
            "parameters": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": { "type": "string" },
                        "type": { "type": "string" },
                        "required": { "type": "boolean" },
                        "description": { "type": "string" }
                    },
                    "required": ["name", "type", "required", "description"]
                }
            },
            "response": {
                "type": "object",
                "properties": {
                    "statusCode": { "type": "integer" },
                    "contentType": { "type": "string" },
                    "schema": { "type": "string" }
                },
                "required": ["statusCode", "contentType", "schema"]
            }
        },
        "required": ["endpoint", "method", "description", "parameters", "response"]
    }
    """);

    var responseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
        "api_documentation",
        jsonSchema
    );

    var options = new ChatCompletionOptions
    {
        ResponseFormat = responseFormat,
        Temperature = 0.1f
    };

    var completion = await chatClient.CompleteChatAsync(
        [
            new SystemChatMessage("Generate API documentation from code."),
            new UserChatMessage($"Document this API endpoint:\n{codeSnippet}")
        ],
        options
    );

    var json = completion.Value.Content[0].Text;
    return JsonSerializer.Deserialize<ApiDocumentation>(json, 
        new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
}
```

## Error Handling and Validation

```csharp
public async Task<T?> GetStructuredOutput<T>(
    ChatClient chatClient,
    string prompt,
    string jsonSchema) where T : class
{
    try
    {
        var responseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
            typeof(T).Name.ToLower(),
            BinaryData.FromString(jsonSchema)
        );

        var options = new ChatCompletionOptions
        {
            ResponseFormat = responseFormat,
            Temperature = 0.2f
        };

        var completion = await chatClient.CompleteChatAsync(
            [new UserChatMessage(prompt)],
            options
        );

        var jsonResponse = completion.Value.Content[0].Text;
        
        // Validate JSON before deserializing
        using var doc = JsonDocument.Parse(jsonResponse);
        
        return JsonSerializer.Deserialize<T>(jsonResponse);
    }
    catch (JsonException ex)
    {
        Console.WriteLine($"Invalid JSON response: {ex.Message}");
        return null;
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error getting structured output: {ex.Message}");
        return null;
    }
}
```

## Performance Optimization

### Configuration for Consistent Structured Output

```csharp
public class FoundryLocalStructuredService
{
    private readonly FoundryLocalManager _manager;
    private readonly ChatClient _chatClient;
    
    public async Task<bool> InitializeAsync(string modelAlias = "qwen2.5-coder-7b-instruct")
    {
        // Use the single-line initialization for simplicity
        _manager = await FoundryLocalManager.StartModelAsync(modelAlias);
        
        // Create OpenAI client with managed endpoint
        var client = new OpenAIClient(
            new ApiKeyCredential(_manager.ApiKey),
            new OpenAIClientOptions { Endpoint = _manager.Endpoint }
        );
        
        // Get model info to use the correct model ID
        var modelInfo = await _manager.GetModelInfoAsync(modelAlias);
        _chatClient = client.GetChatClient(modelInfo.ModelId);
        
        return _manager.IsServiceRunning;
    }
    
    public ChatCompletionOptions GetOptimalStructuredOutputOptions(
        ChatResponseFormat responseFormat)
    {
        return new ChatCompletionOptions
        {
            ResponseFormat = responseFormat,
            Temperature = 0.1f,      // Very low for consistency
            TopP = 0.9f,            // Slightly reduced for focus
            MaxOutputTokens = 1000,  // Limit output size
            FrequencyPenalty = 0.0f, // No penalty for structured fields
            PresencePenalty = 0.0f   // No penalty for repeated structures
        };
    }
    
    public async Task ShutdownAsync()
    {
        if (_manager?.IsServiceRunning == true)
        {
            await _manager.StopServiceAsync();
        }
    }
}
```

## Hardware Considerations

### Model Selection by Hardware

| Hardware Type | Recommended Models | Expected Performance |
|--------------|-------------------|---------------------|
| CPU Only | phi-3.5-mini | 5-10 tokens/sec |
| NVIDIA GPU (8GB+) | qwen2.5-coder-7b | 20-50 tokens/sec |
| NVIDIA GPU (16GB+) | mistral-7b, larger models | 30-70 tokens/sec |
| Apple Silicon | phi-3.5-mini, mistral-7b | 15-40 tokens/sec |

### Memory Requirements

- **Minimum**: 16GB RAM for small models (phi-3.5-mini)
- **Recommended**: 32GB RAM for 7B parameter models
- **GPU VRAM**: 8GB minimum for GPU acceleration

## Comparison: Local vs Cloud

| Aspect | Foundry Local | Cloud Services (OpenAI/Azure) |
|--------|--------------|-------------------------------|
| **Latency** | 10-50ms | 200-2000ms |
| **Cost** | Hardware only | $0.001-0.02 per 1K tokens |
| **Privacy** | Complete | Data sent to provider |
| **Availability** | Always (offline) | Internet required |
| **Model Updates** | Manual | Automatic |
| **Scalability** | Single machine | Unlimited |

## Common Use Cases

### 1. Code Generation and Analysis
```csharp
public record CodeReview(
    string Summary,
    string[] Issues,
    string[] Improvements
);

var review = await GetStructuredOutput<CodeReview>(
    chatClient,
    $"Review this code: {sourceCode}",
    codeReviewSchema
);
```

### 2. Data Extraction
```csharp
public record ExtractedData(
    string[] Names,
    string[] Dates,
    decimal[] Amounts
);

var data = await GetStructuredOutput<ExtractedData>(
    chatClient,
    $"Extract data from: {document}",
    extractionSchema
);
```

### 3. Content Generation
```csharp
public record BlogPost(
    string Title,
    string Summary,
    string[] Sections,
    string[] Tags
);

var post = await GetStructuredOutput<BlogPost>(
    chatClient,
    $"Write about: {topic}",
    blogPostSchema
);
```

## Best Practices

1. **Keep Schemas Simple**: Simpler schemas yield more reliable results
2. **Use Low Temperature**: Set temperature to 0.1-0.3 for structured output
3. **Validate Output**: Always validate JSON before deserializing
4. **Handle Failures**: Implement retry logic with exponential backoff
5. **Cache Models**: Keep frequently used models loaded in memory
6. **Monitor Resources**: Track CPU/GPU/memory usage during inference

## Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Model fails to load | Check available disk space and RAM |
| Slow inference | Ensure GPU drivers are updated; use GPU-optimized variant |
| Invalid JSON output | Lower temperature; simplify schema |
| Connection refused | Verify Foundry service is running on correct port |
| Out of memory | Use smaller model or increase system RAM |

## Conclusion

Windows Foundry Local provides a powerful solution for running AI models locally in C#/.NET applications. By leveraging the native structured output support in the OpenAI .NET SDK, developers can build robust, privacy-preserving AI applications with predictable, strongly-typed outputs while maintaining full control over their data and infrastructure.