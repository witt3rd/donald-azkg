# Modern C++ Project Setup on Windows

This comprehensive guide covers C++ development workflows on Windows for both:

1. **Visual Studio Code** with CMake, Ninja, and Clang
2. **Visual Studio** (Community/Professional/Enterprise) with MSBuild

Both environments support:

- **vcpkg** for dependency management
- Manual library integration
- Modern C++ standards

## Part 1: Visual Studio Code Setup

### Prerequisites for VS Code

### 1. Toolchain Installation (Prefer WinGet)

**IMPORTANT**: Install development tools via WinGet for better version control and consistency. These installations should take precedence over Visual Studio's bundled versions.

#### Required Tools via WinGet

```powershell
# CMake - Build system generator
winget install Kitware.CMake

# LLVM/Clang - Complete compiler toolchain with debugger
winget install LLVM.LLVM

# Ninja - Fast build system
winget install Ninja-build.Ninja
```

#### Visual Studio Build Tools

Install Visual Studio (Community/Professional/Enterprise) with:

- "Desktop development with C++" workload
- This provides the Windows SDK and necessary libraries
- **IMPORTANT**: Do NOT install the optional CMake or Clang/LLVM components from Visual Studio Installer
- We exclusively use WinGet-installed versions for consistency and full feature support

### 2. PowerShell Profile Configuration

Add WinGet-installed tools to your PowerShell profile (`$PROFILE`):

```powershell
# CMake - WinGet installation
$wingetCmakePath = 'C:\Program Files\CMake\bin'
if (Test-Path $wingetCmakePath) {
    $env:PATH = "$wingetCmakePath;$env:PATH"
}

# LLVM/Clang - Full WinGet LLVM installation (includes LLDB)
$fullLlvmPath = 'C:\Program Files\LLVM\bin'
if (Test-Path $fullLlvmPath) {
    $env:PATH = "$fullLlvmPath;$env:PATH"
}

# Ninja - WinGet installation
$wingetNinjaPath = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter "Ninja-build.Ninja*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
if ($wingetNinjaPath) {
    $env:PATH = "$($wingetNinjaPath.FullName);$env:PATH"
}
```

**Note**: Since Visual Studio's CMake and LLVM components are not installed, these WinGet paths are the only sources for these tools.

### 3. VS Code Extensions

Install these extensions:

- **clangd** (by LLVM) - For IntelliSense with CMake projects
- **C/C++** (by Microsoft) - Disable IntelliSense if using clangd
- **CodeLLDB** - Native LLDB debugger support (works with WinGet LLVM)

**WARNING**: Do NOT install the CMake Tools extension. It has serious issues with PowerShell environment inheritance on Windows and will not properly use your configured build environment (PATH, VCPKG_ROOT, etc.). Use VS Code tasks instead (see configuration below).

### 4. vcpkg Setup

```powershell
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install
```

Set the `VCPKG_ROOT` environment variable to your vcpkg directory (e.g., `C:\tools\vcpkg`)

### 5. LLDB Debugger (Included with WinGet LLVM)

The WinGet LLVM installation includes LLDB debugger and liblldb.dll, providing complete debugging support for Clang-compiled programs.

**Python Requirement**: LLDB may require Python (typically Python 3.10+) for some features. Install Python and add it to your PATH if needed.

## Project Structure

```
MyApp/
├── CMakeLists.txt
├── CMakePresets.json
├── vcpkg.json (optional but recommended)
├── .clangd (clangd configuration for IntelliSense)
├── .gitignore
├── .vscode/
│   ├── settings.json (workspace settings)
│   ├── tasks.json (build tasks)
│   └── launch.json (debug configurations)
├── out/                    # Build output directory (gitignored)
│   ├── clang-gnu-debug/   # Debug build with Clang
│   ├── clang-gnu-release/ # Release build with Clang
│   └── vs2022/            # Visual Studio solution files
├── llm-docs/
│   └── cpp/
│       └── cpp_project.md (this file)
└── src/
    └── main.cpp
```

