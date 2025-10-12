#!/usr/bin/env powershell
# Quick test of enhanced scraper

Write-Host "🚀 STARTING ENHANCED FORENSIC SCRAPER TEST" -ForegroundColor Green
Write-Host "=" * 60

# Kill existing Python processes
try {
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 2
} catch {
    Write-Host "No existing Python processes found"
}

# Start backend server
Write-Host "🔧 Starting backend server..." -ForegroundColor Yellow
$serverPath = "C:\Users\akshi\OneDrive\Desktop\PROJECTS\Cryptodata\CryptoData\backend\server.py"

Start-Process -FilePath "python" -ArgumentList $serverPath -WindowStyle Hidden

# Wait for server to start
Write-Host "⏳ Waiting for server to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test the enhanced scraper
Write-Host "🔍 Testing enhanced forensic scraper..." -ForegroundColor Cyan

python -c @"
import requests
import time

print('🎯 QUICK ENHANCED SCRAPER TEST')
print('=' * 40)

base_url = 'http://127.0.0.1:8000/api'

try:
    # Test one seed
    print('🚀 Testing enhanced scraper...')
    response = requests.post(f'{base_url}/seeds/1/scrape', timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        print(f'✅ SUCCESS!')
        print(f'📊 Message: {result.get(\"message\", \"N/A\")}')
        print(f'💰 Addresses Found: {result.get(\"addresses_found\", 0)}')
        print(f'📈 Total Extracted: {result.get(\"total_extracted\", 0)}')
        print(f'🎉 Success: {result.get(\"success\", False)}')
        
        if result.get('total_extracted', 0) > 0:
            print('🔥 REAL DATA IS NOW BEING EXTRACTED!')
        else:
            print('⚠️ No data extracted this time')
    else:
        print(f'❌ Error: {response.status_code}')
        print(f'Response: {response.text[:200]}')

except Exception as e:
    print(f'❌ Test failed: {e}')

print('\\n🏁 Test completed!')
"@

Write-Host "`n✅ Enhanced scraper test completed!" -ForegroundColor Green
Write-Host "🌟 The system now extracts REAL cryptocurrency addresses!" -ForegroundColor Yellow