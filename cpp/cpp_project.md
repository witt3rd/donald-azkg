# C++ Project Setup on Windows with VS Code - Best Practices

## The Core Problem and Solution

**Problem**: VS Code and its extensions don't inherit PowerShell profiles, so they can't find tools configured there.

**Solution**: Set environment variables at the SYSTEM level, not in PowerShell profiles.

## Prerequisites

### 1. Install Development Tools

Use WinGet for consistent, system-wide installations:

```powershell
# CMake - Build system generator
winget install Kitware.CMake

# LLVM/Clang - Complete compiler toolchain
winget install LLVM.LLVM

# Ninja - Fast build system
winget install Ninja-build.Ninja

# VS Code
winget install Microsoft.VisualStudioCode
```

### 2. Install vcpkg

```powershell
git clone https://github.com/Microsoft/vcpkg.git C:\vcpkg
cd C:\vcpkg
.\bootstrap-vcpkg.bat
```

#### Integrate vcpkg with shells and buildsystems

```powershell
vcpkg integrate install
```

Integrates with Visual Studio (Windows-only), sets the user-wide vcpkg instance, and displays CMake integration help.

On Windows with Visual Studio 2015, this subcommand will add redirecting logic into the MSBuild installation which will automatically pick up each user's user-wide vcpkg instance. Visual Studio 2017 and newer have this logic in the box.

To set the user-wide vcpkg instance, vcpkg creates a few short files containing the absolute path to the vcpkg instance inside the user's user-wide configuration location:

- `%LOCALAPPDATA%\vcpkg` or `%APPDATA%\Local\vcpkg` on Windows
- `$HOME/.vcpkg` or `/var/.vcpkg` on non-Windows

Displays the full path to the CMake toolchain file. Running this command is not required to use the toolchain file.

```powershell
vcpkg integrate project
```

Creates a linked NuGet package for MSBuild integration.

See MSBuild Per-Project Integration for more information.

```powershell
vcpkg integrate powershell
```

Windows only
Adds vcpkg tab-completion support to the current user's Powershell profile.

### 3. Set System Environment Variables

**Required system environment variables:**

| Variable | Value | Description |
|----------|-------|-------------|
| `VCPKG_ROOT` | `C:\vcpkg` (or your vcpkg location) | Points to vcpkg installation |

**Setting VCPKG_ROOT in PowerShell:**

```powershell
# Set for current user (permanent)
[System.Environment]::SetEnvironmentVariable("VCPKG_ROOT", "C:\vcpkg", "User")

# Or set system-wide (requires admin)
[System.Environment]::SetEnvironmentVariable("VCPKG_ROOT", "C:\vcpkg", "Machine")

# Apply to current session
$env:VCPKG_ROOT = "C:\vcpkg"
```

**Required in system PATH:**

| Tool | Typical Path | Notes |
|------|--------------|-------|
| CMake | `C:\Program Files\CMake\bin` | From WinGet installation |
| LLVM/Clang | `C:\Program Files\LLVM\bin` | Must appear BEFORE any Visual Studio paths |
| Ninja | `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Ninja-build.Ninja_*` | Path varies with WinGet version |

**How to set:** Use System Properties → Environment Variables, or run `set-system-env.ps1` as Administrator (see repository).

**Important:** After setting, restart your computer or log out/in for changes to take effect.

### 4. Install VS Code Extensions

Required:

- **CMake Tools** (ms-vscode.cmake-tools)
- **C/C++** (ms-vscode.cpptools)
- **clangd** (llvm-vs-code-extensions.vscode-clangd) - For better IntelliSense

## Project Structure

```
MyProject/
├── CMakeLists.txt          # Build configuration
├── CMakePresets.json       # Build presets
├── .clangd                 # Clangd configuration
├── .gitignore
├── .vscode/
│   ├── settings.json       # VS Code settings
│   └── extensions.json     # Recommended extensions
├── src/
│   └── main.cpp
└── out/                    # Build output (gitignored)
    ├── windows-x64-debug/
    ├── windows-arm64-debug/
    └── vs2022-x64/         # Visual Studio solutions
```

## Essential Configuration Files

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 4.1)

# vcpkg integration - must be set before project()
# Priority: CMAKE_TOOLCHAIN_FILE (from presets) > VCPKG_ROOT env var
if(NOT DEFINED CMAKE_TOOLCHAIN_FILE)
    if(DEFINED ENV{VCPKG_ROOT} AND NOT "$ENV{VCPKG_ROOT}" STREQUAL "")
        set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE STRING "vcpkg toolchain file")
        message(STATUS "Using vcpkg from VCPKG_ROOT: $ENV{VCPKG_ROOT}")
    else()
        message(WARNING "Neither CMAKE_TOOLCHAIN_FILE nor VCPKG_ROOT is set. Please set VCPKG_ROOT environment variable or use CMake presets.")
    endif()
