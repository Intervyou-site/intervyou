#!/usr/bin/env pwsh
# Deploy Static Files Fix to Railway

Write-Host "🔧 Deploying Static Files Fix to Railway..." -ForegroundColor Cyan
Write-Host ""

# Check if git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if there are changes to commit
Write-Host "📝 Checking for changes..." -ForegroundColor Yellow
$status = git status --porcelain

if (-not $status) {
    Write-Host "✅ No changes to commit" -ForegroundColor Green
    Write-Host "The .dockerignore fix is already committed." -ForegroundColor Green
    Write-Host ""
    Write-Host "To redeploy on Railway:" -ForegroundColor Cyan
    Write-Host "1. Go to https://railway.app" -ForegroundColor White
    Write-Host "2. Select your IntervYou project" -ForegroundColor White
    Write-Host "3. Click 'Deployments' → 'Redeploy'" -ForegroundColor White
    exit 0
}

# Show what will be committed
Write-Host "📋 Changes to commit:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Confirm with user
$confirm = Read-Host "Do you want to commit and push these changes? (y/n)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "❌ Deployment cancelled" -ForegroundColor Red
    exit 0
}

# Stage the .dockerignore file
Write-Host "📦 Staging .dockerignore..." -ForegroundColor Yellow
git add .dockerignore

# Also stage the documentation if it exists
if (Test-Path "STATIC_FILES_FIX.md") {
    git add STATIC_FILES_FIX.md
}

# Commit the changes
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
git commit -m "Fix: Include static files (CSS/JS/images) in Docker build

- Updated .dockerignore to exclude only large media files
- Ensured CSS, JS, images, and icons are included in build
- Fixes broken UI where no styles were loading
- Critical fix for Railway deployment"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Commit failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Changes committed successfully" -ForegroundColor Green
Write-Host ""

# Push to remote
Write-Host "🚀 Pushing to remote repository..." -ForegroundColor Yellow
$branch = git branch --show-current
Write-Host "Current branch: $branch" -ForegroundColor Cyan

git push origin $branch

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Push failed" -ForegroundColor Red
    Write-Host "You may need to pull changes first or check your remote configuration" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "✅ Successfully pushed to remote!" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 Deployment initiated!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Railway will automatically detect the push and start building" -ForegroundColor White
Write-Host "2. Wait 2-3 minutes for the build to complete" -ForegroundColor White
Write-Host "3. Check Railway dashboard: https://railway.app" -ForegroundColor White
Write-Host "4. Once deployed, clear your browser cache (Ctrl+Shift+Delete)" -ForegroundColor White
Write-Host "5. Visit: https://intervyou.up.railway.app" -ForegroundColor White
Write-Host ""
Write-Host "To monitor deployment:" -ForegroundColor Cyan
Write-Host "  railway logs --follow" -ForegroundColor White
Write-Host ""
Write-Host "To check deployment status:" -ForegroundColor Cyan
Write-Host "  railway status" -ForegroundColor White
Write-Host ""
