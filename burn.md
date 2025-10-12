---
tags: [rust, ml, deep-learning, framework, burn, tensors]
---
# Burn Rust Deep Learning Framework - Comprehensive Cheatsheet

## Overview

Burn is a next-generation deep learning framework built in Rust that prioritizes:

- **Flexibility**: Dynamic computational graphs with static graph performance
- **Performance**: Automatic kernel fusion, async execution, JIT compilation
- **Portability**: Runs on CPU, GPU (CUDA, Metal, Vulkan), WebGPU, and embedded devices
- **Safety**: Rust's memory safety prevents common ML bugs

---

## 🚀 Installation & Setup

### Basic Installation

```toml
[dependencies]
burn = "0.14"  # Latest stable version
burn-wgpu = "0.14"  # For WGPU backend
burn-tch = "0.14"   # For LibTorch backend
burn-candle = "0.14"  # For Candle backend
burn-ndarray = "0.14"  # For CPU-only NdArray backend
```

### Backend Selection Examples

```rust
// WGPU Backend (cross-platform GPU)
use burn::backend::{Autodiff, Wgpu};
use burn_wgpu::{WgpuDevice, AutoGraphicsApi};
type Backend = Autodiff<Wgpu<AutoGraphicsApi, f32, i32>>;
let device = WgpuDevice::default();

// LibTorch Backend (CPU/CUDA)
use burn::backend::{Autodiff, LibTorch};
use burn_tch::LibTorchDevice;
type Backend = Autodiff<LibTorch>;
let device = LibTorchDevice::Cpu;  // or LibTorchDevice::Cuda(0)

// NdArray Backend (CPU only)
use burn::backend::{Autodiff, NdArray};
use burn_ndarray::NdArrayDevice;
type Backend = Autodiff<NdArray>;
let device = NdArrayDevice::Cpu;
```

---

## 🧮 Tensor Operations

### Tensor Creation

```rust
use burn::tensor::{Tensor, Distribution, Data};

// Basic creation
let zeros = Tensor::<Backend, 2>::zeros([3, 4], &device);
let ones = Tensor::<Backend, 2>::ones([3, 4], &device);
let empty = Tensor::<Backend, 2>::empty([3, 4], &device);

// From data
let data = Data::from([[1.0, 2.0], [3.0, 4.0]]);
let tensor = Tensor::<Backend, 2>::from_data(data, &device);

// Random tensors
let random_normal = Tensor::<Backend, 2>::random([3, 4], Distribution::Default, &device);
let random_uniform = Tensor::<Backend, 2>::random([3, 4], Distribution::Uniform(0.0, 1.0), &device);

// From arrays/vectors
let from_array = Tensor::<Backend, 2>::from_floats([[1.0, 2.0], [3.0, 4.0]], &device);
let from_vec = Tensor::<Backend, 1>::from_floats([1.0, 2.0, 3.0], &device);
```

### Shape Manipulation

```rust
// Reshape (-1 infers dimension, 0 keeps current dimension)
let reshaped = tensor.reshape([2, -1]);  // [2, 3, 4] -> [2, 12]
let keep_dim = tensor.reshape([0, -1]);  // [2, 3, 4] -> [2, 12]

// Transpose and permute
let transposed = tensor.transpose();  // 2D only
let permuted = tensor.permute([1, 0, 2]);  // Reorder dimensions

// Squeeze and unsqueeze
let squeezed = tensor.squeeze(1);  // Remove dimension of size 1
let unsqueezed = tensor.unsqueeze_dim::<3>(1);  // Add dimension of size 1

// View operations
let flattened = tensor.flatten(0, 2);  // Flatten dimensions 0-2
```

### Indexing and Slicing

```rust
use burn::tensor::s;

// Slicing with s! macro
let slice = tensor.slice([0..2, 1..3]);  // Slice rows 0-1, cols 1-2
let advanced_slice = tensor.slice([s![0..2], s![..], s![1..3]]);

// Select specific indices
let indices = Tensor::<Backend, 1, Int>::from_data([0, 2], &device);
let selected = tensor.select(1, indices);  // Select columns 0 and 2

// Boolean indexing
let mask = tensor.greater_elem(0.5);
let masked = tensor.mask_where(mask, tensor, zeros);

// Single element access
let element = tensor.clone().slice([0..1, 1..2]);  // Get element at [0, 1]
```

### Mathematical Operations

