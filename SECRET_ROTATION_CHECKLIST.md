# 🔐 Secret Rotation Checklist

**Use this checklist to track your progress rotating exposed secrets.**

---

## ⏰ Estimated Time: 30-45 minutes

---

## 🔴 CRITICAL: Rotate Secrets (Priority 0)

### 1. OpenAI API Key
- [ ] Go to https://platform.openai.com/api-keys
- [ ] Find key starting with: `sk-proj-5F9Qfs...`
- [ ] Click "Revoke" or "Delete"
- [ ] Create new secret key
- [ ] Name it: "IntervYou Production - April 2026"
- [ ] Copy new key (shown only once!)
- [ ] Update production environment: `railway variables set OPENAI_API_KEY="new-key"`
- [ ] Update local .env (DO NOT COMMIT)
- [ ] Test: `curl https://api.openai.com/v1/models -H "Authorization: Bearer NEW_KEY"`
- [ ] Verify application works

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### 2. Google OAuth Credentials
- [ ] Go to https://console.cloud.google.com/apis/credentials
- [ ] Find Client ID: `492241635514-t59fkb3g31l2hodagfqbjjbm1le04in3`
- [ ] Click on client ID name
- [ ] Click "Reset Secret" or create new credentials
- [ ] Copy new Client ID and Client Secret
- [ ] Update Authorized redirect URIs (remove localhost from production)
- [ ] Update production: `railway variables set GOOGLE_CLIENT_ID="new-id"`
- [ ] Update production: `railway variables set GOOGLE_CLIENT_SECRET="new-secret"`
- [ ] Update local .env (DO NOT COMMIT)
- [ ] Test OAuth flow: Visit `/auth/google`

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### 3. Gmail App Password
- [ ] Go to https://myaccount.google.com/apppasswords
- [ ] Find and revoke password: `msuk zwrm magy sbfd`
- [ ] Generate new app password
- [ ] Name it: "IntervYou Email Service"
- [ ] Copy 16-character password
- [ ] Update production: `railway variables set MAIL_PASSWORD="new-password"`
- [ ] Update local .env (DO NOT COMMIT)
- [ ] Test: Trigger password reset flow
- [ ] Verify email is received

**Bonus:** Consider creating dedicated service email
- [ ] Create new Gmail: `intervyou-noreply@gmail.com`
- [ ] Enable 2FA
- [ ] Generate app password
- [ ] Update MAIL_USERNAME and MAIL_PASSWORD

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### 4. SerpAPI Key
- [ ] Go to https://serpapi.com/manage-api-key
- [ ] Revoke key: `75c6ec123b521903d917bfb0772c560285a21246d130703572dc93a9e91b70af`
- [ ] Generate new API key
- [ ] Copy new key
- [ ] Update production: `railway variables set SERPAPI_KEY="new-key"`
- [ ] Update local .env (DO NOT COMMIT)
- [ ] Test: `curl "https://serpapi.com/search?q=test&api_key=NEW_KEY"`
- [ ] Verify application works

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### 5. Hugging Face Token
- [ ] Go to https://huggingface.co/settings/tokens
- [ ] Find and revoke token: `hf_CLbXkns...`
- [ ] Create new access token
- [ ] Name: "IntervYou Production"
- [ ] Type: Read (minimal permissions)
- [ ] Copy new token
- [ ] Update production: `railway variables set HUGGINGFACE_API_TOKEN="new-token"`
- [ ] Update local .env (DO NOT COMMIT)
- [ ] Test: `curl https://huggingface.co/api/whoami-v2 -H "Authorization: Bearer NEW_TOKEN"`
- [ ] Verify application works

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### 6. Application SECRET_KEY
- [ ] Generate new key: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Copy generated key
- [ ] Update production: `railway variables set SECRET_KEY="new-secret"`
- [ ] Update local .env (DO NOT COMMIT)
- [ ] Restart application
- [ ] ⚠️ Note: This will log out all users
- [ ] Test login flow
- [ ] Verify new sessions work

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 🟡 Repository Security (Priority 1)

### 7. Git Repository Cleanup
- [✅] Remove .env.production from Git (DONE)
- [✅] Update .gitignore (DONE)
- [✅] Commit security fixes (DONE)
- [ ] Push to remote: `git push origin main`
- [ ] Verify .env files not tracked: `git ls-files .env*`

**Status:** ⏳ In Progress | ✅ Complete

---

