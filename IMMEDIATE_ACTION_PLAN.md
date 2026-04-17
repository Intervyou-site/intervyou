# 🚨 IMMEDIATE ACTION PLAN - Security Incident Response

**Date:** April 17, 2026  
**Severity:** CRITICAL  
**Status:** ACTION REQUIRED NOW

---

## ⏰ Timeline

| Priority | Action | Time Required | Deadline |
|----------|--------|---------------|----------|
| 🔴 P0 | Rotate OpenAI API Key | 5 minutes | **NOW** |
| 🔴 P0 | Rotate Google OAuth Secret | 5 minutes | **NOW** |
| 🔴 P0 | Rotate Gmail App Password | 5 minutes | **NOW** |
| 🔴 P0 | Rotate SerpAPI Key | 5 minutes | **NOW** |
| 🔴 P0 | Rotate Hugging Face Token | 5 minutes | **NOW** |
| 🔴 P0 | Generate New SECRET_KEY | 2 minutes | **NOW** |
| 🟡 P1 | Remove .env.production from Git | 2 minutes | Within 1 hour |
| 🟡 P1 | Update .gitignore | 2 minutes | Within 1 hour |
| 🟡 P1 | Commit security fixes | 5 minutes | Within 1 hour |
| 🟢 P2 | Clean Git history | 30 minutes | Within 24 hours |
| 🟢 P2 | Enable secret scanning | 10 minutes | Within 24 hours |
| 🟢 P2 | Install pre-commit hooks | 10 minutes | Within 24 hours |

**Total Time for Critical Actions:** ~30 minutes

---

## 🔴 PRIORITY 0: Rotate All Secrets (DO THIS FIRST)

### 1. OpenAI API Key (5 minutes)

```bash
# Step 1: Open OpenAI dashboard
open https://platform.openai.com/api-keys

# Step 2: Find and click on the exposed key
# Key starts with: sk-proj-[REDACTED]... (now revoked)

# Step 3: Click "Revoke" or "Delete"

# Step 4: Click "Create new secret key"
# Name it: "IntervYou Production - April 2026"

# Step 5: Copy the new key (you'll only see it once!)

# Step 6: Update in your production environment
# Railway: railway variables set OPENAI_API_KEY="new-key-here"
# Render: Dashboard > Environment > Edit
# AWS: aws secretsmanager update-secret --secret-id intervyou/openai-key

# Step 7: Update local .env (DO NOT COMMIT)
# Edit .env and replace OPENAI_API_KEY value

# Step 8: Restart your application
```

**Verification:**
```bash
# Test that new key works
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_NEW_KEY"

# Should return list of models, not an error
```

---

### 2. Google OAuth Credentials (5 minutes)

```bash
# Step 1: Open Google Cloud Console
open https://console.cloud.google.com/apis/credentials

# Step 2: Find OAuth 2.0 Client ID
# Client ID: [REDACTED].apps.googleusercontent.com

# Step 3: Click on the client ID name

# Step 4: Click "Reset Secret" or create new credentials

# Step 5: Copy new Client ID and Client Secret

# Step 6: Update Authorized redirect URIs
# Remove any localhost/development URLs from production credentials
# Keep only: https://yourdomain.com/auth/google/callback

# Step 7: Update in production environment
railway variables set GOOGLE_CLIENT_ID="new-client-id"
railway variables set GOOGLE_CLIENT_SECRET="new-secret"

# Step 8: Update local .env (DO NOT COMMIT)
```

**Verification:**
```bash
# Test OAuth flow
# Visit: https://yourdomain.com/auth/google
# Should redirect to Google login successfully
```

---

### 3. Gmail App Password (5 minutes)

```bash
# Step 1: Open Google Account Security
open https://myaccount.google.com/apppasswords

# Step 2: Find and revoke the exposed password
# Password: msuk zwrm magy sbfd

# Step 3: Generate new app password
# Name it: "IntervYou Email Service"

# Step 4: Copy the 16-character password

# Step 5: Update in production environment
railway variables set MAIL_PASSWORD="new-app-password"

# Step 6: Update local .env (DO NOT COMMIT)
```

**⚠️ IMPORTANT:** Consider using a dedicated service email instead of personal email:
```bash
# Create new Gmail account: intervyou-noreply@gmail.com
# Enable 2FA
# Generate app password
# Update MAIL_USERNAME and MAIL_PASSWORD
```

