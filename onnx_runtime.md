---
tags: [onnx, reference, guide, api, best-practices, patterns]
---

# ONNX Runtime Comprehensive Brief and Cheatsheet for Windows 11

## Overview

ONNX Runtime is a high-performance inference and training engine for machine learning models. It provides cross-platform support and hardware acceleration through execution providers, making it ideal for deploying models across different environments. As of 2024-2025, ONNX Runtime serves as the core inference engine behind Windows ML, providing the foundation for AI execution on Windows while maintaining cross-platform compatibility.

## Key Concepts

### What is ONNX Runtime?

- Cross-platform inference engine for ONNX models
- Core engine powering Windows ML since 2024
- Supports multiple programming languages (C#, Python, C++, Java, JavaScript)
- Hardware acceleration through Execution Providers
- Graph optimizations for improved performance
- Memory-efficient model execution
- Foundation of the Windows AI stack for inference

### Execution Providers

Execution Providers (EPs) are interfaces that allow ONNX Runtime to leverage different hardware accelerators:

- **CPU ExecutionProvider** - Default, runs on CPU
- **CUDA ExecutionProvider** - NVIDIA GPU acceleration
- **DirectML ExecutionProvider** - Windows GPU acceleration (AMD, Intel, NVIDIA)
- **TensorRT ExecutionProvider** - NVIDIA optimized inference
- **OpenVINO ExecutionProvider** - Intel hardware optimization

## Installation on Windows 11

### System Requirements

- Windows 11 (any edition)
- Visual C++ 2019 Redistributable
- For GPU: Compatible drivers (CUDA for NVIDIA, DirectX 12 for DirectML)

### Python Installation

```bash
# CPU version
pip install onnxruntime

# GPU with CUDA support
pip install onnxruntime-gpu

# GPU with DirectML (Windows)
pip install onnxruntime-directml

# Install additional dependencies
pip install numpy
```

### C# / .NET Installation

```bash
# CPU version
dotnet add package Microsoft.ML.OnnxRuntime

# GPU with CUDA support
dotnet add package Microsoft.ML.OnnxRuntime.Gpu

# GPU with DirectML
dotnet add package Microsoft.ML.OnnxRuntime.DirectML

# Helper package for tensors
dotnet add package System.Numerics.Tensors
```

### C++ Installation

1. **Download Pre-built Binaries:**
   - Visit [ONNX Runtime Releases](https://github.com/microsoft/onnxruntime/releases)
   - Download Windows x64 package (e.g., `onnxruntime-win-x64-1.16.0.zip`)
   - Extract to desired location

2. **Build from Source:**

   ```bash
   git clone --recursive https://github.com/Microsoft/onnxruntime
   cd onnxruntime
   .\build.bat --config Release --build_shared_lib --parallel
   ```

## Code Examples

### Python Example

```python
import onnxruntime as ort
import numpy as np

# Basic inference
def run_inference():
    # Create inference session
    session = ort.InferenceSession("model.onnx")

    # Get input/output info
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    # Prepare input data
    input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)

    # Run inference
    results = session.run([output_name], {input_name: input_data})

    return results[0]

# GPU inference with CUDA
def gpu_inference():
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
    session = ort.InferenceSession("model.onnx", providers=providers)

    # Rest of inference code...

# Custom session options
def optimized_session():
    session_options = ort.SessionOptions()
    session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    session_options.intra_op_num_threads = 4
    session_options.inter_op_num_threads = 4
    session_options.enable_profiling = True

    session = ort.InferenceSession("model.onnx", session_options)
    return session
```

### C# Example

```csharp
using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main()
    {
        // Basic inference
        RunBasicInference();

        // GPU inference
        RunGpuInference();
    }

    static void RunBasicInference()
    {
        // Create session
        using var session = new InferenceSession("model.onnx");

        // Prepare input data
        var inputData = new float[] { 1.0f, 2.0f, 3.0f, 4.0f };
        var inputTensor = new DenseTensor<float>(inputData, new[] { 1, 4 });

        // Create input
        var inputs = new List<NamedOnnxValue>
        {
            NamedOnnxValue.CreateFromTensor("input", inputTensor)
        };

        // Run inference
        using var results = session.Run(inputs);

        // Get output
        var output = results.First().AsTensor<float>();
        Console.WriteLine($"Output: {string.Join(", ", output.ToArray())}");
    }

    static void RunGpuInference()
    {
        // Configure session for GPU
        var sessionOptions = new SessionOptions();
        sessionOptions.GraphOptimizationLevel = GraphOptimizationLevel.ORT_ENABLE_ALL;

        // Use CUDA if available, fallback to CPU
        sessionOptions.AppendExecutionProvider_CUDA(0);

        using var session = new InferenceSession("model.onnx", sessionOptions);

        // Rest of inference code...
    }

    static void OptimizedSession()
    {
        var sessionOptions = new SessionOptions();

        // Graph optimizations
        sessionOptions.GraphOptimizationLevel = GraphOptimizationLevel.ORT_ENABLE_ALL;

        // Threading
        sessionOptions.InterOpNumThreads = 4;
        sessionOptions.IntraOpNumThreads = 4;

        // Memory optimization
        sessionOptions.EnableMemPattern = true;
        sessionOptions.EnableCpuMemArena = true;

        // Profiling
        sessionOptions.EnableProfiling = true;

        using var session = new InferenceSession("model.onnx", sessionOptions);
    }
}
```

### C++ Example

```cpp
#include <onnxruntime_cxx_api.h>
#include <iostream>
#include <vector>

int main() {
    // Initialize ONNX Runtime
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "ONNXRuntimeExample");

    // Basic inference
    RunBasicInference(env);

    // GPU inference
    RunGpuInference(env);

    return 0;
}

void RunBasicInference(Ort::Env& env) {
    // Session options
    Ort::SessionOptions session_options;
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

    // Create session
    Ort::Session session(env, L"model.onnx", session_options);

    // Get input/output info
    size_t num_input_nodes = session.GetInputCount();
    size_t num_output_nodes = session.GetOutputCount();

    std::vector<const char*> input_names;
    std::vector<const char*> output_names;

    // Get input names
    for (size_t i = 0; i < num_input_nodes; i++) {
        char* input_name = session.GetInputName(i, Ort::AllocatorWithDefaultOptions());
        input_names.push_back(input_name);
    }

    // Get output names
    for (size_t i = 0; i < num_output_nodes; i++) {
        char* output_name = session.GetOutputName(i, Ort::AllocatorWithDefaultOptions());
        output_names.push_back(output_name);
    }

    // Prepare input data
    std::vector<float> input_data = {1.0f, 2.0f, 3.0f, 4.0f};
    std::vector<int64_t> input_shape = {1, 4};

    // Create input tensor
    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
        memory_info, input_data.data(), input_data.size(),
        input_shape.data(), input_shape.size()
    );

    // Run inference
    auto output_tensors = session.Run(
        Ort::RunOptions{nullptr},
        input_names.data(),
        &input_tensor,
        1,
        output_names.data(),
        1
    );

    // Get output
    float* output_data = output_tensors.front().GetTensorMutableData<float>();
    std::cout << "Output: " << output_data[0] << std::endl;
}

void RunGpuInference(Ort::Env& env) {
    // Session options with GPU
    Ort::SessionOptions session_options;

    // Enable CUDA if available
    OrtCUDAProviderOptions cuda_options{};
    cuda_options.device_id = 0;
    session_options.AppendExecutionProvider_CUDA(cuda_options);

    // Fallback to CPU
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

    Ort::Session session(env, L"model.onnx", session_options);

    // Rest of inference code...
}
```

## Performance Optimization

### Session Configuration

```python
# Python optimization
session_options = ort.SessionOptions()

# Graph optimization
session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

# Threading
session_options.intra_op_num_threads = 0  # Use all cores
session_options.inter_op_num_threads = 0  # Use all cores

# Memory optimization
session_options.enable_cpu_mem_arena = True
session_options.enable_mem_pattern = True

# Execution mode
session_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
```

### Memory Management

```csharp
// C# memory optimization
var sessionOptions = new SessionOptions();

// Enable memory patterns
sessionOptions.EnableMemPattern = true;
sessionOptions.EnableCpuMemArena = true;

// Use OrtValue for better memory management
using var inputOrtValue = OrtValue.CreateTensorFromMemory(inputData, shape);
using var outputs = session.Run(runOptions, inputs, outputNames);
```

### Execution Provider Selection

```cpp
// C++ provider configuration
Ort::SessionOptions session_options;

// Try CUDA first, fallback to CPU
try {
    OrtCUDAProviderOptions cuda_options{};
    cuda_options.device_id = 0;
    session_options.AppendExecutionProvider_CUDA(cuda_options);
} catch (...) {
    std::cout << "CUDA not available, using CPU" << std::endl;
}
```

## Model Optimization Techniques

### Graph Optimization Levels

- **ORT_DISABLE_ALL** - No optimizations
- **ORT_ENABLE_BASIC** - Basic optimizations (constant folding, redundant node elimination)
- **ORT_ENABLE_EXTENDED** - Extended optimizations (operator fusion)
- **ORT_ENABLE_ALL** - All available optimizations (recommended)

### Model Quantization

```python
# Example model optimization with quantization
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType

model_fp32 = 'model.onnx'
model_quant = 'model_quantized.onnx'

# Dynamic quantization
quantize_dynamic(model_fp32, model_quant, weight_type=QuantType.QUInt8)
```

## Troubleshooting Common Issues

### Installation Issues

```bash
# Windows CUDA DLL issues
set CUDA_PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.0
set PATH=%CUDA_PATH%\bin;%PATH%

# DirectML issues
# Ensure DirectX 12 is available
# Update graphics drivers
```

### Memory Issues

```python
# Reduce memory usage
session_options = ort.SessionOptions()
session_options.enable_cpu_mem_arena = False  # Disable if memory is limited
session_options.enable_mem_pattern = False   # Disable for variable input sizes

# Use smaller batch sizes
# Consider model quantization
```

### Performance Issues

```csharp
// C# performance tips
var sessionOptions = new SessionOptions();

// Warm up the model
for (int i = 0; i < 5; i++) {
    session.Run(inputs);  // Warm-up runs
}

// Profile execution
sessionOptions.EnableProfiling = true;
```

## Best Practices

### Model Loading

- Load models once, reuse sessions
- Use appropriate execution providers for your hardware
- Enable graph optimizations
- Consider model quantization for deployment

### Threading

- Let ONNX Runtime manage threads (set to 0)
- Avoid oversubscription in multi-threaded applications
- Use session per thread for thread safety

### Memory Management

- Use OrtValue for efficient memory handling (C#/C++)
- Pre-allocate output buffers when possible
- Enable memory patterns for consistent input shapes
- Disable memory arena for limited memory scenarios

### Error Handling

```python
try:
    session = ort.InferenceSession("model.onnx")
    results = session.run(None, inputs)
except ort.OnnxRuntimeError as e:
    print(f"ONNX Runtime error: {e}")
except Exception as e:
    print(f"General error: {e}")
```

## Quick Reference Commands

### Python Commands

```bash
# Check ONNX Runtime version
python -c "import onnxruntime; print(onnxruntime.__version__)"

# List available providers
python -c "import onnxruntime as ort; print(ort.get_available_providers())"

# Model info
python -c "import onnxruntime as ort; sess=ort.InferenceSession('model.onnx'); print([i.name for i in sess.get_inputs()])"
```

### C# Package Management

```bash
# Update packages
dotnet add package Microsoft.ML.OnnxRuntime --version 1.16.0

# Check installed version
dotnet list package | findstr OnnxRuntime
```

### C++ Build Commands

```bash
# Build ONNX Runtime from source
.\build.bat --config Release --build_shared_lib --parallel --cmake_extra_defines CMAKE_INSTALL_PREFIX=install

# CMake integration
find_package(onnxruntime REQUIRED)
target_link_libraries(your_app onnxruntime::onnxruntime)
```

This comprehensive guide provides the foundation for using ONNX Runtime effectively on Windows 11 across multiple programming languages, with practical examples and optimization techniques for production deployment.
