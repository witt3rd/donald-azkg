<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## Windows App SDK AI Namespaces

Yes, there are **Microsoft.*** namespaces specifically for AI in the Windows App SDK, but **no**, there is no `Microsoft.AI.*` or `Microsoft.Agents.*` namespace in the Windows App SDK itself. Let me clarify the different SDK contexts:

### **Windows App SDK AI Namespaces** (for Windows Desktop Apps)

The Windows App SDK provides **on-device AI capabilities** through several `Microsoft.Windows.AI.*` namespaces, available in the **experimental channel** (version 1.7+):[^1][^2]

#### **Microsoft.Windows.AI**[^1]

The base namespace providing core AI feature readiness checking:

- `AIFeatureReadyResult` - Check if AI models are available
- `AIFeatureReadyState` - Enum for AI feature states
- `AIFeatureReadyResultState` - Result state enum


#### **Microsoft.Windows.AI.Text**[^3][^4]

Language model capabilities (Phi Silica):

- `LanguageModel` - Main class for local language model inference[^5][^4]
    - `CreateAsync()` - Create language model instance
    - `GenerateResponseAsync()` - Generate text responses from prompts[^6][^5]
    - `CreateContext()` - Create conversation contexts
    - `GenerateEmbeddingVectors()` - Generate embeddings
    - `EnsureReadyAsync()` - Download/install model if needed
- `LanguageModelOptions` - Configuration options
- `LanguageModelContext` - Conversation context management
- `InputKind` - Enum for input types
- `LanguageModelResponseStatus` - Response status enum


#### **Microsoft.Windows.AI.Imaging**[^7][^8][^9]

Vision and image processing capabilities:

- `ImageScaler` - Image super-resolution (upscaling/sharpening)[^10][^7]
    - `ScaleSoftwareBitmap()` - Scale bitmap images
    - `ScaleImageBuffer()` - Scale image buffers
- `TextRecognizer` - Optical Character Recognition (OCR)[^8][^11]
    - `RecognizeTextFromImage()` - Extract text from images
    - `RecognizeTextFromImageAsync()` - Async text recognition
- `ImageDescriptionGenerator` - Generate natural language descriptions of images[^9][^10]
- `ImageObjectExtractor` - Segment objects within images[^9]
- `ImageObjectRemover` - Remove objects from images (Object Erase)[^10][^9]
- `RecognizedText`, `RecognizedLine`, `RecognizedWord` - OCR result classes[^9]


#### **Microsoft.Windows.AI.ContentSafety** (also called ContentModeration)[^2][^12][^13]

Content moderation for responsible AI:

- `ContentFilterOptions` - Configure content safety filters[^12]
- `SeverityLevel` - Enum for filter severity (Minimum, Low, Medium, High)[^13]
- Categories for filtering: Violent, Hate, SelfHarm, Sexual content[^12]

These APIs are part of **Windows AI Foundry** (formerly Windows Copilot Runtime), which provides:[^14][^15][^16]

- **Phi Silica** - Microsoft's NPU-optimized small language model for on-device inference[^17][^18][^5]
- **Hardware acceleration** via NPU on Copilot+ PCs[^15][^14][^5]
- **Inbox models** - Pre-installed on supported devices[^16][^14]
- **No cloud dependency** - All inference runs locally[^15][^5]

**Important Requirements**:[^19][^20][^6][^5]

- Available only in **Windows App SDK 1.7+ experimental channel**[^21][^1]
- Requires **Copilot+ PC** with NPU for most features[^14][^5][^15]
- Requires **Windows 11 Insider Preview (Dev channel)** for model downloads[^22][^19]
- Apps need `systemAIModels` capability in manifest[^6]
- **Cannot be published to Microsoft Store** (experimental features)[^20][^1]
- Phi Silica requires **Limited Access Feature (LAF) token** for production[^23][^5][^20]


### **Microsoft 365 Agents SDK** (Different SDK - for Enterprise Agents)

This is a **completely separate SDK** from Windows App SDK, designed for building conversational agents that deploy to Microsoft 365, Teams, Copilot, etc.:[^24][^25][^26]

#### **Microsoft.Agents.*** namespaces**[^27][^28][^29][^24]

- `Microsoft.Agents.Builder` - Agent hosting and channel adapters[^24]
    - `IAgent`, `AgentExtension`, `TurnContext`
    - `IChannelAdapter` for connecting to services
- `Microsoft.Agents.AI` - Core agent abstractions[^27]
    - `AIAgent` - Base class for all AI agents
    - `ChatClientAgent` - Agent using `IChatClient`
    - `AgentThread`, `AgentRunResponse`
    - Works with **Microsoft.Extensions.AI**[^26]
