# IntervYou - High-Level Architecture

## 🏗️ System Overview

**IntervYou** is an AI-powered interview coaching platform built with modern web technologies, featuring real-time feedback, personalized learning paths, and comprehensive performance tracking.

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  Browser (HTML/CSS/JS)                                          │
│  ├── Jinja2 Templates (SSR)                                     │
│  ├── Alpine.js (Reactive UI)                                    │
│  ├── Tailwind CSS (Styling)                                     │
│  └── Custom JS (Audio/Video handling)                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI Application (Python 3.9+)                              │
│  ├── Main App (fastapi_app.py)                                  │
│  ├── Auth Routes (auth_routes.py)                               │
│  ├── Session Middleware (Starlette)                             │
│  └── CORS & Security Headers                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       BUSINESS LOGIC                             │
├─────────────────────────────────────────────────────────────────┤
│  Core Services:                                                  │
│  ├── Authentication Service                                      │
│  │   ├── Email/Password (Argon2 + bcrypt)                       │
│  │   ├── OAuth 2.0 (Google)                                     │
│  │   └── OTP-based Password Reset                               │
│  ├── Interview Engine                                            │
│  │   ├── Question Generation (LLM)                              │
│  │   ├── Answer Evaluation (AI)                                 │
│  │   ├── Mock Interview Simulator                               │
│  │   └── Video Interview Processor                              │
│  ├── Performance Analytics                                       │
│  │   ├── Score Tracking                                         │
│  │   ├── Category Analysis                                      │
│  │   ├── Progress Reports                                       │
│  │   └── Leaderboard System                                     │
│  ├── AI Advisor                                                  │
│  │   ├── Learning Plan Generator                                │
│  │   ├── Weakness Identifier                                    │
│  │   └── Personalized Recommendations                           │
│  └── Content Management                                          │
│      ├── Question Bank (Dynamic + Static)                       │
│      ├── Saved Questions                                        │
│      └── User Uploads (Audio/Video)                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  SQLAlchemy ORM                                                  │
│  ├── User Model                                                  │
│  ├── Attempt Model                                               │
│  ├── SavedQuestion Model                                         │
│  └── Session Management (Scoped Sessions)                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       DATABASE LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL 15.15                                                │
│  ├── Host: localhost:5433                                        │
│  ├── Database: intervyou                                         │
│  └── Tables: user, attempt, saved_question                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     EXTERNAL SERVICES                            │
├─────────────────────────────────────────────────────────────────┤
│  ├── OpenAI API (GPT-4o-mini)                                   │
│  │   ├── Question Generation                                    │
│  │   ├── Answer Evaluation                                      │
│  │   └── Embeddings (text-embedding-3-small)                    │
│  ├── Google OAuth 2.0                                            │
│  │   └── Social Login                                           │
│  ├── SMTP Server (Gmail)                                         │
│  │   ├── OTP Emails                                             │
│  │   └── Welcome Emails                                         │
│  ├── Copyleaks API (Optional)                                    │
│  │   └── Plagiarism Detection                                   │
│  └── SerpAPI (Optional)                                          │
│      └── Question Research                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Technology Stack

### Backend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI 0.115+ | High-performance async web framework |
| **Server** | Uvicorn | ASGI server with hot reload |
| **ORM** | SQLAlchemy 2.0+ | Database abstraction layer |
| **Database** | PostgreSQL 15.15 | Production database |
| **Migrations** | Alembic 1.13+ | Database schema versioning |
| **Auth** | Authlib + Passlib | OAuth & password hashing |
| **Sessions** | Starlette Middleware | Secure cookie-based sessions |

### Frontend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Templates** | Jinja2 | Server-side rendering |
| **CSS Framework** | Tailwind CSS | Utility-first styling |
| **JS Framework** | Alpine.js | Reactive components |
| **Icons** | Custom CSS | UI elements |

### AI/ML
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | OpenAI GPT-4o-mini | Question generation & evaluation |
| **Embeddings** | text-embedding-3-small | Semantic search |
| **Vector Store** | FAISS | Similarity search |
| **NLP** | TextBlob, LanguageTool | Grammar & sentiment analysis |
| **Audio** | Librosa, gTTS | Voice analysis & synthesis |
| **Video** | MoviePy | Video processing |

### Infrastructure
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Environment** | python-dotenv | Configuration management |
| **Email** | SMTP (Gmail) | Transactional emails |
| **File Storage** | Local filesystem | Audio/video uploads |
| **Logging** | Python logging | Application monitoring |

---

## 📁 Project Structure

