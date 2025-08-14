# NumPy to PyTorch to Rust (Burn & CubeCL) Tensor Translation Guide

This comprehensive guide provides solid tutorials on translating between NumPy arrays, PyTorch tensors, and their Rust equivalents in Burn and CubeCL.

## Overview of Tensor Types

### NumPy (Python)
- **Primary Type**: `numpy.ndarray` 
- **Purpose**: Multi-dimensional array for scientific computing
- **Backend**: C/C++ with Python bindings
- **Memory**: Row-major by default

### PyTorch (Python)
- **Primary Type**: `torch.Tensor`
- **Purpose**: Deep learning tensors with autograd support
- **Backend**: C++ (LibTorch) with Python bindings
- **Memory**: Various layouts supported

### Burn (Rust)
- **Primary Type**: `Tensor<B, const D: usize, K = Float>`
- **Purpose**: Deep learning framework tensors
- **Backend**: Multiple backends (WGPU, LibTorch, NdArray, etc.)
- **Memory**: Backend-dependent

### CubeCL (Rust)
- **Primary Type**: `Array<T>` (for GPU kernels)
- **Purpose**: GPU computing with Rust syntax
- **Backend**: Multi-platform (CUDA, WGPU, ROCm, Metal)
- **Memory**: GPU memory management

## Part 1: NumPy Array Fundamentals

### Creating NumPy Arrays

```python
import numpy as np

# From lists
arr1d = np.array([1, 2, 3, 4])
arr2d = np.array([[1, 2], [3, 4]])

# Built-in creation functions
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
eye = np.eye(3)  # Identity matrix
arange = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]
random = np.random.random((2, 2))

# Array properties
print(arr2d.shape)  # (2, 2)
print(arr2d.dtype)  # int64
print(arr2d.ndim)   # 2
```

### NumPy Operations

```python
# Element-wise operations
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])

addition = x + y        # [5, 7, 9]
multiplication = x * y  # [4, 10, 18]
division = x / y        # [0.25, 0.4, 0.5]

# Matrix operations
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
matmul = np.dot(a, b)  # Matrix multiplication

# Reshaping and slicing
reshaped = arr1d.reshape(2, 2)
sliced = arr2d[0, :]  # First row
```

## Part 2: PyTorch Tensor Fundamentals

### Creating PyTorch Tensors

```python
import torch

# From lists/arrays
tensor1d = torch.tensor([1, 2, 3, 4])
tensor2d = torch.tensor([[1, 2], [3, 4]])

# Built-in creation functions
zeros = torch.zeros(3, 4)
ones = torch.ones(2, 3)
eye = torch.eye(3)
arange = torch.arange(0, 10, 2)
linspace = torch.linspace(0, 1, 5)
randn = torch.randn(2, 2)  # Normal distribution

# From NumPy
numpy_arr = np.array([1, 2, 3])
from_numpy = torch.from_numpy(numpy_arr)

# Tensor properties
print(tensor2d.shape)  # torch.Size([2, 2])
print(tensor2d.dtype)  # torch.int64
print(tensor2d.ndim)   # 2
```

### PyTorch Operations

```python
# Element-wise operations
x = torch.tensor([1, 2, 3])
y = torch.tensor([4, 5, 6])

addition = x + y            # tensor([5, 7, 9])
multiplication = x * y      # tensor([4, 10, 18])
element_mul = torch.mul(x, y)

# Matrix operations
a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)
matmul = torch.matmul(a, b)

# Reshaping and slicing
reshaped = tensor1d.view(2, 2)
sliced = tensor2d[0, :]  # First row
```

## Part 3: Burn Tensor Fundamentals

### Setting up Burn

```rust
use burn::tensor::{Tensor, TensorData};
use burn::backend::NdArray;

type Backend = NdArray;
```

### Creating Burn Tensors

