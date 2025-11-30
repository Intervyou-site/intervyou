# GitHub Setup for IntervYou

## Step 1: Create GitHub Repository

1. **Go to GitHub:**
   - Visit: https://github.com/new

2. **Create Repository:**
   - Repository name: `intervyou`
   - Description: "AI-Powered Interview Coach"
   - Visibility: Public (or Private if you prefer)
   - **DO NOT** check "Initialize with README"
   - Click "Create repository"

3. **Copy your repository URL:**
   - It will look like: `https://github.com/YOUR_USERNAME/intervyou.git`
   - Example: `https://github.com/abishek123/intervyou.git`

---

## Step 2: Push Your Code

Once you have your GitHub username, run these commands:

```bash
# Remove old remote
git remote remove origin

# Add your actual GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/intervyou.git

# Commit your code
git add .
git commit -m "Initial commit - Deploy to Railway"

# Push to GitHub
git push -u origin main
```

---

## If You Get Authentication Error

GitHub requires a Personal Access Token (not password):

1. **Create Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: "IntervYou Deploy"
   - Select scopes: `repo` (all)
   - Click "Generate token"
   - **COPY THE TOKEN** (you won't see it again!)

2. **Use Token When Pushing:**
   ```bash
   git push -u origin main
   # Username: YOUR_GITHUB_USERNAME
   # Password: PASTE_YOUR_TOKEN_HERE
   ```

---

## Alternative: Use GitHub Desktop (Easier)

1. **Download GitHub Desktop:**
   - https://desktop.github.com

2. **Open GitHub Desktop:**
   - File → Add Local Repository
   - Choose your project folder
   - Click "Publish repository"
   - Done!

---

## Quick Commands Reference

```bash
# Check current remote
git remote -v

# Remove remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/USERNAME/intervyou.git

# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Your message"

# Push
git push -u origin main
```

---

**Next:** Once code is on GitHub, go to Railway.app and deploy!
