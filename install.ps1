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

# 3. Commands
Write-Host ""
Write-Host "--- Commands ---"
if (-not (Test-Path "$ClaudeDir\commands")) {
    New-Item -ItemType Directory -Path "$ClaudeDir\commands" | Out-Null
}
Get-ChildItem "$ScriptDir\commands\*.md" | ForEach-Object {
    Backup-And-Copy $_.FullName "$ClaudeDir\commands\$($_.Name)"
}

# 4. Skills
Write-Host ""
Write-Host "--- Skills ---"
if (-not (Test-Path "$ClaudeDir\skills")) {
    New-Item -ItemType Directory -Path "$ClaudeDir\skills" | Out-Null
}

# Copy skill files at root level (e.g., gyro-kb.md)
Get-ChildItem "$ScriptDir\skills\*.md" -ErrorAction SilentlyContinue | ForEach-Object {
    Backup-And-Copy $_.FullName "$ClaudeDir\skills\$($_.Name)"
}

# Copy skill directories
Get-ChildItem "$ScriptDir\skills" -Directory | ForEach-Object {
    $skillName = $_.Name
    $destSkill = "$ClaudeDir\skills\$skillName"
    if (Test-Path $destSkill) {
        $backup = "$destSkill.bak"
        if (Test-Path $backup) { Remove-Item -Recurse -Force $backup }
        Rename-Item $destSkill $backup
        Write-Host "  [BAK] $destSkill -> $backup" -ForegroundColor Yellow
    }
    Copy-Item -Recurse -Path $_.FullName -Destination $destSkill
    Write-Host "  [OK]  $destSkill" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "=== Done! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Copy gmail OAuth files manually:" -ForegroundColor White
Write-Host "     token.json + client_secret.json -> $ClaudeDir\skills\gmail\assets\" -ForegroundColor Gray
Write-Host "  2. Reinstall marketplace plugins: claude plugins install" -ForegroundColor White
Write-Host "  3. Reconnect MCP connectors (Gmail, GCal, Slack) - requires OAuth" -ForegroundColor White
Write-Host "  4. Check gyro-kb skill paths match your new machine" -ForegroundColor White