```rust
// From TensorData
let device = Default::default();

// 1D tensor
let data1d = TensorData::from([1.0, 2.0, 3.0, 4.0]);
let tensor1d = Tensor::<Backend, 1>::from_data(data1d, &device);

// 2D tensor
let data2d = TensorData::from([[1.0, 2.0], [3.0, 4.0]]);
let tensor2d = Tensor::<Backend, 2>::from_data(data2d, &device);

// From Vec and shape
let vec_data = vec![1.0, 2.0, 3.0, 4.0, 5.0, 6.0];
let tensor_data = TensorData::new(vec_data, [2, 3]);
let tensor = Tensor::<Backend, 2>::from_data(tensor_data, &device);

// Built-in creation functions
let zeros = Tensor::<Backend, 2>::zeros([3, 4], &device);
let ones = Tensor::<Backend, 2>::ones([2, 3], &device);
let random = Tensor::<Backend, 2>::random(
    [2, 2], 
    burn::tensor::Distribution::Default, 
    &device
);

// From array literals (compile-time known shapes)
let tensor = Tensor::<Backend, 2>::from_data([[1.0, 2.0], [3.0, 4.0]], &device);
```

### Burn Operations

```rust
// Element-wise operations
let x = Tensor::<Backend, 1>::from_data([1.0, 2.0, 3.0], &device);
let y = Tensor::<Backend, 1>::from_data([4.0, 5.0, 6.0], &device);

let addition = x.clone() + y.clone();           // [5, 7, 9]
let multiplication = x.clone() * y.clone();     // [4, 10, 18]
let division = x.clone() / y.clone();           // [0.25, 0.4, 0.5]

// Matrix operations
let a = Tensor::<Backend, 2>::from_data([[1.0, 2.0], [3.0, 4.0]], &device);
let b = Tensor::<Backend, 2>::from_data([[5.0, 6.0], [7.0, 8.0]], &device);
let matmul = a.matmul(b);

// Reshaping and slicing
let reshaped = tensor1d.reshape([2, 2]);
let sliced = tensor2d.slice([0..1, 0..2]);  // First row

// Advanced slicing with s! macro
use burn::tensor::s;
let slice = tensor.slice(s![.., 0..2]);  // All rows, first 2 columns
```

## Part 4: CubeCL Array/Tensor Fundamentals

### CubeCL Kernel Structure

```rust
use cubecl::prelude::*;

#[cube(launch_unchecked)]
fn example_kernel<F: Float>(
    input: &Array<F>, 
    output: &mut Array<F>
) {
    if ABSOLUTE_POS < input.len() {
        output[ABSOLUTE_POS] = input[ABSOLUTE_POS] * F::from_f32(2.0);
    }
}
```

### CubeCL Array Operations

```rust
use cubecl::prelude::*;

#[cube]
fn elementwise_add<F: Float>(
    lhs: &Array<F>,
    rhs: &Array<F>,
    output: &mut Array<F>
) {
    if ABSOLUTE_POS < output.len() {
        output[ABSOLUTE_POS] = lhs[ABSOLUTE_POS] + rhs[ABSOLUTE_POS];
    }
}

#[cube]
fn matrix_multiply_element<F: Float>(
    lhs: &Array<F>,
    rhs: &Array<F>,
    output: &mut Array<F>,
    m: u32,
    n: u32,
    k: u32,
) {
    let row = ABSOLUTE_POS / n;
    let col = ABSOLUTE_POS % n;
    
    if row < m && col < n {
        let mut sum = F::from_f32(0.0);
        for i in 0..k {
            sum += lhs[row * k + i] * rhs[i * n + col];
        }
        output[ABSOLUTE_POS] = sum;
    }
}
```

### Launching CubeCL Kernels

