# Using NuGet Packages in CMake C++ Projects

## Overview

NuGet packages can be integrated into CMake C++ projects using CMake's `FetchContent` module. This approach automatically downloads and configures NuGet packages during the CMake configuration phase, making them available as dependencies without manual installation.

## Basic Integration Pattern

### 1. Include FetchContent Module

```cmake
cmake_minimum_required(VERSION 3.14)  # FetchContent requires 3.14+
include(FetchContent)
```

### 2. Declare and Download NuGet Package

```cmake
FetchContent_Declare(
    package_name
    URL https://www.nuget.org/api/v2/package/Package.Name/1.0.0
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
FetchContent_MakeAvailable(package_name)
```

### 3. Configure Package Paths

NuGet packages typically have a standard structure that you need to navigate:

```cmake
# Set paths based on NuGet package structure
set(PACKAGE_ROOT "${package_name_SOURCE_DIR}")
set(PACKAGE_INCLUDE "${PACKAGE_ROOT}/build/native/include")
set(PACKAGE_LIB "${PACKAGE_ROOT}/lib")
```

## Architecture-Specific Configuration

Many NuGet packages contain platform-specific binaries. Here's how to handle multiple architectures:

```cmake
# Detect architecture
if(CMAKE_SYSTEM_PROCESSOR MATCHES "ARM64" OR CMAKE_GENERATOR_PLATFORM MATCHES "ARM64")
    set(PLATFORM_ARCH "arm64")
    set(PLATFORM_NAME "win-arm64")
elseif(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(PLATFORM_ARCH "x64")
    set(PLATFORM_NAME "win-x64")
else()
    set(PLATFORM_ARCH "x86")
    set(PLATFORM_NAME "win-x86")
endif()

# Use architecture-specific paths
set(PACKAGE_RUNTIME "${PACKAGE_ROOT}/runtimes/${PLATFORM_NAME}/native")
set(PACKAGE_LIB_DIR "${PACKAGE_ROOT}/lib/${PLATFORM_NAME}")
```

## Complete Example: ONNX Runtime Integration

Here's a real-world example of integrating the Microsoft.AI.MachineLearning NuGet package:

```cmake
cmake_minimum_required(VERSION 3.14)
project(MyMLProject)

include(FetchContent)

# Download ONNX Runtime NuGet package
message(STATUS "Fetching ONNX Runtime NuGet package...")
FetchContent_Declare(
    onnxruntime
    URL https://www.nuget.org/api/v2/package/Microsoft.AI.MachineLearning/1.19.2
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
FetchContent_MakeAvailable(onnxruntime)

# Determine architecture
if(CMAKE_SYSTEM_PROCESSOR MATCHES "ARM64")
    set(ORT_PLATFORM "win-arm64")
else()
    set(ORT_PLATFORM "win-x64")
endif()

# Configure paths
set(ORT_ROOT "${onnxruntime_SOURCE_DIR}")
set(ORT_INCLUDE_DIR "${ORT_ROOT}/build/native/include")
set(ORT_RUNTIME_DIR "${ORT_ROOT}/runtimes/${ORT_PLATFORM}/_native")
set(ORT_LIB_DIR "${ORT_RUNTIME_DIR}")

# Add to your target
add_executable(${PROJECT_NAME} main.cpp)

target_include_directories(${PROJECT_NAME} PRIVATE ${ORT_INCLUDE_DIR})

target_link_libraries(${PROJECT_NAME} PRIVATE
    "${ORT_LIB_DIR}/onnxruntime.lib"
)

# Copy runtime DLLs to output directory
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${ORT_RUNTIME_DIR}/onnxruntime.dll"
        "$<TARGET_FILE_DIR:${PROJECT_NAME}>"
    COMMENT "Copying ONNX Runtime DLL"
)
```

## Handling Different NuGet Package Structures

NuGet packages can have varying internal structures. Common patterns include:

