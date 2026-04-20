<#
.SYNOPSIS
  Probe-driven WAN connectivity watchdog with exponential backoff recovery.

.DESCRIPTION
  Periodically probes external connectivity (ICMP + HTTP). On outage, enters
  an exponential-backoff retry loop and progressively escalates recovery
  actions: ipconfig renew, then adapter bounce. Logs to file.

  Intended to run as a Scheduled Task under SYSTEM at startup.
  Install via install-wifi-watchdog.ps1.

.PARAMETER InitialDelay
  First retry delay in seconds. Default 5.

.PARAMETER MaxDelay
  Maximum delay cap in seconds. Default 21600 (6 hours).

.PARAMETER NormalPollInterval
  Poll interval in seconds when healthy. Default 30.

.PARAMETER LogPath
  Path to log file. Default %ProgramData%\wifi-watchdog\wifi-watchdog.log.

.PARAMETER ProbeTargets
  ICMP targets (array). Default: 8.8.8.8, 1.1.1.1.

.PARAMETER ProbeUrl
  HTTP fallback probe URL. Default: MS NCSI endpoint.
#>

[CmdletBinding()]
param(
  [int]$InitialDelay = 5,
  [int]$MaxDelay = 21600,
  [int]$NormalPollInterval = 30,
  [string]$LogPath = "$env:ProgramData\wifi-watchdog\wifi-watchdog.log",
  [string[]]$ProbeTargets = @('8.8.8.8', '1.1.1.1'),
  [string]$ProbeUrl = 'http://www.msftconnecttest.com/connecttest.txt',
  [int]$PingTimeoutMs = 2000,
  [int]$HttpTimeoutSec = 5
)

$ErrorActionPreference = 'Continue'

$logDir = Split-Path -Parent $LogPath
if (-not (Test-Path $logDir)) {
  New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

function Write-Log {
  param([string]$Level, [string]$Msg)
  $line = '{0} [{1,-7}] {2}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Level, $Msg
  try {
    Add-Content -Path $LogPath -Value $line -ErrorAction Stop
  } catch {
    # If log write fails (disk full, perms), fall back to stderr so Task Scheduler
    # event log still captures something. Do not crash the watchdog.
    [Console]::Error.WriteLine($line)
  }
}

function Test-Ping {
  param([string]$TargetHost, [int]$TimeoutMs = 2000)
  $ping = New-Object System.Net.NetworkInformation.Ping
  try {
    $r = $ping.Send($TargetHost, $TimeoutMs)
    return ($r -and $r.Status -eq 'Success')
  } catch {
    return $false
  } finally {
    if ($ping) { $ping.Dispose() }
  }
}

function Test-Http {
  param([string]$Url, [int]$TimeoutSec = 5)
  try {
    $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec $TimeoutSec -ErrorAction Stop
    return ($r.StatusCode -ge 200 -and $r.StatusCode -lt 400)
  } catch {
    return $false
  }
}

function Test-Connectivity {
  foreach ($t in $ProbeTargets) {
    if (Test-Ping -TargetHost $t -TimeoutMs $PingTimeoutMs) { return $true }
  }
  # HTTP fallback — covers cases where ICMP is blocked but the net is up.
  if (Test-Http -Url $ProbeUrl -TimeoutSec $HttpTimeoutSec) { return $true }
  return $false
}

function Get-WifiAdapter {
  try {
    $a = Get-NetAdapter -Physical -ErrorAction Stop | Where-Object {
      $_.Status -ne 'Disabled' -and (
        $_.MediaType -eq 'Native 802.11' -or
        $_.PhysicalMediaType -eq 'Native 802.11' -or
        $_.InterfaceDescription -match 'Wi-?Fi|Wireless|802\.11'
      )
    } | Select-Object -First 1
    return $a
  } catch {
    return $null
  }
}

function Invoke-Recover {
  param([int]$Attempt)

  Write-Log 'INFO' "Recovery attempt #$Attempt"

  if ($Attempt -ge 2) {
    Write-Log 'ACTION' 'ipconfig /release + /renew + /flushdns'
    & ipconfig /release 2>&1 | Out-Null
    Start-Sleep -Seconds 1
    & ipconfig /renew   2>&1 | Out-Null
    & ipconfig /flushdns 2>&1 | Out-Null
  }

  if ($Attempt -ge 3) {
    $iface = Get-WifiAdapter
    if ($iface) {
      Write-Log 'ACTION' ("Bounce adapter '{0}' ({1})" -f $iface.Name, $iface.InterfaceDescription)
      try {
        Disable-NetAdapter -Name $iface.Name -Confirm:$false -ErrorAction Stop
        Start-Sleep -Seconds 2
        Enable-NetAdapter -Name $iface.Name -Confirm:$false -ErrorAction Stop
      } catch {
        Write-Log 'WARN' "Adapter bounce failed: $($_.Exception.Message)"
      }
    } else {
      Write-Log 'WARN' 'No Wi-Fi adapter found for bounce'
    }
  }
}

Write-Log 'START' ("wifi-watchdog started. InitialDelay={0}s MaxDelay={1}s Poll={2}s PID={3}" -f `
  $InitialDelay, $MaxDelay, $NormalPollInterval, $PID)

while ($true) {
  if (Test-Connectivity) {
    Start-Sleep -Seconds $NormalPollInterval
    continue
  }

  Write-Log 'OUTAGE' 'WAN connectivity lost - entering backoff retry mode'
  $outageStart = Get-Date
  $delay = $InitialDelay
  $attempt = 1

  while ($true) {
    Invoke-Recover -Attempt $attempt
    Start-Sleep -Seconds $delay

    if (Test-Connectivity) {
      $elapsed = (Get-Date) - $outageStart
      Write-Log 'RECOVER' ('Connectivity restored after {0:N1} min (attempts={1})' -f $elapsed.TotalMinutes, $attempt)
      break
    }

    $attempt++
    $nextDelay = [Math]::Min([int]($delay * 2), $MaxDelay)
    Write-Log 'RETRY' "attempt=$attempt next_delay=${nextDelay}s"
    $delay = $nextDelay
  }
}
