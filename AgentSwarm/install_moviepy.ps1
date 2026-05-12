Write-Host "=============================================="
Write-Host "   Installing MoviePy & Dependencies          "
Write-Host "=============================================="
Write-Host ""

# Если мы внутри venv AgentSwarm/dashboard, установим туда, иначе системно
if ($env:VIRTUAL_ENV) {
    Write-Host "Active Virtual Environment detected: $($env:VIRTUAL_ENV)" -ForegroundColor Cyan
} else {
    Write-Host "No Virtual Environment detected. Installing globally..." -ForegroundColor Yellow
}

pip install moviepy

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "  OK: MoviePy installed successfully." -ForegroundColor Green
    Write-Host "  Note: For advanced video editing, you might need to install ImageMagick and add it to PATH." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "  ERROR: Failed to install MoviePy." -ForegroundColor Red
}
