# Secrets Remediation Guide - URGENT ACTION REQUIRED

## 🚨 CRITICAL: Exposed Secrets Detected

Your `.env` file contains **REAL SECRETS** that must be rotated immediately.

---

## Step 1: Rotate All Secrets (DO THIS NOW)

### 1.1 OpenAI API Key ⚡ CRITICAL

**Current Key (EXPOSED):** `sk-proj-[REDACTED]...` (now revoked)

**Action:**
```bash
# 1. Go to OpenAI dashboard
open https://platform.openai.com/api-keys

# 2. Find and REVOKE the exposed key
# 3. Create a new API key
# 4. Update your environment variables (NOT in .env file)
```

**Cost Impact:** Exposed key could result in $100-$10,000+ in unauthorized charges.

---

### 1.2 Google OAuth Credentials ⚡ CRITICAL

**Exposed Client Secret:** `GOCSPX-[REDACTED]` (now revoked)

**Action:**
```bash
# 1. Go to Google Cloud Console
open https://console.cloud.google.com/apis/credentials

# 2. Find OAuth 2.0 Client ID: [REDACTED].apps.googleusercontent.com
# 3. Delete or regenerate the client secret
# 4. Update redirect URIs to production domains only
```

---

### 1.3 Gmail App Password ⚡ CRITICAL

**Exposed Email:** `nayeemabisharan@gmail.com`  
**Exposed Password:** `msuk zwrm magy sbfd`

**Action:**
```bash
# 1. Go to Google Account Security
open https://myaccount.google.com/apppasswords

# 2. Revoke the exposed app password
# 3. Generate a new app password
# 4. Consider using a dedicated service email (not personal)
```

**Security Risk:** Personal email account could be compromised.

---

### 1.4 SerpAPI Key

**Exposed Key:** `75c6ec123b521903d917bfb0772c560285a21246d130703572dc93a9e91b70af`

**Action:**
```bash
# 1. Go to SerpAPI dashboard
open https://serpapi.com/manage-api-key

# 2. Revoke the exposed key
# 3. Generate a new API key
```

---

### 1.5 Hugging Face Token

**Exposed Token:** `hf_[REDACTED]` (now revoked)

**Action:**
```bash
# 1. Go to Hugging Face settings
open https://huggingface.co/settings/tokens

# 2. Revoke the exposed token
# 3. Generate a new access token with minimal permissions
```

---

### 1.6 Application SECRET_KEY

**Exposed Key:** `8GSoa5jZBNgP_zZbczd685Xs473CD0kP86BTS2XiGKA`

**Action:**
```bash
# Generate a new secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update in your production environment variables
```

**Security Risk:** Session hijacking, authentication bypass possible.

---

## Step 2: Clean Up Git History

### 2.1 Remove .env.production from Git

```bash
# Remove from tracking (already done)
git rm --cached .env.production

# Commit the change
git commit -m "security: Remove .env.production from version control"

# Push to remote
git push origin main
```

### 2.2 Purge from Git History (Optional but Recommended)

⚠️ **WARNING:** This rewrites Git history. Coordinate with your team first.

```bash
# Install BFG Repo-Cleaner (faster than git filter-branch)
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

# Clone a fresh copy
git clone --mirror https://github.com/yourusername/intervyou.git

# Remove .env files from history
java -jar bfg.jar --delete-files .env.production intervyou.git

# Clean up
cd intervyou.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (coordinate with team!)
git push --force
```

---

## Step 3: Secure Your Environment Variables

### 3.1 Local Development

**DO NOT** store secrets in `.env` file. Instead:

```bash
# Option 1: Use a secure password manager
# Store secrets in 1Password, LastPass, or Bitwarden

# Option 2: Use direnv (recommended)
# Install: https://direnv.net/
echo 'export OPENAI_API_KEY="your-new-key"' >> .envrc
direnv allow

# Option 3: Use system environment variables
# Add to ~/.bashrc or ~/.zshrc (NOT committed to Git)
export OPENAI_API_KEY="your-new-key"
export SECRET_KEY="your-new-secret"
```

### 3.2 Production Deployment

**Use platform environment variables:**

#### Railway
```bash
# Set via Railway dashboard or CLI
railway variables set OPENAI_API_KEY="your-new-key"
railway variables set SECRET_KEY="your-new-secret"
```

#### Render
```bash
# Set in Render dashboard:
# Dashboard > Service > Environment > Add Environment Variable
```

#### AWS
```bash
# Use AWS Secrets Manager
aws secretsmanager create-secret \
  --name intervyou/openai-key \
  --secret-string "your-new-key"
```

#### Docker Compose
```bash
# Use .env file (NOT committed) or pass via command line
docker-compose up -d \
  -e OPENAI_API_KEY="your-new-key" \
  -e SECRET_KEY="your-new-secret"
```

