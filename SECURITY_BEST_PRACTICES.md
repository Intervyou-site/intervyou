# Security Best Practices for IntervYou

## 🔐 Secrets Management

### Never Commit Secrets

**NEVER commit these files:**
- `.env`
- `.env.local`
- `.env.production`
- `.env.*.local`
- Any file containing API keys, passwords, or tokens

### Where to Store Secrets

#### Local Development

**Option 1: System Environment Variables (Recommended)**
```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="your-key-here"
export SECRET_KEY="your-secret-here"

# Reload shell
source ~/.bashrc
```

**Option 2: direnv (Recommended for per-project)**
```bash
# Install direnv
# macOS: brew install direnv
# Linux: apt-get install direnv

# Create .envrc (add to .gitignore)
echo 'export OPENAI_API_KEY="your-key-here"' >> .envrc
direnv allow
```

**Option 3: Password Manager**
- Use 1Password, LastPass, or Bitwarden
- Store secrets in secure notes
- Copy when needed (don't save to files)

#### Production Deployment

**Railway**
```bash
railway variables set OPENAI_API_KEY="your-key"
railway variables set SECRET_KEY="your-secret"
```

**Render**
- Dashboard > Service > Environment
- Add environment variables via UI

**AWS**
```bash
# Use AWS Secrets Manager
aws secretsmanager create-secret \
  --name intervyou/openai-key \
  --secret-string "your-key"
```

**Docker**
```bash
# Use environment variables, NOT .env files
docker run -e OPENAI_API_KEY="your-key" intervyou
```

---

## 🛡️ API Key Security

### OpenAI API Keys

1. **Rotate regularly** (every 90 days)
2. **Monitor usage** at https://platform.openai.com/usage
3. **Set spending limits** in OpenAI dashboard
4. **Use separate keys** for dev/staging/prod
5. **Revoke immediately** if exposed

### OAuth Credentials

1. **Restrict redirect URIs** to production domains only
2. **Use separate credentials** for each environment
3. **Enable OAuth consent screen** verification
4. **Review authorized domains** regularly

### Email Credentials

1. **Use app-specific passwords**, not main password
2. **Use dedicated service account**, not personal email
3. **Enable 2FA** on email account
4. **Monitor for suspicious activity**

---

## 🔍 Secret Detection

### Pre-commit Hooks

Install and enable:
```bash
pip install pre-commit
pre-commit install
```

This will:
- Scan for secrets before each commit
- Block commits containing secrets
- Check for common security issues

### GitHub Secret Scanning

Enable in repository settings:
- Settings > Security > Code security and analysis
- Enable "Secret scanning"
- Enable "Push protection"

### IDE Plugins

Install secret detection plugins:
- **VS Code:** GitGuardian, TruffleHog
- **PyCharm:** GitGuardian plugin
- **IntelliJ:** Secret Lens

---

## 🚨 Incident Response

### If Secrets Are Exposed

1. **Rotate immediately** - Don't wait
2. **Revoke old secrets** - Make them invalid
3. **Check for abuse** - Review API usage logs
4. **Update all environments** - Dev, staging, prod
5. **Notify team** - Ensure everyone updates
6. **Document incident** - Learn from mistakes

### Monitoring for Abuse

**OpenAI:**
- Check usage dashboard daily
- Set up billing alerts
- Monitor for unusual patterns

**Google OAuth:**
- Review OAuth consent screen activity
- Check for unauthorized apps
- Monitor redirect URI usage

**Email:**
- Enable login alerts
- Review recent activity
- Check for forwarding rules

---

## 📋 Security Checklist

### Before Every Commit

- [ ] No secrets in code
- [ ] No secrets in comments
- [ ] No hardcoded credentials
- [ ] .env files in .gitignore
- [ ] Pre-commit hooks pass

### Before Every Deployment

- [ ] Environment variables set on platform
- [ ] Secrets rotated if needed
- [ ] Production uses strong secrets
- [ ] Monitoring enabled
- [ ] Backup secrets stored securely

### Monthly Review

- [ ] Check API usage for anomalies
- [ ] Review access logs
- [ ] Audit environment variables
- [ ] Update dependencies
- [ ] Review security alerts

### Quarterly Tasks

- [ ] Rotate all secrets
- [ ] Security audit
- [ ] Review access controls
- [ ] Update documentation
- [ ] Team security training

---

## 🔧 Tools and Resources

### Secret Management Tools

- **AWS Secrets Manager** - Enterprise secret storage
- **HashiCorp Vault** - Open-source secret management
- **Azure Key Vault** - Microsoft cloud secrets
- **Google Secret Manager** - Google Cloud secrets

### Secret Scanning Tools

- **detect-secrets** - Yelp's secret scanner
- **TruffleHog** - Git history scanner
- **GitGuardian** - Real-time secret detection
- **git-secrets** - AWS secret prevention

### Security Resources

- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [12-Factor App Config](https://12factor.net/config)

---

## 👥 Team Guidelines

### For Developers

1. **Never commit secrets** - Use environment variables
2. **Use pre-commit hooks** - Catch mistakes early
3. **Report exposures immediately** - Don't hide mistakes
4. **Keep secrets in password manager** - Not in files
5. **Review PRs for secrets** - Help catch issues

### For DevOps

1. **Use platform environment variables** - Not config files
2. **Implement secret rotation** - Automate when possible
3. **Monitor for abuse** - Set up alerts
4. **Document procedures** - Make it easy to do right
5. **Regular audits** - Check for issues

### For Security Team

1. **Enable secret scanning** - GitHub, GitLab, etc.
2. **Regular security audits** - Quarterly minimum
3. **Incident response plan** - Know what to do
4. **Team training** - Educate developers
5. **Tool evaluation** - Keep improving

---

## 📚 Additional Reading

- [NIST Secret Management Guidelines](https://csrc.nist.gov/publications)
- [CIS Controls for Secret Management](https://www.cisecurity.org/controls)
- [SANS Secure Coding Practices](https://www.sans.org/security-resources)

---

**Last Updated:** April 17, 2026  
**Next Review:** May 17, 2026
