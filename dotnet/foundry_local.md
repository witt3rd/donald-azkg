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

## REST API Reference

### API Overview

Foundry Local provides both OpenAI-compatible endpoints and custom management endpoints. The API is currently in preview and may have breaking changes.

### Base URL
```
http://localhost:{port}
```
Default port is typically 1234, but can vary based on configuration.

### OpenAI Compatible Endpoints

#### Chat Completions
```http
POST /v1/chat/completions
```

Standard OpenAI chat completions endpoint with full compatibility.

**Request Body:**
```json
{
  "model": "string",                    // Required: Model ID
  "messages": [                         // Required: Conversation history
    {
      "role": "system|user|assistant|tool",
      "content": "string",
      "name": "string",                 // Optional: User/assistant name
      "tool_call_id": "string"          // Optional: For tool responses
    }
  ],
  "temperature": 0.7,                   // Optional: 0-2, default 1
  "top_p": 1.0,                         // Optional: 0-1, default 1
  "n": 1,                               // Optional: Number of choices
  "max_tokens": 1000,                   // Optional: Max response tokens
  "stream": false,                      // Optional: Enable SSE streaming
  "stop": ["string"],                   // Optional: Up to 4 stop sequences
  "presence_penalty": 0,                // Optional: -2 to 2
  "frequency_penalty": 0,               // Optional: -2 to 2
  "logit_bias": {},                     // Optional: Token ID to bias map
  "user": "string",                     // Optional: User identifier
  "response_format": {                  // Optional: Response structure
    "type": "text|json_object|json_schema",
    "json_schema": {                    // When type is json_schema
      "name": "string",
      "schema": {},
      "strict": true
    }
  },
  "tools": [                            // Optional: Tool definitions
    {
      "type": "function",
      "function": {
        "name": "string",
        "description": "string",
        "parameters": {}                // JSON Schema
      }
    }
  ],
  "tool_choice": "none|auto|required"   // Optional: Tool selection
}
```

**Response:**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "model-name",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "string",              // May be null when using tools
        "tool_calls": [                   // Optional: Tool invocations
          {
            "id": "call_xxx",
            "type": "function",
            "function": {
              "name": "function_name",
              "arguments": "json_string"
            }
          }
        ]
      },
      "finish_reason": "stop|length|tool_calls|content_filter"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

**Streaming Response (when stream=true):**
```
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","created":1234567890,"model":"model-name","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","created":1234567890,"model":"model-name","choices":[{"index":0,"delta":{"content":" world"},"finish_reason":null}]}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","created":1234567890,"model":"model-name","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

#### Embeddings
```http
POST /v1/embeddings
```

Generate text embeddings compatible with OpenAI's embedding API.

**Request Body:**
```json
{
  "model": "string",
  "input": "string or array of strings",
  "encoding_format": "float"
}
```

### Custom Foundry Endpoints

#### List Available Models
```http
GET /foundry/list
```

Returns catalog of all available Foundry Local models.

**Response:**
```json
{
  "models": [
    {
      "name": "model-name",
      "displayName": "Model Display Name",
      "providerType": "FoundryLocal",
      "version": "1.0.0",
      "runtime": {
        "type": "ONNX",
        "version": "1.18"
      },
      "modelSettings": {
        "contextLength": 4096,
        "embeddingDimension": 768
      }
    }
  ]
}
```

#### Load Model
```http
GET /openai/load/{modelName}
```

Load a specific model into memory.

**Query Parameters:**
- `unload` (boolean): Unload other models first
- `ttl` (integer): Time-to-live in seconds
- `ep` (string): Execution provider (CPU, CUDA, DirectML)

#### Unload Model
```http
GET /openai/unload/{modelName}
```

Remove a specific model from memory.

#### List Loaded Models
```http
GET /openai/loadedmodels
```

Returns array of currently loaded model names.

#### Download Model
```http
POST /openai/download
```

Download a model to local storage.

**Request Body:**
```json
{
  "modelName": "string",
  "provider": "FoundryLocal",
  "stream": true
}
```

#### Register External Model
```http
POST /openai/register
```

Register an external OpenAI-compatible model provider.

**Request Body:**
```json
{
  "TypeName": "provider-name",
  "ModelName": "model-name",
  "BaseUri": "https://api.example.com"
}
```

#### Get All Models
```http
GET /openai/models
```

List all available models (local and registered external).

#### Server Status
```http
GET /openai/status
```

Get server health and status information.

#### Token Counting
```http
POST /v1/chat/completions/tokenizer/encode/count
```

Count tokens without performing inference.

**Request Body:**
```json
{
  "model": "string",
  "messages": [
    {
      "role": "string",
      "content": "string"
    }
  ]
}
```

**Response:**
```json
{
  "tokenCount": 123
}
```

### GPU Management

#### Get GPU Device
```http
GET /openai/getgpudevice
```

Returns current GPU device ID.

#### Set GPU Device
```http
GET /openai/setgpudevice/{deviceId}
```

Switch to specified GPU device.

## C#/.NET REST API Usage Examples

### Direct REST API Usage with HttpClient

While the `FoundryLocalManager` provides convenient programmatic control, you can also interact directly with the REST API:

```csharp
using System.Net.Http;
using System.Text;
using System.Text.Json;