## Build Directory Best Practices

### Why `out/` Instead of `build/`?

This project uses `out/` as the top-level build directory. Here's our rationale:

1. **Semantic Clarity**: `out/` explicitly indicates "output artifacts" - it's immediately clear this contains generated files, not source code
2. **Visual Studio Heritage**: Aligns with Visual Studio's convention, making it familiar for Windows developers
3. **Gitignore Simplicity**: Single pattern `/out/` in `.gitignore` covers all build artifacts
4. **No Ambiguity**: Unlike `build/`, which could be confused with build scripts or documentation

### Avoiding Redundant Nesting

**Best Practice**: Use a single top-level directory (`out/` or `build/`), then add subdirectories only for different configurations.

**Good Structure** ✅:
```
out/
├── clang-gnu-debug/
├── clang-gnu-release/
└── vs2022/
```

**Avoid Redundant Nesting** ❌:
```
out/
└── build/           # Unnecessary extra layer!
    ├── debug/
    └── release/
```

The nested `out/build/` pattern serves no purpose and just adds complexity to paths, scripts, and documentation.

### Common Conventions

- **`build/`**: Most common in open-source CMake projects (LLVM, OpenCV, etc.)
- **`out/`**: Common in enterprise/corporate settings and Visual Studio projects
- **Never `out/build/`**: This redundant nesting is almost never seen in professional projects

### `.gitignore` Configuration

Keep it simple:
```gitignore
# Build outputs (includes all CMake artifacts and dependencies)
/out/

# IDE artifacts
/.vs/
/.vscode/settings.local.json
```

Note: Dependencies managed by vcpkg and FetchContent are automatically placed in subdirectories under `/out/` (e.g., `out/clang-gnu-debug/vcpkg_installed/` and `out/clang-gnu-debug/_deps/`), so they're already covered by the `/out/` pattern.

## Configuration Files

### CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)

# vcpkg integration (if available) - must be set before project()
if(DEFINED ENV{VCPKG_ROOT} AND NOT "$ENV{VCPKG_ROOT}" STREQUAL "")
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE STRING "")
    message(STATUS "Using vcpkg toolchain from: $ENV{VCPKG_ROOT}")
else()
    message(STATUS "VCPKG_ROOT not set - dependencies will be fetched automatically if needed")
endif()

project(MyApp CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Generate compile_commands.json for clangd
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Use ${PROJECT_NAME} instead of hardcoding the executable name
add_executable(${PROJECT_NAME} src/main.cpp)

# Example: To add packages via vcpkg
# find_package(fmt CONFIG REQUIRED)
# target_link_libraries(${PROJECT_NAME} PRIVATE fmt::fmt)

# Set this project as the default startup project in Visual Studio
# (Prevents ALL_BUILD from being the default)
if(CMAKE_GENERATOR MATCHES "Visual Studio")
    set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT ${PROJECT_NAME})
