# Automated Tor Setup for NTRO CryptoForensics
# This script configures Tor Browser for dark web scraping

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NTRO Tor Browser Setup Automation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install PySocks for Python proxy support
Write-Host "[1/5] Installing PySocks package..." -ForegroundColor Yellow
try {
    pip install pysocks
    Write-Host "✅ PySocks installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ PySocks installation failed. Run manually: pip install pysocks" -ForegroundColor Red
}
Write-Host ""

# Step 2: Find Tor Browser installation
Write-Host "[2/5] Locating Tor Browser..." -ForegroundColor Yellow

$torLocations = @(
    "$env:USERPROFILE\Desktop\Tor Browser",
    "$env:LOCALAPPDATA\Tor Browser",
    "C:\Program Files\Tor Browser",
    "$env:ProgramFiles\Tor Browser",
    "$env:USERPROFILE\Downloads\Tor Browser"
)

$torPath = $null
foreach ($location in $torLocations) {
    if (Test-Path $location) {
        $torPath = $location
        Write-Host "✅ Found Tor Browser at: $torPath" -ForegroundColor Green
        break
    }
}

if (-not $torPath) {
    Write-Host "❌ Tor Browser not found in common locations." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please specify the Tor Browser folder path:" -ForegroundColor Yellow
    $torPath = Read-Host "Enter path (e.g., C:\Tor Browser)"
    
    if (-not (Test-Path $torPath)) {
        Write-Host "❌ Invalid path. Exiting..." -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Step 3: Find Tor executable
Write-Host "[3/5] Locating Tor executable..." -ForegroundColor Yellow

$torExe = Get-ChildItem -Path $torPath -Filter "tor.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($torExe) {
    Write-Host "✅ Found tor.exe at: $($torExe.FullName)" -ForegroundColor Green
    $torExePath = $torExe.DirectoryName
} else {
    Write-Host "⚠️ tor.exe not found. Looking for firefox.exe (Tor Browser Bundle)..." -ForegroundColor Yellow
    $firefoxExe = Get-ChildItem -Path $torPath -Filter "firefox.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    
    if ($firefoxExe) {
        Write-Host "✅ Found Tor Browser Bundle" -ForegroundColor Green
        $torExePath = Join-Path (Split-Path $firefoxExe.DirectoryName -Parent) "Tor"
        
        if (-not (Test-Path $torExePath)) {
            $torExePath = Join-Path $torPath "Browser\TorBrowser\Tor"
        }
    } else {
        Write-Host "❌ Could not find Tor executable. Please start Tor Browser manually." -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Step 4: Start Tor Browser to initialize proxy
Write-Host "[4/5] Starting Tor Browser..." -ForegroundColor Yellow
Write-Host "⚠️ Important: Keep Tor Browser OPEN while scraping dark web!" -ForegroundColor Yellow
Write-Host ""

# Find Tor Browser executable
$torBrowserExe = Get-ChildItem -Path $torPath -Filter "firefox.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($torBrowserExe) {
    Write-Host "Starting Tor Browser..." -ForegroundColor Cyan
    Start-Process -FilePath $torBrowserExe.FullName -WindowStyle Normal
    Write-Host "✅ Tor Browser started!" -ForegroundColor Green
    Write-Host "⏳ Waiting 15 seconds for Tor to bootstrap..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
} else {
    Write-Host "⚠️ Could not auto-start Tor Browser." -ForegroundColor Yellow
    Write-Host "Please start it manually from: $torPath" -ForegroundColor Yellow
    Write-Host "Press any key after Tor Browser is running..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
Write-Host ""

# Step 5: Test Tor connection
Write-Host "[5/5] Testing Tor proxy connection..." -ForegroundColor Yellow

# Tor Browser uses port 9150 (not 9050)
$torPort = 9150

Write-Host "Testing SOCKS5 proxy on localhost:$torPort..." -ForegroundColor Cyan

try {
    # Test using Python
    $testScript = @"
import requests
try:
    proxies = {
        'http': 'socks5h://127.0.0.1:$torPort',
        'https': 'socks5h://127.0.0.1:$torPort'
    }
    response = requests.get('https://check.torproject.org', proxies=proxies, timeout=30)
    if 'Congratulations' in response.text:
        print('SUCCESS: Connected to Tor network!')
        exit(0)
    else:
        print('ERROR: Not using Tor network')
        exit(1)
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)
"@
    
    $testScript | python
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Tor proxy is working!" -ForegroundColor Green
        $torWorking = $true
    } else {
        Write-Host "⚠️ Tor proxy test failed" -ForegroundColor Yellow
        $torWorking = $false
    }
} catch {
    Write-Host "⚠️ Could not test Tor connection" -ForegroundColor Yellow
    $torWorking = $false
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "          Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($torWorking) {
    Write-Host "✅ Tor Browser: Running" -ForegroundColor Green
    Write-Host "✅ SOCKS5 Proxy: localhost:$torPort" -ForegroundColor Green
    Write-Host "✅ PySocks: Installed" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎯 You can now enable dark web scraping!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Keep Tor Browser OPEN" -ForegroundColor White
    Write-Host "2. Open http://localhost:3000" -ForegroundColor White
    Write-Host "3. Go to Scraping → Seed Manager" -ForegroundColor White
    Write-Host "4. Enable seeds with 🧅 icon" -ForegroundColor White
    Write-Host "5. Click Play to scrape dark web!" -ForegroundColor White
} else {
    Write-Host "⚠️ Tor connection could not be verified" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual steps:" -ForegroundColor Yellow
    Write-Host "1. Make sure Tor Browser is running" -ForegroundColor White
    Write-Host "2. Check that Tor has bootstrapped (100%)" -ForegroundColor White
    Write-Host "3. The proxy should be on: localhost:$torPort" -ForegroundColor White
    Write-Host "4. Try scraping again after Tor is fully connected" -ForegroundColor White
}

Write-Host ""
Write-Host "Tor Browser location: $torPath" -ForegroundColor Cyan
Write-Host "Proxy port: $torPort" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
