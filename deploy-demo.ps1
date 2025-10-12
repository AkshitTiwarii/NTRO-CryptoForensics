# Quick Vercel Deployment Script
# Run this to deploy your demo to Vercel

Write-Host "🚀 NTRO Crypto Forensics - Vercel Deployment" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "frontend\package.json")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Pre-deployment Checklist:" -ForegroundColor Yellow
Write-Host "  ✓ Demo mode enabled in .env.production" -ForegroundColor Green
Write-Host "  ✓ Mock data service created" -ForegroundColor Green
Write-Host "  ✓ API service supports demo mode" -ForegroundColor Green
Write-Host "  ✓ DemoLogin component ready" -ForegroundColor Green
Write-Host ""

# Check if Vercel CLI is installed
Write-Host "🔍 Checking for Vercel CLI..." -ForegroundColor Cyan
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue

if (-not $vercelInstalled) {
    Write-Host "⚠️  Vercel CLI not found. Installing..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Run: npm install -g vercel" -ForegroundColor White
    Write-Host ""
    
    $install = Read-Host "Install Vercel CLI now? (y/n)"
    if ($install -eq "y") {
        npm install -g vercel
    } else {
        Write-Host "❌ Deployment cancelled. Please install Vercel CLI first." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Vercel CLI found!" -ForegroundColor Green
Write-Host ""

# Navigate to frontend
Set-Location frontend

Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
npm install --legacy-peer-deps

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Dependencies installed!" -ForegroundColor Green
Write-Host ""

Write-Host "🏗️  Building project..." -ForegroundColor Cyan
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build successful!" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Deploying to Vercel..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Choose deployment type:" -ForegroundColor Yellow
Write-Host "  1) Production deployment (your-app.vercel.app)" -ForegroundColor White
Write-Host "  2) Preview deployment (preview-xxx.vercel.app)" -ForegroundColor White
Write-Host ""

$deployType = Read-Host "Enter choice (1 or 2)"

if ($deployType -eq "1") {
    Write-Host ""
    Write-Host "🌐 Deploying to PRODUCTION..." -ForegroundColor Green
    vercel --prod
} else {
    Write-Host ""
    Write-Host "🔍 Deploying PREVIEW..." -ForegroundColor Yellow
    vercel
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host "✨ Deployment Successful! ✨" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Demo Credentials:" -ForegroundColor Cyan
    Write-Host "   Username: demo" -ForegroundColor White
    Write-Host "   Password: demo123" -ForegroundColor White
    Write-Host ""
    Write-Host "🎯 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Visit your deployment URL" -ForegroundColor White
    Write-Host "   2. Click 'Use Demo Credentials' or enter: demo/demo123" -ForegroundColor White
    Write-Host "   3. Explore the full demo experience!" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Deployment failed. Please check the errors above." -ForegroundColor Red
    exit 1
}

# Return to root
Set-Location ..