- `Microsoft.Agents.Client` - Agent-to-agent communication[^29]
- `Microsoft.Agents.Core.Models` - Activity protocol models[^28]

This SDK is for building agents that integrate with:

- Microsoft 365 Copilot[^25][^30][^31]
- Microsoft Teams[^32][^25]
- Copilot Studio[^25][^32]
- Web chat and custom channels[^32][^25]


### **Microsoft Agent Framework** (Multi-Agent Orchestration)

Announced October 2025, this is **yet another SDK** that unifies Semantic Kernel and AutoGen for multi-agent systems:[^33][^34][^26]

**Namespaces**: Same as Microsoft 365 Agents SDK (`Microsoft.Agents.*`)[^26][^27]

**Key features**:[^34][^33][^26]

- Multi-agent orchestration patterns (sequential, concurrent, group chat, handoff, Magentic-One)
- MCP (Model Context Protocol) support
- A2A (Agent2Agent) protocol support
- Deploy to Azure AI Foundry[^33][^34]

**Installation**:

```bash
dotnet add package Microsoft.Agents.AI --prerelease
```


### Summary Table

| **Feature** | **Windows App SDK AI** | **Microsoft 365 Agents SDK** | **Microsoft Agent Framework** |
| :-- | :-- | :-- | :-- |
| **Namespace** | `Microsoft.Windows.AI.*` | `Microsoft.Agents.*` | `Microsoft.Agents.*` |
| **Purpose** | On-device AI for Windows apps | Enterprise agents for M365/Teams | Multi-agent orchestration |
| **Key APIs** | LanguageModel, ImageScaler, TextRecognizer | IAgent, ChatClientAgent, TurnContext | AIAgent, orchestration patterns |
| **Platform** | Windows 11 (Copilot+ PC) | Cross-platform (.NET, JavaScript) | Cross-platform (.NET, Python) |
| **Installation** | Windows App SDK experimental | NuGet: Microsoft.Agents.* | NuGet: Microsoft.Agents.AI |
| **Hardware** | NPU-accelerated (local) | Cloud or hybrid | Cloud or hybrid |

**For your AI/agentic work on Windows**:[^33][^26][^6]

- Use **`Microsoft.Windows.AI.*`** for local, on-device inference with Phi Silica and vision models
- Use **`Microsoft.Agents.*`** for building enterprise agents that integrate with M365/Teams/Copilot
- Use **Microsoft Agent Framework** for complex multi-agent orchestration and workflows
<span style="display:none">[^35][^36][^37][^38][^39][^40][^41][^42][^43][^44][^45][^46][^47][^48][^49][^50][^51][^52][^53][^54][^55][^56][^57][^58][^59][^60][^61][^62][^63][^64][^65][^66][^67][^68][^69][^70][^71][^72][^73][^74][^75][^76]</span>

<div align="center">⁂</div>

[^1]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai?view=windows-app-sdk-1.8

[^2]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/

[^3]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.text?view=windows-app-sdk-1.8

[^4]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.text.languagemodel?view=windows-app-sdk-1.8

[^5]: https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica

[^6]: https://learn.microsoft.com/en-us/windows/ai/apis/get-started

[^7]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.imaging.imagescaler?view=windows-app-sdk-1.8

[^8]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.imaging.textrecognizer?view=windows-app-sdk-1.7

[^9]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.imaging?view=windows-app-sdk-1.8

[^10]: https://learn.microsoft.com/en-us/windows/ai/apis/imaging

[^11]: https://learn.microsoft.com/en-us/windows/ai/apis/text-recognition

[^12]: https://learn.microsoft.com/en-us/windows/ai/apis/content-moderation

[^13]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.contentsafety.severitylevel?view=windows-app-sdk-1.7

[^14]: https://www.youtube.com/watch?v=Ob_63Fv1cLI

[^15]: https://blog.revolution.com.br/2025/05/04/adding-ai-in-your-apps-with-the-windows-copilot-runtime-apis/

[^16]: https://blogs.windows.com/windowsdeveloper/2025/05/19/advancing-windows-for-ai-development-new-platform-capabilities-and-tools-introduced-at-build-2025/

[^17]: https://windowsforum.com/threads/microsofts-phi-silica-on-device-ai-power-for-windows-11-devices.371218/

[^18]: https://blogs.windows.com/windowsexperience/2024/12/06/phi-silica-small-but-mighty-on-device-slm/

[^19]: https://github.com/microsoft/WindowsAppSDK/discussions/5116

[^20]: https://learn.microsoft.com/en-us/windows/ai/apis/troubleshooting

[^21]: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/experimental-channel

[^22]: https://www.thurrott.com/dev/317041/hands-on-coding-to-the-windows-copilot-runtime

