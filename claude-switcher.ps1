# ============================================================
#  Claude Code 環境切換器
#  Cloud 模式：claude.ai Max 訂閱（OAuth 登入）
#  Local 模式：本地 Ollama（完全離線）
# ============================================================

$OLLAMA_MODEL       = "qwen2.5-coder:14b-instruct-q4_K_M"
$OLLAMA_URL         = "http://localhost:11434"
$CLAUDE_CLOUD_MODEL = "claude-sonnet-4-5"

function claude-cloud {
    Write-Host ""
    Write-Host "  Switching to Cloud mode..." -ForegroundColor Cyan

    # 清除 Ollama 環境變數
    Remove-Item Env:ANTHROPIC_BASE_URL    -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_AUTH_TOKEN  -ErrorAction SilentlyContinue
    Remove-Item Env:ANTHROPIC_API_KEY     -ErrorAction SilentlyContinue
    Remove-Item Env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC -ErrorAction SilentlyContinue

    # 登出 Local session，重新 OAuth 登入
    claude auth logout
    claude auth login

    Write-Host ""
    Write-Host "  Cloud Mode (Max / OAuth)" -ForegroundColor Cyan
    Write-Host "  Model : $CLAUDE_CLOUD_MODEL" -ForegroundColor White
    Write-Host ""
    claude --model $CLAUDE_CLOUD_MODEL
}

function claude-local {
    Write-Host ""
    Write-Host "  Switching to Local mode..." -ForegroundColor Yellow

    # 登出 OAuth session
    claude auth logout

    # 設定 Ollama 環境變數
    Remove-Item Env:ANTHROPIC_API_KEY -ErrorAction SilentlyContinue
    $env:ANTHROPIC_BASE_URL                       = $OLLAMA_URL
    $env:ANTHROPIC_AUTH_TOKEN                     = "ollama"
    $env:CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC = "1"

    # 確認 Ollama 是否在跑
    $ollamaOk = $false
    try {
        $null = Invoke-RestMethod -Uri "$OLLAMA_URL/api/tags" -TimeoutSec 2 -ErrorAction Stop
        $ollamaOk = $true
    } catch {
        $ollamaOk = $false
    }

    if ($ollamaOk) {
        Write-Host "  Local Mode  - Ollama running" -ForegroundColor Yellow
        Write-Host "  Model : $OLLAMA_MODEL" -ForegroundColor White
        Write-Host ""
        claude --model $OLLAMA_MODEL
    } else {
        Write-Host "  Local Mode  - Ollama not running" -ForegroundColor Red
        Write-Host "  Please run: ollama serve" -ForegroundColor DarkGray
        Write-Host ""
    }
}

function claude-status {
    Write-Host ""
    if ($env:ANTHROPIC_BASE_URL -like "*11434*") {
        Write-Host "  Mode  : LOCAL (Ollama)" -ForegroundColor Yellow
        Write-Host "  Model : $OLLAMA_MODEL" -ForegroundColor White
    } else {
        Write-Host "  Mode  : CLOUD (Max / OAuth)" -ForegroundColor Cyan
        Write-Host "  Model : $CLAUDE_CLOUD_MODEL" -ForegroundColor White
    }
    Write-Host ""
}

Write-Host ""
Write-Host "  Claude Switcher loaded" -ForegroundColor DarkGreen
Write-Host "  claude-cloud   -> Cloud (Max)  [logout + re-login]" -ForegroundColor DarkGray
Write-Host "  claude-local   -> Local (Ollama offline)  [logout]" -ForegroundColor DarkGray
Write-Host "  claude-status  -> Show current mode" -ForegroundColor DarkGray
Write-Host ""