```rust
// Element-wise operations
let added = tensor1 + tensor2;
let subtracted = tensor1 - tensor2;
let multiplied = tensor1 * tensor2;
let divided = tensor1 / tensor2;

// With scalars
let scaled = tensor + 5.0;
let scaled_mul = tensor * 2.0;

// Mathematical functions
let exp = tensor.exp();
let log = tensor.log();
let sqrt = tensor.sqrt();
let sin = tensor.sin();
let cos = tensor.cos();
let abs = tensor.abs();
let pow = tensor.powf_scalar(2.0);

// Reductions
let sum_all = tensor.sum();
let sum_dim = tensor.sum_dim(1);  // Sum along dimension 1
let mean = tensor.mean();
let mean_dim = tensor.mean_dim(0);
let max = tensor.max();
let min = tensor.min();
let argmax = tensor.argmax(1);
let argmin = tensor.argmin(1);

// Linear algebra
let matmul = tensor1.matmul(tensor2);
let dot = tensor1.dot(tensor2);  // 1D tensors only
```

### Advanced Operations

```rust
// Concatenation and stacking
let tensors = vec![tensor1, tensor2, tensor3];
let concatenated = Tensor::cat(tensors, 0);  // Along dimension 0
let stacked = Tensor::stack::<3>(tensors, 0);  // New dimension

// Splitting
let chunks = tensor.chunk(3, 1);  // Split into 3 chunks along dim 1

// Iteration
for slice in tensor.iter_dim(0) {
    // Process each slice along dimension 0
}

// Cloning and device transfer
let cloned = tensor.clone();
let to_device = tensor.to_device(&other_device);

// Type conversion
let int_tensor = tensor.int();
let bool_tensor = tensor.bool();
```

---

## 🧠 Neural Network Modules

### Module Definition

```rust
use burn::nn::{Linear, LinearConfig, Dropout, DropoutConfig};
use burn::module::Module;

#[derive(Module, Debug)]
struct MyModel<B: Backend> {
    linear1: Linear<B>,
    linear2: Linear<B>,
    dropout: Dropout,
}

impl<B: Backend> MyModel<B> {
    pub fn new(device: &B::Device) -> Self {
        Self {
            linear1: LinearConfig::new(784, 128).init(device),
            linear2: LinearConfig::new(128, 10).init(device),
            dropout: DropoutConfig::new(0.5).init(),
        }
    }

    pub fn forward(&self, x: Tensor<B, 2>) -> Tensor<B, 2> {
        let x = self.linear1.forward(x);
        let x = x.relu();
        let x = self.dropout.forward(x);
        self.linear2.forward(x)
    }
}
```

### Built-in Layers

```rust
use burn::nn::*;

// Linear layers
let linear = LinearConfig::new(input_size, output_size)
    .with_bias(true)  // Default: true
    .init(device);

// Convolutional layers
let conv2d = Conv2dConfig::new([in_channels, out_channels], [kernel_h, kernel_w])
    .with_stride([1, 1])
    .with_padding(PaddingConfig2d::Same)
    .with_dilation([1, 1])
    .init(device);

// Activation functions
let relu = ReLU::new();
let gelu = GELU::new();
let sigmoid = Sigmoid::new();
let tanh = Tanh::new();

// Normalization layers
let batch_norm = BatchNormConfig::new(num_features).init(device);
let layer_norm = LayerNormConfig::new(normalized_shape).init(device);

// Regularization
let dropout = DropoutConfig::new(0.5).init();

// Pooling layers
let max_pool = MaxPool2dConfig::new([2, 2]).init();
let avg_pool = AvgPool2dConfig::new([2, 2]).init();

// Recurrent layers
let lstm = LstmConfig::new(input_size, hidden_size).init(device);
let gru = GruConfig::new(input_size, hidden_size).init(device);
```

### Sequential Models

```rust
use burn::nn::Sequential;

let model = Sequential::new()
    .add(LinearConfig::new(784, 256).init(device))
    .add(ReLU::new())
    .add(DropoutConfig::new(0.2).init())
    .add(LinearConfig::new(256, 128).init(device))
    .add(ReLU::new())
    .add(LinearConfig::new(128, 10).init(device));
```

### Custom Modules with Parameters