public class FoundryLocalRestClient
{
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl;
    
    public FoundryLocalRestClient(string baseUrl = "http://localhost:1234")
    {
        _baseUrl = baseUrl;
        _httpClient = new HttpClient { BaseAddress = new Uri(baseUrl) };
    }
    
    // List all available models in the catalog
    public async Task<JsonDocument> ListAvailableModelsAsync()
    {
        var response = await _httpClient.GetAsync("/foundry/list");
        response.EnsureSuccessStatusCode();
        
        var json = await response.Content.ReadAsStringAsync();
        return JsonDocument.Parse(json);
    }
    
    // Load a specific model
    public async Task<bool> LoadModelAsync(string modelName, string executionProvider = "CPU")
    {
        var response = await _httpClient.GetAsync(
            $"/openai/load/{Uri.EscapeDataString(modelName)}?ep={executionProvider}");
        
        return response.IsSuccessStatusCode;
    }
    
    // Get currently loaded models
    public async Task<string[]> GetLoadedModelsAsync()
    {
        var response = await _httpClient.GetAsync("/openai/loadedmodels");
        response.EnsureSuccessStatusCode();
        
        var json = await response.Content.ReadAsStringAsync();
        return JsonSerializer.Deserialize<string[]>(json) ?? Array.Empty<string>();
    }
    
    // Count tokens without inference
    public async Task<int> CountTokensAsync(string model, List<ChatMessage> messages)
    {
        var request = new
        {
            model = model,
            messages = messages.Select(m => new { role = m.Role, content = m.Content })
        };
        
        var json = JsonSerializer.Serialize(request);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        
        var response = await _httpClient.PostAsync(
            "/v1/chat/completions/tokenizer/encode/count", content);
        response.EnsureSuccessStatusCode();
        
        var responseJson = await response.Content.ReadAsStringAsync();
        using var doc = JsonDocument.Parse(responseJson);
        return doc.RootElement.GetProperty("tokenCount").GetInt32();
    }
    
    // Download a model with progress tracking
    public async Task DownloadModelAsync(
        string modelName, 
        IProgress<double>? progress = null)
    {
        var request = new
        {
            modelName = modelName,
            provider = "FoundryLocal",
            stream = true
        };
        
        var json = JsonSerializer.Serialize(request);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        
        using var response = await _httpClient.PostAsync("/openai/download", content);
        response.EnsureSuccessStatusCode();
        
        // Handle streaming response if needed
        using var stream = await response.Content.ReadAsStreamAsync();
        // Process download stream and report progress
    }
    
    // Register an external OpenAI-compatible provider
    public async Task RegisterExternalProviderAsync(
        string providerName, 
        string modelName, 
        string baseUri)
    {
        var request = new
        {
            TypeName = providerName,
            ModelName = modelName,
            BaseUri = baseUri
        };
        
        var json = JsonSerializer.Serialize(request);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        
        var response = await _httpClient.PostAsync("/openai/register", content);
        response.EnsureSuccessStatusCode();
    }
}

// Chat message helper class
public record ChatMessage(string Role, string Content);
```

### Advanced Model Management

```csharp
public class FoundryModelManager
{
    private readonly FoundryLocalRestClient _restClient;
    private readonly ILogger<FoundryModelManager> _logger;
    
