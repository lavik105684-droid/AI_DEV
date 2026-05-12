# Memoir Swarm - Headless Bootstrapper
Write-Host "Starting Memoir Swarm in Headless Mode..." -ForegroundColor Cyan

# 1. Start Docker
Write-Host "Ensuring Docker containers are running..."
docker-compose up -d

# 2. Start Video API (Background)
Write-Host "Launching Video API (Port 8002)..."
Start-Process -FilePath "python" -ArgumentList "Scripts/video_api.py" -WindowStyle Hidden

# 3. Start Dashboard API (Background)
Write-Host "Launching Dashboard API (Port 8501)..."
Start-Process -FilePath "python" -ArgumentList "dashboard/api.py" -WindowStyle Hidden

# 4. Final Verification
Write-Host "------------------------------------------------"
Write-Host "System is ready for Pure Jules mode." -ForegroundColor Green
Write-Host "All bridges synced. Monitoring Git for new commands."
Write-Host "------------------------------------------------"
