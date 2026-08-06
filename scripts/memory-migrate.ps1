<#
.SYNOPSIS
    匯出/匯入某個專案的 Claude Code memory（~/.claude/projects/<slug>/memory/）。

    memory 不在 git repo 裡（本機累積，install.ps1 故意不碰），要換電腦得手動搬。
    這支腳本處理「專案絕對路徑 -> slug 資料夾名」的轉換，並用 zip 打包/還原。

.PARAMETER Mode
    Export（打包成 zip）或 Import（從 zip 還原進對應專案的 memory 資料夾）。

.PARAMETER ProjectPath
    專案的絕對路徑。Export 用來源機的路徑；Import 用目的機的路徑（可以跟來源機不同，
    例如來源機是 E:\github\claude-dotfiles，目的機是 C:\Users\x\claude-dotfiles）。
    預設用目前所在目錄。

.PARAMETER ArchivePath
    zip 檔路徑。Export 是輸出位置，Import 是來源位置。

.EXAMPLE
    # 來源機：把 claude-dotfiles 的 memory 打包
    .\memory-migrate.ps1 -Mode Export -ProjectPath "E:\github\claude-dotfiles" -ArchivePath ".\dotfiles-memory.zip"

.EXAMPLE
    # 目的機：還原進對應專案（路徑可以跟來源機不同）
    .\memory-migrate.ps1 -Mode Import -ProjectPath "C:\Users\x\claude-dotfiles" -ArchivePath ".\dotfiles-memory.zip"
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("Export", "Import")]
    [string]$Mode,

    [string]$ProjectPath = (Get-Location).Path,

    [Parameter(Mandatory = $true)]
    [string]$ArchivePath
)

function ConvertTo-ClaudeProjectSlug {
    param([string]$Path)
    $full = [System.IO.Path]::GetFullPath($Path)
    return ($full -replace '[:\\]', '-')
}

$slug = ConvertTo-ClaudeProjectSlug $ProjectPath
$memDir = Join-Path $env:USERPROFILE ".claude\projects\$slug\memory"

Write-Host "專案路徑: $ProjectPath"
Write-Host "Slug:     $slug"
Write-Host "Memory:   $memDir"
Write-Host ""

if ($Mode -eq "Export") {
    if (-not (Test-Path $memDir)) {
        Write-Host "[FAIL] 找不到 $memDir，路徑或這台機器上該專案是否跑過 session？" -ForegroundColor Red
        exit 1
    }
    Compress-Archive -Path "$memDir\*" -DestinationPath $ArchivePath -Force
    $count = (Get-ChildItem $memDir -File).Count
    Write-Host "[OK] 已打包 $count 個檔案 -> $ArchivePath" -ForegroundColor Green
    Write-Host "把這個 zip 帶到目的機，跑 -Mode Import。"
}
else {
    if (-not (Test-Path $ArchivePath)) {
        Write-Host "[FAIL] 找不到 zip: $ArchivePath" -ForegroundColor Red
        exit 1
    }
    if (-not (Test-Path $memDir)) {
        New-Item -ItemType Directory -Path $memDir -Force | Out-Null
    }

    $tempDir = Join-Path $env:TEMP "memory-migrate-$(Get-Random)"
    Expand-Archive -Path $ArchivePath -DestinationPath $tempDir -Force

    $mergedNote = @()
    Get-ChildItem $tempDir -File | ForEach-Object {
        $dest = Join-Path $memDir $_.Name
        if (Test-Path $dest) {
            $bak = "$dest.bak"
            Copy-Item -Path $dest -Destination $bak -Force
            if ($_.Name -eq "MEMORY.md") {
                $mergedNote += "  - MEMORY.md 舊版已備份成 MEMORY.md.bak，這台機器原本的索引行可能被覆蓋，記得手動比對合併"
            }
        }
        Copy-Item -Path $_.FullName -Destination $dest -Force
    }
    Remove-Item $tempDir -Recurse -Force

    $count = (Get-ChildItem $memDir -File).Count
    Write-Host "[OK] 已還原進 $memDir（共 $count 個檔案）" -ForegroundColor Green
    if ($mergedNote.Count -gt 0) {
        Write-Host ""
        Write-Host "注意：" -ForegroundColor Yellow
        $mergedNote | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
    }
}
