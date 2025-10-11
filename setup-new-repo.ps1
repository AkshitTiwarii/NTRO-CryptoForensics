# ============================================
# NTRO CryptoForensics - New Repository Setup
# ============================================

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  NTRO CryptoForensics" -ForegroundColor Cyan
Write-Host "  New Repository Setup" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if we're in the right directory
Write-Host "Step 1: Checking directory..." -ForegroundColor Yellow
$currentDir = Get-Location
Write-Host "Current directory: $currentDir" -ForegroundColor Gray

# Step 2: Remove existing Git repository
Write-Host "`nStep 2: Removing existing Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Remove-Item -Path ".git" -Recurse -Force
    Write-Host "✓ Existing .git folder removed" -ForegroundColor Green
} else {
    Write-Host "✓ No existing .git folder found" -ForegroundColor Green
}

# Step 3: Remove AI assistant files
Write-Host "`nStep 3: Cleaning up AI assistant files..." -ForegroundColor Yellow

$aiPatterns = @(
    "vscode-chat-code-block*",
    ".aider*",
    ".cursor",
    "claude-*",
    "*-chat-*",
    ".vscode-chat"
)

$cleaned = 0
foreach ($pattern in $aiPatterns) {
    $files = Get-ChildItem -Path . -Filter $pattern -Recurse -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        Remove-Item -Path $file.FullName -Recurse -Force -ErrorAction SilentlyContinue
        $cleaned++
    }
}

Write-Host "✓ Cleaned $cleaned AI assistant files" -ForegroundColor Green

# Step 4: Remove test/temporary files
Write-Host "`nStep 4: Removing test and temporary files..." -ForegroundColor Yellow

$testFiles = @(
    "test_result.md",
    "scraper_test.py",
    "backend_test.py",
    "check_status.ps1",
    "quick_start.ps1"
)

$removed = 0
foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Remove-Item -Path $file -Force
        Write-Host "  Removed: $file" -ForegroundColor Gray
        $removed++
    }
}

Write-Host "✓ Removed $removed test files" -ForegroundColor Green

# Step 5: Initialize new Git repository
Write-Host "`nStep 5: Initializing new Git repository..." -ForegroundColor Yellow
git init
Write-Host "✓ Git repository initialized" -ForegroundColor Green

# Step 6: Configure Git (user should update these)
Write-Host "`nStep 6: Git configuration..." -ForegroundColor Yellow
Write-Host "  Current Git user:" -ForegroundColor Gray
git config user.name
git config user.email
Write-Host ""
Write-Host "  To update, run:" -ForegroundColor Cyan
Write-Host "  git config user.name 'Your Name'" -ForegroundColor Gray
Write-Host "  git config user.email 'your.email@example.com'" -ForegroundColor Gray

# Step 7: Show files to be committed
Write-Host "`nStep 7: Files to be committed..." -ForegroundColor Yellow
git add -n .
Write-Host ""

# Step 8: Stage all files
Write-Host "Step 8: Staging files..." -ForegroundColor Yellow
git add .
Write-Host "✓ All files staged" -ForegroundColor Green

# Step 9: Show status
Write-Host "`nStep 9: Repository status..." -ForegroundColor Yellow
git status --short
Write-Host ""

# Step 10: Create initial commit
Write-Host "Step 10: Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: NTRO CryptoForensics System

Features:
- Mobile-responsive React frontend with Tailwind CSS
- FastAPI Python backend with MongoDB
- Real-time cryptocurrency address scraping
- Dark web scraping with Tor support
- Advanced analytics and visualization
- Role-based access control (Admin/Analyst/Viewer)
- Vercel deployment ready
- Complete documentation

Mobile optimizations:
- Hamburger menu for mobile navigation
- Responsive grids and layouts
- Touch-friendly buttons (44x44px minimum)
- PWA-ready with mobile meta tags
- Safe area insets for notched devices"

Write-Host "✓ Initial commit created" -ForegroundColor Green

# Step 11: Show commit log
Write-Host "`nStep 11: Commit details..." -ForegroundColor Yellow
git log --oneline -1
Write-Host ""

# Step 12: Instructions for creating new GitHub repo
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor Yellow
Write-Host "   - Go to https://github.com/new" -ForegroundColor Gray
Write-Host "   - Repository name: CryptoForensics (or your choice)" -ForegroundColor Gray
Write-Host "   - Description: NTRO Cryptocurrency Forensics System" -ForegroundColor Gray
Write-Host "   - Make it Private (recommended for security)" -ForegroundColor Gray
Write-Host "   - DO NOT initialize with README, .gitignore, or license" -ForegroundColor Red
Write-Host ""

Write-Host "2. Add the remote and push:" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""

Write-Host "3. Verify on GitHub:" -ForegroundColor Yellow
Write-Host "   - Check that all files are uploaded" -ForegroundColor Gray
Write-Host "   - Ensure no AI assistant files are present" -ForegroundColor Gray
Write-Host "   - Verify .env files are NOT uploaded" -ForegroundColor Gray
Write-Host ""

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Repository Statistics" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Count files
$totalFiles = (git ls-files | Measure-Object).Count
$pythonFiles = (git ls-files "*.py" | Measure-Object).Count
$jsFiles = (git ls-files "*.js" "*.jsx" | Measure-Object).Count
$mdFiles = (git ls-files "*.md" | Measure-Object).Count

Write-Host "Total files: $totalFiles" -ForegroundColor Green
Write-Host "Python files: $pythonFiles" -ForegroundColor Green
Write-Host "JavaScript/React files: $jsFiles" -ForegroundColor Green
Write-Host "Documentation files: $mdFiles" -ForegroundColor Green
Write-Host ""

Write-Host "✓ Setup complete! Ready to push to GitHub." -ForegroundColor Green
Write-Host ""
