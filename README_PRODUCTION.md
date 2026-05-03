# IntervYou - AI-Powered Interview Preparation Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

IntervYou is a comprehensive AI-powered interview preparation platform that helps candidates practice and improve their interview skills through:

- **Practice Sessions**: Category-based interview questions with AI feedback
- **Video Interview**: AI-powered video analysis with real-time feedback
- **Online IDE**: Code challenges with support for multiple programming languages
- **Resume Builder**: ATS-optimized resume templates with AI suggestions
- **AI Career Advisor**: Personalized guidance and learning plans
- **Analytics Dashboard**: Track progress and identify improvement areas
- **Leaderboard**: Compete with other users

## ✨ Features

### Core Features
- 🎯 **15+ Company-Specific Questions** (Google, Amazon, Microsoft, Meta, etc.)
- 🏢 **Mass Recruitment Companies** (TCS, Infosys, Wipro, Cognizant, etc.)
- 📚 **150+ MCQ Questions** in Aptitude section
- 💻 **Online IDE** with C, C++, Java, Python, JavaScript support
- 🎥 **Video Interview Practice** with AI analysis
- 📊 **Performance Analytics** with detailed insights
- 🏆 **Achievement System** with unlockable badges
- 📝 **Resume Builder** with multiple professional templates

### Security Features
- 🔒 Rate limiting and abuse protection
- 🛡️ Input validation and sanitization
- 🔐 Secure password hashing (Argon2)
- 🚫 Account lockout after failed attempts
- 📝 Comprehensive security logging

## 📋 Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized deployment)
- OpenAI API key (for AI features)
- SMTP credentials (for email features)

## 🛠️ Installation

### Option 1: Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd intervyou
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**
```bash
python start.py
```

The application will be available at `https://localhost:8000`

### Option 2: Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **View logs**
```bash
docker-compose logs -f
```

3. **Stop the application**
```bash
docker-compose down
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Application
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./database.db

# OpenAI API
OPENAI_API_KEY=your-openai-api-key

# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# Security
RATE_LIMIT_ENABLED=true
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_MINUTES=15
```

### SSL Certificates

For HTTPS support, generate SSL certificates:

```bash
python -c "from cryptography import x509; from cryptography.hazmat.primitives import hashes, serialization; from cryptography.hazmat.primitives.asymmetric import rsa; from cryptography.x509.oid import NameOID; import datetime; key = rsa.generate_private_key(public_exponent=65537, key_size=2048); subject = issuer = x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'), x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'IntervYou'), x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')]); cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime.utcnow()).not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)).sign(key, hashes.SHA256()); open('cert.pem', 'wb').write(cert.public_bytes(serialization.Encoding.PEM)); open('key.pem', 'wb').write(key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()))"
```

## 📁 Project Structure

```
intervyou/
├── fastapi_app_cleaned.py    # Main application file
├── start.py                   # Application entry point
├── auth_routes.py             # Authentication routes
├── security_config.py         # Security configuration
├── rate_limiter.py            # Rate limiting middleware
├── abuse_protection_middleware.py  # Abuse protection
├── utils_security_helpers.py  # Security utilities
├── models/
│   └── practice_models.py     # Database models
├── services/                  # Business logic services
│   ├── advanced_feedback_engine.py
│   ├── aptitude_service.py
│   ├── video_interview_service.py
│   ├── resume_service.py
│   └── ...
├── online_ide/                # Online IDE functionality
│   ├── code_executor.py
│   ├── ide_routes.py
│   └── language_configs.py
├── templates/                 # HTML templates
│   ├── components/
│   │   ├── sidebar.html
│   │   └── topbar.html
│   ├── practice_new.html
│   ├── profile_new.html
│   ├── video_interview_new.html
│   └── ...
├── static/                    # Static assets
│   ├── design-system.css
│   ├── ide.js
│   └── ...
├── logs/                      # Application logs
├── uploads/                   # User uploads
├── database.db                # SQLite database
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This file
```

## 🎯 Usage

### For Users

1. **Register/Login**: Create an account or log in
2. **Practice**: Select a category and start practicing
3. **Video Interview**: Practice with AI-powered video analysis
4. **Code Challenges**: Solve coding problems in the online IDE
5. **Build Resume**: Create ATS-optimized resumes
6. **Track Progress**: View analytics and performance reports

### For Administrators

1. **Access Admin Panel**: Navigate to `/admin`
2. **Manage Users**: View and manage user accounts
3. **Monitor Platform**: Track usage statistics
4. **View Logs**: Check security and error logs

## 🔒 Security

- **Rate Limiting**: Prevents abuse and brute force attacks
- **Input Validation**: All user inputs are validated and sanitized
- **Secure Sessions**: Session-based authentication with secure cookies
- **Password Security**: Argon2 hashing with automatic migration
- **Account Lockout**: Automatic lockout after failed login attempts
- **HTTPS**: SSL/TLS encryption for all communications
- **Security Logging**: Comprehensive logging of security events

## 📊 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout
- `POST /forgot-password` - Password reset request

### Practice
- `GET /practice` - Practice page
- `POST /api/practice/submit` - Submit answer
- `GET /api/questions` - Get questions

### Video Interview
- `GET /video_interview` - Video interview page
- `POST /api/video/analyze` - Analyze video response

### IDE
- `GET /ide` - Online IDE page
- `POST /api/ide/execute` - Execute code

### Profile
- `GET /profile` - User profile
- `POST /api/update-profile` - Update profile

## 🐛 Troubleshooting

### Common Issues

**Issue**: Camera not working in Video Interview
- **Solution**: Ensure HTTPS is enabled and browser permissions are granted

**Issue**: IDE execution timeout
- **Solution**: Check Docker is running and images are pulled

**Issue**: Login fails repeatedly
- **Solution**: Check account lockout status, wait 15 minutes or reset password

**Issue**: OpenAI API errors
- **Solution**: Verify API key is valid and has sufficient credits

## 📝 Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## 🚀 Deployment

### Production Checklist

- [ ] Update `.env` with production values
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up SSL certificates
- [ ] Enable rate limiting
- [ ] Configure email service
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Test all features
- [ ] Review security settings

### Deployment Options

1. **Docker** (Recommended)
2. **Cloud Platforms** (AWS, Azure, GCP)
3. **Platform-as-a-Service** (Heroku, Render, Railway)
4. **VPS** (DigitalOcean, Linode, Vultr)

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For support, email support@intervyou.com or open an issue on GitHub.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- OpenAI for AI capabilities
- All contributors and users

---

**Made with ❤️ by the IntervYou Team**