```rust
use burn::module::{Module, Param};
use burn::tensor::Tensor;

#[derive(Module, Debug)]
struct CustomLayer<B: Backend> {
    weight: Param<Tensor<B, 2>>,
    bias: Param<Tensor<B, 1>>,
    scale: f32,  // Not a parameter
}

impl<B: Backend> CustomLayer<B> {
    pub fn new(input_dim: usize, output_dim: usize, device: &B::Device) -> Self {
        let weight = Tensor::random([output_dim, input_dim], Distribution::Default, device);
        let bias = Tensor::zeros([output_dim], device);

        Self {
            weight: Param::from_tensor(weight),
            bias: Param::from_tensor(bias),
            scale: 1.0,
        }
    }

    pub fn forward(&self, input: Tensor<B, 2>) -> Tensor<B, 2> {
        let output = input.matmul(self.weight.val().transpose());
        output + self.bias.val() * self.scale
    }
}
```

---

## 🎯 Training Infrastructure

### Loss Functions

```rust
use burn::nn::loss::*;

// Cross-entropy for classification
let cross_entropy = CrossEntropyLossConfig::new()
    .with_pad_tokens(vec![0])  // Ignore padding tokens
    .with_smoothing(Some(0.1))  // Label smoothing
    .init(device);

// Mean squared error for regression
let mse = MseLoss::new();

// Binary cross-entropy
let binary_ce = BinaryCrossEntropyLossConfig::new().init();

// Custom loss function
fn custom_loss<B: Backend>(predictions: Tensor<B, 2>, targets: Tensor<B, 2>) -> Tensor<B, 1> {
    let diff = predictions - targets;
    diff.powf_scalar(2.0).mean()
}
```

### Optimizers

```rust
use burn::optim::*;

// Adam optimizer
let adam = AdamConfig::new()
    .with_beta_1(0.9)
    .with_beta_2(0.999)
    .with_epsilon(1e-8)
    .with_weight_decay(Some(WeightDecayConfig::new(0.01)))
    .init();

// AdamW (Adam with decoupled weight decay)
let adamw = AdamWConfig::new()
    .with_beta_1(0.9)
    .with_beta_2(0.999)
    .with_epsilon(1e-8)
    .with_weight_decay(Some(WeightDecayConfig::new(0.01)))
    .init();

// SGD with momentum
let sgd = SgdConfig::new()
    .with_momentum(Some(MomentumConfig::new(0.9)))
    .with_dampening(Some(0.1))
    .with_weight_decay(Some(WeightDecayConfig::new(0.0001)))
    .init();

// RMSprop
let rmsprop = RmsPropConfig::new()
    .with_alpha(0.99)
    .with_epsilon(1e-8)
    .with_momentum(Some(0.9))
    .init();
```

### Training Step Implementation

```rust
use burn::train::{TrainStep, ValidStep, TrainOutput, ClassificationOutput};

impl<B: AutodiffBackend> TrainStep<MnistBatch<B>, ClassificationOutput<B>> for Model<B> {
    fn step(&self, batch: MnistBatch<B>) -> TrainOutput<ClassificationOutput<B>> {
        let item = self.forward_classification(batch.images, batch.targets);
        TrainOutput::new(self, item.loss.backward(), item)
    }
}

impl<B: Backend> ValidStep<MnistBatch<B>, ClassificationOutput<B>> for Model<B> {
    fn step(&self, batch: MnistBatch<B>) -> ClassificationOutput<B> {
        self.forward_classification(batch.images, batch.targets)
    }
}

impl<B: Backend> Model<B> {
    pub fn forward_classification(
        &self,
        images: Tensor<B, 3>,
        targets: Tensor<B, 1, Int>,
    ) -> ClassificationOutput<B> {
        let output = self.forward(images);
        let loss = CrossEntropyLossConfig::new()
            .init(&output.device())
            .forward(output.clone(), targets.clone());
        ClassificationOutput::new(loss, output, targets)
    }
}
```

### Learner Setup