---

## Step 4: Update .env Files Securely

### 4.1 Create Secure .env (Local Only)

```bash
# Copy from example
cp .env.example .env

# Edit with your NEW rotated secrets
nano .env

# NEVER commit this file
# Verify it's in .gitignore
git check-ignore .env  # Should output: .env
```

### 4.2 Update .env.example (Safe to Commit)

```bash
# Edit .env.example to show structure only
# Use placeholder values like:
OPENAI_API_KEY=sk-your-openai-api-key-here
SECRET_KEY=your-secret-key-here
MAIL_PASSWORD=your-app-password-here
```

---

## Step 5: Implement Secret Scanning

### 5.1 Pre-commit Hook

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
EOF

# Install hooks
pre-commit install

# Create baseline
detect-secrets scan > .secrets.baseline
```

### 5.2 GitHub Secret Scanning

```bash
# Enable in GitHub repository settings:
# Settings > Security > Code security and analysis
# Enable: Secret scanning
# Enable: Push protection
```

---

## Step 6: Verify Security

### 6.1 Check Git Status

```bash
# Verify .env files are not tracked
git status

# Should NOT show:
# - .env
# - .env.production
# - .env.local
```

### 6.2 Check Git History

```bash
# Search for exposed secrets in history
git log --all --full-history --source -- .env.production

# Should be empty or show removal commit only
```

### 6.3 Test Application

```bash
# Verify app works with new secrets
python start.py

# Check logs for authentication errors
# Test API integrations
```

---

## Step 7: Monitor for Abuse

### 7.1 OpenAI Usage

```bash
# Check usage dashboard
open https://platform.openai.com/usage

# Look for:
# - Unusual spikes in usage
# - Requests from unknown IPs
# - Unexpected costs
```

### 7.2 Google OAuth

```bash
# Check OAuth consent screen
open https://console.cloud.google.com/apis/credentials/consent

# Review:
# - Authorized domains
# - Redirect URIs
# - Recent activity
```

### 7.3 Email Account

```bash
# Check Gmail security
open https://myaccount.google.com/security

# Review:
# - Recent security events
# - Devices & activity
# - Third-party access
```

---

## Step 8: Update Documentation

### 8.1 Update README.md

Add security notice:

```markdown
## Security

⚠️ **NEVER commit `.env` files to version control**

All secrets must be stored in:
- Local: System environment variables or secure password manager
- Production: Platform environment variables (Railway, Render, AWS)

See `SECRETS_REMEDIATION_GUIDE.md` for details.
```

### 8.2 Update Deployment Guide

Add environment variable setup instructions for each platform.

---

## Step 9: Team Communication

### 9.1 Notify Team

```
Subject: URGENT: Security Incident - Secrets Rotation Required

Team,

We've identified exposed secrets in our repository. All API keys and 
credentials have been rotated. Please:

1. Pull latest changes
2. Update your local .env file with new secrets (see team password manager)
3. Never commit .env files to Git
4. Enable pre-commit hooks for secret scanning

Details: See SECRETS_REMEDIATION_GUIDE.md

Thanks,
Security Team
```

---

## Step 10: Prevent Future Incidents

### 10.1 Developer Training

- Review secure coding practices
- Understand Git and version control security
- Use password managers for secrets
- Enable IDE secret detection plugins

### 10.2 Automated Scanning

```bash
# Add to CI/CD pipeline (.gitlab-ci.yml or .github/workflows)
secret-scan:
  script:
    - pip install detect-secrets
    - detect-secrets scan --baseline .secrets.baseline
```

### 10.3 Regular Audits

- Monthly: Review environment variables
- Quarterly: Rotate all secrets
- Annually: Full security audit

---

## Verification Checklist

After completing all steps:

- [ ] All secrets rotated and old ones revoked
- [ ] `.env.production` removed from Git
- [ ] `.gitignore` updated with comprehensive patterns
- [ ] Git history cleaned (optional)
- [ ] Production uses platform environment variables
- [ ] Pre-commit hooks installed
- [ ] GitHub secret scanning enabled
- [ ] Team notified
- [ ] Documentation updated
- [ ] Monitoring enabled for API usage
- [ ] No secrets in any committed files
- [ ] Application tested with new secrets

---

## Emergency Contacts

If you suspect ongoing abuse:

- **OpenAI Support:** https://help.openai.com/
- **Google Cloud Support:** https://cloud.google.com/support
- **Your Security Team:** [Add contact info]

---

## Additional Resources

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [HashiCorp Vault](https://www.vaultproject.io/)

---

**Last Updated:** April 17, 2026  
**Status:** 🔴 ACTION REQUIRED
