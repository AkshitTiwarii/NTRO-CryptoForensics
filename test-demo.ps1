# Test Demo Mode Locally
# This starts the frontend in demo mode without needing the backend

Write-Host "🎮 Starting NTRO Crypto Forensics in DEMO MODE" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if in correct directory
if (-not (Test-Path "frontend\package.json")) {
    Write-Host "❌ Error: Please run this from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Demo Mode Features:" -ForegroundColor Yellow
Write-Host "  ✓ No backend required" -ForegroundColor Green
Write-Host "  ✓ Sample cryptocurrency data" -ForegroundColor Green
Write-Host "  ✓ Mock AI analysis" -ForegroundColor Green
Write-Host "  ✓ All UI features working" -ForegroundColor Green
Write-Host ""

Write-Host "🔑 Demo Credentials:" -ForegroundColor Cyan
Write-Host "   Username: demo" -ForegroundColor White
Write-Host "   Password: demo123" -ForegroundColor White
Write-Host ""

# Navigate to frontend
Set-Location frontend

# Set demo mode environment variable
$env:REACT_APP_DEMO_MODE = "true"

Write-Host "🚀 Starting development server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Once started, visit: http://localhost:3000" -ForegroundColor Green
Write-Host "Click 'Use Demo Credentials' or enter demo/demo123" -ForegroundColor Yellow
Write-Host ""

# Start the app
npm start

# Return to root when stopped
Set-Location ..
