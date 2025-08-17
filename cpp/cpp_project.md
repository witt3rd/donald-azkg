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
- **C/C++** (by Microsoft)
- **clangd** (by LLVM, optional but recommended for better IntelliSense)

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
4. Press `Ctrl+Shift+P` and select "CMake: Build"
5. Run the executable or use the Run/Debug features

## Key Points

### Why These Choices?

1. **Ninja instead of MSBuild**: Ninja is faster and simpler than MSBuild for C++ projects
2. **Clang with GNU CLI**: Uses familiar GCC-style flags (`-Wall`, `-O2`) instead of MSVC-style (`/W4`, `/O2`)
3. **CMake Presets**: Provides consistent, reproducible builds across different machines
4. **vcpkg**: Modern C++ package manager that integrates seamlessly with CMake

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
