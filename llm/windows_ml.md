# The Relationship Between Windows ML and DirectML

**Windows ML is an evolution of DirectML** that represents Microsoft's next-generation machine learning platform for Windows, designed to simplify AI deployment while maintaining high performance across diverse hardware configurations.[1][2]

## DirectML: The Foundation Layer

DirectML is a **low-level hardware abstraction API** that enables machine learning workloads on any DirectX 12-compatible GPU. It operates as a DirectX 12 library with a native C++ programming interface, providing developers with fine-grained control over machine learning operations. Key characteristics of DirectML include:[3][4]

- **Hardware abstraction**: Works across AMD, Intel, NVIDIA, and Qualcomm GPUs through a unified DirectX 12 interface[5]
- **Cross-vendor compatibility**: Ensures consistent results regardless of hardware vendor[6]
- **Low-level control**: Suitable for performance-critical, real-time applications like games and frameworks[3]
- **ONNX Runtime integration**: Functions as an execution provider within the ONNX Runtime ecosystem[7]

## Windows ML: The Evolution

**Windows ML represents a significant evolution from DirectML**, launched in May 2025 as part of the Windows AI Foundry platform. This transformation was driven by extensive developer feedback and lessons learned from DirectML's deployment over the past year.[2][1]

### Key Improvements Over DirectML

**Simplified Development Experience**: While DirectML required deep technical expertise in DirectX 12 programming, Windows ML provides a **unified runtime with automatic execution provider management**. Developers no longer need to manually configure hardware-specific optimizations.[8]

**Broader Framework Support**: Windows ML is built around the **ONNX Runtime Engine**, enabling developers to use familiar ORT APIs while gaining access to Windows-specific optimizations. This provides compatibility with models from PyTorch, TensorFlow, Keras, TFLite, and scikit-learn.[1][8]

**Enhanced Performance Architecture**: The new Windows ML **works directly with dedicated execution providers** for GPUs and NPUs, delivering performance comparable to specialized SDKs like TensorRT for RTX and AI Engine Direct. This represents a significant improvement over the previous DirectML-based approach.[8]

## Technical Relationship and Architecture

### Execution Provider Framework

DirectML continues to exist as an **execution provider within the ONNX Runtime ecosystem**, while Windows ML serves as the orchestrating layer that manages these providers automatically. The architecture works as follows:[7][8]

- **Windows ML**: High-level runtime that automatically selects optimal execution providers
- **DirectML EP**: One of several execution providers available through Windows ML
- **Hardware abstraction**: Both layers work together to provide cross-hardware compatibility

### Shared System Runtime

Windows ML provides a **shared, system-wide ONNX Runtime** rather than requiring applications to bundle their own copies. This reduces application size and ensures consistent performance optimizations across all Windows applications using AI capabilities.[8]

### Dynamic Provider Management

A crucial advancement in Windows ML is its ability to **dynamically download and manage execution providers**. This means applications can access the latest hardware-specific optimizations without requiring updates to the core application code.[8]

## Migration Path and Current Status

### From DirectML to Windows ML

The relationship between DirectML and Windows ML reflects an **evolutionary rather than replacement approach**. DirectML remains available for developers who need low-level control, while Windows ML provides a higher-level abstraction for most use cases.[1]

**DirectML continues to serve**: Applications requiring maximum performance control, custom machine learning frameworks, and real-time scenarios where every millisecond matters.[3]

**Windows ML targets**: Application developers seeking simplified deployment, automatic hardware optimization, and integration with the broader Windows AI ecosystem.[8]

### Industry Context

Recent developments indicate some uncertainty in the DirectML ecosystem, with discussions about potential deprecation in favor of vendor-specific solutions. However, Windows ML's architecture ensures that DirectML's cross-hardware capabilities remain accessible through the execution provider framework.[9][8]

## Integration with Windows AI Ecosystem

Windows ML serves as the **foundation for the broader Windows AI platform**, including:[8]

- **Windows AI APIs**: Built-in models for common tasks
- **Foundry Local**: Ready-to-use AI models from various catalogs
- **Custom model support**: Direct API access for advanced scenarios

This comprehensive approach positions Windows ML as Microsoft's strategic platform for AI development on Windows, building upon DirectML's proven hardware abstraction capabilities while dramatically simplifying the developer experience.

The relationship between Windows ML and DirectML exemplifies Microsoft's commitment to maintaining backward compatibility while advancing the state of AI development tools. DirectML's robust foundation enables Windows ML's simplified interface, creating a platform that serves both performance-critical applications and mainstream development scenarios.

