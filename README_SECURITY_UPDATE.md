# 🔐 Security Update - README Addition

Add this section to your README.md file:

---

## ⚠️ Security Notice

**CRITICAL: Never commit `.env` files or secrets to version control!**

### For Developers

All secrets and API keys must be stored securely:

**Local Development:**
- Use system environment variables
- Use password manager (1Password, LastPass, Bitwarden)
- Use direnv for per-project environment variables
- **NEVER** commit `.env` files

**Production Deployment:**
- Use platform environment variables (Railway, Render, AWS)
- Use secret management services (AWS Secrets Manager, HashiCorp Vault)
- Enable secret scanning in CI/CD pipeline

### Quick Start

1. Copy environment template:
   ```bash
   cp .env.example .env
   ```

2. Fill in your secrets (get from team password manager)

3. Verify `.env` is in `.gitignore`:
   ```bash
   git check-ignore .env  # Should output: .env
   ```

4. Install pre-commit hooks:
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Security Resources

- [SECURITY_BEST_PRACTICES.md](SECURITY_BEST_PRACTICES.md) - Comprehensive security guide
- [SECRETS_REMEDIATION_GUIDE.md](SECRETS_REMEDIATION_GUIDE.md) - Secret rotation procedures
- [IMMEDIATE_ACTION_PLAN.md](IMMEDIATE_ACTION_PLAN.md) - Emergency response plan

### Reporting Security Issues

If you discover a security vulnerability, please email: [security@yourdomain.com]

**DO NOT** create public GitHub issues for security vulnerabilities.

---

## 🔒 Required Environment Variables

### Core Services (Required)

```bash
# Application Security
SECRET_KEY=your-secret-key-here  # Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"

# Database
DATABASE_URL=postgresql://user:password@host:5432/intervyou

# OpenAI API (for AI features)
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Optional Services

```bash
# Email (for password reset)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password-here

# Google OAuth (for social login)
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# SerpAPI (for question generation)
SERPAPI_KEY=your-serpapi-key-here

# Hugging Face (for AI models)
HUGGINGFACE_API_TOKEN=your-huggingface-token-here
```

See `.env.example` for complete configuration options.

---

## 🛡️ Security Features

- ✅ Rate limiting and abuse protection
- ✅ HTTPS enforcement in production
- ✅ Secure session management
- ✅ Password strength validation
- ✅ Email verification
- ✅ OAuth social login
- ✅ Pre-commit secret scanning
- ✅ Security headers (CSP, HSTS, etc.)

---
