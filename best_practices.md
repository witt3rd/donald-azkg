---
tags: [reference, guide, api, best-practices, patterns]
---

# Rust Best Practices - Distilled

A concise guide to idiomatic Rust patterns for maintainable, type-safe code.

## Import Conventions

### Functions vs Types Convention

```rust
// For FUNCTIONS: Import the parent module
use std::fs;  // ✅ Then: fs::read_to_string()
use std::io;  // ✅ Then: io::stdin()

// For TYPES: Import the item directly
use std::collections::HashMap;  // ✅ Then: HashMap::new()
use std::path::PathBuf;        // ✅ Then: PathBuf::from()
```

### Import Organization (Three Sections)

```rust
// Standard library imports (alphabetically sorted)
use std::collections::HashMap;
use std::io::{self, Read, Write};

// External crate imports (alphabetically sorted)
use regex::Regex;
use reqwest::Client;

// Internal imports (when in library code)
use crate::config::Config;
use crate::utils::helpers;
```

### Key Principles

1. **Avoid glob imports** except in tests and designed preludes
2. **Import traits explicitly** when you need their methods
3. **Use `as` for conflicts**: `use std::io::Result as IoResult;`
4. **Be consistent** within your codebase

## Type-Safe Configuration with Enums

### Prefer Enums Over Strings for CLI Arguments

```rust
// ❌ Avoid: String-based configuration
#[derive(Parser)]
struct Args {
    #[arg(default_value = "json")]
    format: String,  // Runtime validation needed
}

// ✅ Prefer: Enum with clap's ValueEnum
#[derive(Debug, Clone, Copy, clap::ValueEnum)]
enum OutputFormat {
    /// JSON output format
    Json,
    /// YAML output format
    Yaml,
    /// Plain text output
    Text,
}

#[derive(Parser)]
struct Args {
    #[arg(value_enum, default_value = "json")]
    format: OutputFormat,
}
```

### Benefits of Enum-Based Configuration

1. **Compile-time validation** - Invalid values caught during compilation
2. **IDE support** - Auto-completion and type hints
3. **Self-documenting** - `--help` shows all valid options
4. **Exhaustive matching** - Compiler ensures all cases handled
5. **Refactoring safety** - Renaming variants updates all usages

### Implementation Pattern

```rust
// Implement Display for user-friendly output
impl fmt::Display for OutputFormat {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            OutputFormat::Json => write!(f, "json"),
            OutputFormat::Yaml => write!(f, "yaml"),
            OutputFormat::Text => write!(f, "text"),
        }
    }
}

// Use exhaustive matching
match args.format {
    OutputFormat::Json => output_json(&data),
    OutputFormat::Yaml => output_yaml(&data),
    OutputFormat::Text => output_text(&data),
    // No default case needed - compiler ensures completeness
}
```

### When to Use This Pattern

- CLI argument parsing with fixed set of options
- Configuration files with known variants
- State machines with defined states
- Any scenario where string comparison would be error-prone

## Smart Pointer Selection: Arc vs Vec

### When to Use Arc Instead of Vec

A common pattern in Rust is using `Arc<[T]>` (atomically reference-counted slice) instead of `Vec<T>` for specific scenarios involving large, immutable data that needs to be shared efficiently.

#### Key Reasons to Use Arc

1. **Efficient Cloning**
   - Cloning an `Arc` is O(1) - just increments reference count
   - Cloning a `Vec` is O(n) - allocates new memory and copies all data
   
2. **Memory Layout**
   - `Arc<[T]>`: 16 bytes (pointer + length)
   - `Vec<T>`: 24 bytes (pointer + length + capacity)
   - Better cache locality with many instances

3. **Immutability Guarantee**
   - `Vec` is designed for mutability (push/pop/insert/remove)
   - `Arc` makes immutability explicit at the type level
   - Prevents accidental modifications

4. **Thread Safety**
   - `Arc` enables safe sharing between threads
   - `Rc` is single-threaded only

5. **Ergonomic API**
   - `Arc<[T]>` implements `Deref` to `&[T]`
   - Works seamlessly where slices are expected

### Usage Guidelines

| Use Case | Recommended Type |
|----------|-----------------|
| Mutable, resizable data owned by one thread | `Vec<T>` |
| Immutable shared data (single-thread) | `Rc<[T]>` or `Arc<[T]>` |
| Immutable shared data (multi-thread) | `Arc<[T]>` |
| No sharing needed | `Box<[T]>` or slice |

### Example Pattern

```rust
// ❌ Avoid: Cloning large vectors repeatedly
struct Config {
    data: Vec<String>,  // Expensive to clone
}

// ✅ Prefer: Efficient reference counting
struct Config {
    data: Arc<[String]>,  // Cheap to clone
}

// Construction
let data: Vec<String> = load_data();
let config = Config {
    data: data.into(),  // Vec<T> -> Arc<[T]>
};

// Cloning is now O(1)
let config_clone = config.clone();
```

### When to Use Each

**Use `Vec<T>` when:**
- Data needs to be modified after creation
- Single ownership is sufficient
- Building data incrementally

**Use `Arc<[T]>` when:**
- Data is constructed once, read many times
- Frequently cloning/sharing large sequences
- Sharing across threads
- Optimizing for clone performance

**Consider `Rc<[T]>` when:**
- Same as Arc but single-threaded only
- Slightly better performance (no atomics)

**Consider `Box<[T]>` when:**
- No sharing needed
- Want simplest immutable container

## Summary

These patterns form the foundation of idiomatic Rust:

- **Import conventions** ensure readable, maintainable code
- **Enum-based configuration** leverages Rust's type system for safety
- **Smart pointer selection** optimizes performance and safety
- **Compiler-driven development** catches errors early
- **Explicit over implicit** makes code self-documenting

>

## Related Concepts

### Related Topics
- [[cli_rust]] - Best practices demonstrate enum-based CLI argument handling
- [[cargo]] - Cargo project structure follows Rust best practices

### Examples
- [[cli_rust]] - CLI guide shows practical application of best practices
- [[burn]] - Burn framework follows Rust best practices