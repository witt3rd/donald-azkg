# C++ Specification

## C++23 Modern Output: std::format, std::print, and std::println

C++23 introduces `std::format` and `std::print`/`std::println` to modernize and unify C++ output, directly inspired by the fmt library. This new approach replaces much of the need for the traditional `std::cout` and brings Python-style formatting to standard C++.

### Key Features

- **std::format** (C++20): Provides type-safe, composable string formatting, similar to Python's f-strings and inspired by fmt's format syntax
- **std::print** and **std::println** (C++23): Allow direct formatted output to standard output (or a file/stream), bypassing iostreams while supporting std::format's formatting
- The fmt library pioneered this model; C++20 adopted std::format, and C++23 added std::print, bringing comprehensive support into the standard library

### Code Examples

#### Traditional std::cout Usage (Pre-C++23)

```cpp
#include <iostream>
#include <string>

int main() {
    int value = 42;
    std::string name = "Alice";
    std::cout << "Hello, " << name << "! The answer is " << value << ".\n";
}
```

Manual concatenation and type conversion; no format specifiers; slower and less readable.

#### C++23 std::format + std::print / std::println

```cpp
#include <format>
#include <print>

int main() {
    int value = 42;
    std::string name = "Alice";

    // Just format (returns std::string)
    std::string message = std::format("Hello, {}! The answer is {}.", name, value);

    // Print formatted string directly
    std::print("Hello, {}! The answer is {}.\n", name, value);

    // Or use println for automatic newline
    std::println("Hello, {}! The answer is {}", name, value);
}
```

No `std::cout` needed, supports all std::format features directly. Output is type-safe, efficient, and simple to extend.

### Benefits Over std::cout

- **Type safety**: Arguments are checked at compile time; format errors are runtime exceptions, not silent bugs
- **Performance**: std::print is faster than std::cout and printf due to efficient handling and less overhead
- **Unicode reliability**: More robust handling of Unicode, especially on Windows
- **Locale handling**: By default, std::format/std::print do not use locale, giving predictable cross-platform results
- **Simple syntax**: More readable and maintainable, reduces error-prone string manipulation

### Feature Comparison

| Feature            | std::cout         | fmt Library / std::format   | std::print / std::println       |
|--------------------|------------------|-----------------------------|---------------------------------|
| Format Specifiers  | No               | Yes                         | Yes                             |
| Type Safety        | Partial          | Full                        | Full                            |
| Unicode Output     | Platform-dependent| Good (fmt), Better (std::print)| Better                          |
| Performance        | Moderate         | Fast                        | Fastest (often)                 |
| Syntax             | Verbose          | Concise                     | Concise                         |

### Summary

- **std::format** in C++20/23 replaces `fmt::format` for standard string formatting
- **std::print** and **std::println** offer direct, type-safe formatted outputremoving most use cases for `std::cout`, and supporting format strings natively
- You can now write concise, performant, and maintainable output code using the core language tools
- For advanced tasks (e.g., formatting ranges, custom delimiters), the fmt library remains richer until future C++ standards close the gap
