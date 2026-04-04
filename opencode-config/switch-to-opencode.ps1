# switch-to-opencode.ps1
# 從 Claude Code 切換到 OpenCode 的快捷腳本
# 用法：. ~/.config/opencode/switch-to-opencode.ps1 [專案路徑]

param(
    [string]$ProjectPath = (Get-Location).Path
)

Write-Host "`n=== Switch to OpenCode ===" -ForegroundColor Cyan

# 1. 檢查 Docker Ollama
$ollamaRunning = docker ps --filter "name=ollama" --format "{{.Names}}" 2>$null
if ($ollamaRunning -eq "ollama") {
    Write-Host "[OK] Ollama Docker 運行中" -ForegroundColor Green
} else {
    Write-Host "[..] 啟動 Ollama Docker..." -ForegroundColor Yellow
    docker start ollama 2>$null
    if ($LASTEXITCODE -ne 0) {
        docker run -d --gpus all -v ollama-data:/root/.ollama -p 11434:11434 --name ollama --restart unless-stopped ollama/ollama 2>$null
    }
    Start-Sleep 3
    Write-Host "[OK] Ollama Docker 已啟動" -ForegroundColor Green
}

# 2. 顯示 Claude Code 最後狀態
$pmLast = "$env:USERPROFILE\.claude\pm-last.txt"
if (Test-Path $pmLast) {
    $state = Get-Content $pmLast -Raw
    Write-Host "`n[Claude Code 狀態] $state" -ForegroundColor DarkGray
}

# 3. 設定 Gemini API Key（如果 .env 存在）
$envFile = Join-Path $ProjectPath ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^GOOGLE_GENERATIVE_AI_API_KEY=(.+)$") {
            $env:GOOGLE_GENERATIVE_AI_API_KEY = $Matches[1]
        }
    }
}

# 4. 啟動 OpenCode
Write-Host "`n啟動 OpenCode..." -ForegroundColor Cyan
Write-Host "提示：/sync-from-claude 可查看 Claude Code 進度`n" -ForegroundColor DarkGray
Set-Location $ProjectPath
opencode
