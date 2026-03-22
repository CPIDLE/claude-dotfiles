# Claude Code Dotfiles Installer (Windows)
# Usage: powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"
$ClaudeDir = "$env:USERPROFILE\.claude"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Claude Code Dotfiles Installer ===" -ForegroundColor Cyan
Write-Host ""

# Ensure ~/.claude/ exists
if (-not (Test-Path $ClaudeDir)) {
    New-Item -ItemType Directory -Path $ClaudeDir | Out-Null
    Write-Host "[OK] Created $ClaudeDir" -ForegroundColor Green
}

function Backup-And-Copy {
    param([string]$Source, [string]$Dest)
    if (Test-Path $Dest) {
        $backup = "$Dest.bak"
        Copy-Item -Path $Dest -Destination $backup -Force
        Write-Host "  [BAK] $Dest -> $backup" -ForegroundColor Yellow
    }
    Copy-Item -Path $Source -Destination $Dest -Force
    Write-Host "  [OK]  $Dest" -ForegroundColor Green
}

# 1. CLAUDE.md
Write-Host ""
Write-Host "--- CLAUDE.md ---"
Backup-And-Copy "$ScriptDir\CLAUDE.md" "$ClaudeDir\CLAUDE.md"

# 2. settings.json
Write-Host ""
Write-Host "--- settings.json ---"
Backup-And-Copy "$ScriptDir\settings.json" "$ClaudeDir\settings.json"

# 3. Status Line
Write-Host ""
Write-Host "--- Status Line ---"
Backup-And-Copy "$ScriptDir\statusline.sh" "$ClaudeDir\statusline.sh"
Backup-And-Copy "$ScriptDir\statusline.js" "$ClaudeDir\statusline.js"
Backup-And-Copy "$ScriptDir\pm-update.sh" "$ClaudeDir\pm-update.sh"

# 4. Commands
Write-Host ""
Write-Host "--- Commands ---"
if (-not (Test-Path "$ClaudeDir\commands")) {
    New-Item -ItemType Directory -Path "$ClaudeDir\commands" | Out-Null
}
Get-ChildItem "$ScriptDir\commands\*.md" | ForEach-Object {
    Backup-And-Copy $_.FullName "$ClaudeDir\commands\$($_.Name)"
}

# Summary
Write-Host ""
Write-Host "=== Done! ===" -ForegroundColor Cyan