    public FoundryModelManager(
        FoundryLocalRestClient restClient, 
        ILogger<FoundryModelManager> logger)
    {
        _restClient = restClient;
        _logger = logger;
    }
    
    // Ensure a model is loaded with automatic download if needed
    public async Task<bool> EnsureModelLoadedAsync(
        string modelName, 
        string? executionProvider = null)
    {
        // Check if already loaded
        var loadedModels = await _restClient.GetLoadedModelsAsync();
        if (loadedModels.Contains(modelName))
        {
            _logger.LogInformation("Model {ModelName} is already loaded", modelName);
            return true;
        }
        
        // Try to load the model
        var ep = executionProvider ?? GetOptimalExecutionProvider();
        var loaded = await _restClient.LoadModelAsync(modelName, ep);
        
        if (!loaded)
        {
            _logger.LogInformation("Model not found locally, downloading {ModelName}", modelName);
            
            // Download the model
            var progress = new Progress<double>(p => 
                _logger.LogInformation("Download progress: {Progress:P}", p));
            
            await _restClient.DownloadModelAsync(modelName, progress);
            
            // Try loading again
            loaded = await _restClient.LoadModelAsync(modelName, ep);
        }
        
        return loaded;
    }
    
    // Determine optimal execution provider based on hardware
    private string GetOptimalExecutionProvider()
    {
        // Check for NVIDIA GPU
        if (IsNvidiaGpuAvailable())
            return "CUDA";
        
        // Check for DirectML support (Windows)
        if (OperatingSystem.IsWindows())
            return "DirectML";
        
        return "CPU";
    }
    
    private bool IsNvidiaGpuAvailable()
    {
        // Implementation to check for NVIDIA GPU
        // This could check for CUDA runtime or query system info
        return false; // Placeholder
    }
}
```

### Hybrid Approach: Combining FoundryLocalManager with REST API

```csharp
public class HybridFoundryClient
{
    private readonly FoundryLocalManager _manager;
    private readonly HttpClient _httpClient;
    
    public async Task InitializeAsync(string modelAlias)
    {
        // Use FoundryLocalManager for service management
        _manager = await FoundryLocalManager.StartModelAsync(modelAlias);
        
        // Create HttpClient for direct REST calls
        _httpClient = new HttpClient 
        { 
            BaseAddress = new Uri(_manager.ServiceUri) 
        };
        _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_manager.ApiKey}");
    }
    
    // Use REST API for custom operations not in SDK
    public async Task<int> GetTokenCountAsync(string text)
    {
        var request = new
        {
            model = "current-model",
            messages = new[] { new { role = "user", content = text } }
        };
        
        var response = await _httpClient.PostAsJsonAsync(
            "/v1/chat/completions/tokenizer/encode/count", request);
        
        response.EnsureSuccessStatusCode();
        var result = await response.Content.ReadFromJsonAsync<TokenCountResponse>();
        return result?.TokenCount ?? 0;
    }
    
    // Use REST API to check GPU status
    public async Task<int> GetCurrentGpuDeviceAsync()
    {
        var response = await _httpClient.GetAsync("/openai/getgpudevice");
        response.EnsureSuccessStatusCode();
        
        var deviceId = await response.Content.ReadAsStringAsync();
        return int.Parse(deviceId);
    }
    
    // Switch GPU device for multi-GPU systems
    public async Task SetGpuDeviceAsync(int deviceId)
    {
        var response = await _httpClient.GetAsync($"/openai/setgpudevice/{deviceId}");
        response.EnsureSuccessStatusCode();
    }
    
    private record TokenCountResponse(int TokenCount);
}
```

### Working with Tool/Function Calling

```csharp
using System.Text.Json;
using System.Net.Http;

public class FoundryToolCallingExample
{
    private readonly HttpClient _httpClient;
    
