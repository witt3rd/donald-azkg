---
tags: [api, patterns, development]
---
# .NET Windows Copilot Runtime SDK Capabilities

The **Windows Copilot Runtime** provides a comprehensive set of AI-powered APIs for .NET developers to integrate local, on-device AI capabilities into Windows applications. This system leverages Neural Processing Units (NPUs) on **Copilot+ PCs** to deliver high-performance AI features without requiring cloud connectivity.

## Core Architecture

The Windows Copilot Runtime is built around the **Windows App SDK experimental releases** (currently version 1.8 experimental) and provides AI functionality through several key namespaces:[1][2]

- `Microsoft.Windows.AI` - Core AI features and device management
- `Microsoft.Windows.AI.Generative` - Language model APIs including Phi Silica
- `Microsoft.Windows.AI.ContentModeration` - Content filtering and safety
- `Microsoft.Windows.Vision` - Computer vision and image analysis

## Hardware Requirements

**Copilot+ PC Requirement**: All Windows Copilot Runtime APIs require a Copilot+ PC with a Neural Processing Unit (NPU). These devices must be running the latest Windows 11 Insider Preview builds to access the experimental features.[3][4][5][6]

**Supported Hardware**: The APIs work on Snapdragon X Elite, Intel Lunar Lake, and AMD Zen 5-based Copilot+ PCs, though current documentation suggests initial focus on Snapdragon X devices.[4]

## Language Model Capabilities

### Phi Silica Integration

**Phi Silica** is Microsoft's most powerful NPU-tuned Small Language Model (SLM), designed specifically for on-device processing. Key capabilities include:[7][8][9]

**Basic Text Generation**:[10][7]

```csharp
using Microsoft.Windows.AI.Generative;

// Ensure model is ready
if (LanguageModel.GetReadyState() != AIFeatureReadyState.Ready)
{
    await LanguageModel.EnsureReadyAsync();
}

// Create language model instance
using var languageModel = await LanguageModel.CreateAsync();

// Generate response
var result = await languageModel.GenerateResponseAsync("What is the molecular formula for glucose?");
Console.WriteLine(result.Text); // Output: C6H12O6
```

**Advanced Configuration Options**:[10]

```csharp
var contentFilterOptions = new ContentFilterOptions();
contentFilterOptions.PromptMaxAllowedSeverityLevel.SelfHarm = SeverityLevel.Low;
contentFilterOptions.PromptMaxAllowedSeverityLevel.Violent = SeverityLevel.Low;

var languageModelOptions = new LanguageModelOptions();
languageModelOptions.Temperature = 0.0f;
languageModelOptions.TopP = 0.1f;
languageModelOptions.TopK = 1;
languageModelOptions.ContentFilterOptions = contentFilterOptions;

var result = await languageModel.GenerateResponseAsync(prompt, languageModelOptions);
```

### Text Intelligence Skills

Phi Silica includes built-in text transformation capabilities:[7]

**Text Summarization**:

```csharp
using var languageModel = await LanguageModel.CreateAsync();
var textSummarizer = new TextSummarizer(languageModel);
string text = "Large amount of text to summarize...";
var result = await textSummarizer.SummarizeAsync(text);
Console.WriteLine(result.Text);
```

**Additional Skills Available**:[7]

- **Text-to-Table**: Converts responses into structured table format
- **Rewrite**: Rephrases content for improved clarity and readability
- **Summarize**: Creates concise summaries of input text

## Computer Vision APIs

The Windows AI APIs provide comprehensive image processing capabilities:[11][3]

### Text Recognition (OCR)

Extract and recognize text from images with high accuracy:[11]

```csharp
using Microsoft.Windows.Vision;

// Process image for text extraction
var textRecognizer = await TextRecognizer.CreateAsync();
var result = await textRecognizer.RecognizeTextAsync(imageData);
```

### Image Processing Features

**Image Super Resolution**: Scale and enhance image quality using AI[3][11]
**Image Segmentation**: Identify and segment objects within images[11][3]
**Image Description**: Generate natural language descriptions of image content[3][11]
**Object Erase**: Remove unwanted objects from images with intelligent background filling[11][3]

### Windows Studio Effects

AI-powered camera and microphone enhancements:[3][11]

- Background blur and replacement
- Eye contact correction
- Automatic framing
- Portrait lighting adjustments
- Voice focus and noise reduction

## Development Setup and Configuration

### NuGet Package Installation