```rust
use cubecl::wgpu::{WgpuDevice, WgpuRuntime};

fn main() {
    let device = WgpuDevice::default();
    let client = WgpuRuntime::client(&device);
    
    // Create input data
    let input_data = vec![1.0f32, 2.0, 3.0, 4.0];
    let input_handle = client.create(input_data);
    
    // Create output buffer
    let output_handle = client.empty(4 * size_of::<f32>());
    
    // Launch kernel
    example_kernel::launch::<F32, WgpuRuntime>(
        &client,
        CubeCount::Static(1, 1, 1),
        CubeDim::new(4, 1, 1),
        ArrayArg::new(&input_handle, 4),
        ArrayArg::new(&output_handle, 4),
    );
    
    // Read results
    let output: Vec<f32> = client.read(output_handle);
}
```

## Part 5: Comprehensive Translation Examples

### Example 1: Basic Array Creation

**NumPy:**
```python
import numpy as np
arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(arr.shape)  # (2, 3)
```

**PyTorch:**
```python
import torch
tensor = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(tensor.shape)  # torch.Size([2, 3])
```

**Burn:**
```rust
use burn::tensor::{Tensor, TensorData};
use burn::backend::NdArray;

type Backend = NdArray;
let device = Default::default();

let tensor_data = TensorData::from([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]);
let tensor = Tensor::<Backend, 2>::from_data(tensor_data, &device);
println!("{:?}", tensor.dims());  // [2, 3]
```

**CubeCL:**
```rust
use cubecl::prelude::*;

#[cube(launch_unchecked)]
fn process_array<F: Float>(input: &Array<F>, output: &mut Array<F>) {
    if ABSOLUTE_POS < input.len() {
        output[ABSOLUTE_POS] = input[ABSOLUTE_POS];
    }
}

// Usage in host code
let input_data = vec![1.0f32, 2.0, 3.0, 4.0, 5.0, 6.0];
// Launch with appropriate grid dimensions for 2x3 layout
```

### Example 2: Mathematical Operations

**NumPy:**
```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
result = a + b * 2
print(result)  # [9, 12, 15]
```

**PyTorch:**
```python
import torch
a = torch.tensor([1, 2, 3])
b = torch.tensor([4, 5, 6])
result = a + b * 2
print(result)  # tensor([9, 12, 15])
```

**Burn:**
```rust
let a = Tensor::<Backend, 1>::from_data([1.0, 2.0, 3.0], &device);
let b = Tensor::<Backend, 1>::from_data([4.0, 5.0, 6.0], &device);
let two = Tensor::<Backend, 1>::from_data([2.0], &device);
let result = a + b * two;
println!("{}", result);  // [9, 12, 15]
```

**CubeCL:**
```rust
#[cube(launch_unchecked)]
fn fused_operation<F: Float>(
    a: &Array<F>, 
    b: &Array<F>, 
    output: &mut Array<F>
) {
    if ABSOLUTE_POS < a.len() {
        let two = F::from_f32(2.0);
        output[ABSOLUTE_POS] = a[ABSOLUTE_POS] + b[ABSOLUTE_POS] * two;
    }
}
```

### Example 3: Matrix Multiplication

**NumPy:**
```python
import numpy as np
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
result = np.dot(a, b)
print(result)  # [[19, 22], [43, 50]]
```

**PyTorch:**
```python
import torch
a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)
result = torch.matmul(a, b)
print(result)  # tensor([[19., 22.], [43., 50.]])
```

**Burn:**
```rust
let a = Tensor::<Backend, 2>::from_data([[1.0, 2.0], [3.0, 4.0]], &device);
let b = Tensor::<Backend, 2>::from_data([[5.0, 6.0], [7.0, 8.0]], &device);
let result = a.matmul(b);
println!("{}", result);  // [[19, 22], [43, 50]]
```

**CubeCL (Simplified):**
```rust
#[cube(launch_unchecked)]
fn matmul_2x2<F: Float>(
    a: &Array<F>, 
    b: &Array<F>, 
    output: &mut Array<F>
) {
    let row = ABSOLUTE_POS / 2;
    let col = ABSOLUTE_POS % 2;
    
    if row < 2 && col < 2 {
        let mut sum = F::from_f32(0.0);
        for k in 0..2 {
            sum += a[row * 2 + k] * b[k * 2 + col];
        }
        output[ABSOLUTE_POS] = sum;
    }
}
```