### Pattern 1: Simple Library Package
```
package/
├── lib/
│   ├── net5.0/
│   └── native/
├── include/
└── package.nuspec
```

### Pattern 2: Multi-Platform Package
```
package/
├── runtimes/
│   ├── win-x64/
│   │   └── native/
│   ├── win-x86/
│   │   └── native/
│   └── win-arm64/
│       └── native/
├── build/
│   └── native/
│       └── include/
└── package.nuspec
```

### Pattern 3: Framework-Dependent Package
```
package/
├── lib/
│   ├── net6.0/
│   ├── netstandard2.0/
│   └── uap10.0/
├── ref/
└── tools/
```

## Verification and Error Handling

Always verify that expected files exist:

```cmake
# Verify critical files exist
if(NOT EXISTS "${PACKAGE_LIB_DIR}/library.lib")
    message(FATAL_ERROR "Library not found at ${PACKAGE_LIB_DIR}")
endif()

# Optional: List package contents for debugging
message(STATUS "Package root: ${PACKAGE_ROOT}")
message(STATUS "Package includes: ${PACKAGE_INCLUDE_DIR}")
message(STATUS "Package libraries: ${PACKAGE_LIB_DIR}")
```

## Runtime DLL Management

For Windows packages with DLLs, ensure they're copied to the output:

```cmake
# Copy all DLLs from package to output
file(GLOB PACKAGE_DLLS "${PACKAGE_RUNTIME_DIR}/*.dll")
foreach(DLL ${PACKAGE_DLLS})
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            "${DLL}"
            "$<TARGET_FILE_DIR:${PROJECT_NAME}>"
    )
endforeach()
```

## Advanced: Using CMake Presets with NuGet

Configure presets for different architectures:

```json
{
  "version": 3,
  "presets": [
    {
      "name": "x64",
      "generator": "Visual Studio 17 2022",
      "architecture": "x64",
      "binaryDir": "build"
    },
    {
      "name": "arm64",
      "generator": "Visual Studio 17 2022",
      "architecture": "ARM64",
      "binaryDir": "build-arm64"
    }
  ]
}
```

## Troubleshooting Common Issues

### Issue 1: Download Failures
- Check the NuGet package URL format
- Try the v3 API: `https://api.nuget.org/v3-flatcontainer/package.name/version/package.name.version.nupkg`
- Verify package name capitalization

### Issue 2: Missing Headers
- NuGet packages may not include headers
- Some packages require separate development packages
- Check `build/native/include` or `include` directories

### Issue 3: Architecture Mismatch
- Ensure CMAKE_GENERATOR_PLATFORM matches the target architecture
- Check that the NuGet package supports your target platform

### Issue 4: Version Conflicts
- Pin specific versions in FetchContent_Declare
- Use package.lock.json for reproducible builds
- Consider using vcpkg instead for C++ libraries when available

## Best Practices

1. **Cache Downloads**: FetchContent caches downloads in the build directory
2. **Version Pinning**: Always specify exact versions for reproducibility
3. **Platform Detection**: Use CMake variables to detect the target platform
4. **Error Messages**: Provide clear error messages when packages aren't found
5. **Documentation**: Document which NuGet packages are required and why

## Alternative: Using NuGet CLI

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

## When to Use NuGet vs Other Package Managers

### Use NuGet when:
- The library is only available as a NuGet package
- You're targeting Windows platforms exclusively
- The package includes Windows-specific binaries or APIs
- You need .NET interop libraries

### Consider alternatives when:
- **vcpkg**: For cross-platform C++ libraries
- **Conan**: For complex dependency management
- **CPM**: For header-only libraries from GitHub
- **FetchContent with Git**: For source-based dependencies

## Conclusion

Integrating NuGet packages with CMake provides a clean way to manage Windows-specific dependencies in C++ projects. The key is understanding the package structure and properly configuring paths for your target architecture.