else()
    message(STATUS "Using vcpkg toolchain: ${CMAKE_TOOLCHAIN_FILE}")
endif()

project(MyProject CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)  # For clangd

add_executable(${PROJECT_NAME} src/main.cpp)

# Find and link dependencies from vcpkg.json
find_package(fmt CONFIG REQUIRED)
find_package(spdlog CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

target_link_libraries(${PROJECT_NAME}
    PRIVATE
        fmt::fmt
        spdlog::spdlog
        nlohmann_json::nlohmann_json
)

# Set as Visual Studio startup project (if using VS generator)
if(CMAKE_GENERATOR MATCHES "Visual Studio")
    set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                 PROPERTY VS_STARTUP_PROJECT ${PROJECT_NAME})
endif()
```

### CMakePresets.json (Architecture-aware with vcpkg integration)

```json
{
  "version": 3,
  "configurePresets": [
    {
      "name": "windows-base",
      "hidden": true,
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/out/${presetName}",
      "cacheVariables": {
        "CMAKE_C_COMPILER": "clang",
        "CMAKE_CXX_COMPILER": "clang++",
        "CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
      }
    },
    {
      "name": "windows-x64-debug",
      "inherits": "windows-base",
      "displayName": "Windows x64 Debug",
      "architecture": {"value": "x64", "strategy": "external"},
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "VCPKG_TARGET_TRIPLET": "x64-windows"
      }
    },
    {
      "name": "windows-arm64-debug",
      "inherits": "windows-base",
      "displayName": "Windows ARM64 Debug",
      "architecture": {"value": "arm64", "strategy": "external"},
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "VCPKG_TARGET_TRIPLET": "arm64-windows"
      }
    }
    // Plus release variants and VS2022 presets
  ]
}
```

### .clangd

```yaml
# Point clangd to the compile_commands.json for IntelliSense
# Update path based on your architecture:
#   out/windows-x64-debug    (for x64)
#   out/windows-arm64-debug  (for ARM64)
CompileFlags:
  CompilationDatabase: out/windows-arm64-debug  # Change based on your architecture
```

### .vscode/settings.json

```json
{
  "cmake.configureOnOpen": true,
  "cmake.useCMakePresets": "always",

  // Disable Microsoft IntelliSense for clangd
  "C_Cpp.intelliSenseEngine": "disabled",

  // clangd configuration
  "clangd.arguments": [
    "--header-insertion=never",
    "--clang-tidy",
    "--background-index",
    "--completion-style=detailed"
  ]
}
```

### .vscode/extensions.json

```json
{
  "recommendations": [
    "ms-vscode.cmake-tools",
    "ms-vscode.cpptools",
    "llvm-vs-code-extensions.vscode-clangd"
  ]
}
```

### Debugging

**Note**: VS Code does not currently support native debugging on Windows ARM64 with Clang. For debugging with breakpoints, use Visual Studio:

1. Generate a Visual Studio solution:

   ```powershell
   cmake --preset vs2022-x64    # For x64
   cmake --preset vs2022-arm64  # For ARM64
   ```

2. Open the solution in Visual Studio:

   ```powershell
   start out\vs2022-x64\MyProject.sln  # or vs2022-arm64
   ```

3. Set breakpoints and press `F5` to debug in Visual Studio

### src/main.cpp (Example with vcpkg dependencies)

```cpp
#include <iostream>
#include <fmt/core.h>
#include <fmt/color.h>
#include <spdlog/spdlog.h>
#include <nlohmann/json.hpp>

int main(int argc, char* argv[]) {
    // Using fmt for formatted output with colors
    fmt::print(fg(fmt::color::cyan), "=== C++ Template Demo ===\n\n");

    // Using spdlog for logging
    spdlog::info("Application started with {} arguments", argc);

    // Using nlohmann-json
    nlohmann::json config = {
        {"name", "MyProject"},
        {"version", "1.0.0"},
        {"features", {"logging", "json", "formatting"}}
    };

    fmt::print("Configuration:\n");
    fmt::print(fg(fmt::color::green), "{}\n", config.dump(2));

    spdlog::info("Application completed successfully");
    return 0;
}
```

### .gitignore

```gitignore
# Build outputs
out/
build/

