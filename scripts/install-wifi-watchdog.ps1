<#
.SYNOPSIS
  Install wifi-watchdog.ps1 as a Scheduled Task (SYSTEM, at startup).

.DESCRIPTION
  Registers a scheduled task named 'WifiWatchdog' that runs wifi-watchdog.ps1
  under the SYSTEM account at system startup. SYSTEM has the privileges needed
  for Disable-NetAdapter / Enable-NetAdapter and works even when no user is
  logged on.

  Must be run from an elevated PowerShell (Admin).
#>

#Requires -RunAsAdministrator

[CmdletBinding()]
param(
  [string]$TaskName = 'WifiWatchdog',
  [string]$ScriptPath = (Join-Path $PSScriptRoot 'wifi-watchdog.ps1')
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $ScriptPath)) {
  throw "Watchdog script not found: $ScriptPath"
}
$ScriptPath = (Resolve-Path -LiteralPath $ScriptPath).Path

Write-Host "Installing scheduled task '$TaskName'" -ForegroundColor Cyan
Write-Host "  Script: $ScriptPath"

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
  Write-Host "  Existing task found - removing..." -ForegroundColor Yellow
  Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
  Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

$action = New-ScheduledTaskAction `
  -Execute 'powershell.exe' `
  -Argument ('-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "{0}"' -f $ScriptPath)

$triggerBoot  = New-ScheduledTaskTrigger -AtStartup
$triggerLogon = New-ScheduledTaskTrigger -AtLogOn

$principal = New-ScheduledTaskPrincipal `
  -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest

$settings = New-ScheduledTaskSettingsSet `
  -AllowStartIfOnBatteries `
  -DontStopIfGoingOnBatteries `
  -StartWhenAvailable `
  -RestartCount 999 `
  -RestartInterval (New-TimeSpan -Minutes 1) `
  -ExecutionTimeLimit (New-TimeSpan -Days 365) `
  -MultipleInstances IgnoreNew

Register-ScheduledTask `
  -TaskName $TaskName `
  -Action $action `
  -Trigger @($triggerBoot, $triggerLogon) `
  -Principal $principal `
  -Settings $settings `
  -Description 'Probes WAN connectivity and auto-recovers with exponential backoff (5s -> 6hr cap).' `
  | Out-Null

Write-Host "[OK] Task registered." -ForegroundColor Green
Write-Host "Starting task now..." -ForegroundColor Cyan
Start-ScheduledTask -TaskName $TaskName

$logPath = "$env:ProgramData\wifi-watchdog\wifi-watchdog.log"
Write-Host ""
Write-Host "Log file: $logPath"
Write-Host "Live view: Get-Content -Wait -Tail 20 '$logPath'"
Write-Host "Status:    Get-ScheduledTask -TaskName '$TaskName' | Get-ScheduledTaskInfo"
Write-Host "Remove:    powershell -ExecutionPolicy Bypass -File '$PSScriptRoot\uninstall-wifi-watchdog.ps1'"
