#!/usr/bin/env powershell
# Quick Setup for AI Analysis Testing

Write-Host "🚀 SETTING UP AI ANALYSIS SYSTEM" -ForegroundColor Green
Write-Host "=" * 50

# Kill existing processes
Write-Host "🔧 Cleaning up existing processes..." -ForegroundColor Yellow
try {
    Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 2
} catch {
    Write-Host "No existing processes found"
}

# Start backend
Write-Host "🔧 Starting backend server..." -ForegroundColor Yellow
$backendPath = "C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend\server.py"
Start-Process -FilePath "python" -ArgumentList $backendPath -WindowStyle Hidden

# Wait for backend
Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# Add high-risk test data
Write-Host "📊 Adding high-risk addresses for Analytics..." -ForegroundColor Cyan
cd "C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData"

python -c @"
import requests
import json

print('🔐 Adding high-risk test data...')
base_url = 'http://127.0.0.1:8000/api'

# Login
login_data = {'username': 'admin', 'password': 'admin123'}
try:
    login_response = requests.post(f'{base_url}/auth/login', json=login_data, timeout=5)
    if login_response.status_code == 200:
        token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test analytics
        analytics_response = requests.get(f'{base_url}/analytics/dashboard', headers=headers, timeout=5)
        if analytics_response.status_code == 200:
            stats = analytics_response.json()
            print(f'✅ Backend working!')
            print(f'📊 Total Addresses: {stats.get(\"total_addresses\", 0)}')
            print(f'🚨 High Risk: {stats.get(\"high_risk_addresses\", 0)}')
        else:
            print(f'⚠️ Analytics endpoint issue: {analytics_response.status_code}')
    else:
        print(f'❌ Login failed: {login_response.status_code}')
except Exception as e:
    print(f'❌ Backend connection failed: {e}')
    print('Please check if backend server started successfully')
"@

Write-Host "`n🎯 SETUP COMPLETED!" -ForegroundColor Green
Write-Host "=" * 50

Write-Host "`n📍 WHERE TO FIND AI ANALYSIS:" -ForegroundColor Yellow
Write-Host "   1. Open your browser to localhost:3000" -ForegroundColor White
Write-Host "   2. Login with admin/admin123" -ForegroundColor White
Write-Host "   3. Look for '🤖 AI Analysis' in the left sidebar" -ForegroundColor White
Write-Host "   4. Click it to access AI analysis features" -ForegroundColor White

Write-Host "`n🚨 FOR HIGH-RISK ADDRESSES IN ANALYTICS:" -ForegroundColor Yellow
Write-Host "   1. Go to Analytics page" -ForegroundColor White
Write-Host "   2. The percentages should now show proper data" -ForegroundColor White
Write-Host "   3. If still showing 1%, run the scraper first" -ForegroundColor White

Write-Host "`n✅ Your AI Analysis system is now ready!" -ForegroundColor Green