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

# 1. Global CLAUDE.md (global-claude.md -> ~/.claude/CLAUDE.md)
Write-Host ""
Write-Host "--- CLAUDE.md (global) ---"
Backup-And-Copy "$ScriptDir\global-claude.md" "$ClaudeDir\CLAUDE.md"

# 2. settings.json
Write-Host ""
Write-Host "--- settings.json ---"
Backup-And-Copy "$ScriptDir\settings.json" "$ClaudeDir\settings.json"
Backup-And-Copy "$ScriptDir\sfx_mario_1up.wav" "$ClaudeDir\sfx_mario_1up.wav"

# 2.5. settings.local.json (permissions whitelist)
Write-Host ""
Write-Host "--- settings.local.json ---"
if (Test-Path "$ScriptDir\settings.local.json") {
    Backup-And-Copy "$ScriptDir\settings.local.json" "$ClaudeDir\settings.local.json"
}

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

# 5. opencode Commands + Config (if opencode is installed)
Write-Host ""
Write-Host "--- opencode ---"
if (Get-Command opencode -ErrorAction SilentlyContinue) {
    $OpencodeBase = "$env:USERPROFILE\.config\opencode"
    $OpencodeCmdDir = "$OpencodeBase\commands"
    if (-not (Test-Path $OpencodeCmdDir)) {
        New-Item -ItemType Directory -Path $OpencodeCmdDir -Force | Out-Null
    }

    # 5a. Commands
    if (Test-Path "$ScriptDir\commands-opencode") {
        Get-ChildItem "$ScriptDir\commands-opencode\*.md" | ForEach-Object {
            Backup-And-Copy $_.FullName "$OpencodeCmdDir\$($_.Name)"
        }
    }

    # 5b. Config files (opencode.json, tui.json, AGENTS.md)
    if (Test-Path "$ScriptDir\opencode-config") {
        foreach ($f in @("opencode.json", "tui.json", "AGENTS.md")) {
            $src = "$ScriptDir\opencode-config\$f"
            if (Test-Path $src) {
                Backup-And-Copy $src "$OpencodeBase\$f"
            }
        }
        # switch-to-opencode.ps1
        $switchSrc = "$ScriptDir\opencode-config\switch-to-opencode.ps1"
        if (Test-Path $switchSrc) {
            Backup-And-Copy $switchSrc "$OpencodeBase\switch-to-opencode.ps1"
        }
    }
} else {
    Write-Host "  [SKIP] opencode not installed" -ForegroundColor Yellow
}

# 6. MCP Config
Write-Host ""
Write-Host "--- MCP Config ---"
if (Test-Path "$ScriptDir\mcp.json") {
    Backup-And-Copy "$ScriptDir\mcp.json" "$ClaudeDir\.mcp.json"
}

# 7. Claude Switcher
Write-Host ""
Write-Host "--- Claude Switcher ---"
if (Test-Path "$ScriptDir\claude-switcher.ps1") {
    Backup-And-Copy "$ScriptDir\claude-switcher.ps1" "$ClaudeDir\claude-switcher.ps1"
}

# 8. Skills
Write-Host ""
Write-Host "--- Skills ---"
if (Test-Path "$ScriptDir\skills") {
    $skillsDest = "$ClaudeDir\skills"
    if (-not (Test-Path $skillsDest)) {
        New-Item -ItemType Directory -Path $skillsDest | Out-Null
    }
    # Copy skill directories
    Get-ChildItem "$ScriptDir\skills" -Directory | ForEach-Object {
        $destSkill = "$skillsDest\$($_.Name)"
        if (-not (Test-Path $destSkill)) {
            New-Item -ItemType Directory -Path $destSkill | Out-Null
        }
        Copy-Item -Path "$($_.FullName)\*" -Destination $destSkill -Recurse -Force
        Write-Host "  [OK]  ~\.claude\skills\$($_.Name)\" -ForegroundColor Green
    }
    # Copy standalone skill files
    Get-ChildItem "$ScriptDir\skills\*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        Backup-And-Copy $_.FullName "$skillsDest\$($_.Name)"
    }
}

# 8.5. Hooks
Write-Host ""
Write-Host "--- Hooks ---"
if (Test-Path "$ScriptDir\hooks") {
    $hooksDest = "$ClaudeDir\hooks"
    if (-not (Test-Path $hooksDest)) {
        New-Item -ItemType Directory -Path $hooksDest | Out-Null
    }
    Get-ChildItem "$ScriptDir\hooks\*" -File | ForEach-Object {
        Backup-And-Copy $_.FullName "$hooksDest\$($_.Name)"
    }
}

# 9. Docs
Write-Host ""
Write-Host "--- Docs ---"
if (Test-Path "$ScriptDir\docs") {
    $docsDest = "$ClaudeDir\docs"
    if (-not (Test-Path $docsDest)) {
        New-Item -ItemType Directory -Path $docsDest | Out-Null
    }
    Get-ChildItem "$ScriptDir\docs\*.md" | ForEach-Object {
        Backup-And-Copy $_.FullName "$docsDest\$($_.Name)"
    }
}

