# Start Autonomous System - PowerShell Script
# This script starts all components of the autonomous cryptocurrency intelligence system

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NTRO Autonomous Crypto System Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "[1/6] Checking Docker..." -ForegroundColor Yellow
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✓ Docker found" -ForegroundColor Green
    
    # Start Redis container
    Write-Host "[2/6] Starting Redis container..." -ForegroundColor Yellow
    docker run -d -p 6379:6379 --name redis-crypto --rm redis:latest
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Redis started on port 6379" -ForegroundColor Green
    } else {
        Write-Host "! Redis container may already be running" -ForegroundColor Yellow
        docker start redis-crypto 2>$null
    }
    
    Start-Sleep -Seconds 3
    
    # Test Redis connection
    docker exec redis-crypto redis-cli ping
    Write-Host ""
} else {
    Write-Host "✗ Docker not found" -ForegroundColor Red
    Write-Host "  Install Docker Desktop or use Redis for Windows" -ForegroundColor Yellow
    Write-Host "  Download: https://github.com/microsoftarchive/redis/releases" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to continue without Redis (some features disabled)..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Start Backend Server
Write-Host "[3/6] Starting FastAPI backend..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "backend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; python server.py"
Write-Host "✓ Backend starting on http://localhost:8000" -ForegroundColor Green
Write-Host ""

Start-Sleep -Seconds 5

# Start Celery Worker
Write-Host "[4/6] Starting Celery worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; celery -A celery_app worker --loglevel=info --pool=solo"
Write-Host "✓ Celery worker starting" -ForegroundColor Green
Write-Host ""

Start-Sleep -Seconds 3

# Start Celery Beat Scheduler
Write-Host "[5/6] Starting Celery beat scheduler..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; celery -A celery_app beat --loglevel=info"
Write-Host "✓ Celery beat starting (autonomous scraping every hour)" -ForegroundColor Green
Write-Host ""

# Start Frontend
Write-Host "[6/6] Starting React frontend..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm start"
Write-Host "✓ Frontend starting on http://localhost:3000" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  System Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Yellow
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Flower:    http://localhost:5555 (optional)" -ForegroundColor Gray
Write-Host ""
Write-Host "Autonomous Features:" -ForegroundColor Yellow
Write-Host "  ✓ Seed Manager - 10 pre-configured sources" -ForegroundColor White
Write-Host "  ✓ Hourly autonomous scraping via Celery Beat" -ForegroundColor White
Write-Host "  ✓ Auto-enrichment with Blockchair API" -ForegroundColor White
Write-Host "  ✓ ML categorization (11 categories)" -ForegroundColor White
Write-Host "  ✓ Risk scoring (0-100)" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Go to Seed Manager to view/manage sources" -ForegroundColor White
Write-Host "  2. Click ▶ to manually trigger a scrape" -ForegroundColor White
Write-Host "  3. Wait for hourly autonomous scraping" -ForegroundColor White
Write-Host "  4. Monitor statistics dashboard" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit (services will keep running)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
