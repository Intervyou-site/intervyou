# Railway Setup Script for IntervYou (PowerShell)
# This script helps you prepare for Railway deployment

Write-Host "🚂 IntervYou - Railway Deployment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "❌ Git repository not initialized" -ForegroundColor Red
    Write-Host "Run: git init"
    exit 1
}

Write-Host "✅ Git repository found" -ForegroundColor Green
Write-Host ""

# Check for required files
Write-Host "📋 Checking required files..." -ForegroundColor Yellow
$files = @("Dockerfile", "requirements-docker.txt", ".env.example", "fastapi_app_cleaned.py")
$missing_files = @()

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (missing)" -ForegroundColor Red
        $missing_files += $file
    }
}

if ($missing_files.Count -gt 0) {
    Write-Host ""
    Write-Host "❌ Missing required files. Please ensure all files exist." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ All required files present" -ForegroundColor Green
Write-Host ""

# Generate SECRET_KEY
Write-Host "🔐 Generating SECRET_KEY..." -ForegroundColor Yellow
try {
    $SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"
} catch {
    # Fallback to random string
    $SECRET_KEY = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
}
Write-Host "Generated SECRET_KEY: $SECRET_KEY" -ForegroundColor Cyan
Write-Host ""

# Check git status
Write-Host "📊 Git Status:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Offer to commit and push
$response = Read-Host "Do you want to commit and push to GitHub? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    git add .
    git commit -m "Prepare for Railway deployment"
    
    # Check if remote exists
    $remotes = git remote
    if ($remotes -contains "origin") {
        try {
            git push origin main
            Write-Host "✅ Pushed to GitHub" -ForegroundColor Green
        } catch {
            try {
                git push origin master
                Write-Host "✅ Pushed to GitHub" -ForegroundColor Green
            } catch {
                Write-Host "❌ Push failed. Check your remote configuration." -ForegroundColor Red
            }
        }
    } else {
        Write-Host "❌ No remote 'origin' found. Add your GitHub repository:" -ForegroundColor Red
        Write-Host "   git remote add origin https://github.com/yourusername/your-repo.git"
        Write-Host "   git push -u origin main"
    }
}

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://railway.app"
Write-Host "2. Sign up with GitHub"
Write-Host "3. Click 'New Project' → 'Deploy from GitHub repo'"
Write-Host "4. Select your repository"
Write-Host "5. Add PostgreSQL database"
Write-Host "6. Add environment variables:"
Write-Host "   - SECRET_KEY=$SECRET_KEY" -ForegroundColor Yellow
Write-Host "   - ENVIRONMENT=production"
Write-Host "   - OPENAI_API_KEY=your-key (optional)"
Write-Host ""
Write-Host "📖 Full guide: See RAILWAY_DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host ""