The Windows Copilot Runtime APIs are available through the Windows App SDK experimental releases. Configure your project with:[6][1]

```xml



    net8.0-windows10.0.19041.0
    true
    win-arm64



```

### Required Namespaces

```csharp
using Microsoft.Windows.AI;
using Microsoft.Windows.AI.Generative;
using Microsoft.Windows.AI.ContentModeration;
using Microsoft.Windows.Vision;
```

## Content Safety and Moderation

The Windows Copilot Runtime includes built-in content moderation capabilities:[11][3]

**Configurable Safety Levels**:

- Content filtering for harmful, violent, or inappropriate content
- Prompt-level and response-level filtering
- Adjustable severity thresholds (Low, Medium - High not currently supported)

**Response Status Handling**:[10]

```csharp
var result = await languageModel.GenerateResponseAsync(prompt);
switch (result.Status)
{
    case LanguageModelResponseStatus.Complete:
        // Process successful response
        break;
    case LanguageModelResponseStatus.ResponseBlockedByContentModeration:
        // Handle content moderation block
        break;
    case LanguageModelResponseStatus.PromptBlockedByContentModeration:
        // Handle prompt rejection
        break;
    case LanguageModelResponseStatus.BlockedByPolicy:
        // Handle policy violation
        break;
}
```

## Performance and Resource Management

### Local Processing Benefits

**Resource Efficiency**: Models run entirely on-device, reducing cloud costs and latency[12][13]
**Shared Resources**: AI models are shared across applications and users on the same device[13]
**Hardware Optimization**: Windows automatically targets appropriate hardware (CPU, GPU, NPU) based on device capabilities[12][13]
**Automatic Updates**: Windows manages model downloading, installation, and updates transparently[13]

### Development Tools and Resources

**AI Dev Gallery**: Microsoft Store app for testing and experimenting with Windows AI APIs[3][11]
**Sample Applications**: Comprehensive code samples available in the WindowsAppSDK-Samples repository[14]
**Documentation**: Extensive developer guidance and tutorials available through Microsoft Learn[7][3]

## Integration with Broader .NET Ecosystem

### Microsoft.Extensions.AI Compatibility

The Windows Copilot Runtime can be integrated with the broader .NET AI ecosystem through **Microsoft.Extensions.AI** libraries, providing:[15]

- Unified interfaces for different AI providers
- Dependency injection support
- Middleware patterns for telemetry and caching
- Interoperability with cloud AI services

### Enterprise Integration

**Microsoft 365 Agents SDK**: Integration capabilities with Copilot Studio and enterprise AI workflows[16][17][18]
**Semantic Kernel**: Compatible with Microsoft's orchestration framework for building AI applications[19]
**Azure AI Integration**: Ability to combine local and cloud AI capabilities seamlessly

## Current Status and Limitations

**Experimental Nature**: All Windows Copilot Runtime APIs are currently in experimental preview and subject to breaking changes[1][6]
**Hardware Dependency**: Requires specific NPU-enabled hardware limiting deployment scenarios[4][3]
**Geographic Limitations**: Some features like Phi Silica are not available in China[7][11]
**Development Environment**: Requires Windows 11 Insider Preview builds for development and testing[6][4]

The Windows Copilot Runtime represents Microsoft's vision for democratizing AI development on Windows by providing high-performance, privacy-focused, on-device AI capabilities. While currently in experimental stages, it offers .NET developers powerful tools for building next-generation intelligent Windows applications that leverage the full capabilities of modern AI-optimized hardware.

## Related Concepts

### Prerequisites

- [[windows_ai_stack_explained]] - Need to understand where Copilot Runtime fits in the AI stack
- [[dotnet]] - .NET knowledge required for Copilot Runtime APIs

### Related Topics

- [[windows_ml]] - Copilot Runtime sits above Windows ML layer
- [[windows_app_sdk_setup]] - Accessed through Windows App SDK
- [[onnx_runtime]] - Uses ONNX Runtime under the hood
- [[dotnet]] - Copilot Runtime provides .NET APIs
- [[windows_ai_stack_explained]] - Copilot Runtime sits above Windows ML for Copilot+ PCs
- [[foundry_local]] - Both provide local AI capabilities on Windows

### Extends

- [[windows_ai_stack_explained]] - Higher-level AI runtime layer in the stack

### Related Topics

- [[windows_app_sdk_ai]] - Windows App SDK provides access to Copilot Runtime AI capabilities
