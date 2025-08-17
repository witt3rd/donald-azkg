# Modern C++ Project Setup with CMake, Ninja, Clang, and vcpkg on Windows

This guide provides a working setup for a modern C++ development workflow on Windows using:

- **CMake** for build configuration
- **Ninja** for fast builds
- **Clang** with GNU-style command line (not MSVC-compatible clang-cl)
- **vcpkg** for dependency management
- **VS Code** as the IDE

## Prerequisites

### 1. Visual Studio Build Tools

Install Visual Studio (Community/Professional/Enterprise) with:

- "Desktop development with C++" workload
- This provides the Windows SDK and necessary libraries

### 2. VS Code Extensions

Install these extensions:

- **CMake Tools** (by Microsoft)
- **clangd** (by LLVM) - Recommended for better IntelliSense with CMake projects
- **C/C++** (by Microsoft) - Disable IntelliSense if using clangd

### 3. Ninja Build System

Download from [ninja-build.org](https://ninja-build.org/) or install via:

```powershell
winget install Ninja-build.Ninja
```

### 4. vcpkg Setup

```powershell
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install
```

Set the `VCPKG_ROOT` environment variable to your vcpkg directory (e.g., `C:\tools\vcpkg`)

## Project Structure

```
MyApp/
├── CMakeLists.txt
├── CMakePresets.json
├── vcpkg.json (optional)
└── src/
    └── main.cpp
```

## Configuration Files

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Generate compile_commands.json for clangd
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# vcpkg integration (if VCPKG_ROOT is set)
if(DEFINED ENV{VCPKG_ROOT})
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE STRING "")
endif()

add_executable(MyApp src/main.cpp)

# Example: To add packages via vcpkg
# find_package(fmt CONFIG REQUIRED)
# target_link_libraries(MyApp PRIVATE fmt::fmt)
```

### CMakePresets.json

```json
{
    "version": 8,
    "configurePresets": [
        {
            "name": "clang-gnu-debug",
            "displayName": "Clang (GNU CLI) with Ninja - Debug",
            "description": "Using Ninja generator with Clang compiler (GNU-style)",
            "generator": "Ninja",
            "binaryDir": "${sourceDir}/out/build/${presetName}",
            "cacheVariables": {
                "CMAKE_INSTALL_PREFIX": "${sourceDir}/out/install/${presetName}",
                "CMAKE_C_COMPILER": "clang",
                "CMAKE_CXX_COMPILER": "clang++",
                "CMAKE_BUILD_TYPE": "Debug",
                "CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
            }
        },
        {
            "name": "clang-gnu-release",
            "displayName": "Clang (GNU CLI) with Ninja - Release",
            "description": "Using Ninja generator with Clang compiler (GNU-style)",
            "generator": "Ninja",
            "binaryDir": "${sourceDir}/out/build/${presetName}",
            "cacheVariables": {
                "CMAKE_INSTALL_PREFIX": "${sourceDir}/out/install/${presetName}",
                "CMAKE_C_COMPILER": "clang",
                "CMAKE_CXX_COMPILER": "clang++",
                "CMAKE_BUILD_TYPE": "Release",
                "CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
            }
        }
    ],
    "buildPresets": [
        {
            "name": "clang-gnu-debug",
            "configurePreset": "clang-gnu-debug"
        },
        {
            "name": "clang-gnu-release",
            "configurePreset": "clang-gnu-release"
        }
    ]
}
```

### vcpkg.json (Optional but Recommended)

```json
{
    "name": "myapp",
    "version-string": "0.1.0",
    "dependencies": []
}
```

Note: When using vcpkg.json, CMake will automatically run `vcpkg install` during configuration to install all dependencies.

### src/main.cpp

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

## Building the Project

### Command Line

```powershell
# Configure
cmake --preset clang-gnu-debug

# Build
cmake --build --preset clang-gnu-debug