```rust
use burn::train::{LearnerBuilder, metric::{LossMetric, AccuracyMetric}};
use burn::record::CompactRecorder;

#[derive(Config)]
pub struct TrainingConfig {
    pub model: ModelConfig,
    pub optimizer: AdamConfig,
    #[config(default = 10)]
    pub num_epochs: usize,
    #[config(default = 64)]
    pub batch_size: usize,
    #[config(default = 1.0e-4)]
    pub learning_rate: f64,
}

pub fn train<B: AutodiffBackend>(artifact_dir: &str, config: TrainingConfig, device: B::Device) {
    let model = config.model.init::<B>(&device);
    let optimizer = config.optimizer.init();

    let learner = LearnerBuilder::new(artifact_dir)
        .metric_train_numeric(AccuracyMetric::new())
        .metric_valid_numeric(AccuracyMetric::new())
        .metric_train_numeric(LossMetric::new())
        .metric_valid_numeric(LossMetric::new())
        .with_file_checkpointer(CompactRecorder::new())
        .devices(vec![device.clone()])
        .num_epochs(config.num_epochs)
        .summary()
        .build(model, optimizer, config.learning_rate);

    let model_trained = learner.fit(train_dataloader, valid_dataloader);

    model_trained
        .save_file(format!("{artifact_dir}/model"), &CompactRecorder::new())
        .expect("Trained model should be saved successfully");
}
```

---

## 📊 Data Loading

### Dataset Implementation

```rust
use burn::data::{dataset::Dataset, dataloader::batcher::Batcher};

#[derive(Debug, Clone)]
pub struct MyDatasetItem {
    pub input: Vec<f32>,
    pub target: usize,
}

pub struct MyDataset {
    items: Vec<MyDatasetItem>,
}

impl Dataset<MyDatasetItem> for MyDataset {
    fn get(&self, index: usize) -> Option<MyDatasetItem> {
        self.items.get(index).cloned()
    }

    fn len(&self) -> usize {
        self.items.len()
    }
}

impl MyDataset {
    pub fn new(items: Vec<MyDatasetItem>) -> Self {
        Self { items }
    }

    pub fn from_csv(path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let mut items = Vec::new();
        let mut reader = csv::Reader::from_path(path)?;

        for result in reader.records() {
            let record = result?;
            let input: Vec<f32> = record.iter()
                .take(record.len() - 1)  // All but last column
                .map(|s| s.parse().unwrap())
                .collect();
            let target: usize = record.get(record.len() - 1).unwrap().parse()?;

            items.push(MyDatasetItem { input, target });
        }

        Ok(Self::new(items))
    }
}
```

### Custom Batcher

```rust
#[derive(Clone)]
pub struct MyBatch<B: Backend> {
    pub inputs: Tensor<B, 2>,
    pub targets: Tensor<B, 1, Int>,
}

#[derive(Clone)]
pub struct MyBatcher<B: Backend> {
    device: B::Device,
}

impl<B: Backend> MyBatcher<B> {
    pub fn new(device: B::Device) -> Self {
        Self { device }
    }
}

impl<B: Backend> Batcher<MyDatasetItem, MyBatch<B>> for MyBatcher<B> {
    fn batch(&self, items: Vec<MyDatasetItem>) -> MyBatch<B> {
        let batch_size = items.len();
        let input_size = items[0].input.len();

        let mut inputs = Vec::with_capacity(batch_size * input_size);
        let mut targets = Vec::with_capacity(batch_size);

        for item in items {
            inputs.extend(item.input);
            targets.push(item.target as i32);
        }

        let inputs = Tensor::from_floats(inputs.as_slice(), &self.device)
            .reshape([batch_size, input_size]);
        let targets = Tensor::from_ints(targets.as_slice(), &self.device);

        MyBatch { inputs, targets }
    }
}
```

### DataLoader Usage

```rust
use burn::data::dataloader::DataLoaderBuilder;

let dataset = MyDataset::from_csv("data.csv")?;
let batcher = MyBatcher::new(device.clone());

let dataloader = DataLoaderBuilder::new(batcher)
    .batch_size(32)
    .shuffle(42)  // Random seed
    .num_workers(4)
    .build(dataset);

// Usage in training loop
for batch in dataloader {
    let output = model.forward(batch.inputs);
    let loss = loss_fn.forward(output, batch.targets);
    // ... training step
}
```

---

## 💾 Model Persistence

### Saving and Loading Models

```rust
use burn::record::{CompactRecorder, BinBytesRecorder, DefaultFileRecorder};

// Save model
let recorder = CompactRecorder::new();
model.save_file("model.burn", &recorder)
    .expect("Failed to save model");

// Load model
let model: MyModel<Backend> = MyModel::new(&device);
let model = model.load_file("model.burn", &recorder, &device)
    .expect("Failed to load model");

// Different recorders
let compact_recorder = CompactRecorder::new();  // MessagePack + half precision
let default_recorder = DefaultFileRecorder::new();  // JSON format
let binary_recorder = BinBytesRecorder::new();  // Binary format

// Save with different precision
let model_record = model.into_record();
compact_recorder.record(model_record, "model.burn".into())?;
```

