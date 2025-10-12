---
tags: [windows, reference, guide, api, best-practices, patterns]
---
# Windows App SDK Setup Guide for CMake C++ Projects

## Overview

This guide covers how to properly set up a modern C++23 CMake project to use Windows App SDK, WinRT APIs, and NuGet packages. Windows App SDK is the modern successor to UWP, providing access to the latest Windows APIs for both packaged and unpackaged desktop applications.

**IMPORTANT**: Setting up Windows App SDK for unpackaged C++ applications is complex and requires careful attention to package dependencies, runtime requirements, and build configuration. This guide provides the complete, tested solution.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Understanding Key Concepts](#understanding-key-concepts)
3. [CMake Configuration](#cmake-configuration)
4. [Code Implementation](#code-implementation)
5. [Runtime Requirements](#runtime-requirements)
6. [Troubleshooting](#troubleshooting)
7. [API Comparison](#api-comparison)

## Prerequisites

### Required Software

- **Windows 10/11** (version 1809 or later)
- **Visual Studio 2022** with C++ desktop development workload
- **CMake 3.14+** (for FetchContent support)
- **Windows SDK** (10.0.17763.0 or later)
- **Windows App SDK Runtime** (must be installed separately for unpackaged apps)

### Installing Windows App SDK Runtime

For unpackaged applications, users must install the Windows App SDK runtime:

1. Download from: https://learn.microsoft.com/windows/apps/windows-app-sdk/downloads
2. Choose the appropriate architecture (x64, x86, or ARM64)
3. Install the runtime package (e.g., `WindowsAppRuntimeInstall-1.7.exe`)

## Understanding Key Concepts

### Packaged vs Unpackaged Apps

- **Packaged Apps**: Distributed through MSIX, include all dependencies
- **Unpackaged Apps**: Traditional Win32 apps, require runtime to be installed separately

### WinRT (Windows Runtime)

- Modern Windows API projection for various languages
- In C++, accessed through C++/WinRT headers (`winrt/*.h`)
- Namespace-based organization (e.g., `Windows::Foundation`, `Windows::AI::MachineLearning`)

### Windows App SDK vs Legacy APIs

- **Legacy APIs**: Built into Windows (e.g., `Windows::AI::MachineLearning`)
- **Modern APIs**: Distributed via Windows App SDK (e.g., `Microsoft::Windows::*`)

## CMake Configuration

### Self-Contained Build System (CRITICAL)

For a truly self-contained build that works across thousands of developer machines without pre-installed dependencies, you MUST fetch all required packages automatically. The Windows App SDK is distributed across multiple NuGet packages with complex interdependencies.

### Complete CMakeLists.txt Example (Tested & Working)

```cmake
cmake_minimum_required(VERSION 3.14)
project(MyWinAppSDKProject CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Windows-specific definitions
add_compile_definitions(
    WINRT_LEAN_AND_MEAN
    WIN32_LEAN_AND_MEAN
    NOMINMAX
    _WIN32_WINNT=0x0A00  # Windows 10
    WINVER=0x0A00
)

# Include FetchContent for NuGet packages
include(FetchContent)

# CRITICAL: For experimental features (Windows ML), use 1.8-experimental4
# Main Windows App SDK package
message(STATUS "Fetching Windows App SDK 1.8-experimental4...")
FetchContent_Declare(
    windowsappsdk
    URL https://www.nuget.org/api/v2/package/Microsoft.WindowsAppSDK/1.8.250702007-experimental4
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)

# CRITICAL: Foundation package contains MddBootstrap.h!
message(STATUS "Fetching Windows App SDK Foundation...")
FetchContent_Declare(
    windowsappsdk_foundation
    URL https://www.nuget.org/api/v2/package/Microsoft.WindowsAppSDK.Foundation/1.8.250701000-experimental
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)

# For ML features (optional)
message(STATUS "Fetching Windows App SDK ML...")
FetchContent_Declare(
    windowsml
    URL https://www.nuget.org/api/v2/package/Microsoft.WindowsAppSDK.ML/1.8.126-experimental
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)

# Make all packages available
FetchContent_MakeAvailable(windowsappsdk windowsappsdk_foundation windowsml)

# Determine architecture
if(CMAKE_SYSTEM_PROCESSOR MATCHES "ARM64" OR CMAKE_GENERATOR_PLATFORM MATCHES "ARM64")
    set(ARCH "arm64")
else()
    set(ARCH "x64")
endif()

# CRITICAL PATH CONFIGURATION
# The package structure is NOT intuitive!
set(WINSDK_ROOT "${windowsappsdk_SOURCE_DIR}")
set(WINSDK_FOUNDATION_ROOT "${windowsappsdk_foundation_SOURCE_DIR}")

# MddBootstrap.h is in Foundation package, NOT main package!
set(WINSDK_INCLUDE_DIR "${WINSDK_FOUNDATION_ROOT}/include")

# Libraries are in native/${ARCH}, NOT win10-${ARCH}!
set(WINSDK_LIB_DIR "${WINSDK_FOUNDATION_ROOT}/lib/native/${ARCH}")

# Runtime DLLs path - CRITICAL: It's win-${ARCH}, NOT win10-${ARCH}!
set(WINSDK_RUNTIME_DIR "${WINSDK_FOUNDATION_ROOT}/runtimes/win-${ARCH}/native")

# Create executable
add_executable(${PROJECT_NAME} main.cpp)

# Include directories
target_include_directories(${PROJECT_NAME}
    PRIVATE
        ${WINSDK_INCLUDE_DIR}
)

# Link directories
target_link_directories(${PROJECT_NAME}
    PRIVATE
        ${WINSDK_LIB_DIR}
)

# Link libraries
target_link_libraries(${PROJECT_NAME}
    PRIVATE
        windowsapp.lib  # Windows Runtime support
        Microsoft.WindowsAppRuntime.Bootstrap.lib  # Bootstrap for unpackaged apps
)

# Enable C++/WinRT features
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE
        /EHsc   # Enable C++ exceptions
        /await  # Enable coroutines
    )
endif()

# Copy runtime DLLs to output directory
if(EXISTS "${WINSDK_RUNTIME_DIR}/Microsoft.WindowsAppRuntime.Bootstrap.dll")
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            "${WINSDK_RUNTIME_DIR}/Microsoft.WindowsAppRuntime.Bootstrap.dll"
            "$<TARGET_FILE_DIR:${PROJECT_NAME}>"
        COMMENT "Copying Windows App SDK Bootstrap DLL"
    )
endif()
```

### Using Multiple NuGet Packages

```cmake
# Example: Adding multiple NuGet packages
FetchContent_Declare(
    windowsappsdk
    URL https://www.nuget.org/api/v2/package/Microsoft.WindowsAppSDK/1.7.250606001
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)

FetchContent_Declare(
    win2d
    URL https://www.nuget.org/api/v2/package/Win2D.Win32/1.2.0
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)

FetchContent_MakeAvailable(windowsappsdk win2d)
```

## Code Implementation

### Basic Unpackaged App with Bootstrap

```cpp
// CRITICAL: Include order matters!
#include <windows.h>  // MUST be first for MddBootstrap.h to work
#include <iostream>
#include <winrt/base.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/Windows.Foundation.Collections.h>
#include <MddBootstrap.h>  // Windows App SDK bootstrap

// Include any Windows App SDK headers
#include <winrt/Microsoft.Windows.AppLifecycle.h>

int main() {
    // Initialize COM apartment
    winrt::init_apartment();
    
    // Initialize Windows App SDK for unpackaged app
    // CRITICAL: Version must match your NuGet package version!
    
    // For 1.8-experimental4:
    const UINT32 majorMinorVersion = 0x00010008; // 1.8
    const PCWSTR versionTag = L"experimental4";  // Experimental channel
    PACKAGE_VERSION minVersion = {};
    minVersion.Major = 1;
    minVersion.Minor = 8;
    minVersion.Build = 250702007;  // EXACT build number from package
    minVersion.Revision = 0;
    
    // For stable 1.7:
    // const UINT32 majorMinorVersion = 0x00010007; // 1.7
    // const PCWSTR versionTag = nullptr;
    // PACKAGE_VERSION minVersion = {1, 7, 0, 0};
    
    HRESULT hr = MddBootstrapInitialize2(
        majorMinorVersion,
        versionTag,
        minVersion,
        MddBootstrapInitializeOptions_OnNoMatch_ShowUI  // Shows install dialog
    );
    
    if (FAILED(hr)) {
        std::cerr << "Failed to initialize Windows App SDK: 0x" 
                  << std::hex << hr << std::endl;
        
        // Common error codes:
        // 0x80070490 - Element not found (runtime not installed)
        // 0x80070005 - Access denied
        // 0x-7F98FFEA (0x80670016) - ERROR_INSTALL_PREREQUISITE_FAILED
        
        if (hr == HRESULT_FROM_WIN32(ERROR_FILE_NOT_FOUND) || 
            hr == 0x80670016) {  // ERROR_INSTALL_PREREQUISITE_FAILED
            std::cerr << "Windows App Runtime is not installed.\n";
            std::cerr << "Please install from: "
                      << "https://learn.microsoft.com/windows/apps/windows-app-sdk/downloads\n";
            std::cerr << "Install the runtime for version 1.8-experimental4\n";
        }
        return -1;
    }
    
    // Use Windows App SDK APIs here
    try {
        // Example: Using modern Windows APIs
        auto activation = winrt::Microsoft::Windows::AppLifecycle::AppInstance::GetCurrent();
        // ... your code ...
    }
    catch (winrt::hresult_error const& ex) {
        std::wcerr << L"Error: " << ex.message().c_str() << std::endl;
    }
    
    // CRITICAL: Always shutdown when done
    MddBootstrapShutdown();
    return 0;
}
```

### Using WinRT APIs (Legacy Windows APIs)

```cpp
#include <winrt/Windows.Storage.h>
#include <winrt/Windows.System.h>

void UseBuiltInWindowsAPIs() {
    using namespace winrt;
    using namespace Windows::Storage;
    using namespace Windows::System;
    
    // These APIs are built into Windows, no App SDK required
    auto localFolder = ApplicationData::Current().LocalFolder();
    auto userName = User::FindAllAsync().get().GetAt(0).NonRoamableId();
}
```

## Runtime Requirements

### For Developers

1. Install Visual Studio 2022 with C++ workload
2. Install Windows SDK
3. No additional runtime needed for development

### For End Users (Unpackaged Apps)

1. **Windows App SDK Runtime** must be installed
2. Download from official Microsoft site
3. Version must match or exceed the version used in development

### Bootstrap Options

```cpp
// Different bootstrap options
MddBootstrapInitialize2(
    majorMinorVersion,
    versionTag,
    minVersion,
    MddBootstrapInitializeOptions_OnError_DebugBreak           // Debug break on error
    // OR
    MddBootstrapInitializeOptions_OnError_DebugBreak_IfDebuggerAttached  // Conditional break
    // OR
    MddBootstrapInitializeOptions_OnError_FailFast              // Immediate termination
    // OR
    MddBootstrapInitializeOptions_OnNoMatch_ShowUI              // Show install dialog
    // OR
    MddBootstrapInitializeOptions_OnPackageIdentity_NOOP        // Do nothing for packaged apps
);
```

## Troubleshooting

### Common Errors and Solutions

#### Error: `0x80070490` (Element not found)
- **Cause**: Windows App SDK runtime not installed or wrong version
- **Solution**: Install the runtime from the official download page
- **Note**: This happens when trying to use `Microsoft::Windows::*` APIs without runtime

#### Error: `0x80670016` or `0x-7F98FFEA` (ERROR_INSTALL_PREREQUISITE_FAILED)
- **Cause**: Missing Windows App SDK runtime
- **Solution**: Install runtime - a dialog should appear with download link
- **Important**: The negative hex value is how it appears in some error outputs

#### Error: Cannot open include file 'MddBootstrap.h'
- **Cause 1**: Windows.h not included before MddBootstrap.h
- **Solution**: Always include `<windows.h>` first
- **Cause 2**: Using wrong package - MddBootstrap.h is in Foundation package
- **Solution**: Must fetch Microsoft.WindowsAppSDK.Foundation package

#### Error: Cannot open input file 'Microsoft.WindowsAppRuntime.Bootstrap.lib'
- **Cause**: Wrong library path in CMake
- **Solution**: Library is in `lib/native/${ARCH}/`, NOT `lib/win10-${ARCH}/`

#### Error: Program exits immediately without output
- **Cause**: Missing Microsoft.WindowsAppRuntime.Bootstrap.dll at runtime
- **Solution**: Runtime DLLs are in `runtimes/win-${ARCH}/native/`, NOT `runtimes/win10-${ARCH}/native/`
- **Note**: The Bootstrap DLL must be copied to the output directory or the program will fail to start

#### Error: NuGet package not found (404)
- **Cause**: Wrong version number or package name
- **Real versions**: 
  - 1.8.250702007-experimental4 (NOT 1.8.250730009-experimental4)
  - Check exact version with: `nuget list Microsoft.WindowsAppSDK -PreRelease`

#### Build succeeds but APIs fail at runtime
- **Cause**: Runtime version mismatch
- **Solution**: Ensure MddBootstrapInitialize2 uses exact version from your NuGet package

### Verifying Installation

```powershell
# Check if Windows App SDK is installed
Get-AppxPackage | Where-Object {$_.Name -like "*WindowsAppRuntime*"}

# List all Windows App SDK packages
Get-AppxPackage -AllUsers | Where-Object {$_.Name -match "WindowsAppSDK"}
```

## API Comparison

### Legacy Windows APIs (Built-in)
- **Namespace**: `Windows::*`
- **Example**: `Windows::AI::MachineLearning`
- **Availability**: Always available on Windows 10/11
- **Distribution**: Part of Windows OS
- **Bootstrap**: Not required

### Modern Windows App SDK APIs
- **Namespace**: `Microsoft::Windows::*`
- **Example**: `Microsoft::Windows::AI::MachineLearning`
- **Availability**: Requires Windows App SDK runtime
- **Distribution**: NuGet packages
- **Bootstrap**: Required for unpackaged apps

## Best Practices

1. **Always Initialize Bootstrap First**: Before using any Windows App SDK APIs
2. **Handle Initialization Failures Gracefully**: Provide clear error messages
3. **Use FetchContent for NuGet**: Automates package management in CMake
4. **Copy Runtime DLLs**: Include them with your application for easier deployment
5. **Version Management**: Specify exact versions for reproducible builds
6. **Architecture Awareness**: Handle x64, x86, and ARM64 appropriately

## General NuGet Package Integration with CMake

### Understanding NuGet Package Structures

NuGet packages can have varying internal structures. Common patterns include:

#### Pattern 1: Simple Library Package
```
package/
├── lib/
│   ├── net5.0/
│   └── native/
├── include/
└── package.nuspec
```

#### Pattern 2: Multi-Platform Package (like Windows App SDK)
```
package/
├── runtimes/
│   ├── win-x64/          # Note: Sometimes win10-x64/
│   │   └── native/
│   ├── win-x86/
│   │   └── native/
│   └── win-arm64/
│       └── native/
├── lib/
│   └── native/
│       └── ${ARCH}/      # Architecture-specific libs
├── build/
│   └── native/
│       └── include/
└── package.nuspec
```

#### Pattern 3: Framework-Dependent Package
```
package/
├── lib/
│   ├── net6.0/
│   ├── netstandard2.0/
│   └── uap10.0/
├── ref/
└── tools/
```

### Alternative NuGet API Endpoints

If the v2 API fails, try the v3 API:

```cmake
# V2 API (standard, what we use above)
FetchContent_Declare(
    package
    URL https://www.nuget.org/api/v2/package/Package.Name/1.0.0
)

# V3 API (alternative if v2 fails)
FetchContent_Declare(
    package
    URL https://api.nuget.org/v3-flatcontainer/package.name/1.0.0/package.name.1.0.0.nupkg
)
```

### Using NuGet CLI as Alternative

For packages that don't work well with FetchContent:

```cmake
# Use execute_process to run NuGet CLI
execute_process(
    COMMAND nuget restore packages.config -PackagesDirectory ${CMAKE_BINARY_DIR}/packages
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)

# Then reference the restored packages
set(PACKAGE_DIR "${CMAKE_BINARY_DIR}/packages/Package.Name.1.0.0")
```

### When to Use NuGet vs Other Package Managers

#### Use NuGet when:
- The library is only available as a NuGet package (like Windows App SDK)
- You're targeting Windows platforms exclusively
- The package includes Windows-specific binaries or APIs
- You need .NET interop libraries
- Working with Microsoft frameworks and SDKs

#### Consider alternatives when:
- **vcpkg**: For cross-platform C++ libraries with CMake integration
- **Conan**: For complex dependency management across platforms
- **CPM**: For header-only libraries from GitHub
- **FetchContent with Git**: For source-based dependencies

## Additional Resources

- [Windows App SDK Documentation](https://learn.microsoft.com/windows/apps/windows-app-sdk/)
- [C++/WinRT Documentation](https://learn.microsoft.com/windows/uwp/cpp-and-winrt-apis/)
- [Windows App SDK Samples](https://github.com/microsoft/WindowsAppSDK-Samples)
- [NuGet Package Explorer](https://github.com/NuGetPackageExplorer/NuGetPackageExplorer)
- [NuGet API Documentation](https://docs.microsoft.com/nuget/api/overview)
- [CMake FetchContent Documentation](https://cmake.org/cmake/help/latest/module/FetchContent.html)

## Package Dependencies

### Critical NuGet Packages for Windows App SDK

For a complete Windows App SDK setup with ML features, you need:

1. **Microsoft.WindowsAppSDK** - Main package
2. **Microsoft.WindowsAppSDK.Foundation** - Contains MddBootstrap.h and libraries
3. **Microsoft.WindowsAppSDK.ML** - Machine Learning APIs (experimental)
4. **Microsoft.WindowsAppSDK.Runtime** - Runtime components (renamed from Packages)

### Finding Package Versions

```powershell
# Download nuget.exe
Invoke-WebRequest -Uri 'https://dist.nuget.org/win-x86-commandline/latest/nuget.exe' -OutFile 'nuget.exe'

# List available versions
.\nuget.exe list Microsoft.WindowsAppSDK -PreRelease -AllVersions

# Check specific experimental versions
.\nuget.exe list Microsoft.WindowsAppSDK -PreRelease | Select-String 'experimental'
```

## Version History

### Experimental Versions (As of August 2025)
- **1.8.250702007-experimental4** - Latest experimental with ML features
- **1.8.250610002-experimental3** - Previous experimental
- **Microsoft.WindowsAppSDK.ML 1.8.126-experimental** - ML package version

### Stable Versions
- **Windows App SDK 1.7.3** (Latest stable)
- **Windows App SDK 1.6** (Previous stable)
- **Windows App SDK 1.5** (LTS - Long Term Support)

## Key Learnings

1. **Package Structure is Complex**: The Windows App SDK is split across multiple packages with non-obvious dependencies
2. **Foundation Package is Critical**: MddBootstrap.h is NOT in the main package
3. **Path Structures Vary**: 
   - Libraries are in `lib/native/${ARCH}`, not `lib/win10-${ARCH}`
   - Runtime DLLs are in `runtimes/win-${ARCH}/native/`, NOT `runtimes/win10-${ARCH}/native/`
4. **Version Numbers Must Match Exactly**: Bootstrap initialization requires precise version matching
5. **Runtime Installation is Mandatory**: Unlike legacy APIs, Windows App SDK requires runtime installation
6. **Documentation Can Be Misleading**: Official docs may show version numbers that don't exist on NuGet
7. **Bootstrap DLL is Critical**: The program will exit immediately if Microsoft.WindowsAppRuntime.Bootstrap.dll is missing

## Summary

Setting up Windows App SDK with CMake for a self-contained build requires:

1. **Multiple NuGet packages** via FetchContent (Main, Foundation, ML)
2. **Correct path configuration** (non-intuitive package structure)
3. **Exact version matching** in bootstrap initialization
4. **Runtime installation** on target machines (shows dialog on first run)
5. **Proper include order** (Windows.h must come first)
6. **Understanding package dependencies** (Foundation contains bootstrap components)

This setup enables access to the latest Windows APIs including experimental ML features, while maintaining a build system that works consistently across developer machines without pre-installed dependencies.

## Related Concepts

### Prerequisites
- [[cpp_project]] - Need C++ project setup fundamentals first
- [[powershell]] - PowerShell used for Windows environment configuration

### Related Topics
- [[windows_ml]] - Windows App SDK provides access to Windows ML APIs
- [[dotnet]] - Windows App SDK also available for .NET projects
- [[copilot_runtime]] - Windows App SDK provides access to Copilot Runtime APIs
- [[cpp_project]] - Windows-specific SDK setup builds on this
- [[powershell]] - PowerShell used for Windows environment configuration

### Extends
- [[cpp_project]] - Specialized Windows-specific C++ project setup

### Extended By
- [[windows_ai_stack_explained]] - Practical setup example using Windows App SDK