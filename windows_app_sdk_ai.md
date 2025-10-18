---
tags: [windows, ai, api, sdk, reference, csharp]
---
# Windows App SDK AI Capabilities

The **Windows App SDK** provides on-device AI capabilities through the `Microsoft.Windows.AI.*` namespaces, enabling developers to integrate local language models, computer vision, and content safety features into Windows desktop applications without cloud dependencies.

## Overview

Windows App SDK AI features are part of **Windows AI Foundry** (formerly Windows Copilot Runtime) and provide hardware-accelerated AI inference using Neural Processing Units (NPUs) on Copilot+ PCs. All processing happens locally on-device using pre-installed "inbox" models.

**Current Status (2025)**:

- Available in **Windows App SDK 1.7+ experimental channel**
- Requires **Copilot+ PC with NPU** for most features
- Requires **Windows 11 Insider Preview (Dev channel)** for model downloads
- **Cannot be published to Microsoft Store** (experimental features limitation)

## Core Namespaces

### Microsoft.Windows.AI

Base namespace providing AI feature readiness checking:

```csharp
using Microsoft.Windows.AI;

// Check if AI models are available
var result = await AIFeatureReadyResult.CheckReadyStateAsync();

if (result.State == AIFeatureReadyState.Ready)
{
    // AI features available
}
else if (result.State == AIFeatureReadyState.NotReady)
{
    // Model needs downloading
    await EnsureModelsReady();
}
```

**Key Types**:

- `AIFeatureReadyResult` - Check if AI models are available
- `AIFeatureReadyState` - Enum for AI feature states (Ready, NotReady, Unavailable)
- `AIFeatureReadyResultState` - Result state enum

### Microsoft.Windows.AI.Text

