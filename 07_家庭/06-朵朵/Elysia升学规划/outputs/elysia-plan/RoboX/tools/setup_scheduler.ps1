# setup_scheduler.ps1 - Register Windows Task Scheduler weekly task
# Usage: Run as Administrator: .\setup_scheduler.ps1
# Default: every Monday at 9:00 AM

param(
    [string]$TaskName = "RoboX-BusinessModel-Analysis",
    [string]$ScheduleTime = "09:00",
    [string[]]$WeekDays = @("MON"),
    [switch]$Remove
)

$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$runScript = Join-Path $toolsDir "run_now.ps1"

if (-not (Test-Path $runScript)) {
    Write-Host "ERROR: run_now.ps1 not found: $runScript" -ForegroundColor Red
    exit 1
}

# Check admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "WARNING: Administrator privileges recommended for creating scheduled tasks." -ForegroundColor Yellow
    Write-Host "Please right-click and 'Run as Administrator' and retry." -ForegroundColor Yellow
}

# Remove existing task
if ($Remove) {
    Write-Host "Removing task '$TaskName'..." -ForegroundColor Yellow
    schtasks /Delete /TN $TaskName /F 2>$null
    Write-Host "Task removed." -ForegroundColor Green
    exit 0
}

# Delete if already exists
$existing = schtasks /Query /TN $TaskName 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Task '$TaskName' already exists, updating..." -ForegroundColor Yellow
    schtasks /Delete /TN $TaskName /F 2>$null
}

# Build day string
$daysStr = ($WeekDays -join ",")

# Create scheduled task
$triggerArgs = @(
    "/Create",
    "/TN", $TaskName,
    "/TR", "powershell.exe -ExecutionPolicy Bypass -File `"$runScript`" -Force",
    "/SC", "WEEKLY",
    "/D", $daysStr,
    "/ST", $ScheduleTime,
    "/RL", "HIGHEST",
    "/F"
)

Write-Host "Creating scheduled task..." -ForegroundColor Cyan
Write-Host "  Task Name: $TaskName"
Write-Host "  Script: $runScript"
Write-Host "  Schedule: Every $daysStr at $ScheduleTime"
Write-Host ""

$result = schtasks @triggerArgs 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Manage task:" -ForegroundColor Cyan
    Write-Host "  - Open Task Scheduler (taskschd.msc)"
    Write-Host "  - Or run: schtasks /Query /TN $TaskName /V"
    Write-Host ""
    Write-Host "Manual run:" -ForegroundColor Cyan
    Write-Host "  .\run_now.ps1 -Force"
} else {
    Write-Host "Task creation FAILED!" -ForegroundColor Red
    Write-Host $result -ForegroundColor Red
    Write-Host ""
    Write-Host "Please try running as Administrator." -ForegroundColor Yellow
}
