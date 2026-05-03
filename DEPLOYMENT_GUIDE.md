# IntervYou Deployment Guide

## Option 1: Railway (Recommended - Easiest)

### Step 1: Prepare Your Repository
1. Push your code to GitHub/GitLab
2. Ensure your `.env.example` has all required variables

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your IntervYou repository
5. Railway will auto-detect your Dockerfile

### Step 3: Configure Environment Variables
In Railway dashboard:
- Add all variables from your `.env` file
- Railway will provide a PostgreSQL database URL automatically

### Step 4: Connect Your Domain
1. In Railway project settings → "Domains"
2. Add your custom domain
3. Update your domain's DNS records as shown

### Step 5: SSL Certificate
Railway automatically provides SSL certificates for custom domains.

---

## Option 2: DigitalOcean App Platform

### Step 1: Create App
1. Go to [DigitalOcean](https://digitalocean.com)
2. Create account → Apps → Create App
3. Connect your GitHub repository

### Step 2: Configure Build
- Source: Your repository
- Build Command: `docker build -t intervyou .`
- Run Command: `python -m gunicorn fastapi_app_cleaned:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`

### Step 3: Add Database
- Add PostgreSQL database component
- Note the connection string

### Step 4: Environment Variables
Add all your environment variables in the App settings.

### Step 5: Custom Domain
- Add your domain in App settings
- Update DNS records as instructed

---

## Option 3: VPS Setup (Advanced)

### Step 1: Get a VPS
- DigitalOcean Droplet ($5/month)
- Linode ($5/month)
- Vultr ($2.50/month)

### Step 2: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 3: Deploy Application
```bash
# Clone your repository
git clone <your-repo-url>
cd intervyou

# Set up environment
cp .env.example .env
nano .env  # Edit with your values

# Start application
docker-compose up -d
```

### Step 4: Set Up Nginx (Reverse Proxy)
```bash
# Install Nginx
sudo apt install nginx

# Create configuration
sudo nano /etc/nginx/sites-available/intervyou
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/intervyou /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## DNS Configuration

For any hosting option, you'll need to update your domain's DNS records:

### A Record (for VPS)
- Type: A
- Name: @ (or your subdomain)
- Value: Your server's IP address

### CNAME Record (for cloud platforms)
- Type: CNAME
- Name: @ (or www)
- Value: The URL provided by your hosting platform

---

## Environment Variables Checklist

Make sure to set these in your hosting platform:

```env
# Required
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# AI Features (Optional but recommended)
OPENAI_API_KEY=your-openai-key

# Email (Optional)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

---

## Cost Comparison

| Platform | Cost/Month | Ease | Features |
|----------|------------|------|----------|
| Railway | $5-20 | ⭐⭐⭐⭐⭐ | Auto-deploy, DB included |
| Render | $0-25 | ⭐⭐⭐⭐⭐ | Free tier, easy setup |
| DigitalOcean App | $12-25 | ⭐⭐⭐⭐ | Reliable, good docs |
| VPS | $5-10 | ⭐⭐ | Full control, more work |

---

## Recommended: Start with Railway

1. It's the easiest to set up
2. Automatic deployments from Git
3. Built-in PostgreSQL
4. Automatic SSL
5. Great for FastAPI applications

Would you like me to help you set up any of these options?