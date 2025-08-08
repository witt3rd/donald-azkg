<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# CubeCL: Comprehensive Guide \& Cheatsheet

## Overview

**CubeCL** is a revolutionary multi-platform, high-performance compute language extension for Rust that enables writing GPU kernels directly in Rust syntax. It provides a unified interface for programming GPUs across CUDA, WebGPU, ROCm/HIP, Metal, and Vulkan platforms while maintaining optimal performance through innovative features like automatic vectorization, compile-time optimizations, and runtime autotuning.[^1][^2]

![CubeCL Architecture: From Rust Code to Multi-Platform GPU Execution](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/8d229a8cb1e656494bada852da66cae7/89eb3879-8f9b-4dc6-a77b-da487ec2a63b/f397e52a.png)

CubeCL Architecture: From Rust Code to Multi-Platform GPU Execution

## Table of Contents

1. [Core Architecture](#core-architecture)
2. [Installation \& Setup](#installation--setup)
3. [Topology System](#topology-system)
4. [Core Concepts \& Data Types](#core-concepts--data-types)
5. [Kernel Development](#kernel-development)
6. [Advanced Features](#advanced-features)
7. [Performance Optimization](#performance-optimization)
8. [Runtime \& Execution](#runtime--execution)
9. [Debugging \& Profiling](#debugging--profiling)
10. [Platform-Specific Notes](#platform-specific-notes)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

## Core Architecture

CubeCL employs a unique **two-step compilation process** that distinguishes it from traditional GPU programming approaches:[^1][^2]

### 1. Parsing Phase

- Uses Rust's `proc_macro` system via the `syn` crate
- Parses GPU kernel code while preserving Rust semantics
- No immediate IR generation


### 2. Expansion Phase

- Generates new Rust functions (not direct IR)
- These functions create the Intermediate Representation when called
- Enables advanced features like comptime and automatic vectorization


### Supported Platforms

| Platform | Runtime | Compiler | Hardware Support |
| :-- | :-- | :-- | :-- |
| **CUDA** | `cubecl-cuda` | C++ (CUDA) | NVIDIA GPUs + Tensor Cores |
| **WebGPU** | `cubecl-wgpu` | WGSL | Most GPUs (cross-platform) |
| **ROCm** | `cubecl-hip` | C++ (HIP) | AMD GPUs |
| **Metal** | `cubecl-wgpu` | C++ (Metal) | Apple GPUs |
| **Vulkan** | `cubecl-wgpu` | SPIR-V | Most GPUs (Linux/Windows) |

## Installation \& Setup

### Basic Installation

```toml
[dependencies]
cubecl = "0.6"
cubecl-cuda = "0.6"  # For CUDA support
cubecl-wgpu = "0.6"  # For WebGPU/WGSL support
```


### Runtime Selection

```rust
use cubecl::prelude::*;

// CUDA Runtime
type Runtime = cubecl::cuda::CudaRuntime;

// WebGPU Runtime  
type Runtime = cubecl::wgpu::WgpuRuntime;

// Setup device and client
let device = Runtime::default_device();
let client = Runtime::client(&device);
```


## Topology System

CubeCL uses a **cube-based topology** that provides a unified abstraction across different GPU architectures. Understanding this system is crucial for efficient kernel development.[^3]

### Hierarchy Levels

1. **Hyper-Cube**: Collection of cubes
2. **Cube**: Collection of units (equivalent to thread blocks/workgroups)
3. **Unit**: Individual execution thread
4. **Plane**: Subgroup/warp within a cube

### Topology Variables

The topology mapping shows how CubeCL variables correspond across different platforms:


| CubeCL Variable | Description | CUDA Equivalent | WebGPU Equivalent |
| :-- | :-- | :-- | :-- |
| `CUBE_COUNT_X/Y/Z` | Number of cubes per dimension | `gridDim.x/y/z` | `num_workgroups.x/y/z` |
| `CUBE_POS_X/Y/Z` | Current cube position | `blockIdx.x/y/z` | `workgroup_id.x/y/z` |
| `CUBE_DIM_X/Y/Z` | Threads per cube dimension | `blockDim.x/y/z` | `workgroup_size.x/y/z` |
| `UNIT_POS_X/Y/Z` | Thread position within cube | `threadIdx.x/y/z` | `local_invocation_id.x/y/z` |
| `ABSOLUTE_POS_X/Y/Z` | Global thread position | N/A | `global_id.x/y/z` |
| `PLANE_POS` | Warp/subgroup ID | N/A | `subgroup_id` |
| `PLANE_DIM` | Warp/subgroup size | `warpSize` | `subgroup_size` |

### Axis-Independent Variables

CubeCL provides axis-independent versions for convenience:

- `CUBE_COUNT`, `CUBE_POS`, `CUBE_DIM`
- `UNIT_POS`, `ABSOLUTE_POS`


## Core Concepts \& Data Types

### Essential Traits

```rust
// Base trait for GPU-compatible types
trait CubeElement: Clone + Send + Sync + 'static {}

// Trait for implementing GPU kernels  
trait Kernel {
    fn launch<R: Runtime>(...);
}

// Runtime abstraction
trait Runtime {
    type Device;
    type Client; 
    fn client(device: &Self::Device) -> Self::Client;
}
```


### Data Types

#### Primitive Types

```rust
// Vectorized types for SIMD operations
Line<f32>    // Vectorized f32
Line<i32>    // Vectorized i32

// Flexible precision types
flex32       // 19-bit float (f16-f32 range)  
tf32         // TensorFloat-32 format

// Standard scalar types
f32, f64, i32, u32, i64, u64, etc.
```


#### Container Types

```rust
// Arrays and tensors
Array<T>           // Contiguous array of elements
Tensor<T>          // Multi-dimensional tensor  
SharedMemory<T>    // Fast on-chip shared memory
Matrix<T, M, N>    // Matrix for linear algebra

// Argument types for kernel launch
ArrayArg<T>        // Array kernel argument
TensorArg<T>       // Tensor kernel argument  
ScalarArg<T>       // Scalar kernel argument
```


### Launch Configuration

```rust
// Cube count specification
CubeCount::Static(x, y, z)     // Fixed dimensions
CubeCount::Dynamic(handle)      // Runtime-determined

// Cube dimensions (threads per cube)
CubeDim::new(x, y, z)          // 3D configuration
CubeDim::new_1d(x)             // 1D configuration
CubeDim::new_2d(x, y)          // 2D configuration
```


## Kernel Development

### Basic Kernel Structure

```rust
use cubecl::prelude::*;

#[cube(launch)]
fn my_kernel<F: Float>(
    input: &Array<F>,
    output: &mut Array<F>,
    scalar_param: F
) {
    // Kernel implementation
    if ABSOLUTE_POS < input.len() {
        output[ABSOLUTE_POS] = input[ABSOLUTE_POS] * scalar_param;
    }
}
```


### Kernel Attributes

```rust
#[cube]              // Basic kernel function
#[cube(launch)]      // Auto-generates launch function
#[cube(launch_unchecked)]  // Unsafe launch (no bounds checking)
```


### Memory Access Patterns

#### Global Memory Access

```rust
#[cube(launch)]
fn global_memory_access<F: Float>(
    input: &Array<F>,
    output: &mut Array<F>
) {
    let idx = ABSOLUTE_POS;
    if idx < input.len() {
        // Coalesced access pattern
        output[idx] = input[idx] * F::new(2.0);
    }
}
```


#### Shared Memory Usage

```rust
#[cube]
fn shared_memory_example<F: Float>(
    input: &Array<F>,
    output: &mut Array<F>
) {
    let shared_data = SharedMemory::<F>::new(256);
    let tid = UNIT_POS_X;
    
    // Collaborative loading
    shared_data[tid] = input[ABSOLUTE_POS];
    sync_units(); // Synchronize threads
    
    // Process with shared data
    output[ABSOLUTE_POS] = shared_data[tid] + shared_data[(tid + 1) % 256];
}
```


### Control Flow

```rust
#[cube(launch)]
fn control_flow_example<F: Float>(
    condition: &Array<bool>,
    input: &Array<F>, 
    output: &mut Array<F>
) {
    if ABSOLUTE_POS < input.len() {
        // Conditional execution
        if condition[ABSOLUTE_POS] {
            output[ABSOLUTE_POS] = F::sqrt(input[ABSOLUTE_POS]);
        } else {
            output[ABSOLUTE_POS] = input[ABSOLUTE_POS] * F::new(-1.0);
        }
        
        // Loops
        for i in 0..10 {
            output[ABSOLUTE_POS] += F::new(i as f32);
        }
    }
}
```


## Advanced Features

### 1. Comptime (Compile-Time Execution)

Comptime allows code execution during kernel compilation, enabling sophisticated optimizations:[^1][^2]

```rust
#[cube(launch)]
fn comptime_example<F: Float>(
    input: &Array<F>,
    output: &mut Array<F>
) {
    // Compile-time constants
    let unroll_factor = comptime!(8);
    let block_size = comptime!(256);
    
    // Compile-time calculations
    let sqrt_two = F::new(comptime!(2.0f32.sqrt()));
    
    // Conditional compilation
    if comptime!(F::is_f16()) {
        // F16-specific optimizations
    } else {
        // F32-specific optimizations  
    }
    
    // Loop unrolling
    for i in 0..unroll_factor {
        if ABSOLUTE_POS + i < input.len() {
            output[ABSOLUTE_POS + i] = input[ABSOLUTE_POS + i] * sqrt_two;
        }
    }
}
```


### 2. Automatic Vectorization

CubeCL automatically vectorizes operations using the `Line<T>` type:[^2][^4]

```rust
#[cube(launch)]
fn vectorized_kernel<F: Float>(
    input: &Array<Line<F>>,   // Automatically vectorized
    output: &mut Array<Line<F>>
) {
    if ABSOLUTE_POS < input.len() {
        let vec_data = input[ABSOLUTE_POS];
        
        // All operations are automatically vectorized
        let result = Line::sqrt(vec_data * vec_data + Line::new(F::new(1.0)));
        output[ABSOLUTE_POS] = result;
    }
}

// Launch with vectorization
fn launch_vectorized<R: Runtime>(client: &R::Client) {
    let vectorization_factor = 4;
    my_kernel::launch::<F, R>(
        client,
        CubeCount::Static(64, 1, 1),
        CubeDim::new(256, 1, 1),
        ArrayArg::from_raw_parts(&input_handle, length, vectorization_factor),
        ArrayArg::from_raw_parts(&output_handle, length, vectorization_factor),
    );
}
```


### 3. Autotuning

Automatic kernel selection based on runtime benchmarking:[^5]

```rust
// Enable autotuning with environment variable
// CUBECL_AUTOTUNE=1

#[cube(launch_autotune)]
fn autotune_kernel<F: Float>(
    input: &Array<F>,
    output: &mut Array<F>
) {
    // Multiple kernel variants will be benchmarked
    // and the best one selected automatically
}

// Explicit autotuning configuration
#[autotune(key = "matmul", cache = "disk")]
fn matmul_variants<F: Float>() -> AutotuneOperation {
    AutotuneOperation::default()
        .register(matmul_tiled_16x16)
        .register(matmul_tiled_32x32) 
        .register(matmul_tensor_core)
}
```


### 4. Tensor Cores Support

Leverage hardware acceleration for matrix operations:[^6][^7]

```rust
#[cube]
fn tensor_core_matmul<F: Float>(
    a: &Matrix<F, 16, 16, 16, MatrixLayout::RowMajor>,
    b: &Matrix<F, 16, 16, 16, MatrixLayout::ColMajor>,
    c: &mut Matrix<F, 16, 16, 16, MatrixLayout::RowMajor>
) {
    // Use tensor core matrix multiply-accumulate
    *c = Matrix::cmma(a, b, c);
}

// Double buffering for tensor cores
#[cube]  
fn double_buffered_matmul<F: Float>(...) {
    let mut a_buffer = [Matrix::<F, 16, 16>::new(); 2];
    let mut b_buffer = [Matrix::<F, 16, 16>::new(); 2]; 
    
    // Pipeline loads and computation
    for k in 0..(K / 16) {
        let buffer_idx = k % 2;
        // Load next tiles while computing current
        // ... implementation
    }
}
```


## Performance Optimization

### Memory Access Optimization

```rust
#[cube(launch)]
fn coalesced_access<F: Float>(
    input: &Array<F>,
    output: &mut Array<F>,
    stride: u32
) {
    let idx = ABSOLUTE_POS;
    
    // Good: Coalesced access pattern
    if idx < input.len() {
        output[idx] = input[idx];
    }
    
    // Bad: Strided access (avoid when possible)  
    let strided_idx = idx * stride;
    if strided_idx < input.len() {
        output[idx] = input[strided_idx];
    }
}
```


### Tiling for Cache Efficiency

```rust
#[cube]
fn tiled_matmul<F: Float>(
    a: &Array<F>, b: &Array<F>, c: &mut Array<F>,
    m: u32, n: u32, k: u32
) {
    const TILE_SIZE: u32 = 16;
    let shared_a = SharedMemory::<F>::new(TILE_SIZE * TILE_SIZE);
    let shared_b = SharedMemory::<F>::new(TILE_SIZE * TILE_SIZE);
    
    let row = UNIT_POS_Y;
    let col = UNIT_POS_X;
    let mut sum = F::new(0.0);
    
    // Process tiles
    for tile in 0..(k / TILE_SIZE) {
        // Load tiles to shared memory
        let a_idx = (CUBE_POS_Y * TILE_SIZE + row) * k + tile * TILE_SIZE + col;
        let b_idx = (tile * TILE_SIZE + row) * n + CUBE_POS_X * TILE_SIZE + col;
        
        shared_a[row * TILE_SIZE + col] = a[a_idx];
        shared_b[row * TILE_SIZE + col] = b[b_idx];
        sync_units();
        
        // Compute on shared data
        for i in 0..TILE_SIZE {
            sum += shared_a[row * TILE_SIZE + i] * shared_b[i * TILE_SIZE + col];
        }
        sync_units();
    }
    
    let c_idx = (CUBE_POS_Y * TILE_SIZE + row) * n + CUBE_POS_X * TILE_SIZE + col;
    c[c_idx] = sum;
}
```


### Occupancy Optimization

```rust
// Choose cube dimensions for optimal occupancy
fn calculate_optimal_launch_config(
    total_elements: usize,
    max_threads_per_cube: u32
) -> (CubeCount, CubeDim) {
    let threads_per_cube = max_threads_per_cube.min(1024); // Hardware limit
    let num_cubes = (total_elements + threads_per_cube as usize - 1) / threads_per_cube as usize;
    
    (
        CubeCount::Static(num_cubes as u32, 1, 1),
        CubeDim::new(threads_per_cube, 1, 1)
    )
}
```


## Runtime \& Execution

### Basic Kernel Launch

```rust
use cubecl::prelude::*;

fn launch_basic<R: Runtime>(device: &R::Device) {
    let client = R::client(device);
    
    // Prepare data
    let input_data = vec![1.0f32; 1024];
    let input_handle = client.create(f32::as_bytes(&input_data));
    let output_handle = client.empty(input_data.len() * std::mem::size_of::<f32>());
    
    // Launch kernel
    my_kernel::launch::<f32, R>(
        &client,
        CubeCount::Static(4, 1, 1),      // 4 cubes
        CubeDim::new(256, 1, 1),         // 256 threads per cube
        ArrayArg::new(&input_handle, input_data.len()),
        ArrayArg::new(&output_handle, input_data.len()),
        ScalarArg::new(2.0f32),
    );
    
    // Read results
    let output_bytes = client.read_one(output_handle.binding());
    let output_data = f32::from_bytes(&output_bytes);
}
```


### Memory Management

```rust
// Memory configuration options
let memory_config = MemoryConfiguration::default()
    .with_buffer_alignment(256)
    .with_pool_size(1024 * 1024 * 1024) // 1GB pool
    .with_reuse_strategy(ReuseStrategy::Aggressive);

let client = R::client_with_config(&device, memory_config);

// Manual memory management
let buffer = client.empty(size_in_bytes);
client.sync(); // Ensure operations complete

// Memory usage statistics  
let memory_usage = client.memory_usage();
println!("Used: {} MB", memory_usage.used / 1024 / 1024);
```


### Asynchronous Execution

```rust
use cubecl::future::Future;

fn launch_async<R: Runtime>(client: &R::Client) {
    // Launch kernel asynchronously
    let future = my_kernel::launch_async::<f32, R>(
        client,
        launch_config,
        args...
    );
    
    // Do other work...
    
    // Wait for completion
    let result = future.await;
}
```


## Debugging \& Profiling

### Environment Variables

```bash
# Enable debug output
CUBECL_DEBUG=1

# Enable profiling
CUBECL_PROFILE=1

# Enable autotuning
CUBECL_AUTOTUNE=1

# Set WGPU maximum tasks
CUBECL_WGPU_MAX_TASKS=64
```


### Debug Printing

```rust
#[cube(launch)]
fn debug_kernel<F: Float>(input: &Array<F>) {
    if ABSOLUTE_POS == 0 {
        // Debug print (target-specific format)
        debug_print!("Kernel started with {} elements", input.len());
    }
    
    // Conditional debug output
    if ABSOLUTE_POS < 10 {
        debug_print!("Thread {} processing element {}", 
                    ABSOLUTE_POS, input[ABSOLUTE_POS]);
    }
}
```


### Performance Profiling

```rust
use cubecl::benchmark::*;

fn benchmark_kernel<R: Runtime>(device: &R::Device) {
    let client = R::client(device);
    
    let benchmark = Benchmark::new("my_kernel", &client)
        .num_samples(100)
        .warmup_iterations(10);
        
    let elapsed = benchmark.run(|| {
        my_kernel::launch::<f32, R>(&client, /* args */);
        client.sync();
    });
    
    println!("Average execution time: {:.2} ms", elapsed.as_millis());
}
```


### Error Handling

```rust
fn safe_kernel_launch<R: Runtime>(client: &R::Client) -> Result<(), CubeError> {
    // Validate inputs
    if input.len() == 0 {
        return Err(CubeError::InvalidInput("Empty input array"));
    }
    
    // Try kernel launch  
    match my_kernel::launch::<f32, R>(client, /* args */) {
        Ok(_) => {
            client.sync()?; // Check for GPU errors
            Ok(())
        }
        Err(e) => {
            eprintln!("Kernel launch failed: {}", e);
            Err(e)
        }
    }
}
```


## Platform-Specific Notes

### CUDA Platform

```rust
use cubecl::cuda::*;

// CUDA-specific features
fn cuda_setup() {
    let device = CudaDevice::new(0); // GPU 0
    let client = CudaRuntime::client(&device);
    
    // Check compute capability
    let properties = device.properties();
    println!("Compute capability: {}.{}", 
             properties.major, properties.minor);
             
    // Tensor core availability
    if properties.major >= 7 { // Volta+
        println!("Tensor cores available");
    }
}
```


### WebGPU Platform

```rust
use cubecl::wgpu::*;

// WebGPU-specific setup
fn wgpu_setup() {
    let device = WgpuDevice::default();
    let client = WgpuRuntime::client(&device);
    
    // Feature detection
    let features = client.features();
    if features.contains(Feature::F16) {
        println!("Half precision supported");
    }
}
```


### ROCm/HIP Platform

```rust  
use cubecl::hip::*;

fn rocm_setup() {
    let device = HipDevice::new(0);
    let client = HipRuntime::client(&device);
    
    // AMD-specific optimizations
    let properties = device.properties();
    println!("Wavefront size: {}", properties.warp_size);
}
```


## Best Practices

### 1. Kernel Design

- **Keep kernels simple**: Focus on single responsibilities
- **Minimize divergence**: Avoid complex branching within warps
- **Use appropriate data types**: `Line<T>` for vectorization, `Matrix<T>` for tensor cores
- **Consider memory hierarchy**: SharedMemory for frequently accessed data


### 2. Memory Management

- **Prefer vectorized access**: Use `Line<T>` for better bandwidth utilization
- **Coalesce memory access**: Ensure adjacent threads access adjacent memory
- **Reuse buffers**: Configure memory management for buffer reuse
- **Align data structures**: Use appropriate alignment for optimal access


### 3. Performance Optimization

- **Profile regularly**: Use built-in profiling tools to identify bottlenecks
- **Use autotuning**: Let CubeCL select optimal kernels automatically
- **Leverage comptime**: Pre-compute constants and specialize code paths
- **Consider occupancy**: Balance threads per cube with resource usage


### 4. Cross-Platform Development

- **Test on multiple platforms**: Ensure kernels work across CUDA/WebGPU/ROCm
- **Use platform-agnostic features**: Prefer CubeCL abstractions over platform-specific code
- **Handle feature differences**: Check platform capabilities before using advanced features
- **Optimize for lowest common denominator**: Ensure good performance on all targets


## Troubleshooting

### Common Issues

#### Compilation Errors

```rust
// Error: Type doesn't implement CubeElement
struct MyStruct { x: f32 }  // ❌

#[derive(CubeElement)] // ✅
struct MyStruct { x: f32 }

// Error: Unsupported control flow
#[cube]
fn bad_kernel() {
    loop { } // ❌ - infinite loops not supported
}
```


#### Runtime Errors

```rust
// Error: Out of bounds access
#[cube(launch)]
fn safe_access<F: Float>(input: &Array<F>, output: &mut Array<F>) {
    // Always check bounds
    if ABSOLUTE_POS < input.len() { // ✅
        output[ABSOLUTE_POS] = input[ABSOLUTE_POS];
    }
}

// Error: Memory allocation failure
fn handle_memory_error<R: Runtime>(client: &R::Client) {
    match client.empty(very_large_size) {
        Ok(buffer) => { /* use buffer */ }
        Err(CubeError::OutOfMemory) => {
            // Fallback strategy
            eprintln!("Not enough GPU memory, using smaller buffer");
        }
        Err(e) => panic!("Unexpected error: {}", e),
    }
}
```


#### Performance Issues

```rust
// Issue: Poor memory access pattern
#[cube(launch)]  
fn bad_pattern<F: Float>(input: &Array<F>, output: &mut Array<F>, stride: u32) {
    let idx = ABSOLUTE_POS * stride; // ❌ - non-coalesced
    output[ABSOLUTE_POS] = input[idx];
}

#[cube(launch)]
fn good_pattern<F: Float>(input: &Array<F>, output: &mut Array<F>) {
    let idx = ABSOLUTE_POS; // ✅ - coalesced access
    if idx < input.len() {
        output[idx] = input[idx];
    }
}
```


### Debugging Tips

1. **Start Simple**: Begin with basic kernels and add complexity gradually
2. **Use Debug Prints**: Leverage `debug_print!` for runtime debugging
3. **Check Platform Support**: Verify features are supported on target platform
4. **Profile Early**: Use profiling tools to identify performance bottlenecks
5. **Test Edge Cases**: Verify behavior with empty arrays, single elements, etc.

## Advanced Topics

### Custom Runtime Implementation

```rust
// Implementing custom runtime (advanced)
pub struct MyRuntime;

impl Runtime for MyRuntime {
    type Device = MyDevice;
    type Client = MyClient;
    
    fn client(device: &Self::Device) -> Self::Client {
        // Custom client implementation
    }
    
    fn name() -> &'static str {
        "my_runtime"
    }
}
```


### Kernel Fusion

```rust
// Fuse multiple operations into single kernel
#[cube(launch)]
fn fused_operations<F: Float>(
    input: &Array<F>,
    output: &mut Array<F>,
    temp_result: &mut Array<F>
) {
    if ABSOLUTE_POS < input.len() {
        // Fused: activation -> normalization -> scaling
        let activated = F::tanh(input[ABSOLUTE_POS]);
        let normalized = activated / F::new(2.0) + F::new(0.5);
        output[ABSOLUTE_POS] = normalized * F::new(255.0);
    }
}
```

This comprehensive guide covers the essential aspects of CubeCL development, from basic concepts to advanced optimization techniques. The framework's innovative approach to GPU programming in Rust makes it a powerful tool for high-performance computing applications across multiple platforms.[^1][^2][^8]

<div style="text-align: center">⁂</div>

[^1]: https://www.reddit.com/r/rust/comments/1e75n89/announcing_cubecl_multiplatform_gpu_computing_in/

[^2]: https://news.ycombinator.com/item?id=41007242

[^3]: https://gist.github.com/nihalpasham/570d4fe01b403985e1eaf620b6613774

[^4]: https://getcoai.com/news/rust-gets-multi-platform-compute-boost-with-cubecl/

[^5]: https://burn.dev/blog/autotune-for-gpu-kernels/

[^6]: https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html

[^7]: https://alexarmbr.github.io/2024/08/10/How-To-Write-A-Fast-Matrix-Multiplication-From-Scratch-With-Tensor-Cores.html

[^8]: https://burn.dev/blog/sota-multiplatform-matmul/

[^9]: https://github.com/tracel-ai/cubecl

[^10]: https://www.youtube.com/watch?v=lmEj-Vana4s

[^11]: https://cube.dev/docs/product/apis-integrations/rest-api/reference

[^12]: https://github.com/tracel-ai/cubecl/blob/main/examples/sum_things/src/lib.rs

[^13]: https://lib.rs/crates/cubecl-wgpu

[^14]: https://www.youtube.com/watch?v=qUMgEnkavdY

[^15]: https://www.youtube.com/playlist?list=PLIUa1VcxJuwlI5sg8M8MH6FgzBzUWuAFI

[^16]: https://lib.rs/crates/cubecl-runtime

[^17]: https://docs.rs/cubecl

[^18]: https://crates.io/crates/burn-cubecl-fusion

[^19]: https://docs.rs/cubecl-core

[^20]: https://github.com/tracel-ai/cubecl-hip

[^21]: https://crates.io/crates/cubecl-runtime

[^22]: https://crates.io/crates/cubecl-hip-sys

[^23]: https://news.ycombinator.com/item?id=43777731

[^24]: https://www.youtube.com/watch?v=tPaa9vIXF-A

[^25]: https://people.inf.ethz.ch/omutlu/pub/mecs_hpca09.pdf

[^26]: https://www.cs.sjtu.edu.cn/~gchen/course/acn/Reading/Topological properties of hypercubes.pdf

[^27]: https://burn.dev/blog/improve-rust-compile-time-by-108x/

[^28]: http://courses.grainger.illinois.edu/cs484/sp2020/20_interconnectTopologiesFinal.pdf

[^29]: https://people.eecs.berkeley.edu/~kubitron/courses/cs258-S08/lectures/lec04-networks2.pdf

[^30]: https://disco.ethz.ch/courses/ss05/distcomp/lecture/chapter5.pdf

[^31]: https://stackoverflow.com/questions/56231449/is-it-possible-to-convince-clang-to-auto-vectorize-this-code-without-using-intri

[^32]: https://crates.io/crates/cubecl-core

[^33]: https://github.com/tracel-ai/cubecl/issues/55

[^34]: https://burn.dev/blog/release-0.14.0/

[^35]: https://docs.rs/cubecl/latest/cubecl/prelude/struct.Array.html

[^36]: https://vivilearns2code.github.io/k8s/2021/03/12/diving-into-controller-runtime.html

[^37]: https://github.com/tracel-ai/cubecl/issues/357

[^38]: https://docs.rs/cubecl-runtime

[^39]: https://docs.rs/cubecl-hip-sys

[^40]: https://lib.rs/science/math

[^41]: https://lists.freebsd.org/archives/dev-commits-ports-all/2025-July/167126.html

[^42]: https://lib.rs/algorithms

[^43]: https://www.reddit.com/r/rust/comments/1jjf96y/why_isnt_rust_used_more_for_scientific_computing/

[^44]: https://docs.alliancecan.ca/wiki/Debugging_and_profiling

[^45]: https://www.linkedin.com/posts/aniketmish_parallelprogramming-deeplearning-cuda-activity-7236657963686350849-wXm5

[^46]: https://stackoverflow.com/questions/5132628/profiling-opencl-kernels

[^47]: https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=cubes-manage-cube-attributes

[^48]: https://hpc.cea.fr/tgcc-public/en/html/toc/fulldoc/Profiling.html

[^49]: https://www.youtube.com/watch?v=dToaepIXW4s

[^50]: https://missing.csail.mit.edu/2020/debugging-profiling/

[^51]: https://www.reddit.com/r/rust/comments/1fyown4/rust_gpu_the_future_of_gpu_programming/

[^52]: https://users.rust-lang.org/t/profiling-in-rust-application/18195

[^53]: https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-164.pdf

[^54]: https://www.reddit.com/r/rust/comments/1geb3m2/cubecl_03_released_rocmhip_spirv_support_for/

[^55]: https://www.reddit.com/r/MachineLearning/comments/1cqhsln/p_simplegemm_fast_and_minimal_tensor_core_matrix/

[^56]: https://crates.io/crates/burn-cubecl

[^57]: https://www.netlib.org/utk/people/JackDongarra/PAPERS/performance-portable-autotuning.pdf

[^58]: https://news.ycombinator.com/item?id=43736739

[^59]: https://github.com/tracel-ai/cubecl/releases

[^60]: https://discuss.pytorch.org/t/tensor-cores-and-mixed-precision-matrix-multiplication-output-in-float32/42831

[^61]: https://x.com/tracel_ai

[^62]: https://forums.developer.nvidia.com/t/how-does-it-compute-exactly-in-tensor-core/294323

[^63]: https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/8d229a8cb1e656494bada852da66cae7/410acbca-1a8e-4f5e-a006-6bccc71d9fa8/ae16f83b.csv

[^64]: https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/8d229a8cb1e656494bada852da66cae7/93c2d78f-f97d-486e-9b8b-a84317731e7c/df1d3a8a.csv

[^65]: https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/8d229a8cb1e656494bada852da66cae7/3e732e47-bc44-4ad3-892b-66fa5bf11b00/eb93ef2d.csv

