---
tags: [rust, cargo, build-tools, package-manager, reference, cheatsheet]
---

# Comprehensive Cargo Cheatsheet & Reference Guide

This comprehensive guide covers everything you need to know about using Cargo, Rust's package manager and build tool, from your Windows PowerShell command line to be maximally productive.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Creation & Management](#project-creation--management)
3. [Building & Running](#building--running)
4. [Dependency Management](#dependency-management)
5. [Testing & Debugging](#testing--debugging)
6. [Code Quality & Formatting](#code-quality--formatting)
7. [Documentation](#documentation)
8. [Performance Analysis](#performance-analysis)
9. [Workspace Management](#workspace-management)
10. [Publishing & Distribution](#publishing--distribution)
11. [Toolchain Management](#toolchain-management)
12. [Advanced Configuration](#advanced-configuration)
13. [Essential Commands Reference](#essential-commands-reference)

## Getting Started

### Basic Information Commands

```powershell
# Check Cargo version
cargo --version

# List all available commands
cargo --list

# Get help for any command
cargo help <command>
cargo <command> --help

# Show all help topics
cargo --help
```

### Project Structure Understanding

Cargo follows specific conventions for project structure[1]:

```
your_project/
├── Cargo.toml          # Project manifest
├── Cargo.lock          # Dependency lock file (auto-generated)
├── src/
│   ├── main.rs         # Binary crate entry point
│   ├── lib.rs          # Library crate entry point
│   └── bin/            # Additional binary targets
├── examples/           # Example code
├── tests/              # Integration tests
├── benches/            # Benchmarks
└── target/             # Build artifacts
```

## Project Creation & Management

### Creating New Projects

```powershell
# Create a new binary project
cargo new my_project

# Create a new library project
cargo new my_library --lib

# Initialize Cargo in existing directory
cargo init

# Initialize as library in existing directory
cargo init --lib
```

### Project Information

```powershell
# Check project for errors (fast, no linking)
cargo check

# Verify project configuration
cargo metadata

# Display dependency tree
cargo tree

# Find project location
cargo locate-project
```

## Building & Running

### Build Commands

```powershell
# Build in debug mode (default)
cargo build

# Build in release mode (optimized)
cargo build --release

# Build all targets
cargo build --all-targets

# Build specific binary
cargo build --bin my_binary

# Build for specific target
cargo build --target x86_64-pc-windows-gnu
```

### Running Programs

```powershell
# Run the main binary
cargo run

# Run in release mode
cargo run --release

# Run specific binary
cargo run --bin my_binary

# Pass arguments to your program
cargo run -- arg1 arg2 --flag

# Run with specific features
cargo run --features "feature1,feature2"
```

### Build Profiles

Configure build profiles in `Cargo.toml`[2]:

```toml
[profile.dev]
opt-level = 0
debug = true
overflow-checks = true

[profile.release]
opt-level = 3
debug = false
lto = true

# Custom profile (Rust 1.57+)
[profile.release-with-debug]
inherits = "release"
debug = true
```

Use custom profiles:

```powershell
cargo build --profile release-with-debug
```

## Dependency Management

### Adding Dependencies

```powershell
# Add a dependency
cargo add serde

# Add with specific version
cargo add serde@1.0.193

# Add dev dependency
cargo add --dev tokio

# Add build dependency
cargo add --build cc

# Add with features
cargo add serde --features derive
```

### Updating Dependencies

```powershell
# Update all dependencies
cargo update

# Update specific dependency
cargo update serde

# Update to precise version
cargo update serde --precise 1.0.193

# Conservative update (workspace)
cargo update --workspace
```

### Removing Dependencies

```powershell
# Remove dependency
cargo remove serde

# Remove dev dependency
cargo remove --dev tokio

# Remove build dependency
cargo remove --build cc
```

### Dependency Analysis

```powershell
# Show dependency tree
cargo tree

# Show dependencies of specific package
cargo tree -p serde

# Show duplicate dependencies
cargo tree --duplicates

# Find unused dependencies (requires cargo-machete)
cargo install cargo-machete
cargo machete
```

## Testing & Debugging

### Testing Commands

```powershell
# Run all tests
cargo test

# Run tests in release mode
cargo test --release

# Run specific test
cargo test test_name

# Run tests with output
cargo test -- --nocapture

# Run tests matching pattern
cargo test integration

# Run tests for specific package
cargo test -p my_package

# Build test binaries without running
cargo test --no-run
```

### Debugging

For debugging in Windows PowerShell, you can use various approaches:

```powershell
# Build with debug symbols
cargo build

# Run with debugger (requires cargo-debug)
cargo install cargo-debug
cargo debug run

# Build test binary for debugging
cargo test --no-run
# Then debug the binary in target/debug/deps/
```

### Debugging with Visual Studio

```powershell
# Build with debug info for Visual Studio
cargo build --profile dev
# Or add to Cargo.toml:
# [profile.dev]
# debug = 2
```

## Code Quality & Formatting

### Formatting

```powershell
# Format all code
cargo fmt

# Format specific files
cargo fmt src/main.rs

# Check formatting without changing files
cargo fmt --check

# Format with specific toolchain
cargo +nightly fmt
```

### Linting with Clippy

```powershell
# Run clippy (linter)
cargo clippy

# Run clippy with all targets
cargo clippy --all-targets

# Run clippy with specific features
cargo clippy --features "feature1,feature2"

# Treat warnings as errors
cargo clippy -- -D warnings
```

### Automatic Fixes

```powershell
# Automatically fix compiler warnings
cargo fix

# Fix for specific edition
cargo fix --edition

# Fix with all features
cargo fix --all-features

# Fix for specific target
cargo fix --target x86_64-pc-windows-gnu
```

## Documentation

### Building Documentation

```powershell
# Build documentation
cargo doc

# Build and open in browser
cargo doc --open

# Build without dependencies
cargo doc --no-deps

# Include private items
cargo doc --document-private-items

# Build for specific package
cargo doc -p my_package
```

### Documentation Examples

```powershell
# Test documentation examples
cargo test --doc

# Run specific doc test
cargo test --doc test_name
```

## Performance Analysis

### Benchmarking

```powershell
# Run benchmarks (requires nightly)
cargo +nightly bench

# Run specific benchmark
cargo +nightly bench bench_name

# Run benchmarks with Criterion (if using criterion crate)
cargo bench
```

### Profiling

#### Using cargo-flamegraph (Windows compatible)

```powershell
# Install flamegraph
cargo install flamegraph

# Profile your application
cargo flamegraph

# Profile release build
cargo flamegraph --release

# Profile specific binary
cargo flamegraph --bin my_binary

# Profile with custom output
cargo flamegraph -o profile.svg
```

#### Using Windows Performance Toolkit

```powershell
# Build with release optimizations but with debug symbols
cargo build --release
# Then profile with Windows Performance Analyzer (WPA)
```

### Performance Monitoring

```powershell
# Time compilation
cargo build --timings

# Verbose output for build analysis
cargo build -v

# Show why crate was rebuilt
cargo build --explain
```

## Workspace Management

### Creating Workspaces

Create a workspace `Cargo.toml` in the root directory[3]:

```toml
[workspace]
resolver = "2"
members = [
    "app",
    "lib1",
    "lib2",
]

[workspace.dependencies]
serde = "1.0"
```

### Workspace Commands

```powershell
# Build entire workspace
cargo build --workspace

# Test entire workspace
cargo test --workspace

# Run command for specific package
cargo run -p my_app

# Check entire workspace
cargo check --workspace

# Clean workspace
cargo clean --workspace
```

## Publishing & Distribution

### Package Management

```powershell
# Search for packages
cargo search serde

# Get package info
cargo info serde

# Create package tarball
cargo package

# Publish to crates.io
cargo publish

# Publish dry run
cargo publish --dry-run
```

### Authentication

```powershell
# Login to crates.io
cargo login

# Logout
cargo logout

# Use specific registry
cargo login --registry my-registry
```

## Toolchain Management

### Rustup Integration

```powershell
# Update Rust toolchain
rustup update

# Update specific toolchain
rustup update stable

# Update rustup itself
rustup self update

# List installed toolchains
rustup toolchain list

# Install specific toolchain
rustup toolchain install nightly

# Use specific toolchain for command
cargo +nightly build
```

### Component Management

```powershell
# Install rustfmt
rustup component add rustfmt

# Install clippy
rustup component add clippy

# Install rust-src for IDE support
rustup component add rust-src

# Install rust-analyzer
rustup component add rust-analyzer
```

## Advanced Configuration

### Cargo Configuration

Create `.cargo/config.toml` in your project or globally[4]:

```toml
[build]
target = "x86_64-pc-windows-msvc"
rustflags = ["-C", "target-cpu=native"]

[target.x86_64-pc-windows-msvc]
linker = "link.exe"

[registry]
default = "crates-io"

[net]
retry = 3
```

### Environment Variables

```powershell
# Set target directory
$env:CARGO_TARGET_DIR = "custom_target"

# Enable debug logging
$env:CARGO_LOG = "debug"

# Set install root
$env:CARGO_INSTALL_ROOT = "C:\tools\cargo"

# Network debug
$env:CARGO_HTTP_DEBUG = "true"
```

### Features and Conditional Compilation

In `Cargo.toml`:

```toml
[features]
default = ["std"]
std = []
serde = ["dep:serde"]
experimental = []

[dependencies]
serde = { version = "1.0", optional = true }
```

Use features:

```powershell
cargo build --features "serde,experimental"
cargo build --all-features
cargo build --no-default-features
```

## Essential Commands Reference

### Daily Development Commands

```powershell
# Quick project setup
cargo new my_project && cd my_project

# Development cycle
cargo check          # Fast error checking
cargo test           # Run tests
cargo run            # Run program
cargo clippy         # Linting
cargo fmt            # Formatting

# Dependency management
cargo add package_name
cargo remove package_name
cargo update

# Build variations
cargo build --release
cargo run --release
cargo test --release

# Cleanup
cargo clean
```

### Maintenance Commands

```powershell
# Project health
cargo audit           # Security audit (requires cargo-audit)
cargo outdated        # Check for outdated deps (requires cargo-outdated)
cargo tree --duplicates

# Documentation
cargo doc --open

# Performance
cargo bench
cargo flamegraph --release
```

### Global Tool Installation

```powershell
# Essential tools
cargo install cargo-edit      # cargo add/remove
cargo install cargo-audit     # Security auditing
cargo install cargo-outdated  # Check outdated deps
cargo install cargo-tree      # Dependency tree
cargo install cargo-watch     # Auto-rebuild on changes
cargo install flamegraph      # Performance profiling
cargo install cargo-expand    # Macro expansion
cargo install cargo-machete   # Find unused deps
```

### Useful Aliases

Add these to your PowerShell profile:

```powershell
# Cargo aliases
function cr { cargo run $args }
function cb { cargo build $args }
function ct { cargo test $args }
function cc { cargo check $args }
function cf { cargo fmt $args }
function cl { cargo clippy $args }
function cu { cargo update $args }
```

## Tips for Windows PowerShell

### Environment Setup

```powershell
# Ensure Cargo is in PATH
$env:PATH += ";$env:USERPROFILE\.cargo\bin"

# Set default editor
$env:EDITOR = "code"  # or "notepad" or your preferred editor

# Performance: Use local cargo registry mirror if available
$env:CARGO_NET_OFFLINE = "true"  # For offline development
```

### Common Issues and Solutions

1. **Long path issues**: Enable long path support in Windows
2. **Antivirus interference**: Add cargo target directory to exclusions
3. **Permissions**: Run as administrator only when necessary
4. **Network issues**: Configure proxy settings in `.cargo/config.toml`

This comprehensive guide should enable you to be highly productive with Cargo from your Windows PowerShell environment. Each section provides practical commands and configurations you'll use regularly in Rust development.


## Related Concepts

### Related Topics

- [[burn]] - Cargo manages Burn framework dependencies