# IDE
.vs/
.vscode/*.local.json

# CMake
CMakeUserPresets.json
compile_commands.json

# vcpkg (if using manifest mode)
vcpkg_installed/
```

## Example Dependencies: vcpkg.json

The template includes a sample `vcpkg.json` file demonstrating how to use common C++ libraries:

```json
{
  "name": "myproject",
  "version": "1.0.0",
  "dependencies": [
    "fmt",           // Modern formatting library
    "spdlog",        // Fast C++ logging library
    "nlohmann-json"  // JSON for Modern C++
  ]
}
```

**Note**: This vcpkg.json is included as a working example. The sample code in `src/main.cpp` uses these libraries to demonstrate IntelliSense, auto-completion, and proper linking. You can modify or replace this file with your own dependencies.

## Usage

### VS Code Workflow

1. **Open project folder in VS Code**
   - CMake Tools auto-configures on open

2. **Use Command Palette** (`Ctrl+Shift+P`):
   - `CMake: Select Configure Preset` - Choose build configuration
   - `CMake: Configure` - Configure the project
   - `CMake: Build` - Build the project
   - `CMake: Run Without Debugging` - Run the executable (or `Ctrl+F5`)

3. **For debugging**: Generate and use Visual Studio solution (see Debugging section above)

3. **Or use the CMake status bar** (bottom of VS Code)

### Command Line Workflow

```powershell
# Configure (choose based on your architecture)
cmake --preset windows-x64-debug    # For x64 systems
cmake --preset windows-arm64-debug  # For ARM64 systems

# Build
cmake --build --preset windows-x64-debug    # or windows-arm64-debug

# Run
.\out\windows-x64-debug\MyProject.exe      # or windows-arm64-debug
```

### Generate Visual Studio Solution

```powershell
# Configure with VS preset (choose your architecture)
cmake --preset vs2022-x64    # For x64
cmake --preset vs2022-arm64  # For ARM64

# Open in Visual Studio
start out\vs2022-x64\MyProject.sln  # or vs2022-arm64
```

Or from VS Code:

1. `Ctrl+Shift+P` → `CMake: Select Configure Preset`
2. Choose "Visual Studio 2022"
3. Run `CMake: Configure`

## Adding Dependencies with vcpkg

1. Modify the existing `vcpkg.json` or replace it with your own dependencies
2. Update `CMakeLists.txt` to find and link packages:

```cmake
find_package(your_package CONFIG REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE your_package::your_package)
```

4. CMake automatically installs dependencies during configuration

**Note**: The template's sample code demonstrates using fmt, spdlog, and nlohmann-json. These provide:

- **fmt**: Modern string formatting and colored console output
- **spdlog**: High-performance logging with multiple sinks
- **nlohmann-json**: Intuitive JSON parsing and serialization

## Troubleshooting

### CMake Tools uses wrong compiler

**Symptom**: CMake Tools uses Visual Studio's clang instead of LLVM
**Solution**:

- Ensure LLVM's bin directory is BEFORE Visual Studio paths in system PATH
- Verify with `where clang` - LLVM should appear first

### vcpkg packages not found

**Symptom**: CMake can't find vcpkg packages
**Solution**:

- Ensure `VCPKG_ROOT` is set as SYSTEM or USER variable (not just in PowerShell profile)
- Check current value: `$env:VCPKG_ROOT`
- Check user variable: `[Environment]::GetEnvironmentVariable("VCPKG_ROOT", "User")`
- Check system variable: `[Environment]::GetEnvironmentVariable("VCPKG_ROOT", "Machine")`
- Verify toolchain file exists: `Test-Path "$env:VCPKG_ROOT\scripts\buildsystems\vcpkg.cmake"`
- After setting, restart VS Code to pick up the new environment variable

### clangd can't find headers

**Symptom**: Red squiggles under #include statements
**Solution**:

1. Ensure `.clangd` file exists and points to correct build directory for your architecture
2. Run the appropriate cmake preset:
   - `cmake --preset windows-x64-debug` for x64
   - `cmake --preset windows-arm64-debug` for ARM64
3. Update `.clangd` to match your architecture's build directory
4. Reload VS Code window (`Ctrl+Shift+P` → "Developer: Reload Window")

### VS Code doesn't find tools

**Symptom**: CMake Tools can't find cmake, clang, or ninja
**Solution**: Tools must be in SYSTEM PATH, not PowerShell profile:

1. Run `check-system-env.ps1` to verify
2. Run `set-system-env.ps1` as Administrator if needed
3. Restart computer or log out/in

## Key Principles

1. **System Environment Variables**: The root of all solutions - VS Code needs system-level variables
2. **Dual vcpkg Approach**: Use both `CMAKE_TOOLCHAIN_FILE` in presets and `VCPKG_ROOT` fallback for maximum compatibility
3. **Minimal Configuration**: Just the essentials - CMakePresets.json, basic VS Code settings
4. **Standard Tools**: CMake + Ninja + Clang + vcpkg - industry standard, cross-platform
5. **One Build Directory**: Use `out/` with subdirectories for different configurations
6. **clangd for IntelliSense**: Better C++ support than Microsoft's IntelliSense
7. **CMake Tools Extension Works**: When environment is properly configured

## Summary

This setup provides a clean, professional C++ development environment on Windows. The key is setting environment variables at the system level so all tools can find each other regardless of how they're launched. Once configured, everything "just works" with minimal complexity.
