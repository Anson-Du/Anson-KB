# run_now.ps1 - Execute analysis manually
# Usage: .\run_now.ps1 -Force [-Date "2026-08-07"]

param(
    [switch]$Force,
    [string]$Date
)

$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $toolsDir

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  RoboX Business Model Analysis - Manual Run" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVer = python --version 2>&1
    Write-Host "Python: $pythonVer" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import yaml" 2>$null
} catch {
    Write-Host "  Missing PyYAML, installing..." -ForegroundColor Yellow
    pip install PyYAML
}
try {
    python -c "import docx" 2>$null
} catch {
    Write-Host "  Missing python-docx, installing..." -ForegroundColor Yellow
    pip install python-docx
}

# Build arguments
$args = @()
if ($Force) {
    $args += "--force"
    Write-Host "Mode: Full scan" -ForegroundColor Yellow
} else {
    Write-Host "Mode: Incremental scan (this week)" -ForegroundColor Yellow
}
if ($Date) {
    $args += "--date"
    $args += $Date
    Write-Host "Date: $Date" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting analysis..." -ForegroundColor Cyan
Write-Host ""

# Execute
python run.py @args

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