# Run
.\out\build\clang-gnu-debug\MyApp.exe
```

### VS Code

1. Open the project folder in VS Code
2. Press `Ctrl+Shift+P` and select "CMake: Select Configure Preset"
3. Choose "clang-gnu-debug" or "clang-gnu-release"
4. Press `Ctrl+Shift+P` and select "CMake: Configure" (generates compile_commands.json)
5. Press `Ctrl+Shift+P` and select "CMake: Build"
6. Run the executable or use the Run/Debug features

### Advanced: Using CMake Kits with PowerShell Profile

If your development environment relies on PowerShell profile settings (custom paths, environment variables, etc.), you can configure a CMake Kit to load your profile before running CMake:

1. **Create a Setup Script**
   
   Create `cmake-env-setup.ps1`:
   ```powershell
   # Load PowerShell profile
   . $PROFILE
   
   # Or load specific environment settings
   $env:VCPKG_ROOT = "C:\tools\vcpkg"
   $env:PATH = "$env:VCPKG_ROOT;$env:PATH"
   
   # Verify critical tools are available
   if (-not (Get-Command cmake -ErrorAction SilentlyContinue)) {
       Write-Error "CMake not found in PATH"
       exit 1
   }
   ```

2. **Configure CMake Kit**
   
   Press `Ctrl+Shift+P` → "CMake: Edit User-Local CMake Kits"
   
   Add this kit configuration:
   ```json
   [
     {
       "name": "Clang with PowerShell Environment",
       "environmentSetupScript": "C:\\path\\to\\cmake-env-setup.ps1",
       "compilers": {
         "C": "clang",
         "CXX": "clang++"
       },
       "preferredGenerator": {
         "name": "Ninja"
       }
     }
   ]
   ```

3. **Select and Use the Kit**
   - Press `Ctrl+Shift+P` → "CMake: Select a Kit"
   - Choose "Clang with PowerShell Environment"
   - Configure and build as normal

**Benefits:**
- Ensures all PowerShell profile paths and variables are available
- Works with custom tool installations
- Maintains consistency between terminal and VS Code builds
- Useful for corporate environments with complex setups

## Configuring clangd for IntelliSense

clangd needs a `compile_commands.json` file to understand your project's include paths, especially for dependencies from vcpkg and FetchContent.

### Setup Steps

1. **Enable Compilation Database Generation**
   - Already included in the CMakeLists.txt above: `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)`

2. **Configure Your Project**
   ```powershell
   cmake --preset clang-gnu-debug
   ```
   This generates `compile_commands.json` in your build directory (`out/build/clang-gnu-debug/`)

3. **Create .clangd Configuration (Recommended)**
   
   Create a `.clangd` file in your project root with:
   ```yaml
   CompileFlags:
     CompilationDatabase: out/build/clang-gnu-debug
   ```
   
   **Benefits of this approach:**
   - ✅ Cross-platform (Windows, Linux, macOS)
   - ✅ No admin privileges required
   - ✅ No manual file copying after each build
   - ✅ Easy to switch between build configurations
   
   **Note about Debug vs Release**: For header resolution and IntelliSense, it doesn't matter whether you point to the debug or release build directory. The include paths for dependencies (vcpkg, FetchContent) are identical between build types. The only differences are:
   - Optimization flags (`-O0` vs `-O2`)
   - Debug symbols (`-g`)
   - Preprocessor defines like `NDEBUG`
   
   None of these affect finding headers, so just point to whichever build directory you've configured most recently.

4. **VS Code Settings**
   Create/update `.vscode/settings.json`:
   ```json
   {
     // Disable Microsoft C++ IntelliSense in favor of clangd
     "C_Cpp.intelliSenseEngine": "disabled",
     
     // Optional: Additional clangd arguments
     "clangd.arguments": [
       "--header-insertion=never",
       "--clang-tidy"
     ]
   }
   ```
   
   Note: With the `.clangd` file configured, you don't need `--compile-commands-dir` in VS Code settings

5. **Reload VS Code Window**
   - Press `Ctrl+Shift+P` → "Developer: Reload Window"
   - clangd should now resolve all includes from vcpkg and FetchContent

### Verifying Configuration

1. Open `compile_commands.json` and check for include paths:
   - vcpkg paths: Look for `-I` flags containing `vcpkg/installed/`
   - FetchContent paths: Look for paths in `_deps/` directories

2. Test IntelliSense:
   - Hover over an include from a dependency
   - Should show the full path without errors
   - Ctrl+Click should navigate to the header

### Alternative Setup Methods (If .clangd doesn't work)

If you can't use `.clangd` file for some reason, here are platform-specific alternatives:

**Windows - Symbolic Link (requires Admin)**
```powershell
New-Item -ItemType SymbolicLink -Path ".\compile_commands.json" -Target ".\out\build\clang-gnu-debug\compile_commands.json"
```

**Cross-platform - Copy File**
```powershell
Copy-Item ".\out\build\clang-gnu-debug\compile_commands.json" -Destination "."
```

**VS Code - Direct Configuration**
Add to `clangd.arguments` in settings.json:
```json
"--compile-commands-dir=${workspaceFolder}/out/build/clang-gnu-debug"
```

### Troubleshooting clangd Issues

**Problem: Headers not found after configuration**
- Verify `.clangd` file points to correct build directory
- Ensure you've run CMake configure after adding dependencies
- Check that `target_link_libraries()` is properly set
- Verify the compile_commands.json exists in the build directory

**Problem: clangd not starting**
- Check Output panel → clangd for errors
- Ensure clangd extension is installed and enabled
- Try: `clangd --version` in terminal to verify installation

**Problem: Conflicting IntelliSense providers**
- Disable Microsoft C/C++ IntelliSense: Set `"C_Cpp.intelliSenseEngine": "disabled"`
- Or disable clangd and use Microsoft's IntelliSense

**Problem: Multiple build directories**
- Simply update the path in `.clangd` file when switching configurations
- Or maintain separate `.clangd` files per configuration and swap them

## Key Points

### Why These Choices?

1. **Ninja instead of MSBuild**: Ninja is faster and simpler than MSBuild for C++ projects
2. **Clang with GNU CLI**: Uses familiar GCC-style flags (`-Wall`, `-O2`) instead of MSVC-style (`/W4`, `/O2`)
3. **CMake Presets**: Provides consistent, reproducible builds across different machines
4. **vcpkg**: Modern C++ package manager that integrates seamlessly with CMake
5. **clangd**: Provides superior IntelliSense for modern C++ with proper CMake integration

### Common Issues and Solutions

#### Issue: CMake generates Visual Studio project files (.sln, .vcxproj)

**Solution**: Make sure your CMakePresets.json includes `"generator": "Ninja"`

#### Issue: "MSBuild version X for .NET Framework" message

**Explanation**: This is MSBuild identifying itself. MSBuild is written in .NET but builds native C++ code. If you see this, CMake is using the Visual Studio generator instead of Ninja.

#### Issue: vcpkg packages not found

**Solution**: Ensure `VCPKG_ROOT` environment variable is set and specify the toolchain file in CMakePresets.json:

```json
"CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
```

Note: It's recommended to specify the toolchain file in both CMakeLists.txt (for fallback) and CMakePresets.json (for explicit configuration).

#### Issue: Clang not found

**Solution**: Install Clang via Visual Studio Installer (under Individual Components) or LLVM directly. Ensure it's in your PATH.

## CMake 3.24+ Dependency Providers (Advanced)

Starting with CMake 3.24, you can configure dependency providers that enable seamless integration between package managers (like vcpkg) and fallback mechanisms (like FetchContent). This allows `find_package()` to:

1. First try to find the package via vcpkg or system packages
2. Automatically fall back to downloading and building from source if not found

### Setting Up Dependency Provider with FetchContent Fallback

#### CMakeLists.txt with FetchContent Integration

```cmake
cmake_minimum_required(VERSION 3.24)
project(MyApp CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# vcpkg integration (if VCPKG_ROOT is set)
if(DEFINED ENV{VCPKG_ROOT})
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE STRING "")
endif()

