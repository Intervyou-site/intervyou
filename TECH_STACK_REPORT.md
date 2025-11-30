# IntervYou - Technology Stack Summary

## 🎯 Overview
AI-powered interview coaching platform with real-time feedback, video analysis, and personalized learning paths.

---

## 🖥️ Backend Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.115.0+ |
| **Server** | Uvicorn + Gunicorn | 0.30.0+ / 22.0.0+ |
| **Language** | Python | 3.9+ |
| **Architecture** | Async/Await, REST API | - |

---

## 🗄️ Database

| Component | Technology | Version |
|-----------|-----------|---------|
| **Database** | PostgreSQL | 15.15 |
| **ORM** | SQLAlchemy | 2.0.25+ |
| **Migrations** | Alembic | 1.13.1+ |
| **Connection** | localhost:5433 | - |

**Schema:**
- `user` (id, name, email, password, total_score, attempts, badge)
- `attempt` (id, user_id, question, score, feedback, timestamp)
- `saved_question` (id, user_id, question, company, timestamp)

---

## 🎨 Frontend Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Templates** | Jinja2 | 3.1.4+ |
| **CSS Framework** | Tailwind CSS | CDN |
| **JavaScript** | Alpine.js + Vanilla JS | CDN / ES6+ |
| **Pages** | 17 HTML templates | - |

**Features:** Dark mode, responsive design, audio/video recording, real-time feedback

---

## 🤖 AI & Machine Learning

| Component | Technology | Version |
|-----------|-----------|---------|
| **Primary LLM** | OpenAI GPT-4o-mini | Latest |
| **Embeddings** | text-embedding-3-small | Latest |
| **Local Models** | Hugging Face Transformers | 4.44.0+ |
| **NLP** | TextBlob, LanguageTool | 0.18.0+ / 2.8.0+ |
| **ML Framework** | PyTorch + scikit-learn | 2.4.0+ / 1.5.1+ |

**Capabilities:** Question generation, answer evaluation, sentiment analysis, grammar checking, semantic similarity

---

## 🎥 Media Processing

### Video
- **MoviePy** 1.0.3+ - Video editing
- **OpenCV** 4.8.0+ - Computer vision
- **MediaPipe** 0.10.0+ - Face detection
- **FER** 22.5.0+ - Emotion recognition
- **DeepFace** 0.0.79+ - Facial analysis

### Audio
- **Librosa** 0.10.2+ - Audio analysis
- **gTTS** 2.5.0+ - Text-to-speech
- **SpeechRecognition** 3.10.0+ - Transcription
- **SoundFile** 0.12.1+ - Audio I/O

---

## 🔐 Security & Authentication

| Component | Technology | Version |
|-----------|-----------|---------|
| **Password Hashing** | Argon2 + bcrypt | via Passlib 1.7.4+ |
| **OAuth** | Google OAuth 2.0 | via Authlib 1.3.0+ |
| **Sessions** | Starlette Middleware | Cookie-based |
| **Tokens** | JWT, itsdangerous | python-jose 3.3.0+ |

**Features:** OTP password reset, secure cookies, CSRF protection

---

## 📧 Communication

| Component | Technology | Version |
|-----------|-----------|---------|
| **Email Service** | fastapi-mail | 1.4.1+ |
| **SMTP Provider** | Gmail | smtp.gmail.com:587 |

---

## 🔌 External APIs

| Service | Purpose | Status |
|---------|---------|--------|
| **OpenAI API** | LLM & embeddings | ✅ Active |
| **Google OAuth** | Social login | ✅ Active |
| **Copyleaks** | Plagiarism detection | ⚠️ Optional |
| **SerpAPI** | Question research | ⚠️ Optional |

---

## 📦 Key Dependencies (40+ total)

**Core:** fastapi, uvicorn, gunicorn, sqlalchemy, alembic, psycopg2-binary  
**Security:** passlib, authlib, python-jose, itsdangerous  
**AI/ML:** transformers, torch, scikit-learn, sentence-transformers  
**Media:** moviepy, opencv-python, librosa, mediapipe, fer, deepface  
**NLP:** textblob, language-tool-python  
**Utils:** jinja2, pydantic, httpx, requests, reportlab

---

## 🏗️ Architecture

```
Frontend (Jinja2 + Alpine.js + Tailwind)
    ↓
FastAPI Application (Async/Await)
    ↓
Business Logic (AI, Media Processing, Auth)
    ↓
SQLAlchemy ORM
    ↓
PostgreSQL Database
```

**Design Patterns:** Dependency injection, repository pattern, service layer, caching

---

## ⚡ Performance Features

- ✅ Async/await for non-blocking I/O
- ✅ In-memory caching (question bank, tokens)
- ✅ Connection pooling (scoped sessions)
- ✅ Stateless cookie-based sessions
- ✅ Optimized LLM token limits

---

## 📊 Project Stats

- **API Endpoints:** 35+
- **Lines of Code:** 5,000+
- **Database Tables:** 3
- **Template Files:** 17
- **Features:** 15+ (auth, practice, mock interviews, video analysis, AI advisor, leaderboard, reports, etc.)

---

## 🚀 Deployment

**Development:** `python start.py` (localhost:8000)  
**Production:** Gunicorn + Uvicorn workers, PostgreSQL, HTTPS recommended  
**Config:** Environment variables via `.env` file

---

## ☁️ Cloud & Hosting

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Cloud Platforms** | AWS / Azure / GCP | Deployment options |
| **Containerization** | Docker | Application packaging |
| **Version Control** | GitHub | Code repository |

---

## 🛠️ Development Tools

| Tool | Purpose |
|------|---------|
| **GitHub** | Version control, collaboration |
| **Docker** | Containerization, deployment |
| **Figma** | UI/UX design |
| **Postman** | API testing |

---

## 🔮 Future Enhancements

**Short-term:** Unit tests, rate limiting, Redis caching  
**Medium-term:** Mobile app, real-time collaboration, advanced analytics  
**Long-term:** Self-hosted LLM, multi-language support, enterprise features

---

**Version:** 1.0.0 | **Status:** ✅ Production Ready | **Updated:** November 24, 2025
