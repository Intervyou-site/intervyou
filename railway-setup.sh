#!/bin/bash

# Railway Setup Script for IntervYou
# This script helps you prepare for Railway deployment

echo "🚂 IntervYou - Railway Deployment Setup"
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git repository not initialized"
    echo "Run: git init"
    exit 1
fi

echo "✅ Git repository found"
echo ""

# Check for required files
echo "📋 Checking required files..."
files=("Dockerfile" "requirements-docker.txt" ".env.example" "fastapi_app_cleaned.py")
missing_files=()

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo ""
    echo "❌ Missing required files. Please ensure all files exist."
    exit 1
fi

echo ""
echo "✅ All required files present"
echo ""

# Generate SECRET_KEY if needed
echo "🔐 Generating SECRET_KEY..."
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
echo "Generated SECRET_KEY: $SECRET_KEY"
echo ""

# Check git status
echo "📊 Git Status:"
git status --short
echo ""

# Offer to commit and push
read -p "Do you want to commit and push to GitHub? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add .
    git commit -m "Prepare for Railway deployment"
    
    # Check if remote exists
    if git remote | grep -q "origin"; then
        git push origin main || git push origin master
        echo "✅ Pushed to GitHub"
    else
        echo "❌ No remote 'origin' found. Add your GitHub repository:"
        echo "   git remote add origin https://github.com/yourusername/your-repo.git"
        echo "   git push -u origin main"
    fi
fi

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "Next Steps:"
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select your repository"
echo "5. Add PostgreSQL database"
echo "6. Add environment variables:"
echo "   - SECRET_KEY=$SECRET_KEY"
echo "   - ENVIRONMENT=production"
echo "   - OPENAI_API_KEY=your-key (optional)"
echo ""
echo "📖 Full guide: See RAILWAY_DEPLOYMENT.md"
echo ""