```
intervyou/
├── 🚀 Core Application
│   ├── fastapi_app.py          # Main application (2300+ lines)
│   ├── start.py                # Application launcher
│   └── wsgi.py                 # WSGI entry point
│
├── 🔐 Authentication & Security
│   ├── auth_routes.py          # OAuth & password reset routes
│   ├── oauth_config.py         # OAuth provider configuration
│   ├── email_service.py        # OTP & email service
│   └── utils_security_helpers.py # Password hashing & file uploads
│
├── 🤖 AI & Intelligence
│   ├── llm_utils.py            # OpenAI API integration
│   ├── vector_store.py         # FAISS vector storage
│   └── schemas.py              # Pydantic data models
│
├── 🗄️ Database
│   ├── alembic/                # Database migrations
│   ├── alembic.ini             # Alembic configuration
│   └── setup_intervyou_db.sql  # PostgreSQL setup script
│
├── 🎨 Frontend
│   ├── templates/              # Jinja2 HTML templates (17 files)
│   │   ├── index.html          # Dashboard
│   │   ├── practice.html       # Practice session
│   │   ├── mock_interview.html # Mock interview
│   │   ├── video_interview.html # Video practice
│   │   ├── report.html         # Performance report
│   │   ├── profile.html        # User profile
│   │   ├── advisor.html        # AI advisor
│   │   ├── leaderboard.html    # Rankings
│   │   ├── saved.html          # Saved questions
│   │   ├── login.html          # Authentication
│   │   └── ...
│   └── static/                 # CSS, JS, assets
│       ├── style.css           # Main styles
│       ├── theme.css           # Dark mode
│       ├── expanding-menu.css  # Navigation
│       ├── password-beam.css   # Password strength
│       └── audio/              # Audio files
│
├── 📦 Storage
│   ├── uploads/                # User uploads
│   └── backup/                 # Database backups
│
├── ⚙️ Configuration
│   ├── .env                    # Environment variables
│   ├── .env.example            # Template
│   ├── requirements.txt        # Python dependencies
│   └── README.md               # Documentation
│
└── 📚 Documentation
    ├── ARCHITECTURE.md         # This file
    ├── POSTGRES_MIGRATION_COMPLETE.md
    ├── SQLITE_CLEANUP_COMPLETE.md
    ├── CLEANUP_SUMMARY.md
    └── QUICK_START.md
```

---

## 🔄 Data Flow

### 1. User Authentication Flow
```
User → Login Page → FastAPI
                    ↓
              Verify Password (Argon2/bcrypt)
                    ↓
              Create Session → Set Cookie
                    ↓
              Redirect to Dashboard
```

### 2. OAuth Flow (Google)
```
User → Click "Login with Google"
       ↓
Google OAuth → Authorization
       ↓
Callback → Get User Info
       ↓
Create/Update User → Session
       ↓
Redirect to Dashboard
```

### 3. Practice Session Flow
```
User → Select Category
       ↓
Generate Questions (LLM) → Cache
       ↓
Display Question
       ↓
User Submits Answer
       ↓
Evaluate Answer (AI)
       ├── Grammar Check (LanguageTool)
       ├── Sentiment Analysis (TextBlob)
       ├── Keyword Matching
       └── LLM Feedback
       ↓
Store Attempt → Update Stats
       ↓
Show Feedback + Score
```

### 4. Mock Interview Flow
```
User → Start Mock Interview
       ↓
Generate 5 Questions (LLM)
       ↓
For each question:
  ├── Display Question
  ├── Record Answer (Audio/Text)
  ├── Evaluate Answer
  └── Store Score
       ↓
Calculate Total Score
       ↓
Generate Report
       ↓
Update Leaderboard
```

### 5. AI Advisor Flow
```
User → Visit Advisor
       ↓
Analyze Performance
  ├── Get All Attempts
  ├── Calculate Category Scores
  ├── Identify Weak Areas
  └── Determine Skill Level
       ↓
Generate Learning Plans (LLM)
  ├── Daily Practice
  ├── Improve Weak Areas
  ├── Advanced Prep
  └── Category Mastery
       ↓
Display Recommendations
```

---

## 🗃️ Database Schema

### User Table
```sql
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,  -- Argon2 hash
    total_score FLOAT DEFAULT 0.0,
    attempts INTEGER DEFAULT 0,
    badge VARCHAR(100) DEFAULT '🎯 Rising Learner'
);
```

### Attempt Table
```sql
CREATE TABLE attempt (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user(id),
    question VARCHAR(500),
    score FLOAT,
    feedback TEXT,  -- JSON string
    timestamp TIMESTAMP DEFAULT NOW()
);
```

