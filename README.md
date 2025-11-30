# IntervYou - AI Interview Coach

An AI-powered interview preparation platform built with FastAPI, featuring mock interviews, practice sessions, performance tracking, and video analysis.

## Features

- 🎯 **Practice Sessions** - Category-based interview practice with AI feedback
- 🎤 **Mock Interviews** - Full interview simulations with scoring
- 📹 **Video Interviews** - Practice with video recording and AI analysis
- 📊 **Performance Reports** - Track your progress with detailed analytics
- 🧭 **AI Advisor** - Personalized learning plans based on your performance
- 🏆 **Leaderboard** - Compete with other users
- 👤 **User Profiles** - Track your stats, badges, and category breakdown
- ⭐ **Saved Questions** - Bookmark questions for later review
- 🌓 **Dark Mode** - Full dark mode support
- 🔐 **Authentication** - Google OAuth and email/password login

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Jinja2 Templates, Alpine.js, Tailwind CSS
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **AI/LLM**: OpenAI GPT-4 / Hugging Face Transformers
- **Video Analysis**: OpenCV, MediaPipe, librosa, TextBlob
- **Authentication**: OAuth 2.0 (Google), JWT sessions
- **Email**: SMTP with OTP verification

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required environment variables:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5433/intervyou
OPENAI_API_KEY=your-openai-key  # Optional
```

### 3. Setup Database

```bash
python -c "from fastapi_app import init_db; init_db()"
```

### 4. Run the Application

```bash
python start.py
```

Visit `http://localhost:8000`

## Video Interview Analysis

The video interview feature includes:

- **Validation**: Checks video duration, face detection, and audio presence
- **Scoring**: Confidence, professionalism, and engagement scores (0-10)
- **AI Analysis**: Sentiment, emotion, and text quality analysis
- **Feedback**: Actionable recommendations for improvement

## Project Structure

```
intervyou/
├── fastapi_app.py              # Main application
├── video_analysis.py           # Video evaluation
├── free_ai_models.py           # AI text analysis
├── realtime_analysis.py        # Real-time feedback
├── question_generator.py       # Question generation
├── auth_routes.py              # Authentication
├── templates/                  # HTML templates
├── static/                     # CSS, JS, images
└── requirements.txt            # Dependencies
```

## API Endpoints

### Video Interview
- `POST /api/video_interview` - Upload and analyze video
- `GET /api/video_analysis/status` - Check available features

### Practice & Mock
- `POST /api/practice` - Submit practice answer
- `POST /api/mock_interview` - Start mock interview
- `GET /api/performance` - Get performance stats

### User Management
- `POST /api/register` - Register user
- `POST /api/login` - Login user
- `GET /api/profile` - Get user profile

## License

MIT License

## Acknowledgments

- OpenAI for GPT models
- Hugging Face for transformers
- FastAPI framework
- MediaPipe for face detection
