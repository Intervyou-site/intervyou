# IntervYou - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Clean Up Project (First Time Only)
```powershell
# Run the cleanup script to remove unnecessary files
.\cleanup_project.ps1
```

### Step 2: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your credentials:
# - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
# - OPENAI_API_KEY
# - MAIL_USERNAME and MAIL_PASSWORD
```

### Step 3: Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Generate SSL Certificates (for HTTPS)
```bash
python start.py --generate-cert
```

### Step 5: Start the Application
```bash
python start.py
```

The application will be available at: **https://localhost:8000**

## 📱 First Login

1. Navigate to https://localhost:8000
2. Click "Register" to create an account
3. Fill in your details and submit
4. Login with your credentials
5. You'll land on your Profile page!

## 🎯 Key Features to Try

### 1. Practice Sessions
- Go to "Practice" from the sidebar
- Select a category (e.g., "Python", "Behavioral")
- Choose a company (optional)
- Answer questions and get AI feedback

### 2. Video Interview
- Go to "Video Interview"
- Allow camera permissions
- Practice answering questions on video
- Get AI-powered feedback

### 3. Online IDE
- Go to "Code Editor"
- Select a programming language
- Write and execute code
- Get code quality analysis

### 4. Resume Builder
- Go to "Resume Analyzer"
- Fill in your details
- Choose a template
- Download your ATS-optimized resume

### 5. Track Progress
- Go to "Reports" to see your performance
- Go to "Analytics" for detailed insights
- Go to "Profile" to see achievements

## 🔧 Troubleshooting

### Camera Not Working
- Ensure you're using HTTPS (https://localhost:8000)
- Allow camera permissions in your browser
- Try a different browser (Chrome recommended)

### IDE Not Executing Code
- Ensure Docker is running
- Pull required images: `docker pull gcc:11 python:3.11-slim node:20-slim`

### Login Issues
- Check your email and password
- If locked out, wait 15 minutes
- Use "Forgot Password" to reset

### OpenAI API Errors
- Verify your API key in .env
- Check you have sufficient credits
- Review rate limits

## 📚 Next Steps

1. **Explore Features**: Try all the features to understand the platform
2. **Customize**: Update branding, colors, and content as needed
3. **Deploy**: Follow DEPLOYMENT_GUIDE.md for production deployment
4. **Monitor**: Set up logging and monitoring
5. **Iterate**: Gather feedback and improve

## 🆘 Need Help?

- Check README_PRODUCTION.md for detailed documentation
- Review PRODUCTION_CHECKLIST.md for deployment
- Check logs in `logs/` directory
- Open an issue on GitHub

## 🎉 You're All Set!

Start practicing and improving your interview skills with IntervYou!

---

**Happy Interviewing! 🚀**
