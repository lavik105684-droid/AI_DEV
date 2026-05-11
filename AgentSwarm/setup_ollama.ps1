Write-Host "=============================================="
Write-Host "   Agent Swarm Ollama Setup (AMD ROCm ready)  "
Write-Host "=============================================="
Write-Host ""

# 1. Проверка установки Ollama
Write-Host "[1/2] Checking Ollama installation..." -ForegroundColor Cyan
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "  OK: Ollama is installed." -ForegroundColor Green
} else {
    Write-Host "  ERROR: Ollama is NOT installed." -ForegroundColor Red
    Write-Host "  Please install it from https://ollama.com/download/windows"
    Write-Host "  For AMD ROCm support, ensure you are running the appropriate version for your RX 6900 XT."
    exit 1
}

Write-Host ""
# 2. Загрузка моделей
Write-Host "[2/2] Pulling required models (Total VRAM: ~16GB limit)..." -ForegroundColor Cyan

$models = @(
    "qwen2.5-coder:14b", # Dev, Analyst
    "qwen2.5:7b",        # QA
    "llama3.2-vision",   # Design / Vision
    "gemma2:9b"          # SEO / RAG
)

foreach ($model in $models) {
    Write-Host "  -> Pulling $model..." -ForegroundColor Yellow
    ollama pull $model
    if ($LASTEXITCODE -eq 0) {
        Write-Host "     Success: $model" -ForegroundColor Green
    } else {
        Write-Host "     Failed to pull $model" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=============================================="
Write-Host "   Setup Complete! Models are ready to use.   "
Write-Host "=============================================="