[^23]: https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica-tutorial

[^24]: https://learn.microsoft.com/en-us/dotnet/api/microsoft.agents.builder?view=m365-agents-sdk

[^25]: https://github.com/microsoft/Agents

[^26]: https://devblogs.microsoft.com/dotnet/introducing-microsoft-agent-framework-preview/

[^27]: https://learn.microsoft.com/en-us/dotnet/api/microsoft.agents.ai

[^28]: https://learn.microsoft.com/en-us/dotnet/api/microsoft.agents.core.models?view=m365-agents-sdk

[^29]: https://learn.microsoft.com/en-us/dotnet/api/microsoft.agents.client?view=m365-agents-sdk

[^30]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-integrate-web-or-native-app-m365-agents-sdk

[^31]: https://devblogs.microsoft.com/microsoft365dev/microsoft-365-copilot-apis/

[^32]: https://learn.microsoft.com/en-us/javascript/api/overview/agents-overview?view=agents-sdk-js-latest

[^33]: https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/

[^34]: https://azure.microsoft.com/en-us/blog/introducing-microsoft-agent-framework/

[^35]: https://learn.microsoft.com/en-us/uwp/api/

[^36]: https://learn.microsoft.com/en-us/uwp/

[^37]: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/

[^38]: https://github.com/microsoft/WindowsAppSDK/issues/4902

[^39]: https://www.thomasclaudiushuber.com/2025/05/03/use-windows-ai-in-wpf/

[^40]: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/

[^41]: https://www.youtube.com/watch?v=BgCK6E8Qt-4

[^42]: https://cloudwars.com/ai/microsoft-agent-framework-taps-open-source-standards-to-tie-in-third-party-agents-systems/

[^43]: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/release-notes-archive/experimental-channel-1.7

[^44]: https://learn.microsoft.com/en-us/agent-framework/tutorials/quick-start

[^45]: https://learn.microsoft.com/en-us/windows/ai/apis/

[^46]: https://www.voitanos.io/blog/microsoft-teams-sdk-evolution-2025/

[^47]: https://www.gocodeo.com/post/key-takeaways-from-microsoft-build-2025

[^48]: https://learn.microsoft.com/en-us/dotnet/ai/conceptual/how-genai-and-llms-work

[^49]: https://learn.microsoft.com/en-us/windows/ai/apis/imaging-api-ref

[^50]: https://learn.microsoft.com/en-us/windows/ai/models/get-started-models-genai

[^51]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.vision?view=windows-app-sdk-1.8

[^52]: https://learn.microsoft.com/pt-br/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.imaging.imagescaler?view=windows-app-sdk-1.8

[^53]: https://learn.microsoft.com/en-us/windows/ai/apis/text-recognition-tutorial

[^54]: https://learn.microsoft.com/en-us/windows/ai/apis/imaging-tutorial

[^55]: https://learn.microsoft.com/es-es/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.imaging.textrecognizer?view=windows-app-sdk-1.7

[^56]: https://learn.microsoft.com/en-us/shows/generative-ai-for-beginners/introduction-to-generative-ai-and-llms-generative-ai-for-beginners

[^57]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.imaging.imagescaler.scalesoftwarebitmap?view=windows-app-sdk-1.8

[^58]: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

[^59]: https://learn.microsoft.com/en-us/dotnet/api/microsoft.teams.ai.ai.moderator?view=msteams-client-dotnet-latest

[^60]: https://learn.microsoft.com/en-us/dotnet/api/azure.ai.agents.persistent?view=azure-dotnet

[^61]: https://www.youtube.com/watch?v=KDxi3NG3nfU

[^62]: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-text

[^63]: https://github.com/microsoft/agent-framework

[^64]: https://learn.microsoft.com/en-us/rest/api/notificationhubs/namespaces/list-all?view=rest-notificationhubs-2023-09-01

[^65]: https://devblogs.microsoft.com/foundry/building-ai-agents-a2a-dotnet-sdk/

[^66]: https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.windows.ai.contentsafety?view=windows-app-sdk-1.8

[^67]: https://learn.microsoft.com/en-us/dotnet/api/microsoft.xrm.sdk?view=dataverse-sdk-latest

[^68]: https://www.youtube.com/watch?v=d3nMVvZQcnE

[^69]: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/release-notes-archive/experimental-channel-1-8

[^70]: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/

[^71]: https://learn.microsoft.com/pt-pt/windows/windows-app-sdk/api/winrt/microsoft.windows.ai?view=windows-app-sdk-1.8

[^72]: https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/

[^73]: https://github.com/microsoft/windowsappsdk/releases?USOzY=t81XGFWO

[^74]: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads

[^75]: https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview

[^76]: https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/bf-migration-dotnet

