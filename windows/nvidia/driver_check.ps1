# NVIDIA Driver and CUDA Check Script
# This script checks for NVIDIA GPU, driver version, and CUDA availability

Write-Host "NVIDIA GPU and CUDA Information Check" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check GPU Information
Write-Host "GPU Information:" -ForegroundColor Yellow
$gpu = Get-CimInstance Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }
if ($gpu) {
    Write-Host "  GPU Name: $($gpu.Name)" -ForegroundColor Green
    Write-Host "  Driver Version: $($gpu.DriverVersion)" -ForegroundColor Green
    Write-Host "  VRAM: $([math]::Round($gpu.AdapterRAM / 1GB, 2)) GB" -ForegroundColor Green
} else {
    Write-Host "  No NVIDIA GPU detected" -ForegroundColor Red
}
Write-Host ""

# Check nvidia-smi
Write-Host "NVIDIA System Management Interface:" -ForegroundColor Yellow
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    # Get full nvidia-smi output
    $smiOutput = nvidia-smi | Select-String "Driver Version|CUDA Version"
    if ($smiOutput) {
        Write-Host "  $smiOutput" -ForegroundColor Green
    }
    # Also try simplified query
    try {
        $driverVersion = (nvidia-smi --query-gpu=driver_version --format=csv,noheader).Trim()
        Write-Host "  Driver Version: $driverVersion" -ForegroundColor Green
    } catch {
        # Fallback to parsing from full output
    }
} else {
    Write-Host "  nvidia-smi not found" -ForegroundColor Red
}
Write-Host ""

# Check CUDA Toolkit
Write-Host "CUDA Toolkit Installation:" -ForegroundColor Yellow
if (Get-Command nvcc -ErrorAction SilentlyContinue) {
    $nvccVersion = nvcc --version | Select-String "release"
    Write-Host "  CUDA Toolkit: Installed" -ForegroundColor Green
    Write-Host "  $nvccVersion" -ForegroundColor Gray
} else {
    Write-Host "  CUDA Toolkit: Not installed (nvcc not found)" -ForegroundColor Yellow
    Write-Host "  To install: winget install Nvidia.CUDA" -ForegroundColor Cyan
}
Write-Host ""

# Check for CUDA Environment Variables
Write-Host "CUDA Environment Variables:" -ForegroundColor Yellow
$cudaPath = [System.Environment]::GetEnvironmentVariable("CUDA_PATH")
if ($cudaPath) {
    Write-Host "  CUDA_PATH: $cudaPath" -ForegroundColor Green
} else {
    Write-Host "  CUDA_PATH: Not set" -ForegroundColor Yellow
}

$cudaPathV13 = [System.Environment]::GetEnvironmentVariable("CUDA_PATH_V13_0")
if ($cudaPathV13) {
    Write-Host "  CUDA_PATH_V13_0: $cudaPathV13" -ForegroundColor Green
}
Write-Host ""

# Installation Commands
Write-Host "Installation Commands:" -ForegroundColor Magenta
Write-Host "  Install CUDA Toolkit 13.0:" -ForegroundColor White
Write-Host "    winget install Nvidia.CUDA" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Or using Chocolatey:" -ForegroundColor White
Write-Host "    choco install cuda-toolkit" -ForegroundColor Cyan
Write-Host ""

# Summary
Write-Host "Summary:" -ForegroundColor Magenta
if ($gpu -and (Get-Command nvidia-smi -ErrorAction SilentlyContinue)) {
    Write-Host "  ✓ NVIDIA GPU detected and drivers installed" -ForegroundColor Green
    if (Get-Command nvcc -ErrorAction SilentlyContinue) {
        Write-Host "  ✓ CUDA Toolkit installed" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ CUDA Toolkit not installed (optional for ONNX Runtime)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✗ No NVIDIA GPU or drivers detected" -ForegroundColor Red
}