    public async Task<string> ExecuteWithToolsAsync(string userPrompt)
    {
        var request = new
        {
            model = "qwen2.5-coder-7b-instruct",
            messages = new[]
            {
                new { role = "system", content = "You are a helpful assistant with access to tools." },
                new { role = "user", content = userPrompt }
            },
            tools = new[]
            {
                new
                {
                    type = "function",
                    function = new
                    {
                        name = "get_weather",
                        description = "Get the current weather in a location",
                        parameters = new
                        {
                            type = "object",
                            properties = new
                            {
                                location = new { type = "string", description = "City name" },
                                unit = new { type = "string", @enum = new[] { "celsius", "fahrenheit" } }
                            },
                            required = new[] { "location" }
                        }
                    }
                }
            },
            tool_choice = "auto"
        };
        
        var response = await _httpClient.PostAsJsonAsync("/v1/chat/completions", request);
        var result = await response.Content.ReadFromJsonAsync<ChatCompletionResponse>();
        
        // Check if the model wants to call a tool
        if (result?.Choices?[0].Message.ToolCalls != null)
        {
            foreach (var toolCall in result.Choices[0].Message.ToolCalls)
            {
                if (toolCall.Function.Name == "get_weather")
                {
                    // Parse arguments and execute the function
                    var args = JsonSerializer.Deserialize<WeatherArgs>(toolCall.Function.Arguments);
                    var weatherData = await GetWeatherData(args.Location, args.Unit);
                    
                    // Send the tool response back to the model
                    var followUpRequest = new
                    {
                        model = "qwen2.5-coder-7b-instruct",
                        messages = new object[]
                        {
                            new { role = "system", content = "You are a helpful assistant." },
                            new { role = "user", content = userPrompt },
                            result.Choices[0].Message,  // Include the assistant's message with tool calls
                            new 
                            { 
                                role = "tool",
                                content = JsonSerializer.Serialize(weatherData),
                                tool_call_id = toolCall.Id
                            }
                        }
                    };
                    
                    var finalResponse = await _httpClient.PostAsJsonAsync("/v1/chat/completions", followUpRequest);
                    var finalResult = await finalResponse.Content.ReadFromJsonAsync<ChatCompletionResponse>();
                    return finalResult?.Choices?[0].Message.Content ?? "";
                }
            }
        }
        
        return result?.Choices?[0].Message.Content ?? "";
    }
    
    private record WeatherArgs(string Location, string Unit = "celsius");
    private async Task<object> GetWeatherData(string location, string unit)
    {
        // Simulate weather API call
        return new { location, temperature = 22, unit, condition = "sunny" };
    }
}
```

### Streaming Responses with HttpClient

```csharp
using System.Text;
using System.Text.Json;
using System.Runtime.CompilerServices;

public class FoundryStreamingClient
{
    private readonly HttpClient _httpClient;
    
    public async IAsyncEnumerable<string> StreamChatAsync(
        string prompt,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        var request = new
        {
            model = "phi-3.5-mini",
            messages = new[] { new { role = "user", content = prompt } },
            stream = true,
            temperature = 0.7f,
            max_tokens = 500
        };
        
        var httpRequest = new HttpRequestMessage(HttpMethod.Post, "/v1/chat/completions")
        {
            Content = new StringContent(
                JsonSerializer.Serialize(request),
                Encoding.UTF8,
                "application/json")
        };
        
        using var response = await _httpClient.SendAsync(
            httpRequest, 
            HttpCompletionOption.ResponseHeadersRead,
            cancellationToken);
        
        response.EnsureSuccessStatusCode();
        
        using var stream = await response.Content.ReadAsStreamAsync(cancellationToken);
        using var reader = new StreamReader(stream);
        
        while (!reader.EndOfStream && !cancellationToken.IsCancellationRequested)
        {
            var line = await reader.ReadLineAsync();
            
            if (string.IsNullOrWhiteSpace(line) || !line.StartsWith("data: "))
                continue;
            
            var data = line.Substring(6); // Remove "data: " prefix
            
            if (data == "[DONE]")
                break;
            
            try
            {
                using var doc = JsonDocument.Parse(data);
                var root = doc.RootElement;
                
                if (root.TryGetProperty("choices", out var choices) &&
                    choices.GetArrayLength() > 0)
                {
                    var delta = choices[0].GetProperty("delta");
                    if (delta.TryGetProperty("content", out var content))
                    {
                        var text = content.GetString();
                        if (!string.IsNullOrEmpty(text))
                            yield return text;
                    }
                }
            }
            catch (JsonException)
            {
                // Skip malformed JSON chunks
                continue;
            }
        }
    }
    
    // Usage example
    public async Task StreamExample()
    {
        await foreach (var chunk in StreamChatAsync("Write a haiku about coding"))
        {
            Console.Write(chunk);
        }
        Console.WriteLine();
    }
}
```

### Advanced OpenAI Parameters Usage

```csharp
public class AdvancedFoundryClient
{
    private readonly HttpClient _httpClient;
    
