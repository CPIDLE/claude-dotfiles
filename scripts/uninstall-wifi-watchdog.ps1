<#
.SYNOPSIS
  Remove the WifiWatchdog scheduled task.

.DESCRIPTION
  Stops and unregisters the 'WifiWatchdog' scheduled task.
  Log file at %ProgramData%\wifi-watchdog\ is left in place.

  Must be run from an elevated PowerShell (Admin).
#>

#Requires -RunAsAdministrator

[CmdletBinding()]
param(
  [string]$TaskName = 'WifiWatchdog'
)

$ErrorActionPreference = 'Continue'

$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if (-not $task) {
  Write-Host "[SKIP] Task '$TaskName' not found." -ForegroundColor Yellow
  return
}

Write-Host "Stopping '$TaskName'..." -ForegroundColor Cyan
Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

Write-Host "Unregistering '$TaskName'..." -ForegroundColor Cyan
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false

Write-Host "[OK] Removed. Log retained at $env:ProgramData\wifi-watchdog\" -ForegroundColor Green
