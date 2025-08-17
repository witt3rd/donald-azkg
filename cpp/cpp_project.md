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