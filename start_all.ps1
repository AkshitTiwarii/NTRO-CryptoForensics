#!/usr/bin/env pwsh
# Start all services for autonomous scraping

Write-Host @"

========================================
  NTRO CryptoForensics - Full Start
========================================

Starting all services:
1. MongoDB
2. Redis
3. Backend Server
4. Celery Worker
5. Celery Beat (Scheduler)
6. Frontend

"@ -ForegroundColor Cyan

$projectRoot = "C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData"

# Check if Redis is running
Write-Host "[1/6] Checking Redis..." -ForegroundColor Yellow
try {
    $redisRunning = Get-Process -Name "redis-server" -ErrorAction SilentlyContinue
    if (-not $redisRunning) {
        Write-Host "Starting Redis..." -ForegroundColor Yellow
        Start-Process -FilePath "redis-server" -WindowStyle Hidden
        Start-Sleep -Seconds 2
    }
    Write-Host "✅ Redis is running" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Redis not installed. Run setup_redis.ps1 first!" -ForegroundColor Red
    exit 1
}

# Check MongoDB
Write-Host "`n[2/6] Checking MongoDB..." -ForegroundColor Yellow
$mongoRunning = Get-Process -Name "mongod" -ErrorAction SilentlyContinue
if ($mongoRunning) {
    Write-Host "✅ MongoDB is running" -ForegroundColor Green
} else {
    Write-Host "⚠️ MongoDB not running. Please start MongoDB first!" -ForegroundColor Red
    exit 1
}

# Start Backend Server
Write-Host "`n[3/6] Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\backend'; python server.py"
Start-Sleep -Seconds 3
Write-Host "✅ Backend started on http://localhost:8000" -ForegroundColor Green

# Start Celery Worker
Write-Host "`n[4/6] Starting Celery Worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\backend'; celery -A celery_app worker --loglevel=info --pool=solo"
Start-Sleep -Seconds 3
Write-Host "✅ Celery Worker started" -ForegroundColor Green

# Start Celery Beat (Scheduler)
Write-Host "`n[5/6] Starting Celery Beat (Autonomous Scraper)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\backend'; celery -A celery_app beat --loglevel=info"
Start-Sleep -Seconds 2
Write-Host "✅ Celery Beat started - Autonomous scraping enabled!" -ForegroundColor Green

# Start Frontend
Write-Host "`n[6/6] Starting Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\frontend'; npm start"
Start-Sleep -Seconds 3
Write-Host "✅ Frontend started on http://localhost:3000" -ForegroundColor Green

Write-Host @"

========================================
       All Services Started! 🚀
========================================

✅ Backend:  http://localhost:8000
✅ Frontend: http://localhost:3000
✅ Redis:    localhost:6379
✅ MongoDB:  localhost:27017
✅ Celery:   Worker & Beat running

AUTONOMOUS SCRAPING SCHEDULE:
=============================
⏰ Hourly:       Scrape all enabled seeds
⏰ Every 30 min: Enrich pending addresses
⏰ Every 15 min: Check watchlist alerts
⏰ Daily 2 AM:   Cleanup old jobs

Your system will now scrape automatically!
Enable seeds in the UI and they'll scrape every hour.

Press any key to exit...
"@ -ForegroundColor Green

$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