Language model capabilities powered by **Phi Silica** (Microsoft's NPU-optimized small language model):

```csharp
using Microsoft.Windows.AI.Text;

// Ensure model is ready
if (LanguageModel.GetReadyState() != AIFeatureReadyState.Ready)
{
    await LanguageModel.EnsureReadyAsync();
}

// Create language model instance
using var languageModel = await LanguageModel.CreateAsync();

// Generate response
var result = await languageModel.GenerateResponseAsync(
    "What is the molecular formula for glucose?"
);
Console.WriteLine(result.Text); // C6H12O6
```

**Key APIs**:

- `LanguageModel` - Main class for local language model inference
  - `CreateAsync()` - Create language model instance
  - `GenerateResponseAsync()` - Generate text responses from prompts
  - `CreateContext()` - Create conversation contexts
  - `GenerateEmbeddingVectors()` - Generate vector embeddings
  - `EnsureReadyAsync()` - Download/install model if needed
- `LanguageModelOptions` - Configuration options
- `LanguageModelContext` - Conversation context management
- `InputKind` - Enum for input types
- `LanguageModelResponseStatus` - Response status enum

**Conversation Context**:

```csharp
// Create context for multi-turn conversations
var context = languageModel.CreateContext();

// Add conversation history
context.AddSystemMessage("You are a helpful coding assistant.");
context.AddUserMessage("How do I create a list in Python?");

var response = await languageModel.GenerateResponseAsync(context);
```

### Microsoft.Windows.AI.Imaging

Computer vision and image processing capabilities:

**Image Super-Resolution**:

```csharp
using Microsoft.Windows.AI.Imaging;

var imageScaler = new ImageScaler();

// Upscale and sharpen image
SoftwareBitmap outputBitmap = await imageScaler.ScaleSoftwareBitmap(
    inputBitmap,
    targetWidth: 3840,
    targetHeight: 2160
);
```

**Optical Character Recognition (OCR)**:

```csharp
var textRecognizer = new TextRecognizer();

// Extract text from image
var recognizedText = await textRecognizer.RecognizeTextFromImageAsync(inputImage);

foreach (var line in recognizedText.Lines)
{
    Console.WriteLine(line.Text);
    foreach (var word in line.Words)
    {
        Console.WriteLine($"  {word.Text} at {word.BoundingBox}");
    }
}
```

**Key APIs**:

- `ImageScaler` - Image super-resolution (upscaling/sharpening)
  - `ScaleSoftwareBitmap()` - Scale bitmap images
  - `ScaleImageBuffer()` - Scale image buffers
- `TextRecognizer` - Optical Character Recognition
  - `RecognizeTextFromImage()` - Extract text from images
  - `RecognizeTextFromImageAsync()` - Async text recognition
- `ImageDescriptionGenerator` - Generate natural language descriptions of images
- `ImageObjectExtractor` - Segment objects within images
- `ImageObjectRemover` - Remove objects from images (Object Erase feature)
- `RecognizedText`, `RecognizedLine`, `RecognizedWord` - OCR result classes

### Microsoft.Windows.AI.ContentSafety

Content moderation for responsible AI applications:

```csharp
using Microsoft.Windows.AI.ContentSafety;

var filterOptions = new ContentFilterOptions
{
    ViolentContentSeverity = SeverityLevel.Medium,
    HateSpeechSeverity = SeverityLevel.High,
    SelfHarmSeverity = SeverityLevel.High,
    SexualContentSeverity = SeverityLevel.Medium
};

// Apply filters to language model
var safeModel = await LanguageModel.CreateAsync(filterOptions);
```

**Key APIs**:

- `ContentFilterOptions` - Configure content safety filters
- `SeverityLevel` - Enum for filter severity (Minimum, Low, Medium, High)
- **Filter categories**: Violent, Hate, SelfHarm, Sexual content

## Hardware and Platform Requirements

### Copilot+ PC Requirement

All Windows App SDK AI APIs require hardware with NPU (Neural Processing Unit):

**Supported Hardware**:

- Snapdragon X Elite (Qualcomm)
- Intel Lunar Lake
- AMD Zen 5-based processors

**Why NPU Required**:

- Phi Silica and vision models are optimized for NPU execution
- NPU provides power-efficient inference compared to CPU/GPU
- Enables real-time AI features without battery drain

### Software Requirements

- **Windows 11 Insider Preview (Dev channel)** - Required for model downloads
- **Windows App SDK 1.7+** (experimental channel)
- **.NET 8 or later** for C# development
- **Visual Studio 2022** with Windows App SDK extension

### Application Manifest Configuration

Apps need `systemAIModels` capability:

```xml
<Package xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities">
  <Capabilities>
    <rescap:Capability Name="systemAIModels"/>
  </Capabilities>
</Package>
```

### Limited Access Feature Token

**Phi Silica** requires a **Limited Access Feature (LAF) token** for production use. During development/preview, this requirement may be waived, but production applications must obtain approval from Microsoft.

## Phi Silica Language Model

**Phi Silica** is Microsoft's NPU-optimized small language model (SLM) designed for on-device inference:

**Characteristics**:

- **Optimized for NPU** - Runs efficiently on Copilot+ PC neural processors
- **Inbox model** - Pre-installed on supported devices, no download needed
- **Offline-capable** - No cloud connection required for inference
- **Small footprint** - Optimized for local execution with low memory usage
- **Task-focused** - Best for factual queries, summarization, code assistance

**Use Cases**:

- Local code completion and suggestions
- Offline summarization of documents
- Factual question answering without latency
- Privacy-sensitive applications (data never leaves device)
- Quick local classification and extraction tasks

**Limitations**:

- Smaller context window than cloud models
- Less capable than GPT-4 class models for complex reasoning
- No access to real-time information (knowledge cutoff built into model)

## Installation and Setup

### Install Experimental Windows App SDK

```powershell
# Via NuGet Package Manager
Install-Package Microsoft.WindowsAppSDK -Version 1.8.0-experimental1 -IncludePrerelease

# Or via .NET CLI
dotnet add package Microsoft.WindowsAppSDK --version 1.8.0-experimental1
```

### Enable Experimental Features

In Visual Studio:

1. Tools → Options → Environment → Preview Features
2. Enable "Windows App SDK Experimental Features"
3. Restart Visual Studio

### Verify Model Availability

```csharp
// Check if device supports AI features
var textModelReady = await LanguageModel.GetReadyStateAsync();
var imagingReady = await ImageScaler.GetReadyStateAsync();

if (textModelReady == AIFeatureReadyState.Unavailable)
{
    // Device does not have required NPU hardware
    ShowUnsupportedHardwareMessage();
}
else if (textModelReady == AIFeatureReadyState.NotReady)
{
    // Model needs downloading (Windows Insider Preview required)
    await LanguageModel.EnsureReadyAsync();
}
```

## Common Patterns

### Local Text Summarization

```csharp
using var model = await LanguageModel.CreateAsync();

string document = LoadLongDocument();
var prompt = $"Summarize the following text in 3 bullet points:\n\n{document}";

var response = await model.GenerateResponseAsync(prompt);
DisplaySummary(response.Text);
```

### Image Text Extraction (OCR) Pipeline

```csharp
var recognizer = new TextRecognizer();
var bitmap = await LoadImageAsync("document.jpg");

var result = await recognizer.RecognizeTextFromImageAsync(bitmap);

// Extract all text in reading order
var fullText = string.Join("\n", result.Lines.Select(l => l.Text));

// Or process structured data (tables, forms)
foreach (var line in result.Lines)
{
    if (IsTableRow(line))
    {
        ProcessTableRow(line.Words);
    }
}
```

### Content Safety Filtering

```csharp
var filterOptions = new ContentFilterOptions
{
    ViolentContentSeverity = SeverityLevel.High,
    HateSpeechSeverity = SeverityLevel.High,
    SelfHarmSeverity = SeverityLevel.High,
    SexualContentSeverity = SeverityLevel.Medium
};

using var safeModel = await LanguageModel.CreateAsync(filterOptions);

var userInput = GetUserInput();
var response = await safeModel.GenerateResponseAsync(userInput);

// Response is automatically filtered based on configured severity levels
```

## Limitations and Constraints

### Experimental Status

- **No Microsoft Store publishing** - Experimental features cannot be distributed via Store
- **API stability not guaranteed** - APIs may change in future releases
- **Limited documentation** - Experimental features have sparse official docs

### Hardware Dependency

- **NPU required** - Most features unavailable on devices without NPU
- **Device compatibility** - Not all Copilot+ PCs may support all features
- **Performance varies** - NPU implementation differs across hardware vendors

### Model Constraints

- **Offline models only** - No cloud model fallback
- **Fixed model versions** - Cannot upgrade models without OS updates
- **Limited model selection** - Only Phi Silica for language tasks
- **Context window limits** - Smaller than cloud-based LLMs

### Production Deployment

- **LAF token required** - Phi Silica requires Limited Access Feature approval
- **Device targeting** - Must detect NPU availability and gracefully degrade
- **Update dependencies** - Model updates tied to Windows Update schedule

## Comparison: Windows App SDK AI vs. Other Microsoft AI SDKs

### vs. Microsoft 365 Agents SDK

| **Feature** | **Windows App SDK AI** | **Microsoft 365 Agents SDK** |
|-------------|------------------------|------------------------------|
| **Namespace** | `Microsoft.Windows.AI.*` | `Microsoft.Agents.*` |
| **Purpose** | On-device AI for Windows apps | Enterprise agents for M365/Teams |
| **Platform** | Windows 11 (Copilot+ PC) | Cross-platform (.NET, JavaScript) |
| **Execution** | Local NPU | Cloud or hybrid |
| **Models** | Phi Silica (inbox) | Azure OpenAI, custom models |
| **Use Case** | Desktop app AI features | Conversational agents, workflows |

### vs. Microsoft Agent Framework

| **Feature** | **Windows App SDK AI** | **Microsoft Agent Framework** |
|-------------|------------------------|-------------------------------|
| **Purpose** | On-device inference APIs | Multi-agent orchestration |
| **Installation** | Windows App SDK experimental | `Microsoft.Agents.AI` NuGet |
| **Orchestration** | Single model, local | Multi-agent, distributed |
| **Deployment** | Windows desktop apps | Azure AI Foundry, cross-platform |

**Use Windows App SDK AI when**:

- Building Windows-native desktop applications
- Need offline/local inference (privacy, latency)
- Have hardware with NPU support
- Want "inbox" models without cloud dependencies

**Use Microsoft 365 Agents SDK or Agent Framework when**:

- Building enterprise conversational agents
- Need multi-agent orchestration
- Require cloud model access (GPT-4, etc.)
- Targeting M365, Teams, or cross-platform deployment

## Relationship to Windows Copilot Runtime

**Windows App SDK AI** is part of the broader **Windows Copilot Runtime** (also called Windows AI Foundry):

- **Windows Copilot Runtime** - Overall platform for AI on Windows
  - Includes: Phi Silica, OCR Enhancements, Windows Studio Effects, Recall
  - Broader than just developer APIs
- **Windows App SDK AI** - Developer-facing APIs (`Microsoft.Windows.AI.*`)
  - Subset of Copilot Runtime exposed to app developers
  - Focused on programmatic access to on-device models

## Related Concepts

### Prerequisites

- [[windows_app_sdk_setup]] - How to install and configure Windows App SDK
- [[copilot_runtime]] - Broader Windows Copilot Runtime platform context

### Related Topics

- [[windows_ai_stack_explained]] - Overall Windows AI ecosystem architecture
- [[windows_ml]] - Windows ML API for ONNX model inference
- [[agentic_production_studio]] - Desktop application architecture that could leverage these APIs

### Extends

- [[windows_ai_stack_explained]] - Specific implementation of Windows AI platform capabilities

### Alternatives

- **Azure OpenAI Service** - Cloud-based LLM access (GPT-4, etc.)
- **ONNX Runtime** - Cross-platform ML inference for custom models
- **DirectML** - Low-level GPU-accelerated ML primitives
- **Windows ML** - ONNX model inference with automatic execution provider selection

## References

Based on research document "Windows App SDK AI Namespaces" compiled from Microsoft official documentation, October 2025.

[1] <https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai>
[2] <https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.text>
[3] <https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica>
[4] <https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.imaging>
[5] <https://learn.microsoft.com/en-us/windows/ai/apis/content-moderation>
[6] <https://learn.microsoft.com/en-us/windows/ai/apis/get-started>
[7] <https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/>