### PyTorch Model Import

```rust
use burn::record::PyTorchFileRecorder;

// Convert PyTorch model to Burn
let device = Default::default();
let pytorch_recorder = PyTorchFileRecorder::<FullPrecisionSettings>::default();

// Load PyTorch weights into Burn model
let model_record = pytorch_recorder.load("pytorch_model.pt".into(), &device)?;
let model = model.load_record(model_record);
```

### Record Configuration

```rust
use burn::record::{FullPrecisionSettings, HalfPrecisionSettings, Settings};

// Full precision (f32)
type FullPrecRecorder = CompactRecorder<FullPrecisionSettings>;

// Half precision (f16) for smaller file size
type HalfPrecRecorder = CompactRecorder<HalfPrecisionSettings>;

// Custom precision settings
#[derive(Debug)]
pub struct CustomSettings;

impl Settings for CustomSettings {
    type FloatElem = f64;  // Custom float precision
    type IntElem = i64;    // Custom int precision
}
```

---

## ⚙️ Backend Configuration

### WGPU Backend Setup

```rust
use burn_wgpu::{Wgpu, WgpuDevice, GraphicsApi, AutoGraphicsApi};

// Auto-select graphics API
type Backend = Autodiff<Wgpu<AutoGraphicsApi, f32, i32>>;
let device = WgpuDevice::default();

// Specific graphics API
let device = WgpuDevice::DiscreteGpu(0);  // First discrete GPU
let device = WgpuDevice::IntegratedGpu(0);  // Integrated GPU
let device = WgpuDevice::VirtualGpu(0);   // Virtual GPU

// Manual API selection
use burn_wgpu::{Vulkan, Metal, Dx12, OpenGl};
type VulkanBackend = Autodiff<Wgpu<Vulkan, f32, i32>>;
type MetalBackend = Autodiff<Wgpu<Metal, f32, i32>>;
```

### LibTorch Backend Setup

```rust
use burn_tch::{LibTorch, LibTorchDevice};

type Backend = Autodiff<LibTorch<f32>>;

// Device selection
let cpu_device = LibTorchDevice::Cpu;
let cuda_device = LibTorchDevice::Cuda(0);  // GPU 0
let mps_device = LibTorchDevice::Mps;       // Apple Metal

// Check device availability
if LibTorchDevice::cuda_is_available() {
    let device = LibTorchDevice::Cuda(0);
} else {
    let device = LibTorchDevice::Cpu;
}
```

### Multi-GPU Training

```rust
// Multi-device setup
let devices = vec![
    WgpuDevice::DiscreteGpu(0),
    WgpuDevice::DiscreteGpu(1),
];

let learner = LearnerBuilder::new(artifact_dir)
    .devices(devices)  // Multi-GPU training
    .build(model, optimizer, learning_rate);
```

---

## 🔧 Advanced Features

### Custom Kernels (WGPU)

```rust
use burn_wgpu::kernel::{KernelSource, StaticKernelSource};

const CUSTOM_KERNEL: &str = "
@group(0) @binding(0)
var<storage, read> input: array<f32>;

@group(0) @binding(1)
var<storage, read_write> output: array<f32>;

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) global_id: vec3<u32>) {
    let index = global_id.x;
    if (index >= arrayLength(&input)) {
        return;
    }

    output[index] = input[index] * 2.0;  // Custom operation
}
";

pub struct DoubleKernel;

impl StaticKernelSource for DoubleKernel {
    fn source() -> KernelSource {
        KernelSource::Wgsl(CUSTOM_KERNEL.into())
    }
}
```

### Automatic Differentiation

```rust
// Enable gradient computation
let tensor = tensor.require_grad();

// Forward pass
let output = model.forward(tensor);
let loss = loss_fn.forward(output, targets);

// Backward pass
let grads = loss.backward();

// Extract gradients for specific tensors
if let Some(grad) = tensor.grad(&grads) {
    println!("Gradient: {:?}", grad);
}

// Custom backward function
fn custom_function<B: AutodiffBackend>(
    x: Tensor<B, 2>
) -> Tensor<B, 2> {
    // Custom forward computation
    let output = x.clone().powf_scalar(2.0);

    // Register backward function if needed
    output
}
```

### Memory Management