# Include FetchContent module
include(FetchContent)

# Declare dependencies with FIND_PACKAGE_ARGS for automatic fallback
FetchContent_Declare(
    fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG        10.2.1
    GIT_SHALLOW    TRUE
    FIND_PACKAGE_ARGS 10.0 CONFIG
)

FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
    GIT_SHALLOW    TRUE
    FIND_PACKAGE_ARGS NAMES GTest
)

# This will:
# 1. Try find_package(fmt 10.0 CONFIG) first (uses vcpkg if available)
# 2. Fall back to FetchContent if not found
FetchContent_MakeAvailable(fmt googletest)

add_executable(MyApp src/main.cpp)
target_link_libraries(MyApp PRIVATE fmt::fmt)

# Tests
add_executable(MyApp_test src/test.cpp)
target_link_libraries(MyApp_test PRIVATE GTest::gtest_main)
```

### Git Submodules vs Inlining

**Important**: FetchContent downloads dependencies at configure time but does NOT add them to your git repository. The downloaded sources are placed in your build directory (typically `out/build/*/`), not your source tree.

To use git submodules instead of FetchContent downloads:

```cmake
# Option 1: Use FetchContent with SOURCE_DIR pointing to a submodule
FetchContent_Declare(
    fmt
    SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/external/fmt
)

# Option 2: Traditional add_subdirectory with submodule
add_subdirectory(external/fmt)
```

For git submodules setup:
```bash
git submodule add https://github.com/fmtlib/fmt.git external/fmt
git submodule update --init --recursive
```

### Dependency Provider Configuration

For more control, create a dependency provider script (`cmake/DependencyProvider.cmake`):

```cmake
# This file configures how find_package() calls are handled
macro(custom_find_package PACKAGE_NAME)
    # Try vcpkg first
    if(DEFINED ENV{VCPKG_ROOT})
        find_package(${PACKAGE_NAME} ${ARGN} QUIET)
    endif()
    
    # If not found, check if we have a FetchContent declaration
    if(NOT ${PACKAGE_NAME}_FOUND)
        FetchContent_GetProperties(${PACKAGE_NAME})
        if(NOT ${PACKAGE_NAME}_POPULATED)
            message(STATUS "Package ${PACKAGE_NAME} not found, fetching from source...")
            FetchContent_MakeAvailable(${PACKAGE_NAME})
        endif()
    endif()
endmacro()

# Set this as the dependency provider
set(CMAKE_FIND_PACKAGE_REDIRECTS_DIR ${CMAKE_CURRENT_BINARY_DIR}/cmake)
```

Use it by adding to your preset:
```json
"cacheVariables": {
    "CMAKE_PROJECT_TOP_LEVEL_INCLUDES": "${sourceDir}/cmake/DependencyProvider.cmake"
}
```

### Benefits of This Approach

1. **User Choice**: Users can choose between system packages, vcpkg, or building from source
2. **Reproducible Builds**: FetchContent ensures exact versions when packages aren't available
3. **CI/CD Friendly**: Works in environments where vcpkg might not be set up
4. **No Repository Pollution**: Dependencies stay out of your git repo
5. **Caching**: FetchContent caches downloads, avoiding repeated fetches

## Adding Dependencies with vcpkg

### Example: Adding raylib library

1. Add to vcpkg.json (recommended):

```json
{
    "name": "myapp",
    "version-string": "0.1.0",
    "dependencies": [
        "raylib"
    ]
}
```

2. Update CMakeLists.txt:

```cmake
find_package(raylib CONFIG REQUIRED)
target_link_libraries(MyApp PRIVATE raylib)
```

3. Use in your code:

```cpp
#include "raylib.h"

int main() {
    InitWindow(800, 600, "Hello Raylib");
    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);
        DrawText("Hello, World!", 10, 10, 20, BLACK);
        EndDrawing();
    }
    CloseWindow();
    return 0;
}
```

Note: When using vcpkg.json, CMake will automatically install dependencies during configuration.

## Architecture Notes

- The configuration doesn't hardcode the target architecture
- Clang automatically detects whether you're on x86_64, ARM64, etc.
- To explicitly target an architecture, add to CMAKE_CXX_FLAGS:
  - `-target x86_64-pc-windows-gnu` for x64 with MinGW ABI
  - `-target aarch64-pc-windows-gnu` for ARM64 with MinGW ABI
  - `-target x86_64-pc-windows-msvc` for x64 with MSVC ABI

## Summary

This setup provides a modern, fast, and portable C++ development environment on Windows without requiring Visual Studio IDE. The combination of CMake + Ninja + Clang + vcpkg is widely used in the industry and provides excellent cross-platform compatibility.