**Verification:**
```bash
# Test email sending
# Trigger password reset flow
# Check that email is received
```

---

### 4. SerpAPI Key (5 minutes)

```bash
# Step 1: Open SerpAPI dashboard
open https://serpapi.com/manage-api-key

# Step 2: Revoke exposed key
# Key: 75c6ec123b521903d917bfb0772c560285a21246d130703572dc93a9e91b70af

# Step 3: Generate new API key

# Step 4: Update in production environment
railway variables set SERPAPI_KEY="new-key"

# Step 5: Update local .env (DO NOT COMMIT)
```

**Verification:**
```bash
# Test SerpAPI
curl "https://serpapi.com/search?q=test&api_key=YOUR_NEW_KEY"

# Should return search results
```

---

### 5. Hugging Face Token (5 minutes)

```bash
# Step 1: Open Hugging Face settings
open https://huggingface.co/settings/tokens

# Step 2: Find and revoke exposed token
# Token: hf_[REDACTED] (now revoked)

# Step 3: Create new access token
# Name: "IntervYou Production"
# Type: Read (minimal permissions needed)

# Step 4: Update in production environment
railway variables set HUGGINGFACE_API_TOKEN="new-token"

# Step 5: Update local .env (DO NOT COMMIT)
```

**Verification:**
```bash
# Test Hugging Face API
curl https://huggingface.co/api/whoami-v2 \
  -H "Authorization: Bearer YOUR_NEW_TOKEN"

# Should return your user info
```

---

### 6. Application SECRET_KEY (2 minutes)

```bash
# Step 1: Generate new secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Example output: xK8vN2mP9qR4sT6uV7wX8yZ0aB1cD2eF3gH4iJ5kL6m

# Step 2: Update in production environment
railway variables set SECRET_KEY="your-new-secret-key"

# Step 3: Update local .env (DO NOT COMMIT)

# Step 4: Restart application
# ⚠️ WARNING: This will log out all users
```

**Verification:**
```bash
# Test login flow
# All existing sessions should be invalidated
# New logins should work
```

---

## 🟡 PRIORITY 1: Secure Git Repository (Within 1 Hour)

### 1. Remove .env.production from Git (DONE ✅)

```bash
# Already executed:
git rm --cached .env.production

# Now commit:
git commit -m "security: Remove .env.production from version control"

# Push to remote:
git push origin main
```

### 2. Update .gitignore (DONE ✅)

```bash
# Already updated with comprehensive patterns

# Verify:
git check-ignore .env
git check-ignore .env.production
git check-ignore .env.local

# All should output the filename (meaning they're ignored)
```

### 3. Commit Security Fixes

```bash
# Stage all security-related files
git add .gitignore
git add .pre-commit-config.yaml
git add .secrets.baseline
git add SECURITY_*.md
git add SECRETS_REMEDIATION_GUIDE.md
git add IMMEDIATE_ACTION_PLAN.md

# Commit
git commit -m "security: Add comprehensive secret protection and documentation

- Update .gitignore with comprehensive environment file patterns
- Add pre-commit hooks for secret detection
- Add security documentation and remediation guides
- Remove .env.production from tracking
- Add secret scanning baseline

BREAKING CHANGE: All secrets have been rotated due to exposure"

# Push
git push origin main
```

---

## 🟢 PRIORITY 2: Long-term Security (Within 24 Hours)

### 1. Clean Git History (Optional but Recommended)

⚠️ **WARNING:** This rewrites Git history. Coordinate with team first.

```bash
# Option 1: Using BFG Repo-Cleaner (Recommended)
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

# Clone fresh mirror
git clone --mirror https://github.com/yourusername/intervyou.git

# Remove .env.production from all history
java -jar bfg.jar --delete-files .env.production intervyou.git

# Clean up
cd intervyou.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (⚠️ COORDINATE WITH TEAM)
git push --force

# Option 2: Using git filter-branch
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env.production" \
  --prune-empty --tag-name-filter cat -- --all

# Force push
git push --force --all
```

### 2. Enable GitHub Secret Scanning