## Two Approaches to Windows ML

### Important Distinction

There are **two different Windows ML API sets** that can cause confusion:

#### 1. Legacy Windows ML APIs (Ships with Windows - 2018)
⚠️ **Note**: These are the **original Windows ML APIs from 2018** that ship with Windows. While still functional and convenient for simple scenarios, Microsoft now recommends using the newer Windows App SDK version for new development.

- **Status**: Legacy/superseded (but still works)
- **Released**: 2018 with Windows 10 version 1809
- **No installation required** - Part of Windows 10/11
- **Namespace**: `Windows::AI::MachineLearning` (no "Microsoft" prefix)
- **Link library**: `windowsapp.lib`
- **Headers**: `winrt/Windows.AI.MachineLearning.h`
- **Main APIs**: `LearningModel`, `LearningModelSession`, `TensorFloat`
- **Device selection**: `LearningModelDevice` with predefined kinds (CPU, DirectX, DirectXHighPerformance)
- **Use case**: Simple ML inference, quick prototyping, tensor operations, zero-dependency scenarios
- **Example**:
```cpp
#include <winrt/Windows.AI.MachineLearning.h>
using namespace Windows::AI::MachineLearning;

LearningModelDevice device(LearningModelDeviceKind::DirectXHighPerformance);
auto tensor = TensorFloat::CreateFromArray(shape, data);
```

#### 2. Current Windows ML APIs via Windows App SDK (2025)
✅ **Note**: These are the **current, recommended Windows ML APIs** that supersede the 2018 version. Part of the Windows AI Foundry platform launched in May 2025.

- **Status**: Current/recommended
- **Released**: 2025 with Windows App SDK
- **Requires NuGet package**: `Microsoft.WindowsAppSDK.ML`
- **Namespace**: `Microsoft.Windows.AI.MachineLearning` (note "Microsoft" prefix)
- **Part of**: Windows App SDK and Windows AI Foundry
- **Main APIs**: `ExecutionProviderCatalog`, `ExecutionProvider`
- **Integration**: Direct ONNX Runtime C API access
- **Use case**: Production applications, advanced provider management, latest optimizations
- **Example**:
```cpp
#include <winrt/Microsoft.Windows.AI.MachineLearning.h>
using namespace Microsoft::Windows::AI::MachineLearning;

auto catalog = ExecutionProviderCatalog::GetDefault();
catalog.EnsureAndRegisterAllAsync().get();
```

### Key Differences Table

| Aspect | Legacy APIs (2018) | Current APIs (2025) |
|--------|-------------------|---------------------|
| **Status** | Superseded but functional | Current/recommended |
| **Installation** | None - ships with Windows | Requires NuGet package |
| **Availability** | Windows 10 1809+ | Windows App SDK |
| **Namespace** | `Windows::AI::MachineLearning` | `Microsoft.Windows.AI.MachineLearning` |
| **Documentation** | Limited/archived | Actively maintained |
| **Complexity** | Simple, high-level | More features, more control |
| **Provider Control** | Automatic (DirectML) | Manual provider selection |
| **ONNX Runtime** | Indirect access | Direct C API access |
| **Deployment** | Zero dependencies | Framework-dependent |
| **GPU Acceleration** | Automatic via DirectML | Multiple providers available |
| **Future Support** | Maintenance mode | Active development |

### Why Both Still Exist

The legacy APIs continue to work because:
1. **Backward compatibility** - Existing applications rely on them
2. **Zero dependencies** - Useful for lightweight scenarios
3. **Simplicity** - Lower barrier to entry for basic ML tasks
4. **Built-in availability** - No package management required

However, for new development, Microsoft recommends using the Windows App SDK version for access to the latest features and optimizations.

## Windows ML C++ APIs (NuGet Package)

### Overview

The new Windows ML runtime (via NuGet) provides comprehensive C++ APIs for machine learning and AI operations in Windows applications. These APIs are available through two main components:

1. **Windows ML APIs**: Windows Runtime APIs in the `Microsoft.Windows.AI.MachineLearning` namespace, including the ExecutionProviderCatalog class
2. **ONNX Runtime APIs**: Windows ML implementations of certain ONNX Runtime APIs through the Microsoft.WindowsAppSDK.ML NuGet package

### The Microsoft.WindowsAppSDK.ML NuGet Package

The Microsoft.WindowsAppSDK.ML NuGet package provides Windows ML runtime .winmd files for use in both C# and C++ projects. This package is the foundation for accessing hardware-optimized machine learning acceleration through the Windows ML runtime.