# 10. .env reminder
Write-Host ""
if (-not (Test-Path "$ClaudeDir\.env")) {
    Write-Host "[INFO] No .env found at $ClaudeDir\.env" -ForegroundColor Yellow
    Write-Host "       Copy .env.example and fill in your secrets:" -ForegroundColor Yellow
    Write-Host "       Copy-Item $ScriptDir\.env.example $ClaudeDir\.env" -ForegroundColor Yellow
}

# 10.5. Notepad++ MarkdownPanel CSS + Sarasa Mono TC fonts (Windows-only, best-effort)
Write-Host ""
Write-Host "--- Notepad++ MarkdownPanel CSS ---"
$NppPluginDir = "C:\Program Files\Notepad++\plugins\NppMarkdownPanel"
if (Test-Path $NppPluginDir) {
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if ($isAdmin) {
        foreach ($f in @("style.css", "style-dark.css")) {
            $src = "$ScriptDir\notepad++-config\$f"
            if (Test-Path $src) {
                Backup-And-Copy $src "$NppPluginDir\$f"
            }
        }
    } else {
        Write-Host "  [SKIP] Need admin. Manual copy:" -ForegroundColor Yellow
        Write-Host "    Copy-Item '$ScriptDir\notepad++-config\*.css' '$NppPluginDir\' -Force" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [SKIP] Notepad++ NppMarkdownPanel not installed" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "--- Sarasa Mono TC fonts ---"
$FontDir = "$env:WINDIR\Fonts"
$FontRegKey = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
$FontFiles = @{
    "SarasaMonoTC-Regular.ttf"    = "Sarasa Mono TC (TrueType)"
    "SarasaMonoTC-Bold.ttf"       = "Sarasa Mono TC Bold (TrueType)"
    "SarasaMonoTC-Italic.ttf"     = "Sarasa Mono TC Italic (TrueType)"
    "SarasaMonoTC-BoldItalic.ttf" = "Sarasa Mono TC Bold Italic (TrueType)"
}
$allPresent = $true
foreach ($f in $FontFiles.Keys) {
    if (-not (Test-Path "$FontDir\$f")) { $allPresent = $false; break }
}
if ($allPresent) {
    Write-Host "  [OK]  All 4 Sarasa Mono TC fonts already installed" -ForegroundColor Green
} else {
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    $SevenZip = "C:\Program Files\7-Zip\7z.exe"
    if (-not $isAdmin) {
        Write-Host "  [SKIP] Need admin to install fonts. Run installer as Administrator." -ForegroundColor Yellow
    } elseif (-not (Test-Path $SevenZip)) {
        Write-Host "  [SKIP] 7-Zip not found at $SevenZip. Install 7-Zip first." -ForegroundColor Yellow
    } else {
        try {
            Write-Host "  Fetching latest Sarasa Gothic release info..." -ForegroundColor Cyan
            $api = Invoke-RestMethod -Uri "https://api.github.com/repos/be5invis/Sarasa-Gothic/releases/latest" -UseBasicParsing
            $asset = $api.assets | Where-Object { $_.name -match '^SarasaMonoTC-TTF-[\d.]+\.7z$' } | Select-Object -First 1
            if (-not $asset) { throw "No SarasaMonoTC-TTF archive in latest release" }
            $tmp = Join-Path $env:TEMP "sarasa-dotfiles"
            New-Item -ItemType Directory -Path $tmp -Force | Out-Null
            $archive = Join-Path $tmp $asset.name
            Write-Host "  Downloading $($asset.name) ($([math]::Round($asset.size/1MB,1)) MB)..." -ForegroundColor Cyan
            Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $archive -UseBasicParsing
            Write-Host "  Extracting..." -ForegroundColor Cyan
            & $SevenZip x $archive "-o$tmp" -y | Out-Null
            foreach ($f in $FontFiles.Keys) {
                $fp = Get-ChildItem -Path $tmp -Filter $f -Recurse -File | Select-Object -First 1
                if ($fp) {
                    Copy-Item $fp.FullName -Destination $FontDir -Force
                    New-ItemProperty -Path $FontRegKey -Name $FontFiles[$f] -Value $f -PropertyType String -Force | Out-Null
                    Write-Host "  [OK]  Installed $f" -ForegroundColor Green
                }
            }
            Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
        } catch {
            Write-Host "  [FAIL] $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# 11. Plugin summary
Write-Host ""
Write-Host "--- Plugins ---"
Write-Host "  Configured in settings.json (auto-install on first launch):"
Write-Host "    skill-creator, code-simplifier, context7, coderabbit,"
Write-Host "    claude-md-management, playwright"
Write-Host "  Optional plugins: see docs/plugins.md"

# Summary
Write-Host ""
Write-Host "=== Done! ===" -ForegroundColor Cyan
