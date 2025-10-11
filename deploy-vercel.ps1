# 🚀 Quick Deployment Script for Vercel

Write-Host "🚀 NTRO CryptoForensics - Vercel Deployment Helper" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check if in correct directory
if (!(Test-Path "frontend\package.json")) {
    Write-Host "❌ Error: Please run this script from the CryptoData root directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Directory check passed" -ForegroundColor Green
Write-Host ""

# Navigate to frontend
Set-Location frontend

Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install --legacy-peer-deps

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Dependency installation failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "🔨 Building production bundle..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build successful" -ForegroundColor Green
Write-Host ""

Write-Host "📊 Build Statistics:" -ForegroundColor Cyan
Get-ChildItem build -Recurse | Measure-Object -Property Length -Sum | ForEach-Object {
    $sizeMB = [math]::Round($_.Sum / 1MB, 2)
    Write-Host "  Total Size: $sizeMB MB" -ForegroundColor White
}

Write-Host ""
Write-Host "✅ Ready for Deployment!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Go to vercel.com and sign in" -ForegroundColor White
Write-Host "  2. Click 'Add New Project'" -ForegroundColor White
Write-Host "  3. Import your GitHub repository" -ForegroundColor White
Write-Host "  4. Set Root Directory: CryptoData/frontend" -ForegroundColor White
Write-Host "  5. Framework: Create React App" -ForegroundColor White
Write-Host "  6. Build Command: npm run build" -ForegroundColor White
Write-Host "  7. Output Directory: build" -ForegroundColor White
Write-Host "  8. Install Command: npm install --legacy-peer-deps" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Environment Variables to add in Vercel:" -ForegroundColor Cyan
Write-Host "  REACT_APP_BACKEND_URL = https://your-backend-url.vercel.app" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Or deploy via Vercel CLI:" -ForegroundColor Cyan
Write-Host "  npm i -g vercel" -ForegroundColor White
Write-Host "  vercel --prod" -ForegroundColor White
Write-Host ""

# Return to root
Set-Location ..

Write-Host "✨ Deployment preparation complete!" -ForegroundColor Green