## Part 6: Advanced Translation Patterns

### Slicing and Indexing

**NumPy:**
```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
slice1 = arr[0, :]      # First row: [1, 2, 3]
slice2 = arr[:, 1]      # Second column: [2, 5, 8]
slice3 = arr[0:2, 1:3]  # Submatrix: [[2, 3], [5, 6]]
```

**PyTorch:**
```python
tensor = torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
slice1 = tensor[0, :]      # First row: tensor([1, 2, 3])
slice2 = tensor[:, 1]      # Second column: tensor([2, 5, 8])
slice3 = tensor[0:2, 1:3]  # Submatrix: tensor([[2, 3], [5, 6]])
```

**Burn:**
```rust
use burn::tensor::s;

let tensor = Tensor::<Backend, 2>::from_data(
    [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], 
    &device
);

let slice1 = tensor.clone().slice([0..1, ..]);      // First row
let slice2 = tensor.clone().slice([.., 1..2]);      // Second column  
let slice3 = tensor.clone().slice(s![0..2, 1..3]);  // Submatrix using s! macro
```

### Broadcasting

**NumPy:**
```python
a = np.array([[1, 2, 3]])     # Shape: (1, 3)
b = np.array([[1], [2], [3]]) # Shape: (3, 1)
result = a + b                # Broadcasting to (3, 3)
```

**PyTorch:**
```python
a = torch.tensor([[1, 2, 3]])     # Shape: (1, 3)
b = torch.tensor([[1], [2], [3]]) # Shape: (3, 1)
result = a + b                    # Broadcasting to (3, 3)
```

**Burn:**
```rust
// Burn supports broadcasting automatically in many operations
let a = Tensor::<Backend, 2>::from_data([[1.0, 2.0, 3.0]], &device);
let b = Tensor::<Backend, 2>::from_data([[1.0], [2.0], [3.0]], &device);
let result = a + b;  // Automatic broadcasting
```

## Part 7: Key Differences and Considerations

### Memory Management

- **NumPy**: Python's garbage collector manages memory
- **PyTorch**: Reference counting with CUDA memory management for GPU
- **Burn**: Rust's ownership system with backend-specific memory management
- **CubeCL**: Explicit GPU memory management through compute clients

### Type System

- **NumPy**: Dynamic typing with dtype specification
- **PyTorch**: Dynamic typing with device and dtype management
- **Burn**: Static typing with compile-time shape checking where possible
- **CubeCL**: Static typing with CubeType trait requirements

### Error Handling

- **NumPy/PyTorch**: Runtime exceptions
- **Burn/CubeCL**: Rust's Result type and compile-time checking

### Performance Characteristics

- **NumPy**: C/Fortran backend, CPU-optimized
- **PyTorch**: C++/CUDA backend, GPU-first design
- **Burn**: Multiple backends, automatic fusion optimization
- **CubeCL**: Multi-platform GPU computing with compile-time optimizations

## Part 8: Migration Strategies

### From NumPy to Burn

1. Replace `np.array()` with `Tensor::from_data()`
2. Use appropriate Backend type annotation
3. Handle device placement explicitly
4. Convert slicing syntax to Burn's range syntax

### From PyTorch to Burn

1. Replace tensor creation functions with Burn equivalents
2. Update gradient computation to Burn's autodiff system
3. Adapt model definitions to Burn's module system
4. Convert device handling to Burn's backend system

### To CubeCL for GPU Computing

1. Identify compute-intensive operations
2. Rewrite as CubeCL kernels with `#[cube]` attribute
3. Handle data transfer between host and device
4. Use appropriate launch configurations

## Conclusion

This guide provides a comprehensive foundation for translating between NumPy arrays, PyTorch tensors, and their Rust equivalents in Burn and CubeCL. The key to successful translation lies in understanding the fundamental differences in memory management, type systems, and computational models between these frameworks while leveraging their respective strengths for optimal performance and safety.