#### Framework-Dependent Deployment

Windows ML is delivered as a framework-dependent component. Applications must either:
- Reference the main Windows App SDK NuGet package by adding `Microsoft.WindowsAppSDK` (recommended)
- Or reference both `Microsoft.WindowsAppSDK.ML` and `Microsoft.WindowsAppSDK.Runtime`

### ExecutionProviderCatalog Class

The ExecutionProviderCatalog class is the entry point for accessing hardware-optimized machine learning acceleration. It provides methods to discover, acquire, and register AI execution providers (EPs) for use with the ONNX Runtime, handling the complexity of package management and hardware selection.

#### Basic Usage

```cpp
// Get the default catalog
winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog catalog = 
    winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog::GetDefault();

// Ensure and register all compatible execution providers
catalog.EnsureAndRegisterAllAsync().get();

// Use ONNX Runtime C API directly for inference
```

#### Key Methods

##### GetDefault Method
Returns the default ExecutionProviderCatalog instance that provides access to all execution providers on the system.

```cpp
auto catalog = winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog::GetDefault();
```

##### FindAllProviders Method
Returns a collection of all execution providers compatible with the current hardware.

```cpp
auto catalog = winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog::GetDefault();
auto providers = catalog.FindAllProviders();

for (const auto& provider : providers)
{
    std::wcout << L"Found provider: " << provider.Name().c_str() 
              << L", Type: " << static_cast<int>(provider.DeviceType()) << L"\n";
}
```

##### EnsureAndRegisterAllAsync Method
Ensures all compatible execution providers are ready and registers them with ONNX Runtime. This method may trigger downloads of required components.

```cpp
auto catalog = winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog::GetDefault();

try 
{
    // This will ensure providers are ready and register them with ONNX Runtime
    catalog.EnsureAndRegisterAllAsync().get();
    std::wcout << L"All execution providers are ready and registered\n";
}
catch (const winrt::hresult_error& ex) 
{
    std::wcout << L"Failed to prepare execution providers: " << ex.message().c_str() << L"\n";
}
```

##### RegisterAllAsync Method
Registers all compatible execution providers with ONNX Runtime without ensuring they are ready. This only registers providers already present on the machine, avoiding potentially long download times.

```cpp
auto catalog = winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog::GetDefault();
catalog.RegisterAllAsync().get();
```

### ExecutionProvider Class

The ExecutionProvider class represents a specific hardware accelerator that can be used for machine learning inference.

#### Methods

##### EnsureReadyAsync Method
Ensures the execution provider is ready for use by downloading and installing any required components.

```cpp
auto catalog = winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog::GetDefault();
auto providers = catalog.FindAllProviders();

for (const auto& provider : providers)
{
    provider.EnsureReadyAsync().get();
    std::wcout << L"Provider " << provider.Name().c_str() << L" is ready\n";
}
```

##### TryRegister Method
Attempts to register the execution provider with ONNX Runtime and returns a boolean indicating success.

```cpp
auto catalog = winrt::Microsoft::Windows::AI::MachineLearning::ExecutionProviderCatalog::GetDefault();
auto providers = catalog.FindAllProviders();

for (const auto& provider : providers)
{
    provider.EnsureReadyAsync().get();
    bool registered = provider.TryRegister();
    std::wcout << L"Provider " << provider.Name().c_str() 
              << L" registration: " << (registered ? L"Success" : L"Failed") << L"\n";
}
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| Name | string | Gets the name of the execution provider |
| DeviceType | ExecutionProviderDeviceType | Gets the type of device (CPU, GPU, NPU, etc.) |
| IsReady | bool | Gets whether the execution provider is ready for use |
| LibraryPath | string | Gets the path to the execution provider library |

### Implementation Architecture

The Windows ML runtime integrates with the Windows App SDK and relies on its deployment and bootstrapping mechanisms:

- **Automatic Discovery**: Discovers execution providers compatible with current hardware
- **Package Management**: Manages package lifetime and updates
- **Registration Handling**: Handles package registration and activation
- **Version Support**: Supports different versions of execution providers

### Using ONNX Runtime with Windows ML

After registering execution providers through Windows ML, applications can use the ONNX Runtime directly:

#### C++ Applications
Use the ONNX Runtime C API directly to create sessions and run inference after provider registration.

```cpp
// Register providers first
catalog.EnsureAndRegisterAllAsync().get();