### 8. Pre-commit Hooks
- [ ] Install pre-commit: `pip install pre-commit`
- [ ] Install hooks: `pre-commit install`
- [ ] Test: `pre-commit run --all-files`
- [ ] Verify secret detection works
- [ ] Share with team

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### 9. GitHub Secret Scanning
- [ ] Go to repository settings
- [ ] Navigate to: Settings > Security > Code security and analysis
- [ ] Enable: Dependency graph
- [ ] Enable: Dependabot alerts
- [ ] Enable: Dependabot security updates
- [ ] Enable: Secret scanning
- [ ] Enable: Push protection

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 🟢 Verification (Priority 2)

### 10. Test Application
- [ ] Start application: `python start.py`
- [ ] Check logs for errors
- [ ] Test login/logout
- [ ] Test AI features (OpenAI)
- [ ] Test email (password reset)
- [ ] Test OAuth (Google login)
- [ ] Test question generation (SerpAPI)
- [ ] Verify all features work

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### 11. Monitor for Abuse
- [ ] Check OpenAI usage: https://platform.openai.com/usage
- [ ] Check for unusual spikes
- [ ] Set spending limit: Settings > Billing > Usage limits
- [ ] Check Google OAuth activity
- [ ] Check Gmail security events
- [ ] Review for suspicious activity

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### 12. Update Documentation
- [ ] Add security section to README.md (use README_SECURITY_UPDATE.md)
- [ ] Update deployment guide with environment variables
- [ ] Update team wiki/docs
- [ ] Document secret rotation procedure
- [ ] Share security best practices

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### 13. Team Communication
- [ ] Notify team of security incident
- [ ] Share new secrets via password manager
- [ ] Ensure everyone updates local .env
- [ ] Remind: NEVER commit .env files
- [ ] Share pre-commit hook installation instructions
- [ ] Schedule security training

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 📊 Progress Tracker

**Overall Progress:**

```
Critical (P0): [ ] [ ] [ ] [ ] [ ] [ ]  (0/6 complete)
Repository (P1): [✅] [✅] [✅] [ ]     (3/4 complete)
Verification (P2): [ ] [ ] [ ] [ ]     (0/4 complete)

Total: 3/14 tasks complete (21%)
```

---

## ⏰ Time Tracking

| Task | Estimated | Actual | Status |
|------|-----------|--------|--------|
| OpenAI Key | 5 min | ___ min | ⬜ |
| Google OAuth | 5 min | ___ min | ⬜ |
| Gmail Password | 5 min | ___ min | ⬜ |
| SerpAPI Key | 5 min | ___ min | ⬜ |
| Hugging Face | 5 min | ___ min | ⬜ |
| SECRET_KEY | 2 min | ___ min | ⬜ |
| Git Push | 2 min | ___ min | ⬜ |
| Pre-commit | 10 min | ___ min | ⬜ |
| GitHub Scanning | 10 min | ___ min | ⬜ |
| Testing | 15 min | ___ min | ⬜ |
| Monitoring | 10 min | ___ min | ⬜ |
| Documentation | 15 min | ___ min | ⬜ |
| Team Comm | 10 min | ___ min | ⬜ |
| **TOTAL** | **99 min** | **___ min** | |

---

## 🚨 If You Get Stuck

### Quick Help

**Can't access a service?**
- Check if you have the right account/permissions
- Contact service support
- Ask team lead for help

**Not sure about a step?**
- Read detailed guide: `SECRETS_REMEDIATION_GUIDE.md`
- Check action plan: `IMMEDIATE_ACTION_PLAN.md`
- Ask for help - don't skip steps!

**Application not working after rotation?**
- Check environment variables are set correctly
- Restart application
- Check logs for errors
- Verify new secrets are valid

---

## ✅ Final Verification

Before marking complete, verify:

- [ ] All 6 secrets rotated
- [ ] Old secrets revoked/deleted
- [ ] Production environment updated
- [ ] Local .env updated (not committed)
- [ ] Application tested and working
- [ ] No errors in logs
- [ ] Git changes pushed
- [ ] Pre-commit hooks installed
- [ ] Team notified
- [ ] Documentation updated
- [ ] Monitoring enabled
- [ ] No secrets in Git: `git log --all --full-history -- .env*`

---

## 🎉 Completion

When all tasks are complete:

1. Mark this checklist as complete
2. File this document for future reference
3. Schedule next security audit (30 days)
4. Schedule quarterly secret rotation
5. Celebrate - you've secured your application! 🎊

---

**Started:** _______________  
**Completed:** _______________  
**Time Taken:** _______________  
**Completed By:** _______________

---

*For detailed instructions, see:*
- *IMMEDIATE_ACTION_PLAN.md*
- *SECRETS_REMEDIATION_GUIDE.md*
- *SECURITY_BEST_PRACTICES.md*