    // Example using all advanced parameters
    public async Task<ChatCompletionResponse> AdvancedCompletionAsync()
    {
        var request = new
        {
            model = "qwen2.5-coder-7b-instruct",
            messages = new[]
            {
                new { role = "system", content = "You are a code reviewer." },
                new { role = "user", content = "Review this function: def add(a,b): return a+b" }
            },
            
            // Temperature and sampling controls
            temperature = 0.3f,          // Lower for more focused responses
            top_p = 0.95f,              // Nucleus sampling threshold
            
            // Output controls
            max_tokens = 300,           // Limit response length
            n = 1,                      // Number of completions
            
            // Repetition penalties
            presence_penalty = 0.1f,    // Encourage new topics
            frequency_penalty = 0.1f,   // Reduce repetition
            
            // Stop sequences
            stop = new[] { "\n\n", "END" },
            
            // Bias specific tokens
            logit_bias = new Dictionary<string, float>
            {
                ["1234"] = -100,        // Suppress token 1234
                ["5678"] = 5            // Boost token 5678
            },
            
            // Structured output
            response_format = new
            {
                type = "json_object"    // Force JSON response
            },
            
            // User tracking
            user = "user-123"           // For usage tracking
        };
        
        var response = await _httpClient.PostAsJsonAsync("/v1/chat/completions", request);
        return await response.Content.ReadFromJsonAsync<ChatCompletionResponse>();
    }
    
    // Example with JSON Schema response format
    public async Task<T> GetStructuredResponseAsync<T>(string prompt)
    {
        var schema = JsonSchemaGenerator.Generate<T>();
        
        var request = new
        {
            model = "phi-3.5-mini",
            messages = new[] { new { role = "user", content = prompt } },
            response_format = new
            {
                type = "json_schema",
                json_schema = new
                {
                    name = typeof(T).Name.ToLower(),
                    schema = schema,
                    strict = true
                }
            },
            temperature = 0.1f  // Very low for consistent structured output
        };
        
        var response = await _httpClient.PostAsJsonAsync("/v1/chat/completions", request);
        var result = await response.Content.ReadFromJsonAsync<ChatCompletionResponse>();
        
        var jsonContent = result?.Choices?[0].Message.Content;
        return JsonSerializer.Deserialize<T>(jsonContent);
    }
}

// Response models
public record ChatCompletionResponse(
    string Id,
    string Object,
    long Created,
    string Model,
    Choice[] Choices,
    Usage Usage
);

public record Choice(
    int Index,
    Message Message,
    string FinishReason
);

public record Message(
    string Role,
    string Content,
    ToolCall[] ToolCalls = null
);

public record ToolCall(
    string Id,
    string Type,
    FunctionCall Function
);

public record FunctionCall(
    string Name,
    string Arguments
);

public record Usage(
    int PromptTokens,
    int CompletionTokens,
    int TotalTokens
);
```

### Error Handling for REST API Calls

```csharp
public class ResilientFoundryClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<ResilientFoundryClient> _logger;
    private readonly int _maxRetries = 3;
    
    public async Task<T?> ExecuteWithRetryAsync<T>(
        Func<Task<HttpResponseMessage>> operation,
        Func<string, T> parseResponse)
    {
        for (int attempt = 1; attempt <= _maxRetries; attempt++)
        {
            try
            {
                using var response = await operation();
                
                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync();
                    return parseResponse(content);
                }
                
                // Handle specific error codes
                switch (response.StatusCode)
                {
                    case HttpStatusCode.NotFound:
                        _logger.LogWarning("Resource not found");
                        return default;
                        
                    case HttpStatusCode.ServiceUnavailable:
                        if (attempt < _maxRetries)
                        {
                            await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, attempt)));
                            continue;
                        }
                        break;
                }
                
                _logger.LogError("Request failed: {StatusCode}", response.StatusCode);
            }
            catch (HttpRequestException ex)
            {
                _logger.LogError(ex, "HTTP request failed on attempt {Attempt}", attempt);
                
                if (attempt < _maxRetries)
                    await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, attempt)));
                else
                    throw;
            }
        }
        
        return default;
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