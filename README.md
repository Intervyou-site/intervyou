# IntervYou - AI-Powered Interview Intelligence Platform

An intelligent interview preparation platform powered by AI, featuring real-time feedback, video analysis, and personalized coaching.

## Features

- **AI-Powered Feedback**: Get instant, detailed feedback on your interview answers
- **Video Interview Practice**: Practice with AI analysis of body language and speech patterns
- **Resume Builder**: Create ATS-optimized resumes with AI suggestions
- **Performance Analytics**: Track your progress with detailed metrics
- **Question Bank**: Access thousands of interview questions across categories
- **Bookmarking System**: Save and revisit questions for focused practice
- **Leaderboard**: Compete with other users and track your ranking

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript (Alpine.js)
- **Database**: SQLite (development), PostgreSQL (production)
- **AI/ML**: OpenAI GPT, Azure Speech Services
- **Deployment**: Docker, Docker Compose

## Quick Start

### Local Development

1. Clone the repository
```bash
git clone <repository-url>
cd intervyou
```

2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the application
```bash
python start.py
```

Visit `http://localhost:8000`

### Docker Deployment

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed Docker instructions.

Quick start:
```bash
# Build and run
docker-compose up -d

# Or use the management script
./manage-docker.ps1 build
./manage-docker.ps1 start
```

## Project Structure

```
intervyou/
├── services/           # Business logic services
├── templates/          # HTML templates
│   ├── components/     # Reusable UI components
│   └── *_new.html      # New UI templates
├── static/             # CSS, JS, images
├── src/                # ML pipelines and utilities
├── online_ide/         # Code editor functionality
├── tests/              # Test files
├── config/             # Configuration files
└── entrypoint/         # ML training/inference entry points
```

## Environment Variables

Required environment variables:

- `OPENAI_API_KEY`: OpenAI API key for AI features
- `AZURE_SPEECH_KEY`: Azure Speech Services key
- `AZURE_SPEECH_REGION`: Azure region
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection string (optional)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

All rights reserved © 2025 IntervYou

## Support

For issues and questions, please open an issue on GitHub.