```bash
# Go to repository settings
open https://github.com/yourusername/intervyou/settings/security_analysis

# Enable:
# ✅ Dependency graph
# ✅ Dependabot alerts
# ✅ Dependabot security updates
# ✅ Secret scanning
# ✅ Push protection
```

### 3. Install Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Test
pre-commit run --all-files

# Should scan all files for secrets
```

---

## 📊 Monitoring and Verification

### Check for Abuse

#### OpenAI Usage
```bash
# Check usage dashboard
open https://platform.openai.com/usage

# Look for:
# - Unusual spikes in usage
# - Requests from unknown IPs
# - Unexpected costs

# Set spending limit:
# Settings > Billing > Usage limits
# Set to reasonable amount (e.g., $50/month)
```

#### Google OAuth
```bash
# Check OAuth consent screen
open https://console.cloud.google.com/apis/credentials/consent

# Review:
# - Authorized domains
# - Redirect URIs
# - Recent activity
```

#### Email Account
```bash
# Check Gmail security
open https://myaccount.google.com/security

# Review:
# - Recent security events
# - Devices & activity
# - Third-party access
# - Forwarding rules (should be none)
```

---

## 📝 Documentation Updates

### Update README.md

Add security notice at the top:

```markdown
## ⚠️ Security Notice

**NEVER commit `.env` files to version control!**

All secrets must be stored in:
- **Local Development:** System environment variables or password manager
- **Production:** Platform environment variables (Railway, Render, AWS)

See [SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md) for details.
```

### Update DEPLOYMENT_GUIDE.md

Add section on environment variables for each platform.

---

## 👥 Team Communication

### Send to Team

```
Subject: 🚨 URGENT: Security Incident - Action Required

Team,

We've identified exposed secrets in our Git repository. All API keys and 
credentials have been rotated as of [TIME].

IMMEDIATE ACTIONS REQUIRED:
1. Pull latest changes: git pull origin main
2. Update your local .env file with new secrets (see team password manager)
3. Install pre-commit hooks: pip install pre-commit && pre-commit install
4. NEVER commit .env files to Git

NEW SECRETS LOCATION:
- Check team password manager (1Password/LastPass)
- Or contact [ADMIN] for access

WHAT HAPPENED:
- .env file with real secrets was committed to repository
- All secrets have been rotated and old ones revoked
- Security measures implemented to prevent future incidents

QUESTIONS:
Contact [SECURITY LEAD] or [DEVOPS LEAD]

Documentation:
- SECURITY_BEST_PRACTICES.md
- SECRETS_REMEDIATION_GUIDE.md
- IMMEDIATE_ACTION_PLAN.md

Thanks,
Security Team
```

---

## ✅ Verification Checklist

After completing all actions:

### Immediate (P0)
- [ ] OpenAI API key rotated and old key revoked
- [ ] Google OAuth credentials rotated
- [ ] Gmail app password rotated
- [ ] SerpAPI key rotated
- [ ] Hugging Face token rotated
- [ ] Application SECRET_KEY regenerated
- [ ] All production environment variables updated
- [ ] Application restarted with new secrets
- [ ] All services tested and working

### Short-term (P1)
- [ ] .env.production removed from Git
- [ ] .gitignore updated
- [ ] Security fixes committed and pushed
- [ ] Team notified
- [ ] Documentation updated

### Long-term (P2)
- [ ] Git history cleaned (optional)
- [ ] GitHub secret scanning enabled
- [ ] Pre-commit hooks installed
- [ ] Monitoring enabled for API usage
- [ ] No secrets in any committed files
- [ ] Security audit scheduled (monthly)

---

## 📞 Emergency Contacts

- **OpenAI Support:** https://help.openai.com/
- **Google Cloud Support:** https://cloud.google.com/support
- **GitHub Support:** https://support.github.com/
- **Security Lead:** [Add contact]
- **DevOps Lead:** [Add contact]

---

## 📚 Additional Resources

- [SECURITY_SECRETS_AUDIT_REPORT.md](SECURITY_SECRETS_AUDIT_REPORT.md) - Full audit report
- [SECRETS_REMEDIATION_GUIDE.md](SECRETS_REMEDIATION_GUIDE.md) - Detailed remediation steps
- [SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md) - Ongoing security practices

---

**Status:** 🔴 IN PROGRESS  
**Last Updated:** April 17, 2026  
**Next Review:** After all P0 and P1 actions completed
