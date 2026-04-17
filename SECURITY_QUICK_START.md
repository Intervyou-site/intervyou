# 🚀 Security Quick Start Guide

## Get Your Application Production-Ready in 5 Steps

### Step 1: Generate Secure SECRET_KEY

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy the output and set it in your environment
```

### Step 2: Configure Environment Variables

Create `.env.production` or set in your hosting platform:

```bash
# REQUIRED
SECRET_KEY=<your-generated-key-from-step-1>
DATABASE_URL=postgresql://user:password@host:5432/db?sslmode=require
OPENAI_API_KEY=sk-your-key-here
ENVIRONMENT=production

# REQUIRED FOR HTTPS
ALLOWED_ORIGINS=https://yourdomain.com
TRUSTED_HOSTS=yourdomain.com
```

### Step 3: Set Up PostgreSQL Database

```bash
# Create database
createdb intervyou

# Create user with strong password
psql -c "CREATE USER intervyou_user WITH PASSWORD 'strong-random-password';"

# Grant permissions
psql -d intervyou -c "GRANT ALL PRIVILEGES ON DATABASE intervyou TO intervyou_user;"

# Enable SSL (in postgresql.conf)
ssl = on
```

### Step 4: Deploy with Security Enabled

```bash
# The application will automatically:
# ✅ Enforce HTTPS
# ✅ Add security headers
# ✅ Enable request logging
# ✅ Monitor suspicious activity
# ✅ Validate secrets on startup

# Start the application
python start.py
```

### Step 5: Verify Security

```bash
# Check security logs
tail -f logs/security.log
tail -f logs/api_errors.log
tail -f logs/traffic.log

# Test HTTPS redirect
curl -I http://yourdomain.com
# Should return 301 redirect to https://

# Check security headers
curl -I https://yourdomain.com
# Should include Strict-Transport-Security, X-Frame-Options, etc.
```

---

## Platform-Specific Deployment

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Set environment variables
railway variables set SECRET_KEY="your-secret-key"
railway variables set ENVIRONMENT="production"
railway variables set ALLOWED_ORIGINS="https://your-app.railway.app"
railway variables set TRUSTED_HOSTS="your-app.railway.app"

# Add PostgreSQL
railway add postgresql

# Deploy
railway up
```

### Heroku

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set ENVIRONMENT="production"
heroku config:set ALLOWED_ORIGINS="https://your-app.herokuapp.com"
heroku config:set TRUSTED_HOSTS="your-app.herokuapp.com"

# Deploy
git push heroku main
```

### Docker

```bash
# Build image
docker build -t intervyou:latest .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DATABASE_URL="postgresql://..." \
  -e ENVIRONMENT="production" \
  -e ALLOWED_ORIGINS="https://yourdomain.com" \
  -e TRUSTED_HOSTS="yourdomain.com" \
  --name intervyou \
  intervyou:latest
```

---

## Security Checklist

Before going live, verify:

- [ ] `SECRET_KEY` is set and >= 32 characters
- [ ] `ENVIRONMENT=production`
- [ ] Database uses PostgreSQL (not SQLite)
- [ ] Database has SSL enabled (`sslmode=require`)
- [ ] Database is NOT publicly accessible
- [ ] `ALLOWED_ORIGINS` set to your domain
- [ ] `TRUSTED_HOSTS` set to your domain
- [ ] SSL certificate is installed
- [ ] HTTPS redirect works
- [ ] Security headers are present
- [ ] Logs directory exists and is writable
- [ ] No secrets in code repository
- [ ] `.env` files in `.gitignore`

---

## Monitoring

### View Logs

```bash
# Security events (login, logout, suspicious activity)
tail -f logs/security.log

# API errors
tail -f logs/api_errors.log

# Traffic patterns
tail -f logs/traffic.log

# Search for failed logins
grep "LOGIN_FAILED" logs/security.log

# Search for suspicious activity
grep "SUSPICIOUS" logs/security.log

# Search for rate limit violations
grep "RATE_LIMIT" logs/traffic.log
```

### Set Up Alerts

```bash
# Example: Email alert on suspicious activity
grep "SUSPICIOUS" logs/security.log | mail -s "Security Alert" admin@yourdomain.com

# Example: Slack webhook on failed logins
grep "LOGIN_FAILED" logs/security.log | \
  curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Failed login detected"}' \
  YOUR_SLACK_WEBHOOK_URL
```

---

## Troubleshooting

### Issue: "Missing or invalid production secrets"

**Solution**: Ensure all required environment variables are set:
```bash
echo $SECRET_KEY
echo $DATABASE_URL
echo $OPENAI_API_KEY
```

### Issue: "Database URL contains localhost in production"

**Solution**: Use your production database URL, not localhost:
```bash
DATABASE_URL=postgresql://user:pass@production-host:5432/db
```

### Issue: "HTTPS redirect not working"

**Solution**: Check `ENVIRONMENT` variable:
```bash
echo $ENVIRONMENT  # Should be "production"
```

### Issue: "Security logs not being created"

**Solution**: Ensure logs directory exists and is writable:
```bash
mkdir -p logs
chmod 755 logs
```

---

## Next Steps

1. ✅ Read [PRODUCTION_SECURITY_GUIDE.md](PRODUCTION_SECURITY_GUIDE.md) for detailed configuration
2. ✅ Review [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) for development guidelines
3. ✅ Set up monitoring and alerts
4. ✅ Schedule regular security audits
5. ✅ Keep dependencies updated

---

## Support

For security issues, contact: security@yourdomain.com

For general support: support@yourdomain.com

---

**Your application is now secured and ready for production! 🎉**