// Then use ONNX Runtime C API
Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "WindowsML");
Ort::SessionOptions session_options;
Ort::Session session(env, L"model.onnx", session_options);
```

#### C# Applications
Use the ONNX Runtime directly for inference using the `Microsoft.ML.OnnxRuntime` namespace.

#### Python Applications
Use the separate ONNX Runtime wheel (`onnxruntime`) for inference. For experimental release, use `onnxruntime-winml==1.22.0.post2` package.

### Best Practices for C++ Development

1. **Always Initialize First**: Ensure Windows App SDK is initialized before using Windows ML APIs
2. **Handle Async Operations**: Use `.get()` or proper async handling for all async methods
3. **Error Handling**: Wrap provider registration in try-catch blocks to handle potential failures
4. **Provider Selection**: Use `FindAllProviders()` to discover available hardware before registration
5. **Performance Optimization**: Use `RegisterAllAsync()` for faster startup when providers are already installed

### Integration with Legacy Windows ML

For applications using the legacy Windows ML APIs (LearningModel, LearningModelSession), the new ExecutionProviderCatalog can be used alongside:

```cpp
// New API: Register providers
auto catalog = ExecutionProviderCatalog::GetDefault();
catalog.EnsureAndRegisterAllAsync().get();

// Legacy API: Use LearningModel
LearningModel model = LearningModel::LoadFromFilePath(L"model.onnx");
LearningModelDevice device(LearningModelDeviceKind::DirectXHighPerformance);
LearningModelSession session(model, device);
```

This dual approach allows gradual migration from legacy to modern APIs while maintaining full functionality.

[1](https://blogs.windows.com/windowsdeveloper/2025/05/19/introducing-windows-ml-the-future-of-machine-learning-development-on-windows/)
[2](https://blogs.windows.com/windowsdeveloper/2025/05/19/advancing-windows-for-ai-development-new-platform-capabilities-and-tools-introduced-at-build-2025/)
[3](https://learn.microsoft.com/en-us/windows/ai/directml/dml)
[4](https://learn.microsoft.com/en-us/windows/win32/direct3d12/dml-redirect)
[5](https://github.com/microsoft/DirectML)
[6](https://www.w3.org/2020/06/machine-learning-workshop/talks/accelerated_graphics_and_compute_api_for_machine_learning_directml.html)
[7](https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html)
[8](https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/overview)
[9](https://github.com/microsoft/onnxruntime/issues/23783)
[10](https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/tutorial)
[11](https://blogs.windows.com/windowsdeveloper/2024/11/12/directml-unlocks-new-silicon-for-ai-experiences-across-windows-copilot-pcs/)
[12](https://blogs.windows.com/windowsdeveloper/2020/03/18/extending-the-reach-of-windows-ml-and-directml/)
[13](https://learn.microsoft.com/en-us/windows/ai/windows-ml/integrate-model)
[14](https://www.youtube.com/watch?v=AQjOq8qSsbE)
[15](https://www.youtube.com/watch?v=Z8DwlNKS3Zk)
[16](https://learn.microsoft.com/en-us/windows/ai/directml/directml-structures)
[17](https://www.forbes.com/sites/moorinsights/2025/06/17/ai-on-windows-one-year-later-at-microsoft-build-2025/)
[18](https://www.reddit.com/r/MachineLearning/comments/qfaxcv/r_microsoft_ai_opensources_pytorchdirectml_a/)
[19](https://siliconangle.com/2025/05/19/microsoft-debuts-windows-ai-foundry-local-model-development-ai-pcs/)
[20](https://bostoninstituteofanalytics.org/blog/build-2025-microsoft-opens-up-windows-machine-learning/)
[21](https://www.reddit.com/r/MachineLearning/comments/16hqzxy/d_tensorflow_dropped_support_for_windows/)
[22](https://forum.faceswap.dev/viewtopic.php?t=2669)
[23](https://onnxruntime.ai/docs/get-started/with-windows.html)
[24](https://github.com/microsoft/onnxruntime-openenclave/blob/openenclave-public/docs/execution_providers/DirectML-ExecutionProvider.md)
[25](https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/onnx-versions)
[26](https://microsoft.github.io/DirectML/)
[27](https://github.com/vladmandic/sdnext/wiki/ONNX-Runtime)
[28](https://learn.microsoft.com/en-us/windows/ai/new-windows-ml/run-onnx-models)
[29](https://onnxruntime.ai/docs/execution-providers/)
[30](https://www.machinelearningmastery.com/hardware-accelerated-ai-for-windows-apps-using-onnx-rt/)
[31](https://stackoverflow.com/questions/53993236/what-is-difference-between-cntk-and-win-ml)