```rust
// Explicit memory cleanup
tensor.detach();  // Remove from computation graph

// Move to different device
let tensor_gpu = tensor.to_device(&gpu_device);

// Check memory usage
let memory_info = device.memory_info();

// Force garbage collection (backend-specific)
device.sync();
```

---

## 🐛 Debugging and Best Practices

### Error Handling

```rust
use burn::tensor::TensorError;

// Handle tensor operations safely
match tensor1.matmul(tensor2) {
    Ok(result) => result,
    Err(e) => panic!("Matrix multiplication failed: {:?}", e),
}

// Check tensor shapes before operations
assert_eq!(tensor1.dims(), [batch_size, features]);
assert_eq!(tensor2.dims(), [features, output_size]);
```

### Performance Tips

```rust
// Use in-place operations when possible
tensor.relu_();  // In-place ReLU
tensor += 1.0;   // In-place addition

// Batch operations
let batched_tensor = Tensor::stack::<3>(tensors, 0);
let results = model.forward(batched_tensor);

// Avoid unnecessary clones
let result = tensor.matmul(weight);  // tensor consumed
// Instead of: tensor.clone().matmul(weight)

// Use appropriate data types
type FastBackend = Autodiff<Wgpu<AutoGraphicsApi, f16, i32>>;  // Half precision for speed
```

### Type Safety

```rust
// Use const generics for compile-time shape checking
fn matrix_multiply<B: Backend, const N: usize, const M: usize, const K: usize>(
    a: Tensor<B, 2>,  // [N, M]
    b: Tensor<B, 2>,  // [M, K]
) -> Tensor<B, 2> {   // [N, K]
    a.matmul(b)
}

// Explicit tensor kinds
let float_tensor: Tensor<Backend, 2, Float> = Tensor::zeros([2, 3], &device);
let int_tensor: Tensor<Backend, 1, Int> = Tensor::from_ints([1, 2, 3], &device);
let bool_tensor: Tensor<Backend, 2, Bool> = float_tensor.greater_elem(0.5);
```

---

## 📋 Migration from PyTorch

### Key Differences

| PyTorch | Burn | Notes |
|---------|------|--------|
| `torch.tensor()` | `Tensor::from_data()` | Explicit device required |
| `.cuda()` | `.to_device(&device)` | Generic device abstraction |
| `model.train()` | No equivalent | No global training state |
| `model.eval()` | `model.valid()` | Explicit validation mode |
| `loss.backward()` | `loss.backward()` | Returns gradients object |
| `optimizer.step()` | Manual step | More explicit control |

### Common Patterns

```rust
// PyTorch: x = torch.randn(2, 3).cuda()
let x = Tensor::<Backend, 2>::random([2, 3], Distribution::Default, &device);

// PyTorch: y = F.relu(x)
let y = x.relu();

// PyTorch: loss = F.cross_entropy(logits, targets)
let loss = CrossEntropyLossConfig::new().init(&device).forward(logits, targets);

// PyTorch: optimizer.zero_grad(); loss.backward(); optimizer.step()
let grads = loss.backward();
let model = optimizer.step(learning_rate, model, grads);
```

---

## 🔗 Useful Resources

### Documentation

- [Official Burn Book](https://burn.dev/book/)
- [API Documentation](https://docs.rs/burn/)
- [Examples Repository](https://github.com/tracel-ai/burn/tree/main/examples)

### Community

- [GitHub Discussions](https://github.com/tracel-ai/burn/discussions)
- [Discord Server](https://discord.gg/uPEBbYYDB6)

### Example Projects

```bash
# Clone examples
git clone https://github.com/tracel-ai/burn.git
cd burn/examples

# MNIST CNN training
cd mnist
cargo run --release

# Text classification
cd text-classification
cargo run --release -- --dataset ag_news

# Image classification web demo
cd image-classification-web
trunk serve
```

---

*This cheatsheet covers Burn v0.14+ (latest stable). Always refer to official documentation for the most up-to-date information.*

## Related Concepts

### Prerequisites
- [[cargo]] - Cargo required to build and manage Burn dependencies

### Related Topics
- [[cubecl]] - CubeCL provides GPU compute backend for Burn
- [[numpy_pytorch_rust_guide]] - Burn tensors are Rust equivalent to NumPy/PyTorch tensors
- [[optimization]] - Burn includes optimization algorithms for training
- [[cpu_vs_gpu_decision_guide]] - Burn supports both CPU and GPU backends with different characteristics

### Extended By
- [[best_practices]] - Burn framework follows Rust best practices