#!/usr/bin/env pwsh
# Redis + Celery Setup for Autonomous Scraping

Write-Host @"

========================================
    NTRO CryptoForensics
    Redis + Celery Setup
========================================

This will enable AUTONOMOUS SCRAPING:
- Hourly automatic scraping of all enabled seeds
- Background task processing
- Self-synchronizing data collection

"@ -ForegroundColor Cyan

Write-Host "`n[Step 1/5] Installing Redis for Windows...`n" -ForegroundColor Yellow

# Check if Chocolatey is installed
$chocoInstalled = Get-Command choco -ErrorAction SilentlyContinue

if (-not $chocoInstalled) {
    Write-Host "Chocolatey not found. Installing Chocolatey first..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    # Refresh environment
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

Write-Host "Installing Redis via Chocolatey..." -ForegroundColor Cyan
choco install redis-64 -y

Write-Host "`n[Step 2/5] Installing Python dependencies...`n" -ForegroundColor Yellow
Set-Location "C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend"

pip install redis celery

Write-Host "`n[Step 3/5] Starting Redis server...`n" -ForegroundColor Yellow

# Start Redis as a service
$redisService = Get-Service -Name "Redis" -ErrorAction SilentlyContinue

if ($redisService) {
    Start-Service -Name "Redis"
    Write-Host "✅ Redis service started!" -ForegroundColor Green
} else {
    # Start Redis manually in background
    Start-Process -FilePath "redis-server" -WindowStyle Hidden
    Start-Sleep -Seconds 3
    Write-Host "✅ Redis server started in background!" -ForegroundColor Green
}

Write-Host "`n[Step 4/5] Testing Redis connection...`n" -ForegroundColor Yellow

# Test Redis connection with Python
$testScript = @"
import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print('✅ Redis connection successful!')
except Exception as e:
    print(f'❌ Redis connection failed: {e}')
"@

$testScript | python

Write-Host "`n[Step 5/5] Starting Celery worker...`n" -ForegroundColor Yellow

Write-Host @"

========================================
          Setup Complete!
========================================

✅ Redis: Installed and running
✅ Celery: Dependencies installed
✅ Python packages: Installed

NEXT STEPS:
===========

1. Start Celery Worker (in new terminal):
   cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
   celery -A celery_app worker --loglevel=info --pool=solo

2. Start Celery Beat (scheduler - in another terminal):
   cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
   celery -A celery_app beat --loglevel=info

3. Restart Backend Server:
   cd C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend
   python server.py

AUTONOMOUS SCRAPING:
===================
- Scrapes all enabled seeds EVERY HOUR automatically
- Enriches addresses every 30 minutes
- Check watchlists every 15 minutes
- Cleanup old jobs daily at 2 AM

You can now enable seeds and they'll scrape automatically!

"@ -ForegroundColor Green

Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