### SavedQuestion Table
```sql
CREATE TABLE saved_question (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user(id),
    question VARCHAR(500) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## 🔌 API Endpoints

### Authentication (10 endpoints)
- `GET /login` - Login page
- `POST /login` - Login submission
- `GET /register` - Registration page
- `POST /register` - User registration
- `GET /logout` - Logout
- `GET /auth/google` - Google OAuth
- `GET /auth/google/callback` - OAuth callback
- `GET /forgot_password` - Password reset page
- `POST /forgot_password/request_otp` - Request OTP
- `POST /forgot_password/verify_otp` - Verify OTP & reset

### Practice & Interviews (8 endpoints)
- `GET /practice` - Practice session page
- `GET /mock_interview` - Mock interview page
- `GET /video_interview` - Video interview page
- `POST /generate_questions` - Generate AI questions
- `POST /set_category` - Select category
- `POST /evaluate_answer` - Submit answer
- `POST /chat` - Chat with AI
- `GET /get_mock_question` - Get next question

### User Dashboard (5 endpoints)
- `GET /` - Home dashboard
- `GET /report` - Performance report
- `GET /profile` - User profile
- `GET /leaderboard` - Rankings
- `GET /saved` - Saved questions

### AI Advisor (3 endpoints)
- `GET /advisor` - Advisor dashboard
- `GET /advisor/details/{plan_id}` - Plan details
- `GET /advisor/start/{plan_id}` - Start plan

### Content Management (4 endpoints)
- `POST /save_question` - Save question
- `DELETE /delete_saved/{id}` - Delete saved
- `POST /saved/delete/{id}` - Delete (POST)
- `GET /export_pdf` - Export report

### Media Processing (2 endpoints)
- `POST /voice` - Analyze voice
- `POST /upload_video` - Upload video

### Utilities (3 endpoints)
- `GET /health` - Health check
- `POST /plagiarism_check` - Check plagiarism
- `POST /copyleaks/submit_text_for_scan` - Copyleaks

**Total: 35+ API endpoints**

---

## 🔒 Security Features

### Authentication
- ✅ **Password Hashing**: Argon2 (preferred) + bcrypt (legacy fallback)
- ✅ **Session Management**: Secure cookie-based sessions
- ✅ **OAuth 2.0**: Google social login
- ✅ **OTP Verification**: Email-based password reset
- ✅ **HTTPS Only**: Session cookies (production)
- ✅ **SameSite**: CSRF protection

### Data Protection
- ✅ **SQL Injection**: SQLAlchemy ORM parameterization
- ✅ **XSS Protection**: Jinja2 auto-escaping
- ✅ **File Upload Limits**: 10MB max size
- ✅ **UUID Filenames**: Prevent path traversal
- ✅ **Environment Variables**: Sensitive config in .env

### API Security
- ✅ **Rate Limiting**: (Recommended for production)
- ✅ **CORS Configuration**: Allowed origins
- ✅ **Input Validation**: Pydantic schemas
- ✅ **Error Handling**: No sensitive data in errors

---

## 🚀 Performance Optimizations

### Caching
- ✅ **Question Bank**: In-memory cache (`app.state.question_bank`)
- ✅ **Generated Questions**: Cached by category
- ✅ **Copyleaks Tokens**: Token caching with expiry
- ✅ **Session Data**: Cookie-based (no DB lookups)

### Database
- ✅ **Connection Pooling**: SQLAlchemy scoped sessions
- ✅ **Indexes**: Primary keys, foreign keys
- ✅ **Lazy Loading**: Relationships loaded on demand
- ✅ **PostgreSQL**: Production-grade database

### AI/LLM
- ✅ **Model Selection**: gpt-4o-mini (fast & cost-effective)
- ✅ **Token Limits**: max_tokens=400-500
- ✅ **Async Requests**: Non-blocking API calls
- ✅ **Fallback Logic**: Local evaluation if API fails

### Frontend
- ✅ **Alpine.js**: Lightweight reactive framework
- ✅ **Tailwind CSS**: Utility-first, minimal CSS
- ✅ **Server-Side Rendering**: Fast initial load
- ✅ **Static Assets**: Cached by browser

---

## 📈 Scalability Considerations

### Current Architecture (Single Server)
- ✅ Suitable for: 100-1000 concurrent users
- ✅ Database: PostgreSQL (vertical scaling)
- ✅ File Storage: Local filesystem
- ✅ Sessions: Cookie-based (stateless)

### Future Scaling Options

#### Horizontal Scaling
- Add load balancer (Nginx/HAProxy)
- Multiple FastAPI instances
- Shared PostgreSQL database
- Redis for session storage
- S3/Cloud storage for uploads

#### Database Scaling
- Read replicas for analytics
- Connection pooling (PgBouncer)
- Partitioning by user_id
- Caching layer (Redis)

#### AI/LLM Optimization
- Batch question generation
- Response caching
- Self-hosted models (Llama, Mistral)
- Queue system for async processing

---

## 🔧 Configuration Management

### Environment Variables (.env)
```env
# Application
SECRET_KEY=<random-secret>
ENVIRONMENT=development|production

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# AI/LLM
OPENAI_API_KEY=sk-...
SERPAPI_KEY=<optional>
COPYLEAKS_API_KEY=<optional>