endif()
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
            "binaryDir": "${sourceDir}/out/${presetName}",
            "cacheVariables": {
                "CMAKE_INSTALL_PREFIX": "${sourceDir}/out/install/${presetName}",
                "CMAKE_C_COMPILER": "clang",
                "CMAKE_CXX_COMPILER": "clang++",
                "CMAKE_BUILD_TYPE": "Debug"
            }
        },
        {
            "name": "clang-gnu-release",
            "displayName": "Clang (GNU CLI) with Ninja - Release",
            "description": "Using Ninja generator with Clang compiler (GNU-style)",
            "generator": "Ninja",
            "binaryDir": "${sourceDir}/out/${presetName}",
            "cacheVariables": {
                "CMAKE_INSTALL_PREFIX": "${sourceDir}/out/install/${presetName}",
                "CMAKE_C_COMPILER": "clang",
                "CMAKE_CXX_COMPILER": "clang++",
                "CMAKE_BUILD_TYPE": "Release"
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

### VS Code Workspace Configuration (Recommended)

#### Why Use Workspace Configuration?

- **Consistency**: All team members use the same settings
- **Single Tool Source**: Only WinGet-installed tools are available (no Visual Studio variants)
- **Environment Inheritance**: Tasks run in integrated terminal with full PowerShell profile
- **No Extension Issues**: Avoids CMake Tools extension environment problems

Since the CMake Tools extension has issues with PowerShell environment variables on Windows, use VS Code tasks instead:

1. Create `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Configure Debug",
            "type": "shell",
            "command": "cmake",
            "args": [
                "--preset",
                "clang-gnu-debug"
            ],
            "group": "build",
            "problemMatcher": []
        },
        {
            "label": "Configure Release",
            "type": "shell",
            "command": "cmake",
            "args": [
                "--preset",
                "clang-gnu-release"
            ],
            "group": "build",
            "problemMatcher": []
        },
        {
            "label": "Build Debug",
            "type": "shell",
            "command": "cmake",
            "args": [
                "--build",
                "--preset",
                "clang-gnu-debug"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher": ["$gcc"],
            "dependsOn": ["Configure Debug"]
        },
        {
            "label": "Build Release",
            "type": "shell",
            "command": "cmake",
            "args": [
                "--build",
                "--preset",
                "clang-gnu-release"
            ],
            "group": "build",
            "problemMatcher": ["$gcc"],
            "dependsOn": ["Configure Release"]
        },
        {
            "label": "Clean",
            "type": "shell",
            "command": "pwsh",
            "args": [
                "-Command",
                "if (Test-Path '${workspaceFolder}/out') { Remove-Item -Path '${workspaceFolder}/out' -Recurse -Force }"
            ],
            "group": "build",
            "problemMatcher": []
        },
        {
            "label": "Run Debug",
            "type": "shell",
            "command": "${workspaceFolder}/out/clang-gnu-debug/MyApp",
            "group": {
                "kind": "test",
                "isDefault": true
            },
            "dependsOn": ["Build Debug"],
            "problemMatcher": []
        },
        {
            "label": "Run Release",
            "type": "shell",
            "command": "${workspaceFolder}/out/clang-gnu-release/MyApp",
            "group": "test",
            "dependsOn": ["Build Release"],
            "problemMatcher": []
        },
        {
            "label": "Configure VS2022",
            "type": "shell",
            "command": "cmake",
            "args": [
                "-G",
                "Visual Studio 17 2022",
                "-B",
                "out/vs2022"
            ],
            "group": "build",
            "problemMatcher": []
        }
    ]
}
```

#### Recommended settings.json

Create `.vscode/settings.json` with:

```json
{
  // Disable Microsoft C++ IntelliSense in favor of clangd
  "C_Cpp.intelliSenseEngine": "disabled",

  // clangd configuration
  "clangd.arguments": [
    "--header-insertion=never",
    "--clang-tidy",
    "--background-index",
    "--completion-style=detailed"
  ],

  // Terminal configuration - use default PowerShell profile
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.profiles.windows": {
    "PowerShell": {
      "source": "PowerShell",
      "icon": "terminal-powershell"
    }
  },

  // File associations
  "files.associations": {
    "*.h": "cpp",
    "*.hpp": "cpp",
    "*.cpp": "cpp",
    "*.cc": "cpp",
    "*.cxx": "cpp",
    "*.c++": "cpp"
  },

  // Editor settings for C++
  "editor.formatOnSave": true,
  "[cpp]": {
    "editor.defaultFormatter": "llvm-vs-code-extensions.vscode-clangd"
  }
}
```

2. Use the tasks:
   - **Build**: `Ctrl+Shift+B` (runs default build task - Debug)
   - **Run**: `Ctrl+Shift+P` → "Tasks: Run Test Task" (runs Debug executable)
   - **Other tasks**: `Ctrl+Shift+P` → "Tasks: Run Task" → select task

**Note**: The Run tasks directly reference the executable path. If your project name differs from 'MyApp', update the command path accordingly. The VS2022 Configure task generates Visual Studio solution files in a separate build directory for when you need to open the project in Visual Studio.

This approach ensures all your PowerShell profile environment variables (PATH, VCPKG_ROOT, etc.) are properly loaded.

## CMake Environment Configuration

### CMAKE_TOOLCHAIN_FILE and vcpkg Integration

This project uses a **conditional CMAKE_TOOLCHAIN_FILE** approach that provides flexibility:

1. **Automatic vcpkg detection**: If `VCPKG_ROOT` is set, vcpkg is used for dependencies
2. **Graceful fallback**: If vcpkg isn't available, dependencies can use FetchContent
3. **No preset coupling**: Works with any CMake invocation method, not tied to specific presets

The key is setting `CMAKE_TOOLCHAIN_FILE` **before** the `project()` command in CMakeLists.txt. This ensures CMake loads the vcpkg toolchain during initial configuration, making vcpkg packages available via `find_package()`.

**Why not in CMakePresets.json?**
- Setting it only in CMakeLists.txt makes the project more flexible
- Users without vcpkg can still build (using FetchContent fallbacks)
- Simpler configuration - one place to manage the toolchain logic

### PowerShell Profile Integration

If your build environment depends on PowerShell profile settings (custom paths, VCPKG_ROOT, tool locations), the VS Code tasks approach (shown above) automatically inherits these when running in the integrated terminal.

### Why VS Code Tasks Instead of CMake Tools Extension?

The CMake Tools extension has a critical flaw on Windows: it doesn't properly inherit the PowerShell profile environment. This means:

- Environment variables like `VCPKG_ROOT`, custom `PATH` entries, and tool locations set in your PowerShell profile are not available
- The extension often defaults to using Visual Studio's bundled CMake instead of your configured version
- Complex workarounds (environment scripts, kits) are fragile and often fail

**VS Code tasks run in the integrated terminal**, which properly loads your PowerShell profile, ensuring all your carefully configured build tools and environment variables work as expected.

## Configuring clangd for IntelliSense

clangd needs a `compile_commands.json` file to understand your project's include paths, especially for dependencies from vcpkg and FetchContent.

### Setup Steps

1. **Enable Compilation Database Generation**
   - Already included in the CMakeLists.txt above: `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)`

2. **Configure Your Project**

   ```powershell
   cmake --preset clang-gnu-debug
   ```

   This generates `compile_commands.json` in your build directory (`out/clang-gnu-debug/`)

3. **Create .clangd Configuration (Required for IntelliSense)**

   Create a `.clangd` file in your project root with:

   ```yaml
   # Point to any configured build directory - debug and release have the same include paths
   # Just ensure you've run cmake --preset on at least one configuration
   CompileFlags:
     CompilationDatabase: out/clang-gnu-debug
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
   The workspace settings should already be configured (see Workspace Configuration section above).

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
New-Item -ItemType SymbolicLink -Path ".\compile_commands.json" -Target ".\out\clang-gnu-debug\compile_commands.json"
```

**Cross-platform - Copy File**

```powershell
Copy-Item ".\out\clang-gnu-debug\compile_commands.json" -Destination "."
```

**VS Code - Direct Configuration**
Add to `clangd.arguments` in settings.json:

```json
"--compile-commands-dir=${workspaceFolder}/out/clang-gnu-debug"
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

## Debugging Configuration

### Using CodeLLDB with WinGet LLVM

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug (LLDB)",
            "type": "lldb",
            "request": "launch",
            "program": "${workspaceFolder}/out/clang-gnu-debug/${workspaceFolderBasename}.exe",
            "args": [],
            "cwd": "${workspaceFolder}",
            "terminal": "integrated",
            "preLaunchTask": "CMake Build (Debug)"
        },
        {
            "name": "Debug (LLDB) - Release",
            "type": "lldb",
            "request": "launch",
            "program": "${workspaceFolder}/out/clang-gnu-release/${workspaceFolderBasename}.exe",
            "args": [],
            "cwd": "${workspaceFolder}",
            "terminal": "integrated",
            "preLaunchTask": "CMake Build (Release)"
        }
    ]
}
```

## Key Points

### Why These Choices?

1. **WinGet-Only Toolchain**: Single source of truth for tools - no Visual Studio CMake/LLVM installed
2. **Ninja instead of MSBuild**: Ninja is faster and simpler than MSBuild for C++ projects
3. **Clang with GNU CLI**: Uses familiar GCC-style flags (`-Wall`, `-O2`) instead of MSVC-style (`/W4`, `/O2`)
4. **CMake Presets**: Provides consistent, reproducible builds across different machines
5. **vcpkg**: Modern C++ package manager that integrates seamlessly with CMake
6. **clangd**: Provides superior IntelliSense for modern C++ with proper CMake integration
7. **Workspace Configuration**: Team-wide consistency with checked-in VS Code settings

### Common Issues and Solutions

#### Issue: CMake generates Visual Studio project files (.sln, .vcxproj)

**Solution**: Make sure your CMakePresets.json includes `"generator": "Ninja"`

#### Issue: "MSBuild version X for .NET Framework" message

**Explanation**: This is MSBuild identifying itself. MSBuild is written in .NET but builds native C++ code. If you see this, CMake is using the Visual Studio generator instead of Ninja.

#### Issue: vcpkg packages not found

**Solution**: Ensure `VCPKG_ROOT` environment variable is set. The project automatically detects and uses vcpkg when available through the conditional check in CMakeLists.txt:

```cmake
# This must appear BEFORE project() to work correctly
if(DEFINED ENV{VCPKG_ROOT} AND NOT "$ENV{VCPKG_ROOT}" STREQUAL "")
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE STRING "")
endif()
```

**Note**: Setting CMAKE_TOOLCHAIN_FILE in CMakeLists.txt (before project()) is the recommended approach as it:
- Works with any CMake invocation method
- Automatically falls back to FetchContent when vcpkg isn't available
- Doesn't require preset-specific configuration

#### Issue: Clang not found

**Solution**: Install LLVM via WinGet: `winget install LLVM.LLVM`. Ensure your PowerShell profile adds it to PATH.

#### Issue: CMake not found

**Solution**: Install CMake via WinGet: `winget install Kitware.CMake`. Visual Studio's CMake is not installed.

#### Issue: Wrong version of tools being used

**Solution**: Check tool locations with:

```powershell
Get-Command cmake,clang,ninja | Select-Object Name,Source
```

All tools should come from WinGet installations:

- CMake: `C:\Program Files\CMake\bin`
- Clang: `C:\Program Files\LLVM\bin`
- Ninja: `C:\Users\<username>\AppData\Local\Microsoft\WinGet\Packages\Ninja-build.Ninja*`

#### Issue: Visual Studio Opens with ALL_BUILD as Startup Project

**Problem**: When opening the generated `.sln` file in Visual Studio, `ALL_BUILD` is set as the default startup project instead of your executable. Attempting to run the project fails with "Unable to start program ALL_BUILD. Access is denied."

**Why This Happens**: This is **normal CMake behavior**. CMake creates utility targets like `ALL_BUILD` (builds all projects) and `ZERO_CHECK` (checks if CMake needs to regenerate). Visual Studio sets the first project in the `.sln` file as the startup project, and CMake lists `ALL_BUILD` first by default.

**Solution**: Add the following to your `CMakeLists.txt` after defining your executable:

```cmake
# Set this project as the default startup project in Visual Studio
# (Requires CMake 3.6+, prevents ALL_BUILD from being the default)
if(CMAKE_GENERATOR MATCHES "Visual Studio")
    set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT ${PROJECT_NAME})
endif()
```

This tells CMake to set your actual executable as the startup project in the generated Visual Studio solution. The `if` statement ensures this only applies when using the Visual Studio generator, maintaining compatibility with other build systems.

**Alternative Manual Fix**: Right-click your project (e.g., `MyApp`) in Solution Explorer and select "Set as Startup Project". You only need to do this once - Visual Studio remembers your choice.

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

# vcpkg integration (if VCPKG_ROOT is set) - must be set before project()
if(DEFINED ENV{VCPKG_ROOT} AND NOT "$ENV{VCPKG_ROOT}" STREQUAL "")
    set(CMAKE_TOOLCHAIN_FILE "$ENV{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake" CACHE STRING "")
    message(STATUS "Using vcpkg toolchain from: $ENV{VCPKG_ROOT}")
else()
    message(STATUS "VCPKG_ROOT not set - dependencies will be fetched automatically if needed")
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

add_executable(${PROJECT_NAME} src/main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE fmt::fmt)

# Tests
add_executable(MyApp_test src/test.cpp)
target_link_libraries(MyApp_test PRIVATE GTest::gtest_main)
```

### Git Submodules vs Inlining

**Important**: FetchContent downloads dependencies at configure time but does NOT add them to your git repository. The downloaded sources are placed in your build directory (typically `out/*/`), not your source tree.

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
target_link_libraries(${PROJECT_NAME} PRIVATE raylib)
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

## Best Practices Summary

1. **WinGet-Only Toolchain**: Install CMake, LLVM, and Ninja exclusively via WinGet
2. **No Visual Studio Tools**: Do NOT install CMake or Clang/LLVM from Visual Studio Installer
3. **Configure PowerShell Profile**: Add WinGet tool paths to your profile
4. **Commit VS Code Settings**: Check in `.vscode/` folder for team consistency
5. **Use Tasks over Extensions**: VS Code tasks properly inherit PowerShell environment
6. **Leverage clangd**: Superior IntelliSense with proper CMake understanding
7. **Document in llm-docs**: Keep project-specific documentation for AI assistants

### VS Code Summary

This setup provides a modern, fast, and portable C++ development environment on Windows. By using exclusively WinGet-installed tools, you get:

- **Latest tool versions**: Direct from official sources, not tied to Visual Studio release cycles
- **Complete toolchains**: Full LLVM with LLDB debugger (not available in Visual Studio's partial installation)
- **Consistency**: Single source for each tool - no version conflicts
- **Flexibility**: Easy to update tools independently via WinGet
- **Simplicity**: No confusion about which tool version is being used

The combination of CMake + Ninja + Clang + vcpkg is widely used in the industry and provides excellent cross-platform compatibility.

---

## Part 2: Visual Studio Setup

### Prerequisites for Visual Studio

1. **Install Visual Studio** (Community/Professional/Enterprise) with:
   - "Desktop development with C++" workload
   - Windows SDK
   - C++ core features
   - MSVC compiler
   - CMake tools for Windows (optional, for CMake projects)

2. **Install vcpkg** (same as VS Code setup):

   ```powershell
   git clone https://github.com/Microsoft/vcpkg.git
   cd vcpkg
   .\bootstrap-vcpkg.bat
   .\vcpkg integrate install
   ```

### Creating a Visual Studio Project

#### Option 1: Traditional Visual Studio Project

1. **Create New Project**:
   - File → New → Project
   - Choose "Console App" or "Empty Project" for C++
   - Configure project name and location

2. **Project Configuration**:
   - Right-click project → Properties
   - Configuration: All Configurations
   - Platform: All Platforms (or specific x64/x86)
   - C/C++ → Language → C++ Language Standard: Choose your standard (C++17, C++20, C++23)

#### Option 2: CMake Project in Visual Studio

1. **Create CMake Project**:
   - File → New → Project
   - Choose "CMake Project"
   - Visual Studio will create CMakeLists.txt and CMakePresets.json

2. **Configure CMakePresets.json for Visual Studio**:

   ```json
   {
       "version": 3,
       "configurePresets": [
           {
               "name": "windows-base",
               "hidden": true,
               "generator": "Visual Studio 17 2022",
               "binaryDir": "${sourceDir}/out/${presetName}",
               "installDir": "${sourceDir}/out/install/${presetName}",
               "cacheVariables": {
                   "CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake"
               }
           },
           {
               "name": "x64-debug",
               "displayName": "x64 Debug",
               "inherits": "windows-base",
               "architecture": {
                   "value": "x64",
                   "strategy": "external"
               },
               "cacheVariables": {
                   "CMAKE_BUILD_TYPE": "Debug"
               }
           },
           {
               "name": "x64-release",
               "displayName": "x64 Release",
               "inherits": "windows-base",
               "architecture": {
                   "value": "x64",
                   "strategy": "external"
               },
               "cacheVariables": {
                   "CMAKE_BUILD_TYPE": "Release"
               }
           }
       ]
   }
   ```

---

## Part 3: Dependency Management (Both IDEs)

### Adding Dependencies with vcpkg

vcpkg is a C++ package manager that integrates directly with both Visual Studio and VS Code projects.

#### Method 1: Using vcpkg.json (Recommended)

Create `vcpkg.json` in your project root:

```json
{
    "name": "myproject",
    "version": "1.0",
    "dependencies": [
        "raylib",
        "argparse",
        "fmt",
        "nlohmann-json"
    ]
}
```

**For Visual Studio Projects**:

- Right-click project → Properties
- Go to vcpkg section
- Set "Use Vcpkg" to Yes
- Set "Use Vcpkg Manifest" to Yes

**For CMake Projects** (both IDEs):

- Dependencies are automatically installed during CMake configuration
- Add to CMakeLists.txt:

  ```cmake
  find_package(raylib CONFIG REQUIRED)
  find_package(fmt CONFIG REQUIRED)
  target_link_libraries(${PROJECT_NAME} PRIVATE raylib fmt::fmt)
  ```

#### Method 2: Command Line Installation

```powershell
# Install individual packages
.\vcpkg install raylib
.\vcpkg install argparse
.\vcpkg install fmt

# Install for specific triplet (architecture)
.\vcpkg install raylib:x64-windows
.\vcpkg install raylib:x86-windows
```

### Manual Library Integration (Not in vcpkg)

For libraries not available in vcpkg (e.g., libtorch):

#### Visual Studio Configuration

1. **Download and Extract Library**:
   - Download prebuilt binaries from official source
   - Extract to a location like `C:\libraries\libtorch`

2. **Configure Project Properties**:
   - Right-click project → Properties
   - **C/C++ → General → Additional Include Directories**:
     Add `C:\libraries\libtorch\include`
   - **Linker → General → Additional Library Directories**:
     Add `C:\libraries\libtorch\lib`
   - **Linker → Input → Additional Dependencies**:
     Add required `.lib` files (e.g., `torch.lib`, `c10.lib`)

3. **Handle Runtime DLLs**:
   - Copy DLLs to output directory, OR
   - Add library `bin` folder to PATH, OR
   - Set Debugging → Environment: `PATH=$(PATH);C:\libraries\libtorch\lib`

#### CMake Configuration (Both IDEs)

For CMake projects, add to CMakeLists.txt:

```cmake
# Manual library integration
set(LIBTORCH_DIR "C:/libraries/libtorch")
find_package(Torch REQUIRED PATHS ${LIBTORCH_DIR})
target_link_libraries(${PROJECT_NAME} PRIVATE "${TORCH_LIBRARIES}")

# Copy DLLs to output directory
if(MSVC)
    file(GLOB TORCH_DLLS "${LIBTORCH_DIR}/lib/*.dll")
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${TORCH_DLLS}
        $<TARGET_FILE_DIR:${PROJECT_NAME}>)
endif()
```

### Dependency Reference Table

| Library          | vcpkg Support | Installation Method              | Notes                                    |
|------------------|---------------|----------------------------------|------------------------------------------||
| argparse         | ✅ Yes        | `vcpkg install argparse`         | Header-only argument parser              |
| raylib           | ✅ Yes        | `vcpkg install raylib`           | Simple game programming library          |
| fmt              | ✅ Yes        | `vcpkg install fmt`              | Modern formatting library                |
| nlohmann-json    | ✅ Yes        | `vcpkg install nlohmann-json`    | JSON for Modern C++                     |
| boost            | ✅ Yes        | `vcpkg install boost`            | Comprehensive C++ libraries             |
| opencv           | ✅ Yes        | `vcpkg install opencv4`          | Computer vision library                  |
| libtorch         | ❌ No         | Manual integration               | PyTorch C++ API                         |
| CUDA Toolkit     | ❌ No         | Manual integration               | NVIDIA GPU computing                    |

### Mixing vcpkg and Manual Libraries

You can use both approaches in the same project:

1. **Use vcpkg for supported libraries**:

   ```json
   {
       "dependencies": ["fmt", "raylib", "argparse"]
   }
   ```

2. **Manually configure unsupported libraries** in project properties or CMakeLists.txt

3. **Document your dependencies**:

   ```markdown
   # Dependencies
   ## vcpkg-managed:
   - fmt: formatting library
   - raylib: graphics library

   ## Manually integrated:
   - libtorch: C:\libraries\libtorch (v2.0.1)
   ```

### Platform and Architecture Considerations

#### Visual Studio Platform Settings

- **x64**: 64-bit applications (most common)
- **x86**: 32-bit applications (legacy support)
- **ARM64**: ARM processors (Surface Pro X, etc.)

Ensure vcpkg triplet matches your project:

- `x64-windows` for 64-bit
- `x86-windows` for 32-bit
- `arm64-windows` for ARM64

#### Build Configuration Matching

- **Debug**: Use debug versions of libraries (with debug symbols)
- **Release**: Use optimized release versions
- vcpkg typically provides both configurations

### Troubleshooting Common Issues

#### Linker Errors (LNK2019, LNK2001)

1. **Check library paths**: Ensure all directories are correctly specified
2. **Verify architecture**: x64 library with x64 project, etc.
3. **Check dependencies**: Some libraries require additional dependencies
4. **Runtime library**: Ensure consistent use of `/MT` or `/MD`

#### Runtime Errors (DLL not found)

1. **Copy DLLs to output directory**
2. **Add to PATH environment variable**
3. **Use Visual Studio's post-build events**:

   ```
   xcopy /y /d "$(SolutionDir)libs\*.dll" "$(OutDir)"
   ```

#### vcpkg Integration Issues

1. **Run integration command**:

   ```powershell
   .\vcpkg integrate install
   ```

2. **Verify VCPKG_ROOT environment variable**

3. **Check triplet compatibility**:

   ```powershell
   .\vcpkg list
   ```

### Best Practices

1. **Use vcpkg.json** for reproducible builds
2. **Document manual dependencies** with version numbers
3. **Check in vcpkg.json** but not vcpkg_installed folder
4. **Use CMake for cross-platform projects**
5. **Maintain separate debug/release configurations**
6. **Test on clean machines** to verify all dependencies are properly configured

## Summary

This guide provides comprehensive C++ development setup for Windows, supporting both:

- **VS Code**: Lightweight, cross-platform development with CMake/Ninja/Clang
- **Visual Studio**: Full IDE experience with integrated debugging and profiling

Both environments benefit from vcpkg package management while maintaining flexibility for manual library integration when needed.