# Email
MAIL_USERNAME=email@gmail.com
MAIL_PASSWORD=app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

# OAuth
GOOGLE_CLIENT_ID=<client-id>
GOOGLE_CLIENT_SECRET=<secret>

# CORS
ALLOWED_ORIGINS=http://localhost:8000,https://domain.com

# OTP
OTP_LENGTH=6
OTP_EXPIRY_MINUTES=10
OTP_MAX_ATTEMPTS=3
```

---

## 🧪 Testing Strategy

### Manual Testing
- ✅ User registration & login
- ✅ OAuth flow
- ✅ Practice sessions
- ✅ Mock interviews
- ✅ Performance reports
- ✅ AI advisor

### Recommended Automated Tests
- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for critical flows
- Load testing for scalability

---

## 📊 Monitoring & Logging

### Current Logging
- ✅ Console output (uvicorn)
- ✅ Error tracking (Python logging)
- ✅ Email send status
- ✅ LLM API calls

### Production Recommendations
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Database query monitoring
- API rate limiting logs
- User analytics

---

## 🎯 Key Features Summary

| Feature | Status | Technology |
|---------|--------|-----------|
| User Authentication | ✅ | FastAPI + Argon2 |
| OAuth (Google) | ✅ | Authlib |
| Password Reset (OTP) | ✅ | SMTP + Email |
| Practice Sessions | ✅ | LLM + AI Evaluation |
| Mock Interviews | ✅ | Multi-question flow |
| Video Interviews | ✅ | MoviePy + Librosa |
| Performance Reports | ✅ | SQLAlchemy + Charts |
| AI Advisor | ✅ | LLM-generated plans |
| Leaderboard | ✅ | Score ranking |
| Saved Questions | ✅ | User bookmarks |
| Dark Mode | ✅ | CSS themes |
| PDF Export | ✅ | ReportLab |
| Voice Analysis | ✅ | Librosa + gTTS |
| Plagiarism Check | ✅ | Copyleaks API |
| Question Generation | ✅ | OpenAI GPT-4o-mini |

---

## 🚦 Deployment Checklist

### Pre-Production
- [ ] Set strong SECRET_KEY
- [ ] Configure PostgreSQL
- [ ] Set up HTTPS/SSL
- [ ] Configure production SMTP
- [ ] Set ENVIRONMENT=production
- [ ] Update ALLOWED_ORIGINS
- [ ] Enable https_only sessions
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Load test application

### Production
- [ ] Use Gunicorn + Uvicorn workers
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure firewall
- [ ] Set up monitoring
- [ ] Enable rate limiting
- [ ] Configure CDN for static assets
- [ ] Set up error tracking
- [ ] Document runbook

---

## 📝 Architecture Decisions

### Why FastAPI?
- High performance (async/await)
- Automatic API documentation
- Type hints & validation
- Modern Python features
- Easy to scale

### Why PostgreSQL?
- ACID compliance
- Robust for production
- Excellent performance
- Rich feature set
- Strong community

### Why OpenAI?
- State-of-the-art LLMs
- Reliable API
- Cost-effective (gpt-4o-mini)
- Good documentation
- Fast response times

### Why Server-Side Rendering?
- Fast initial load
- SEO friendly
- Simple architecture
- No complex build process
- Progressive enhancement

---

## 🔮 Future Enhancements

### Short Term
- [ ] Add unit tests
- [ ] Implement rate limiting
- [ ] Add Redis caching
- [ ] Improve error handling
- [ ] Add API documentation (Swagger)

### Medium Term
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] Custom question banks
- [ ] Team/organization features

### Long Term
- [ ] Self-hosted LLM option
- [ ] Multi-language support
- [ ] Video interview AI analysis
- [ ] Integration with job boards
- [ ] Enterprise features

---

## 📞 Support & Maintenance

### Regular Maintenance
- Database backups (daily)
- Log rotation
- Dependency updates
- Security patches
- Performance monitoring

### Troubleshooting
- Check logs: `tail -f logs/app.log`
- Database status: `psql -U intervyou_user -d intervyou`
- Health check: `curl http://localhost:8000/health`
- Restart: `systemctl restart intervyou`

---

**Last Updated**: November 23, 2025
**Version**: 1.0.0
**Status**: ✅ Production Ready
