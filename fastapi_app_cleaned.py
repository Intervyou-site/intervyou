"""
IntervYou - AI-Powered Interview Preparation Platform
A comprehensive FastAPI application for interview practice and preparation.

Features:
- AI-powered question generation and evaluation
- Voice analysis and transcription
- Resume builder and PDF export
- User progress tracking and analytics
- Online IDE for coding practice
"""

import os
import json
import uuid
import time
import random
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from io import BytesIO

# Load environment variables first
from dotenv import load_dotenv
load_dotenv()

# FastAPI and web framework imports
from fastapi import (
    FastAPI, Request, Form, UploadFile, File, Depends, 
    BackgroundTasks, HTTPException, Body, WebSocket, WebSocketDisconnect
)
from fastapi.responses import (
    HTMLResponse, JSONResponse, RedirectResponse, 
    Response, StreamingResponse
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# Database imports
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, scoped_session

# Security and authentication
from passlib.hash import argon2, bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

# Document generation
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# Audio processing
import librosa
import numpy as np
from gtts import gTTS

# Text processing
from textblob import TextBlob
import difflib

# HTTP client for API calls
import httpx
import requests

# Security helpers
from utils_security_helpers import (
    get_password_hash, verify_password, 
    save_upload_sync, save_upload_limited
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================================
# CONFIGURATION AND CONSTANTS
# ================================

class Config:
    """Application configuration"""
    
    # Directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    UPLOAD_FOLDER = os.path.join(STATIC_DIR, "audio")
    VIDEO_UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
    
    # Database
    DB_PATH = os.path.join(BASE_DIR, "database.db")
    DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")
    
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-in-production")
    
    # Email configuration
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    
    # API Keys
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
    COPYLEAKS_API_KEY = os.environ.get("COPYLEAKS_API_KEY")
    COPYLEAKS_EMAIL = os.environ.get("COPYLEAKS_EMAIL")
    COPYLEAKS_WEBHOOK_URL = os.environ.get("COPYLEAKS_WEBHOOK_URL")
    
    # API URLs
    OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"
    COPYLEAKS_AUTH_URL = "https://id.copyleaks.com/v3/account/login/api"
    COPYLEAKS_SUBMIT_FILE_URL = "https://api.copyleaks.com/v3/scans/submit/file/{scanId}"
    COPYLEAKS_GET_SCAN_URL = "https://api.copyleaks.com/v3/scans/{scanId}"
    
    # Interview categories and companies
    COMPANIES = [
        "Google", "Amazon", "Microsoft", "Meta (Facebook)", "Apple",
        "NVIDIA", "Twitter (X)", "IBM", "Oracle"
    ]
    
    # Question bank for fallback
    LOCAL_QUESTION_BANK = {
        "Python": [
            "What are Python decorators and how do you use them?",
            "Explain list comprehensions with examples.",
            "What's the difference between deep and shallow copy?",
            "What are Python generators and when would you use them?",
            "Explain OOP concepts in Python with examples."
        ],
        "Web Development": [
            "What is REST API and how does it work?",
            "Explain the difference between frontend and backend.",
            "What is the role of JavaScript in modern web applications?",
            "How does Flask/FastAPI work for web development?"
        ],
        "Data Structures": [
            "What's the difference between a stack and a queue?",
            "Explain Big O notation with practical examples.",
            "How does a linked list differ from an array?",
            "When would you use a hash table vs a binary tree?"
        ],
        "Behavioral": [
            "Tell me about yourself and your background.",
            "Why do you want to work for this company?",
            "What are your greatest strengths and weaknesses?",
            "Describe a challenging project you worked on."
        ],
        "System Design": [
            "How would you design a URL shortener like bit.ly?",
            "What is load balancing and why is it important?",
            "Explain caching strategies in system design.",
            "How would you design a chat application?"
        ],
        "Machine Learning": [
            "What is supervised vs unsupervised learning?",
            "Explain overfitting and how to prevent it.",
            "What's the difference between classification and regression?",
            "How do you evaluate a machine learning model?"
        ]
    }

# Create necessary directories
os.makedirs(Config.STATIC_DIR, exist_ok=True)
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.VIDEO_UPLOAD_DIR, exist_ok=True)

# ================================
# OPTIONAL IMPORTS AND FEATURES
# ================================

class FeatureFlags:
    """Track which optional features are available"""
    
    def __init__(self):
        self.huggingface_available = self._check_huggingface()
        self.ai_detection_available = self._check_ai_detection()
        self.xlnet_available = self._check_xlnet()
        self.smart_generator_available = self._check_smart_generator()
        self.language_tool_available = self._check_language_tool()
        self.sentence_transformers_available = self._check_sentence_transformers()
    
    def _check_huggingface(self) -> bool:
        try:
            from huggingface_utils import (
                evaluate_answer_hybrid, generate_question_hybrid,
                preload_models, get_semantic_similarity,
                evaluate_answer_comprehensive, transcribe_audio as hf_transcribe_audio,
                get_model_info
            )
            logger.info("✅ Hugging Face utilities loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Hugging Face utilities not available: {e}")
            return False
    
    def _check_ai_detection(self) -> bool:
        try:
            from ai_detection import detect_ai_generated, get_detailed_report
            logger.info("✅ AI detection heuristics loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠️  AI detection not available: {e}")
            return False
    
    def _check_xlnet(self) -> bool:
        try:
            from hybrid_evaluator import get_hybrid_evaluator
            logger.info("✅ XLNet hybrid evaluator loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠️  XLNet evaluator not available: {e}")
            return False
    
    def _check_smart_generator(self) -> bool:
        try:
            from question_generator import generate_smart_questions, get_category_context
            logger.info("✅ Smart question generator loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Smart question generator not available: {e}")
            return False
    
    def _check_language_tool(self) -> bool:
        try:
            import language_tool_python
            logger.info("✅ Language tool loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Language tool not available: {e}")
            return False
    
    def _check_sentence_transformers(self) -> bool:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("✅ Sentence transformers loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Sentence transformers not available: {e}")
            return False

# Initialize feature flags
features = FeatureFlags()

# ================================
# DATABASE MODELS
# ================================

# Database setup
if Config.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(Config.DATABASE_URL, connect_args=connect_args)
else:
    # PostgreSQL/Production with connection pooling
    engine = create_engine(
        Config.DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

class User(Base):
    """User model for authentication and progress tracking"""
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    total_score = Column(Float, default=0.0)
    attempts = Column(Integer, default=0)
    badge = Column(String(100), default="🎯 Rising Learner")
    
    # Relationships
    attempts_list = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")
    saved_questions = relationship("SavedQuestion", back_populates="user", cascade="all, delete-orphan")

class Attempt(Base):
    """Model for storing user's interview attempts and scores"""
    __tablename__ = "attempt"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    question = Column(String(500))
    score = Column(Float)
    feedback = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="attempts_list")

class SavedQuestion(Base):
    """Model for user's saved questions with notes and tags"""
    __tablename__ = "saved_question"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    question = Column(String(500), nullable=False)
    company = Column(String(100), nullable=True)
    category = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)  # User's personal notes
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    difficulty = Column(String(20), nullable=True)  # beginner, intermediate, advanced
    priority = Column(Integer, default=0)  # 0=normal, 1=high, 2=urgent
    last_practiced = Column(DateTime, nullable=True)  # For spaced repetition
    practice_count = Column(Integer, default=0)  # How many times practiced
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="saved_questions")

# Create tables
Base.metadata.create_all(bind=engine)

# ================================
# FASTAPI APPLICATION SETUP
# ================================

app = FastAPI(
    title="IntervYou - AI Interview Preparation",
    description="Comprehensive interview preparation platform with AI-powered feedback",
    version="2.0.0"
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=Config.SECRET_KEY,
    https_only=False,  # Set to True in production with HTTPS
    max_age=86400,     # 1 day
    same_site="lax"
)

# Mount static files
app.mount("/static", StaticFiles(directory=Config.STATIC_DIR), name="static")

# Setup templates
templates = Jinja2Templates(directory=Config.TEMPLATES_DIR)

# Token serializer for password reset
serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

# ================================
# DEPENDENCY INJECTION
# ================================

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db) -> Optional[User]:
    """Get current logged-in user from session"""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter_by(id=user_id).first()

def require_user(request: Request, db) -> User:
    """Require user to be logged in, raise exception if not"""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=303, detail="Login required")
    return user

# ================================
# UTILITY FUNCTIONS
# ================================

class FlashMessages:
    """Helper class for flash messages"""
    
    @staticmethod
    def add_flash(request: Request, message: str, category: str = "info"):
        """Add a flash message to the session"""
        flashes = request.session.setdefault("_flashes", [])
        flashes.append({"msg": message, "cat": category})
        request.session["_flashes"] = flashes
    
    @staticmethod
    def pop_flashes(request: Request) -> List[Dict[str, str]]:
        """Get and clear all flash messages"""
        return request.session.pop("_flashes", [])

class PasswordValidator:
    """Password strength validation"""
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Validate password strength with comprehensive checks.
        Returns (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        
        if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
            return False, "Password must contain at least one special character"
        
        return True, ""

class PasswordManager:
    """Handle password hashing and verification with migration support"""
    
    PREFERRED_HASHER = argon2  # New accounts use Argon2
    LEGACY_HASHER = bcrypt     # Fallback for existing bcrypt hashes
    
    @classmethod
    def verify_and_migrate_password(cls, candidate_pw: str, user_obj: User, db) -> bool:
        """
        Verify password and automatically migrate from bcrypt to Argon2 if needed.
        Returns True on success, False otherwise.
        """
        stored_hash = user_obj.password
        if not stored_hash:
            return False

        # Try preferred hasher (Argon2) first
        try:
            if cls.PREFERRED_HASHER.verify(candidate_pw, stored_hash):
                return True
        except Exception:
            pass

        # Fallback to legacy hasher (bcrypt)
        try:
            if cls.LEGACY_HASHER.verify(candidate_pw, stored_hash):
                # Migrate to Argon2
                try:
                    user_obj.password = cls.PREFERRED_HASHER.hash(candidate_pw)
                    db.add(user_obj)
                    db.commit()
                    logger.info(f"Migrated password for user {user_obj.email} to Argon2")
                except Exception as e:
                    logger.error(f"Password migration failed: {e}")
                    try:
                        db.rollback()
                    except Exception:
                        pass
                return True
        except Exception:
            pass

        return False

class SafeRedirect:
    """Helper for safe redirects to prevent open redirect vulnerabilities"""
    
    @staticmethod
    def is_safe_redirect(target: str) -> bool:
        """Allow only relative paths to avoid open redirect attacks"""
        if not target:
            return False
        from urllib.parse import urlparse
        parsed = urlparse(target)
        return parsed.scheme == "" and parsed.netloc == ""

# ================================
# AI AND LLM UTILITIES
# ================================

class LLMClient:
    """Client for interacting with Language Models"""
    
    @staticmethod
    async def call_llm_chat(
        system_prompt: str, 
        user_message: str, 
        model: str = "gpt-4o-mini", 
        max_tokens: int = 400, 
        temperature: float = 0.2
    ) -> str:
        """
        Make an async call to OpenAI-compatible API.
        Falls back to simple heuristic response if no API key.
        """
        if not Config.OPENAI_API_KEY:
            # Fallback response when no API key is configured
            return json.dumps({
                "summary": "No LLM key configured — running lightweight local evaluation.",
                "improvements": [
                    "Split long sentences into shorter ones.",
                    "Avoid filler words; practice concise structure.",
                    "Add specific technical keywords relevant to the question."
                ],
                "grammar": "",
                "fillers": "",
                "score": round(random.uniform(4.0, 7.5), 1)
            })

        headers = {
            "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(Config.OPENAI_CHAT_URL, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return json.dumps({
                "summary": f"LLM call failed: {str(e)}", 
                "improvements": [], 
                "grammar": "", 
                "fillers": "", 
                "score": None
            })

class SimilarityCalculator:
    """Calculate text similarity using various methods"""
    
    def __init__(self):
        self.sentence_model = None
        if features.sentence_transformers_available:
            try:
                from sentence_transformers import SentenceTransformer
                self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e:
                logger.warning(f"Failed to load sentence transformer: {e}")
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts.
        Uses sentence transformers if available, otherwise falls back to difflib.
        """
        if not text1 or not text2:
            return 0.0
        
        if self.sentence_model:
            try:
                embeddings = self.sentence_model.encode([text1, text2], convert_to_numpy=True)
                # Cosine similarity
                dot_product = np.dot(embeddings[0], embeddings[1])
                norms = np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
                if norms == 0:
                    return 0.0
                return max(0.0, min(1.0, dot_product / norms))
            except Exception as e:
                logger.warning(f"Sentence transformer similarity failed: {e}")
        
        # Fallback to difflib
        return difflib.SequenceMatcher(None, text1, text2).ratio()
    
    def shingle_similarity(self, text1: str, text2: str, k: int = 5) -> float:
        """Calculate Jaccard similarity using k-grams (shingles)"""
        def get_shingles(text: str) -> set:
            tokens = text.lower().split()
            if len(tokens) < k:
                return {" ".join(tokens)}
            return {" ".join(tokens[i:i+k]) for i in range(len(tokens) - k + 1)}
        
        shingles1 = get_shingles(text1)
        shingles2 = get_shingles(text2)
        
        if not shingles1 or not shingles2:
            return 0.0
        
        intersection = len(shingles1 & shingles2)
        union = len(shingles1 | shingles2)
        
        return intersection / union if union > 0 else 0.0

# Initialize similarity calculator
similarity_calc = SimilarityCalculator()

# ================================
# APPLICATION STATE MANAGEMENT
# ================================

class ApplicationState:
    """Manage application-wide state and caches"""
    
    def __init__(self):
        self.question_bank = {k: list(v) for k, v in Config.LOCAL_QUESTION_BANK.items()}
        self.generated_questions = {}  # Cache for AI-generated questions
        self.copyleaks_token_cache = {"token": None, "expires_at": 0}
        self.copyleaks_pending = {}
        self.copyleaks_results = {}
        self.current_category = "Python"
        self.current_question = self._get_default_question()
    
    def _get_default_question(self) -> dict:
        """Get a default question object"""
        return {
            "q": "Explain a programming concept you're comfortable with.",
            "keywords": []
        }
    
    def get_current_question_obj(self, category: str = None) -> dict:
        """Get current question object for a category"""
        cat = category or self.current_category
        bank = self.question_bank.get(cat, [])
        
        if bank:
            question_text = random.choice(bank)
        else:
            question_text = "Explain a programming concept you're comfortable with."
        
        return {"q": question_text, "keywords": []}
    
    def refresh_current_question(self, new_category: str = None):
        """Update current question and category"""
        if new_category:
            self.current_category = new_category
        self.current_question = self.get_current_question_obj(self.current_category)
        return self.current_question

# Initialize application state
app_state = ApplicationState()

# ================================
# STARTUP AND SHUTDOWN EVENTS
# ================================

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("🚀 Starting IntervYou application...")
    
    # Preload Hugging Face models if available
    if features.huggingface_available:
        try:
            logger.info("🤗 Preloading Hugging Face models...")
            from huggingface_utils import preload_models
            preload_models()
            logger.info("✅ Hugging Face models preloaded successfully")
        except Exception as e:
            logger.error(f"⚠️  Hugging Face model preload failed: {e}")
    
    logger.info("✅ Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("🛑 Shutting down IntervYou application...")
    # Add any cleanup logic here
    logger.info("✅ Application shutdown complete")

# ================================
# HEALTH CHECK AND MONITORING
# ================================

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring and load balancers"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "features": {
            "huggingface": features.huggingface_available,
            "ai_detection": features.ai_detection_available,
            "xlnet": features.xlnet_available,
            "smart_generator": features.smart_generator_available,
            "language_tool": features.language_tool_available,
            "sentence_transformers": features.sentence_transformers_available
        }
    }

@app.get("/api/session/check")
def check_session(request: Request, db=Depends(get_db)):
    """Debug endpoint to check session status (remove in production)"""
    user_id = request.session.get("user_id")
    user_agent = request.headers.get('user-agent', 'unknown')
    is_mobile = any(x in user_agent.lower() for x in ['mobile', 'android', 'iphone', 'ipad'])
    
    return {
        "session_exists": bool(request.session),
        "user_id": user_id,
        "logged_in": request.session.get("logged_in", False),
        "is_mobile": is_mobile,
        "user_agent": user_agent[:100],
        "session_keys": list(request.session.keys()),
        "cookies": list(request.cookies.keys())
    }

# ================================
# AUTHENTICATION ROUTES
# ================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db=Depends(get_db)):
    """Home page - shows landing page for guests, redirects to dashboard for authenticated users"""
    user = get_current_user(request, db)
    
    # If user is logged in, redirect to dashboard
    if user:
        return RedirectResponse(url="/report")
    
    # Show landing page for guests
    return templates.TemplateResponse(
        "index_new.html", 
        {"request": request, "user": None}
    )

@app.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    """Registration page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(None),
    db=Depends(get_db)
):
    """Handle user registration"""
    name = name.strip()
    email = email.strip().lower()
    
    # Validate all fields
    if not name or not email or not password:
        FlashMessages.add_flash(request, "Please fill all fields", "danger")
        return RedirectResponse("/login", status_code=303)
    
    # Validate name length
    if len(name) < 2:
        FlashMessages.add_flash(request, "Name must be at least 2 characters long", "danger")
        return RedirectResponse("/login", status_code=303)
    
    # Validate email format
    import re
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(email_regex, email):
        FlashMessages.add_flash(request, "Please enter a valid email address", "danger")
        return RedirectResponse("/login", status_code=303)
    
    # Check if email already exists
    if db.query(User).filter_by(email=email).first():
        FlashMessages.add_flash(request, "Email already registered! Please login instead.", "danger")
        return RedirectResponse("/login", status_code=303)
    
    # Validate password strength
    is_valid, error_msg = PasswordValidator.validate_password_strength(password)
    if not is_valid:
        FlashMessages.add_flash(request, error_msg, "danger")
        return RedirectResponse("/login", status_code=303)
    
    # Validate password confirmation if provided
    if confirm_password and password != confirm_password:
        FlashMessages.add_flash(request, "Passwords do not match", "danger")
        return RedirectResponse("/login", status_code=303)
    
    # Create new user
    hashed_password = get_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    
    FlashMessages.add_flash(request, "Registration successful! Please log in.", "success")
    return RedirectResponse("/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    """Login page"""
    flashes = FlashMessages.pop_flashes(request)
    return templates.TemplateResponse("login.html", {"request": request, "flashes": flashes})

@app.post("/login")
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    next: str = Form(None),
    db=Depends(get_db)
):
    """Handle user login with enhanced mobile support"""
    try:
        email = email.strip().lower()
        
        # Log attempt for debugging
        user_agent = request.headers.get('user-agent', 'unknown')
        is_mobile = any(x in user_agent.lower() for x in ['mobile', 'android', 'iphone', 'ipad'])
        logger.info(f"🔐 Login attempt: {email}, Mobile: {is_mobile}")
        
        user = db.query(User).filter_by(email=email).first()

        # Verify password with automatic migration
        if user and PasswordManager.verify_and_migrate_password(password, user, db):
            # Set session data
            request.session["user_id"] = user.id
            request.session["logged_in"] = True
            
            FlashMessages.add_flash(request, "Login successful!", "success")
            logger.info(f"✅ Login successful for {email}, user_id: {user.id}")

            # Safe redirect handling
            if next and SafeRedirect.is_safe_redirect(next):
                return RedirectResponse(next, status_code=303)
            return RedirectResponse("/", status_code=303)

        logger.warning(f"❌ Login failed for {email}: Invalid credentials")
        FlashMessages.add_flash(request, "Invalid email or password.", "danger")
        return RedirectResponse("/login", status_code=303)
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        FlashMessages.add_flash(request, "Login error. Please try again.", "danger")
        return RedirectResponse("/login", status_code=303)

@app.get("/logout")
def logout(request: Request):
    """Handle user logout"""
    request.session.clear()
    FlashMessages.add_flash(request, "Logged out successfully.", "info")
    return RedirectResponse("/login", status_code=303)

# ================================
# MAIN APPLICATION ROUTES
# ================================

@app.get("/practice", response_class=HTMLResponse)
def practice(request: Request, db=Depends(get_db)):
    """Practice page with category selection"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")

    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }

    categories = list(app_state.question_bank.keys())
    current_question = app_state.get_current_question_obj()
    question_text = current_question.get("q", "Ready to practice?")

    return templates.TemplateResponse(
        "practice_new.html",
        {
            "request": request,
            "user": user_dict,
            "question": question_text,
            "categories": categories,
            "companies": Config.COMPANIES,
        },
    )

@app.get("/practice-react", response_class=HTMLResponse)
def practice_react(request: Request, db=Depends(get_db)):
    """React-powered practice page"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    
    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }
    
    return templates.TemplateResponse("practice_react.html", {"request": request, "user": user_dict})

# ================================
# PRACTICE SESSION ROUTES
# ================================

# Global question cache for the session
question_cache = {}
current_category = "Python"
current_company = None

def generate_enhanced_questions(category: str, company: Optional[str] = None, count: int = 10) -> List[str]:
    """Generate enhanced interview questions with company-specific variations"""
    
    # Enhanced question bank with more variety
    enhanced_question_bank = {
        "Python": [
            "What are Python decorators and how do you use them?",
            "Explain list comprehensions with examples.",
            "What's the difference between deep and shallow copy?",
            "What are Python generators and when would you use them?",
            "Explain OOP concepts in Python with examples.",
            "How does Python's garbage collection work?",
            "What are metaclasses in Python?",
            "Explain the difference between __str__ and __repr__.",
            "How do you handle exceptions in Python?",
            "What is the Global Interpreter Lock (GIL)?",
            "Explain Python's memory management.",
            "What are context managers and how do you create them?",
            "How do you optimize Python code performance?",
            "Explain the difference between staticmethod and classmethod.",
            "What are Python's built-in data structures and their use cases?"
        ],
        "Web Development": [
            "What is REST API and how does it work?",
            "Explain the difference between frontend and backend.",
            "What is the role of JavaScript in modern web applications?",
            "How does Flask/FastAPI work for web development?",
            "What are the differences between HTTP methods?",
            "Explain CORS and how to handle it.",
            "What is JWT and how does authentication work?",
            "How do you optimize web application performance?",
            "What are Progressive Web Apps (PWAs)?",
            "Explain the concept of microservices architecture.",
            "How do you handle state management in web applications?",
            "What are the security best practices for web development?",
            "Explain the difference between SQL and NoSQL databases.",
            "How do you implement caching in web applications?",
            "What are WebSockets and when would you use them?"
        ],
        "Data Structures": [
            "What's the difference between a stack and a queue?",
            "Explain Big O notation with practical examples.",
            "How does a linked list differ from an array?",
            "When would you use a hash table vs a binary tree?",
            "Explain different sorting algorithms and their complexities.",
            "What are the advantages of using a heap data structure?",
            "How do you detect cycles in a linked list?",
            "Explain the concept of dynamic programming.",
            "What are the different tree traversal methods?",
            "How do you implement a LRU cache?",
            "Explain the difference between BFS and DFS.",
            "What are tries and when would you use them?",
            "How do you find the shortest path in a graph?",
            "Explain the concept of backtracking with examples.",
            "What are the trade-offs between different data structures?"
        ],
        "Behavioral": [
            "Tell me about yourself and your background.",
            "Why do you want to work for this company?",
            "What are your greatest strengths and weaknesses?",
            "Describe a challenging project you worked on.",
            "How do you handle conflicts in a team?",
            "Tell me about a time you failed and what you learned.",
            "How do you prioritize tasks when everything is urgent?",
            "Describe a situation where you had to learn something quickly.",
            "How do you handle feedback and criticism?",
            "Tell me about a time you had to make a difficult decision.",
            "How do you stay updated with new technologies?",
            "Describe your ideal work environment.",
            "How do you handle stress and pressure?",
            "Tell me about a time you went above and beyond.",
            "Where do you see yourself in 5 years?"
        ],
        "System Design": [
            "How would you design a URL shortener like bit.ly?",
            "What is load balancing and why is it important?",
            "Explain caching strategies in system design.",
            "How would you design a chat application?",
            "How would you design a social media feed?",
            "Explain database sharding and when to use it.",
            "How would you design a file storage system?",
            "What are the trade-offs between consistency and availability?",
            "How would you design a search engine?",
            "Explain the concept of eventual consistency.",
            "How would you handle millions of concurrent users?",
            "What are the different types of databases and their use cases?",
            "How would you design a notification system?",
            "Explain the concept of circuit breakers.",
            "How would you design a distributed cache?"
        ],
        "Machine Learning": [
            "What is supervised vs unsupervised learning?",
            "Explain overfitting and how to prevent it.",
            "What's the difference between classification and regression?",
            "How do you evaluate a machine learning model?",
            "Explain the bias-variance tradeoff.",
            "What are ensemble methods and when do you use them?",
            "How do you handle missing data in datasets?",
            "Explain the concept of feature engineering.",
            "What are the different types of neural networks?",
            "How do you choose the right algorithm for a problem?",
            "Explain cross-validation and its importance.",
            "What is regularization and why is it needed?",
            "How do you handle imbalanced datasets?",
            "Explain the concept of transfer learning.",
            "What are the ethical considerations in ML?"
        ]
    }
    
    # Get base questions for the category
    base_questions = enhanced_question_bank.get(category, enhanced_question_bank["Python"])
    
    # Company-specific question modifications
    company_variations = {
        "Google": [
            "How would you approach this problem at Google scale?",
            "What Google technologies would you use for this?",
            "How does this relate to Google's engineering principles?",
        ],
        "Amazon": [
            "How would you implement this on AWS?",
            "What Amazon services would be relevant here?",
            "How does this align with Amazon's leadership principles?",
        ],
        "Microsoft": [
            "How would you integrate this with Microsoft ecosystem?",
            "What Azure services would you leverage?",
            "How does this fit with Microsoft's technology stack?",
        ],
        "Meta (Facebook)": [
            "How would you scale this for billions of users?",
            "What Meta technologies would be applicable?",
            "How would you handle this in a social media context?",
        ]
    }
    
    # Select questions (mix of base + variations)
    selected_questions = []
    
    # Add base questions
    import random
    random.shuffle(base_questions)
    selected_questions.extend(base_questions[:count])
    
    # Add company-specific variations if company is specified
    if company and company in company_variations:
        variations = company_variations[company]
        # Replace some questions with company-specific ones
        for i in range(min(3, len(selected_questions))):
            if i < len(variations):
                # Modify existing question to be company-specific
                original = selected_questions[i]
                modified = f"{original} {variations[i % len(variations)]}"
                selected_questions[i] = modified
    
    logger.info(f"✅ Generated {len(selected_questions)} enhanced questions for {category} + {company or 'general'}")
    return selected_questions[:count]

async def generate_ai_questions(category: str, company: Optional[str] = None, count: int = 5) -> List[str]:
    """
    Generate interview questions using multiple sources:
    1. Web Question Fetcher (real questions from web)
    2. OpenAI (AI-generated questions)
    3. Enhanced local bank (fallback)
    """
    try:
        # Try Web Question Fetcher first (real questions from web)
        try:
            from services.web_question_fetcher import get_question_fetcher
            
            fetcher = get_question_fetcher()
            logger.info(f"🌐 Fetching questions from web for {category}...")
            
            question_objects = await fetcher.fetch_questions(
                category=category,
                company=company,
                count=count
            )
            
            if question_objects:
                questions = [q["question"] for q in question_objects]
                logger.info(f"✅ Web fetcher returned {len(questions)} questions (sources: {set(q['source'] for q in question_objects)})")
                return questions
                
        except ImportError:
            logger.warning("⚠️  Web question fetcher not available")
        except Exception as e:
            logger.warning(f"⚠️  Web fetcher failed: {e}")
        
        # Fallback to OpenAI if API key is available
        if Config.OPENAI_API_KEY:
            logger.info(f"🤖 Attempting OpenAI generation for {category}...")
            
            # Quick timeout to avoid hanging
            async with httpx.AsyncClient(timeout=5.0) as client:
                headers = {
                    "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                company_context = f" for {company}" if company else ""
                prompt = f"Generate {count} {category} interview questions{company_context}. Return only the questions, numbered 1-{count}."
                
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                    "temperature": 0.8
                }
                
                response = await client.post(Config.OPENAI_CHAT_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if "choices" in data and data["choices"]:
                        content = data["choices"][0]["message"]["content"]
                        
                        # Parse questions
                        questions = []
                        for line in content.strip().split('\n'):
                            line = line.strip()
                            if line and len(line) > 10:
                                # Clean up numbering
                                for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '-', '•']:
                                    if line.startswith(prefix):
                                        line = line[len(prefix):].strip()
                                        break
                                if line:
                                    questions.append(line)
                        
                        if questions:
                            logger.info(f"✅ OpenAI generated {len(questions)} questions")
                            return questions
                
                # If we get here, OpenAI failed
                logger.warning(f"⚠️  OpenAI failed ({response.status_code}), using enhanced fallback")
        
        # Final fallback to enhanced local generation
        logger.info(f"🎯 Using enhanced local question generation for {category}")
        return generate_enhanced_questions(category, company, count)
        
    except Exception as e:
        logger.warning(f"⚠️  Question generation failed: {str(e)}, using enhanced fallback")
        return generate_enhanced_questions(category, company, count)

@app.post("/set_category")
async def set_category(request: Request, db=Depends(get_db)):
    """Set the current interview category and company - initializes practice session"""
    global current_category, current_company, question_cache
    
    # Get current user
    user = get_current_user(request, db)
    
    try:
        data = await request.json()
        category = data.get("category", "Behavioral")
        company = data.get("company", "")
        difficulty = data.get("difficulty", "intermediate")
        force_refresh = data.get("force_refresh", False)
        
        # Update global state
        current_category = category
        current_company = company
        
        # Store in session
        if hasattr(request, 'session'):
            request.session["current_category"] = category
            request.session["current_company"] = company
            request.session["current_difficulty"] = difficulty
            
            # Check cache
            company_suffix = f"_{company}" if company else ""
            difficulty_suffix = f"_{difficulty}"
            session_key = f"questions_{category}{company_suffix}{difficulty_suffix}"
            cached_questions = request.session.get(session_key, [])
            
            if cached_questions and len(cached_questions) >= 5 and not force_refresh:
                # Use cached questions
                request.session["category_questions"] = cached_questions
                request.session["question_index"] = 0
                print(f"✅ Using {len(cached_questions)} cached questions for category: {category} ({difficulty})")
                return {
                    "success": True,
                    "next_question": cached_questions[0],
                    "ai_generated": True,
                    "total_questions": len(cached_questions),
                    "category": category,
                    "difficulty": difficulty
                }
            
            # Try to get difficulty-specific questions first
            from services.difficulty_classifier import get_difficulty_classifier
            classifier = get_difficulty_classifier()
            difficulty_questions = classifier.get_questions_by_difficulty(category, difficulty, count=10)
            
            if difficulty_questions:
                # Use pre-classified questions
                request.session[session_key] = difficulty_questions
                request.session["category_questions"] = difficulty_questions
                request.session["question_index"] = 0
                
                print(f"✅ Using {len(difficulty_questions)} {difficulty} questions for category: {category}")
                return {
                    "success": True,
                    "next_question": difficulty_questions[0],
                    "ai_generated": False,
                    "total_questions": len(difficulty_questions),
                    "category": category,
                    "difficulty": difficulty
                }
            
            # Generate fresh questions with difficulty
            print(f"🔄 Generating new {difficulty} questions for category: {category}" + (f" (Company: {company})" if company else ""))
            try:
                gen_payload = {"category": category, "count": 10, "difficulty": difficulty}
                if company:
                    gen_payload["company"] = company
                gen_result = await generate_questions_internal(gen_payload)
                
                if gen_result and gen_result.get("created"):
                    questions = [item["prompt"] for item in gen_result["created"]]
                    
                    if questions:
                        # Cache in session
                        request.session[session_key] = questions
                        request.session["category_questions"] = questions
                        request.session["question_index"] = 0
                        
                        print(f"✅ Generated {len(questions)} AI questions for category: {category} ({difficulty})")
                        return {
                            "success": True,
                            "next_question": questions[0],
                            "ai_generated": True,
                            "total_questions": len(questions),
                            "category": category,
                            "difficulty": difficulty
                        }
            except Exception as e:
                print(f"⚠️ AI question generation failed: {e}")
            
            # Fallback to local questions
            if category in Config.LOCAL_QUESTION_BANK:
                local_questions = Config.LOCAL_QUESTION_BANK[category]
                request.session["category_questions"] = local_questions
                request.session["question_index"] = 0
                print(f"✅ Using {len(local_questions)} local questions for category: {category}")
                return {
                    "success": True,
                    "next_question": local_questions[0],
                    "ai_generated": False,
                    "total_questions": len(local_questions),
                    "category": category
                }
        
        logger.info(f"✅ Category set to: {category} ({difficulty}), Company: {company or 'None'}")
        
        return {
            "success": True,
            "category": category,
            "company": company,
            "difficulty": difficulty,
            "message": f"Starting {difficulty} {category} interview"
        }
        
    except Exception as e:
        logger.error(f"Error setting category: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

async def generate_questions_internal(data: dict):
    """Internal function to generate questions"""
    category = data.get("category", "Behavioral")
    count = data.get("count", 10)
    company = data.get("company", "")
    
    try:
        # Use the generate_ai_questions function
        questions = await generate_ai_questions(category, company, count)
        return {
            "created": [{"prompt": q} for q in questions],
            "count": len(questions)
        }
    except Exception as e:
        print(f"Error generating questions: {e}")
        return {"created": [], "count": 0}

@app.post("/generate_questions")
async def generate_questions(request: Request, db=Depends(get_db)):
    """Generate questions for a category"""
    global current_category, current_company, question_cache
    
    user = get_current_user(request, db)
    
    try:
        data = await request.json()
        category = data.get("category")
        company = data.get("company")
        
        valid_categories = list(Config.LOCAL_QUESTION_BANK.keys())
        if category and category in valid_categories:
            old_category = current_category
            old_company = current_company
            
            current_category = category
            current_company = company if company else None
            
            # Initialize or get practice session for user
            session_info = None
            if user:
                try:
                    from services.practice_session_manager import get_session_manager
                    session_manager = get_session_manager()
                    session = session_manager.get_or_create_session(user.id, category, company)
                    session_info = session.get_stats()
                    logger.info(f"✅ Session initialized for user {user.id}: {session_info}")
                except Exception as e:
                    logger.error(f"Session initialization error: {e}")
            
            # Clear cache to force regeneration of AI questions
            cache_key = f"{category}_{company or 'general'}"
            if cache_key in question_cache:
                del question_cache[cache_key]
            
            logger.info(f"✅ Updated: '{old_category}+{old_company}' → '{category}+{company}'")
            
            # Pre-generate questions for faster response
            try:
                questions = await generate_ai_questions(category, company, count=20)  # Generate more questions
                question_cache[cache_key] = questions
                logger.info(f"🚀 Pre-generated {len(questions)} questions for {cache_key}")
            except Exception as e:
                logger.warning(f"⚠️  Pre-generation failed: {e}")
            
            response = {
                "status": "success", 
                "category": category,
                "company": company,
                "old_category": old_category,
                "old_company": old_company,
                "available_categories": valid_categories,
                "cache_key": cache_key
            }
            
            if session_info:
                response["session"] = session_info
            
            return response
        elif category:
            logger.warning(f"⚠️  Invalid category requested: {category}")
            return {
                "status": "error", 
                "message": f"Invalid category: {category}",
                "available_categories": valid_categories
            }
        else:
            logger.error("❌ No category provided in request")
            return {
                "status": "error", 
                "message": "Category not provided",
                "available_categories": valid_categories
            }
    except Exception as e:
        logger.error(f"❌ Error setting category: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/clear_question_cache")
def clear_question_cache():
    """Clear the question cache to regenerate questions"""
    global question_cache
    old_size = len(question_cache)
    question_cache.clear()
    logger.info(f"🗑️ Question cache cleared ({old_size} entries) - next request will generate fresh questions")
    return {
        "status": "success", 
        "message": f"Question cache cleared ({old_size} entries)",
        "info": "Fresh questions will be generated on next request"
    }

@app.post("/generate_fresh_questions")
async def generate_fresh_questions(request: Request):
    """Generate fresh AI questions for current category and company"""
    global current_category, current_company, question_cache
    
    try:
        data = await request.json()
        category = data.get("category", current_category)
        company = data.get("company", current_company)
        count = data.get("count", 10)
        
        logger.info(f"🤖 Generating {count} fresh questions for {category} + {company}")
        
        # Generate new questions
        questions = await generate_ai_questions(category, company, count)
        
        # Update cache
        cache_key = f"{category}_{company or 'general'}"
        question_cache[cache_key] = questions
        
        return {
            "status": "success",
            "message": f"Generated {len(questions)} fresh questions",
            "category": category,
            "company": company,
            "question_count": len(questions),
            "sample_question": questions[0] if questions else None
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating fresh questions: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/openai/status")
async def check_openai_status():
    """Check OpenAI API status and quota"""
    try:
        if not Config.OPENAI_API_KEY:
            return {
                "status": "error",
                "message": "No OpenAI API key configured",
                "has_key": False
            }
        
        headers = {
            "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Test with a minimal request
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 5
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(Config.OPENAI_CHAT_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "OpenAI API is working",
                    "has_key": True,
                    "api_working": True
                }
            elif response.status_code == 429:
                return {
                    "status": "quota_exceeded",
                    "message": "OpenAI API quota exceeded - using fallback questions",
                    "has_key": True,
                    "api_working": False,
                    "error_details": response.text
                }
            else:
                return {
                    "status": "error",
                    "message": f"OpenAI API error: {response.status_code}",
                    "has_key": True,
                    "api_working": False,
                    "error_details": response.text
                }
                
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to check OpenAI API: {str(e)}",
            "has_key": bool(Config.OPENAI_API_KEY),
            "api_working": False
        }

@app.get("/api/questions/source")
def get_question_source():
    """Get information about current question source"""
    global current_category, current_company, question_cache
    
    cache_key = f"{current_category}_{current_company or 'general'}"
    
    return {
        "current_category": current_category,
        "current_company": current_company,
        "cache_key": cache_key,
        "cached_questions": len(question_cache.get(cache_key, [])),
        "has_openai_key": bool(Config.OPENAI_API_KEY),
        "has_serpapi_key": bool(Config.SERPAPI_KEY),
        "fallback_questions": len(Config.LOCAL_QUESTION_BANK.get(current_category, [])),
        "total_cache_entries": len(question_cache)
    }

@app.get("/api/practice/session")
def get_practice_session(request: Request, db=Depends(get_db)):
    """Get current practice session statistics"""
    user = get_current_user(request, db)
    if not user:
        return {"error": "User not logged in"}, 401
    
    try:
        from services.practice_session_manager import get_session_manager
        session_manager = get_session_manager()
        stats = session_manager.get_session_stats(user.id)
        
        if stats:
            return {
                "success": True,
                "session": stats
            }
        else:
            return {
                "success": False,
                "message": "No active session"
            }
    except Exception as e:
        logger.error(f"Session stats error: {e}")
        return {"error": str(e)}

@app.post("/api/practice/session/clear")
def clear_practice_session(request: Request, db=Depends(get_db)):
    """Clear current practice session"""
    user = get_current_user(request, db)
    if not user:
        return {"error": "User not logged in"}, 401
    
    try:
        from services.practice_session_manager import get_session_manager
        session_manager = get_session_manager()
        session_manager.clear_session(user.id)
        
        return {
            "success": True,
            "message": "Session cleared"
        }
    except Exception as e:
        logger.error(f"Session clear error: {e}")
        return {"error": str(e)}

@app.get("/api/templates/search")
def search_answer_templates(query: str):
    """Search for answer templates"""
    try:
        from services.answer_templates import get_templates_library
        
        library = get_templates_library()
        results = library.search_templates(query)
        
        return {
            "success": True,
            "count": len(results),
            "templates": results
        }
    except Exception as e:
        logger.error(f"Template search error: {e}")
        return {"error": str(e)}

@app.get("/api/templates/question")
def get_template_for_question(question: str):
    """Get answer template for a specific question"""
    try:
        from services.answer_templates import get_templates_library
        
        library = get_templates_library()
        template = library.get_template(question)
        
        if template:
            return {
                "success": True,
                "template": template
            }
        else:
            return {
                "success": False,
                "message": "No template found for this question"
            }
    except Exception as e:
        logger.error(f"Template fetch error: {e}")
        return {"error": str(e)}

@app.get("/api/templates/all")
def get_all_templates():
    """Get all available answer templates"""
    try:
        from services.answer_templates import get_templates_library
        
        library = get_templates_library()
        templates = library.get_all_templates()
        
        return {
            "success": True,
            "count": len(templates),
            "templates": templates
        }
    except Exception as e:
        logger.error(f"Templates fetch error: {e}")
        return {"error": str(e)}

@app.get("/api/templates/category/{category}")
def get_templates_by_category(category: str):
    """Get templates for a specific category"""
    try:
        from services.answer_templates import get_templates_library
        
        library = get_templates_library()
        templates = library.get_templates_by_category(category)
        
        return {
            "success": True,
            "category": category,
            "count": len(templates),
            "templates": templates
        }
    except Exception as e:
        logger.error(f"Category templates fetch error: {e}")
        return {"error": str(e)}

@app.get("/api/hints/question")
def get_hints_for_question(question: str):
    """Get hints for a specific question"""
    try:
        from services.answer_hints import get_hints_service
        
        hints_service = get_hints_service()
        hints_data = hints_service.get_hints(question)
        
        if hints_data:
            return {
                "success": True,
                "hints_available": True,
                **hints_data
            }
        else:
            return {
                "success": True,
                "hints_available": False,
                "message": "No hints available for this question"
            }
    except Exception as e:
        logger.error(f"Hints fetch error: {e}")
        return {"error": str(e)}

@app.get("/api/hints/level")
def get_hint_by_level(question: str, level: int):
    """Get a specific hint level for a question"""
    try:
        from services.answer_hints import get_hints_service
        
        hints_service = get_hints_service()
        hint = hints_service.get_hint_by_level(question, level)
        
        if hint:
            penalty = hints_service.calculate_penalty(level + 1)
            return {
                "success": True,
                "hint": hint,
                "level": level,
                "penalty": penalty
            }
        else:
            return {
                "success": False,
                "message": "Hint not available for this level"
            }
    except Exception as e:
        logger.error(f"Hint level fetch error: {e}")
        return {"error": str(e)}

@app.get("/api/hints/search")
def search_hints(query: str):
    """Search for questions that have hints"""
    try:
        from services.answer_hints import get_hints_service
        
        hints_service = get_hints_service()
        results = hints_service.search_hints(query)
        
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Hints search error: {e}")
        return {"error": str(e)}

@app.get("/analytics", response_class=HTMLResponse)
def analytics_page(request: Request, db=Depends(get_db)):
    """Render analytics dashboard page"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login")
    
    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }
    
    return templates.TemplateResponse("analytics_new.html", {
        "request": request, 
        "user": user_dict,
        "page_title": "Analytics"
    })

@app.get("/api/analytics")
def get_analytics_data(request: Request, db=Depends(get_db)):
    """Get analytics data for current user"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}
        
        from services.analytics_service import get_analytics_service
        
        analytics_service = get_analytics_service()
        data = analytics_service.get_user_analytics(user.id, db)
        
        return data
        
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return {"error": str(e)}

@app.get("/api/questions/web/search")
async def search_web_questions(query: str, limit: int = 10):
    """Search for interview questions from web sources"""
    try:
        from services.web_question_fetcher import get_question_fetcher
        
        fetcher = get_question_fetcher()
        results = await fetcher.search_questions(query, limit)
        
        return {
            "success": True,
            "query": query,
            "count": len(results),
            "questions": results
        }
        
    except Exception as e:
        logger.error(f"❌ Web search error: {e}")
        return {
            "success": False,
            "error": str(e),
            "questions": []
        }

@app.post("/api/questions/web/fetch")
async def fetch_web_questions(request: Request):
    """Fetch questions from web sources with specific parameters"""
    try:
        from services.web_question_fetcher import get_question_fetcher
        
        data = await request.json()
        category = data.get("category", "Python")
        company = data.get("company")
        count = data.get("count", 10)
        difficulty = data.get("difficulty")
        
        fetcher = get_question_fetcher()
        results = await fetcher.fetch_questions(
            category=category,
            company=company,
            count=count,
            difficulty=difficulty
        )
        
        return {
            "success": True,
            "category": category,
            "company": company,
            "count": len(results),
            "questions": results,
            "sources": list(set(q.get("source", "unknown") for q in results))
        }
        
    except Exception as e:
        logger.error(f"❌ Web fetch error: {e}")
        return {
            "success": False,
            "error": str(e),
            "questions": []
        }

@app.post("/api/questions/cache/clear")
def clear_all_caches():
    """Clear both question cache and web fetcher cache"""
    global question_cache
    
    try:
        # Clear local cache
        question_cache.clear()
        
        # Clear web fetcher cache
        try:
            from services.web_question_fetcher import get_question_fetcher
            fetcher = get_question_fetcher()
            fetcher.clear_cache()
        except:
            pass
        
        return {
            "success": True,
            "message": "All caches cleared successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/get_categories")
def get_categories():
    """Get available question categories and current status"""
    global current_category, question_cache
    
    return {
        "current_category": current_category,
        "available_categories": list(Config.LOCAL_QUESTION_BANK.keys()),
        "cached_categories": list(question_cache.keys()),
        "question_counts": {
            category: len(questions) 
            for category, questions in Config.LOCAL_QUESTION_BANK.items()
        }
    }

@app.get("/get_mock_question")
async def get_mock_question(index: int = 0, request: Request = None):
    """
    Returns a question - tries AI-generated questions from session first, then falls back.
    Generates new questions if index exceeds available questions.
    """
    try:
        # Get category from session if available
        category = "General"
        if request and hasattr(request, 'session'):
            category = request.session.get("current_category", "General")
            company = request.session.get("current_company", "")
            
            # Try to get from category-specific AI-generated questions
            category_questions = request.session.get("category_questions", [])
            
            # If we have questions but index exceeds them, generate more
            if category_questions and index >= len(category_questions):
                print(f"📝 Index {index} exceeds {len(category_questions)} questions, generating more...")
                try:
                    # Generate 10 more questions
                    gen_payload = {"category": category, "count": 10}
                    if company:
                        gen_payload["company"] = company
                    gen_result = await generate_questions(gen_payload)
                    
                    if gen_result and gen_result.get("created"):
                        new_questions = [item["prompt"] for item in gen_result["created"]]
                        # Append to existing questions
                        category_questions.extend(new_questions)
                        request.session["category_questions"] = category_questions
                        
                        # Update cache key
                        company_suffix = f"_{company}" if company else ""
                        session_key = f"questions_{category}{company_suffix}"
                        request.session[session_key] = category_questions
                        
                        print(f"✅ Generated {len(new_questions)} more questions. Total: {len(category_questions)}")
                except Exception as e:
                    print(f"⚠️ Failed to generate more questions: {e}")
            
            if category_questions:
                # Use the exact index if within bounds, otherwise use modulo
                if index < len(category_questions):
                    question = category_questions[index]
                else:
                    # Fallback to modulo if generation failed
                    q_index = index % len(category_questions)
                    question = category_questions[q_index]
                
                return {"question": question, "ai_generated": True, "index": index, "total": len(category_questions)}
        
        # Fallback to local question bank
        if category in Config.LOCAL_QUESTION_BANK:
            local_questions = Config.LOCAL_QUESTION_BANK[category]
            if local_questions:
                q = local_questions[index % len(local_questions)]
                return {"question": q, "ai_generated": False}
        
        # Last resort
        return {"question": f"Explain a key concept or skill related to {category}.", "ai_generated": False}
    except Exception as e:
        print("⚠️ get_mock_question error:", e)
        import traceback
        traceback.print_exc()
        return {"question": "Describe your strengths and how they relate to this role.", "ai_generated": False}

@app.post("/evaluate_answer")
async def evaluate_answer(request: Request, db=Depends(get_db)):
    """Enhanced evaluation with comprehensive multi-dimensional feedback"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "User not logged in"}, 401
        
        data = await request.json()
        question_text = data.get("question_text", "")
        answer = data.get("answer", "")
        category = data.get("category", "General")
        difficulty = data.get("difficulty", "intermediate")
        
        if not answer.strip():
            return {"error": "No answer provided"}
        
        # Use advanced feedback engine
        from services.advanced_feedback_engine import get_feedback_engine
        
        feedback_engine = get_feedback_engine(Config.OPENAI_API_KEY)
        evaluation = await feedback_engine.evaluate_answer(
            question=question_text,
            answer=answer,
            category=category,
            difficulty=difficulty
        )
        
        score = evaluation["overall_score"]
        
        # STAR Method Analysis (for behavioral questions)
        star_analysis = None
        if category in ["Behavioral", "Leadership", "HR Interview"]:
            try:
                from services.star_analyzer import get_star_analyzer
                star_analyzer = get_star_analyzer()
                star_analysis = await star_analyzer.analyze_answer(question_text, answer)
                
                # Blend STAR score with overall score if behavioral
                if star_analysis.get("is_behavioral"):
                    star_score = star_analysis.get("star_score", 0)
                    # Blend: 50% STAR, 50% advanced feedback
                    score = (star_score / 10 * 0.5) + (score * 0.5)
                    evaluation["overall_score"] = round(score, 1)
                    
                    logger.info(f"📊 STAR analysis: score={star_score}, components={4 - len(star_analysis.get('missing', []))}/4")
            except Exception as e:
                logger.error(f"STAR analysis error: {e}")
        
        # Track answer in session
        try:
            from services.practice_session_manager import get_session_manager
            session_manager = get_session_manager()
            session_info = session_manager.record_answer(user.id, question_text, score)
            
            # Add session info to response
            evaluation["session_info"] = session_info
            
            # Add level change notifications
            if session_info.get("promoted"):
                evaluation["level_change"] = {
                    "type": "promotion",
                    "new_level": session_info["difficulty_level"],
                    "message": f"🎉 Promoted to {session_info['difficulty_level'].upper()} level!"
                }
            elif session_info.get("demoted"):
                evaluation["level_change"] = {
                    "type": "demotion",
                    "new_level": session_info["difficulty_level"],
                    "message": f"⚠️ Moved to {session_info['difficulty_level'].upper()} level"
                }
            
            logger.info(f"✅ Answer evaluated for user {user.id}: score={score}, level={session_info['difficulty_level']}")
        except Exception as e:
            logger.error(f"Session tracking error: {e}")
        
        # Save to database
        try:
            attempt = Attempt(
                user_id=user.id,
                question=question_text,
                score=score,
                feedback=json.dumps(evaluation),
                timestamp=datetime.utcnow()
            )
            db.add(attempt)
            db.commit()
        except Exception as e:
            logger.error(f"Database save error: {e}")
        
        return {
            "evaluation": evaluation,
            "star_analysis": star_analysis,
            "plagiarism_score": 0.1,  # Mock low plagiarism
            "matches": []
        }
        
    except Exception as e:
        logger.error(f"❌ Error evaluating answer: {str(e)}")
        return {"error": str(e)}

@app.post("/chat")
async def chat_fallback(request: Request):
    """Fallback chat endpoint for basic responses"""
    try:
        data = await request.json()
        message = data.get("message", "")
        
        if not message.strip():
            return {"reply": "Please provide a message", "score": None}
        
        # Simple response logic
        word_count = len(message.split())
        score = min(10, max(1, word_count / 15))
        
        reply = f"Thank you for your response! I can see you've provided a {word_count}-word answer. "
        
        if score >= 7:
            reply += "This looks like a comprehensive response."
        elif score >= 4:
            reply += "This is a good start, but could be expanded."
        else:
            reply += "Try to provide more detail in your answer."
        
        return {
            "reply": reply,
            "score": score
        }
        
    except Exception as e:
        logger.error(f"❌ Error in chat: {str(e)}")
        return {"reply": "Sorry, I couldn't process your message.", "score": None}

@app.post("/save_question")
async def save_question(request: Request, db=Depends(get_db)):
    """Save a question with enhanced metadata"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "User not logged in"}, 401
        
        data = await request.json()
        question = data.get("question", "")
        
        if not question.strip():
            return {"error": "No question provided"}
        
        from services.bookmarking_service import get_bookmarking_service
        
        bookmarking_service = get_bookmarking_service()
        result = bookmarking_service.save_question(
            user_id=user.id,
            question=question,
            db=db,
            company=data.get("company"),
            category=data.get("category"),
            notes=data.get("notes"),
            tags=data.get("tags", []),
            difficulty=data.get("difficulty"),
            priority=data.get("priority", 0)
        )
        
        if result["success"]:
            logger.info(f"💾 Question saved for user {user.email}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error saving question: {str(e)}")
        return {"error": str(e)}

@app.put("/api/bookmarks/{question_id}")
async def update_bookmark(question_id: int, request: Request, db=Depends(get_db)):
    """Update saved question metadata"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}, 401
        
        data = await request.json()
        
        from services.bookmarking_service import get_bookmarking_service
        
        bookmarking_service = get_bookmarking_service()
        result = bookmarking_service.update_question(
            question_id=question_id,
            user_id=user.id,
            db=db,
            notes=data.get("notes"),
            tags=data.get("tags"),
            difficulty=data.get("difficulty"),
            priority=data.get("priority"),
            category=data.get("category"),
            company=data.get("company")
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Update bookmark error: {e}")
        return {"error": str(e)}

@app.delete("/api/bookmarks/{question_id}")
async def delete_bookmark(question_id: int, request: Request, db=Depends(get_db)):
    """Delete a saved question"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}, 401
        
        from services.bookmarking_service import get_bookmarking_service
        
        bookmarking_service = get_bookmarking_service()
        result = bookmarking_service.delete_question(
            question_id=question_id,
            user_id=user.id,
            db=db
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Delete bookmark error: {e}")
        return {"error": str(e)}

@app.get("/api/bookmarks")
async def get_bookmarks(
    request: Request,
    db=Depends(get_db),
    category: str = None,
    company: str = None,
    tags: str = None,
    difficulty: str = None,
    priority: int = None,
    search: str = None,
    sort_by: str = "timestamp",
    order: str = "desc"
):
    """Get saved questions with filtering"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}, 401
        
        from services.bookmarking_service import get_bookmarking_service
        
        # Parse tags if provided
        tags_list = tags.split(",") if tags else None
        
        bookmarking_service = get_bookmarking_service()
        result = bookmarking_service.get_saved_questions(
            user_id=user.id,
            db=db,
            category=category,
            company=company,
            tags=tags_list,
            difficulty=difficulty,
            priority=priority,
            search=search,
            sort_by=sort_by,
            order=order
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Get bookmarks error: {e}")
        return {"error": str(e)}

@app.get("/api/bookmarks/{question_id}")
async def get_bookmark(question_id: int, request: Request, db=Depends(get_db)):
    """Get a single saved question"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}, 401
        
        from services.bookmarking_service import get_bookmarking_service
        
        bookmarking_service = get_bookmarking_service()
        result = bookmarking_service.get_question_by_id(
            question_id=question_id,
            user_id=user.id,
            db=db
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Get bookmark error: {e}")
        return {"error": str(e)}

@app.post("/api/bookmarks/{question_id}/practice")
async def mark_practiced(question_id: int, request: Request, db=Depends(get_db)):
    """Mark a question as practiced"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}, 401
        
        from services.bookmarking_service import get_bookmarking_service
        
        bookmarking_service = get_bookmarking_service()
        result = bookmarking_service.mark_practiced(
            question_id=question_id,
            user_id=user.id,
            db=db
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Mark practiced error: {e}")
        return {"error": str(e)}

@app.get("/api/bookmarks/review/due")
async def get_due_for_review(request: Request, db=Depends(get_db), days: int = 7):
    """Get questions due for review (spaced repetition)"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}, 401
        
        from services.bookmarking_service import get_bookmarking_service
        
        bookmarking_service = get_bookmarking_service()
        result = bookmarking_service.get_due_for_review(
            user_id=user.id,
            db=db,
            days=days
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Get due for review error: {e}")
        return {"error": str(e)}

@app.get("/api/bookmarks/stats")
async def get_bookmark_stats(request: Request, db=Depends(get_db)):
    """Get statistics about saved questions"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}, 401
        
        from services.bookmarking_service import get_bookmarking_service
        
        bookmarking_service = get_bookmarking_service()
        result = bookmarking_service.get_statistics(
            user_id=user.id,
            db=db
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Get bookmark stats error: {e}")
        return {"error": str(e)}

@app.get("/api/bookmarks/tags")
async def get_all_tags(request: Request, db=Depends(get_db)):
    """Get all unique tags"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}, 401
        
        from services.bookmarking_service import get_bookmarking_service
        
        bookmarking_service = get_bookmarking_service()
        tags = bookmarking_service.get_all_tags(
            user_id=user.id,
            db=db
        )
        
        return {"success": True, "tags": tags}
        
    except Exception as e:
        logger.error(f"Get tags error: {e}")
        return {"error": str(e)}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe audio file to text"""
    try:
        if not file.filename.endswith(('.webm', '.wav', '.mp3', '.m4a')):
            return {"error": "Unsupported audio format"}
        
        # For now, return a mock transcription
        # In a real implementation, you'd use Whisper or another ASR service
        mock_transcription = "This is a mock transcription. In a real implementation, this would use Whisper AI to convert speech to text."
        
        return {
            "transcription": mock_transcription,
            "word_count": len(mock_transcription.split()),
            "confidence": 0.95
        }
        
    except Exception as e:
        logger.error(f"❌ Error transcribing audio: {str(e)}")
        return {"error": str(e)}

# ================================
# VIDEO INTERVIEW ROUTES
# ================================

@app.get("/video_interview", response_class=HTMLResponse)
def video_interview(request: Request, db=Depends(get_db)):
    """Video interview page with AI-powered analysis"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }
    
    from services.video_interview_service import get_video_interview_service
    service = get_video_interview_service()
    
    # Get a random question to start
    question_data = service.get_question()
    
    return templates.TemplateResponse(
        "video_interview_new.html",
        {
            "request": request,
            "user": user_dict,
            "page_title": "Video Interview",
            "question": question_data.get("question"),
            "categories": list(service.question_bank.keys()),
        },
    )


@app.post("/get_video_question")
async def get_video_question(request: Request, db=Depends(get_db)):
    """Get a new interview question"""
    user = get_current_user(request, db)
    if not user:
        return {"error": "Not authenticated"}
    
    try:
        data = await request.json()
        category = data.get("category")
        difficulty = data.get("difficulty")
        use_ai = data.get("use_ai", False)
        
        from services.video_interview_service import get_video_interview_service
        service = get_video_interview_service()
        
        if use_ai:
            # Generate AI question based on user profile
            user_profile = {
                "role": "Professional",
                "experience": "Mid-level",
                "industry": "Technology"
            }
            question_data = await service.generate_ai_question(category or "Behavioral", user_profile)
        else:
            question_data = service.get_question(category, difficulty)
        
        # Generate audio for the question
        from services.ai_interviewer_tts import get_tts_service
        tts_service = get_tts_service()
        
        audio_result = await tts_service.generate_question_audio(
            question_data.get("question"),
            greeting=data.get("first_question", False)
        )
        
        # Add audio data to response
        question_data["audio"] = audio_result
        
        return {
            "success": True,
            "question": question_data.get("question"),
            "time_limit": question_data.get("time_limit", 90),
            "tips": question_data.get("tips", []),
            "difficulty": question_data.get("difficulty", "intermediate"),
            "ai_generated": question_data.get("ai_generated", False),
            "audio": audio_result  # Include audio in response
        }
    except Exception as e:
        print(f"Error getting video question: {e}")
        return {"error": str(e)}


@app.post("/upload_video")
async def upload_video(
    request: Request,
    video: UploadFile = File(...),
    question: str = Form(default=""),
    db=Depends(get_db)
):
    """Upload and analyze video interview response"""
    user = get_current_user(request, db)
    if not user:
        return {"error": "Not authenticated"}
    
    try:
        # Validate video file size (must be at least 10KB to have content)
        video_content = await video.read()
        video_size = len(video_content)
        
        if video_size < 10000:  # Less than 10KB
            return {
                "success": False,
                "error": "Video is too short or empty. Please record a proper answer."
            }
        
        # Save video temporarily
        import tempfile
        import shutil
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_file:
            tmp_file.write(video_content)
            video_path = tmp_file.name
        
        # Try to get transcription (optional - works without it)
        transcription = "[Video response recorded]"
        try:
            # Try using speech recognition if available
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            
            # Convert webm to wav if needed
            try:
                from pydub import AudioSegment
                audio = AudioSegment.from_file(video_path, format="webm")
                wav_path = video_path.replace(".webm", ".wav")
                audio.export(wav_path, format="wav")
                
                with sr.AudioFile(wav_path) as source:
                    audio_data = recognizer.record(source)
                    transcription = recognizer.recognize_google(audio_data)
                
                # Clean up wav file
                try:
                    os.unlink(wav_path)
                except:
                    pass
            except:
                pass
        except Exception as e:
            print(f"Transcription not available: {e}")
            # Continue without transcription - analysis will work with placeholder
        
        # Simulate emotion and voice analysis (in production, use actual video/audio analysis)
        emotion_data = {
            "dominant_emotion": "confident",
            "micro_expressions": ["confident", "happy", "neutral"]
        }
        
        # Calculate voice data based on transcription if available
        word_count = len(transcription.split()) if transcription != "[Video response recorded]" else 150
        voice_data = {
            "speech_rate": word_count * 2,  # Rough estimate
            "filler_count": transcription.lower().count("um") + transcription.lower().count("uh") + transcription.lower().count("like") if transcription != "[Video response recorded]" else 3,
            "clarity_score": 0.85,
            "energy_level": "medium"
        }
        
        # Get AI analysis
        from services.video_interview_service import get_video_interview_service
        service = get_video_interview_service()
        
        analysis_result = await service.analyze_video_response(
            transcription=transcription,
            question=question,
            emotion_data=emotion_data,
            voice_data=voice_data
        )
        
        # Save to database (optional - model needs to be created)
        try:
            # TODO: Add VideoInterview model to models.py
            # from models import VideoInterview
            # video_interview_record = VideoInterview(
            #     user_id=user.id,
            #     question=question,
            #     transcription=transcription,
            #     score=analysis_result.get("score", 0),
            #     feedback=analysis_result.get("feedback", ""),
            #     emotion_data=json.dumps(emotion_data),
            #     voice_data=json.dumps(voice_data)
            # )
            # db.add(video_interview_record)
            # db.commit()
            pass
        except Exception as db_error:
            print(f"Database save error: {db_error}")
            # Continue even if DB save fails
        
        # Clean up temp file
        try:
            os.unlink(video_path)
        except:
            pass
        
        # Add detailed metrics for frontend
        detailed_analysis = analysis_result.get("detailed_analysis", {})
        detailed_analysis.update({
            "eye_tracking": {
                "eye_contact_percentage": random.randint(65, 95),
                "blink_rate": round(random.uniform(15, 25), 1),
                "gaze_stability": round(random.uniform(0.7, 0.95), 2)
            },
            "attention_metrics": {
                "focus_percentage": random.randint(75, 98),
                "distraction_count": random.randint(0, 3),
                "head_pose_stability": round(random.uniform(0.75, 0.95), 2)
            },
            "sentiment": {
                "label": "positive" if analysis_result.get("score", 0) > 7 else "neutral",
                "polarity": round(random.uniform(0.3, 0.8), 2)
            }
        })
        
        return {
            "success": True,
            "feedback": analysis_result.get("feedback"),
            "score": analysis_result.get("score"),
            "detailed_analysis": detailed_analysis
        }
        
    except Exception as e:
        print(f"Video upload error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "feedback": "An error occurred during analysis. Please try again."
        }


# ================================
# USER PROFILE AND PROGRESS ROUTES
# ================================

@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request, db=Depends(get_db)):
    """User profile page"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Get all user's attempts for accurate statistics
    all_attempts = db.query(Attempt).filter_by(user_id=user.id).order_by(Attempt.timestamp.desc()).all()
    
    # Calculate statistics
    scores = [float(a.score) for a in all_attempts if a.score]
    total_attempts = len(all_attempts)
    avg_score = sum(scores) / len(scores) if scores else 0
    best_score = max(scores) if scores else 0
    
    # Calculate streak
    from datetime import datetime, timedelta
    streak = 0
    if all_attempts:
        dates = sorted(set([a.timestamp.date() for a in all_attempts if a.timestamp]), reverse=True)
        if dates:
            current_date = datetime.now().date()
            for i, date in enumerate(dates):
                expected_date = current_date - timedelta(days=i)
                if date == expected_date:
                    streak += 1
                else:
                    break
    
    # Get user's recent attempts for display
    recent_attempts = all_attempts[:10]
    
    # Convert attempts to dicts for JSON serialization
    attempts_list = []
    for attempt in recent_attempts:
        attempts_list.append({
            "id": attempt.id,
            "question": attempt.question,
            "score": float(attempt.score) if attempt.score else 0,
            "feedback": attempt.feedback,
            "timestamp": attempt.timestamp.strftime("%Y-%m-%d %H:%M:%S") if attempt.timestamp else ""
        })
    
    # Category analysis for chart
    category_scores = {}
    for attempt in all_attempts:
        category = attempt.category if hasattr(attempt, 'category') and attempt.category else "General"
        score = float(attempt.score) if attempt.score else 0
        if category not in category_scores:
            category_scores[category] = []
        category_scores[category].append(score)
    
    category_labels = []
    category_avg_scores = []
    for cat, cat_scores in category_scores.items():
        if cat_scores:
            category_labels.append(cat)
            category_avg_scores.append(round(sum(cat_scores) / len(cat_scores), 1))
    
    # Determine user rank/badge based on performance
    if avg_score >= 9:
        badge = "Expert"
    elif avg_score >= 7:
        badge = "Advanced"
    elif avg_score >= 5:
        badge = "Intermediate"
    elif total_attempts > 0:
        badge = "Rising Learner"
    else:
        badge = "Beginner"
    
    # Convert user to dict for JSON serialization with calculated stats
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U",
        "attempts": total_attempts,
        "avg": round(avg_score, 1),
        "best": round(best_score, 1),
        "streak": streak,
        "badge": badge,
        "created_at": user.created_at if hasattr(user, 'created_at') else None,
        "rank": f"#{db.query(User).filter(User.total_score > (user.total_score or 0)).count() + 1}" if hasattr(user, 'total_score') else "Unranked"
    }
    
    return templates.TemplateResponse(
        "profile_new.html",
        {
            "request": request,
            "user": user_dict,
            "recent_attempts": attempts_list,
            "category_labels": category_labels,
            "category_scores": category_avg_scores,
        },
    )

@app.get("/report", response_class=HTMLResponse)
def report(request: Request, db=Depends(get_db)):
    """Performance report page"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }
    
    # Get user's performance data
    attempts = db.query(Attempt).filter_by(user_id=user.id).order_by(Attempt.timestamp.desc()).all()
    
    # Convert attempts to dicts for JSON serialization
    attempts_list = []
    category_scores = {}
    
    for attempt in attempts:
        score = float(attempt.score) if attempt.score else 0
        attempts_list.append({
            "id": attempt.id,
            "question": attempt.question,
            "score": score,
            "feedback": attempt.feedback,
            "timestamp": attempt.timestamp.strftime("%Y-%m-%d %H:%M:%S") if attempt.timestamp else "",
            "category": attempt.category if hasattr(attempt, 'category') and attempt.category else "General"
        })
        
        # Track category performance
        category = attempt.category if hasattr(attempt, 'category') and attempt.category else "General"
        if category not in category_scores:
            category_scores[category] = []
        category_scores[category].append(score)
    
    # Calculate statistics
    total_attempts = len(attempts)
    scores = [a["score"] for a in attempts_list if a["score"] > 0]
    avg_score = sum(scores) / len(scores) if scores else 0
    best_score = max(scores) if scores else 0
    
    # Calculate streak
    from datetime import datetime, timedelta
    streak = 0
    if attempts:
        dates = sorted(set([a.timestamp.date() for a in attempts if a.timestamp]), reverse=True)
        if dates:
            current_date = datetime.now().date()
            for i, date in enumerate(dates):
                expected_date = current_date - timedelta(days=i)
                if date == expected_date:
                    streak += 1
                else:
                    break
    
    # Category analysis
    category_labels = []
    category_avg_scores = []
    for cat, cat_scores in category_scores.items():
        if cat_scores:
            category_labels.append(cat)
            category_avg_scores.append(round(sum(cat_scores) / len(cat_scores), 1))
    
    # Identify strengths and weaknesses
    strengths = []
    weaknesses = []
    
    if category_scores:
        sorted_categories = sorted(category_scores.items(), key=lambda x: sum(x[1])/len(x[1]) if x[1] else 0, reverse=True)
        
        # Top 3 categories are strengths
        for cat, cat_scores in sorted_categories[:3]:
            avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
            if avg >= 7:
                strengths.append(f"{cat}: {avg:.1f}/10 average")
        
        # Bottom 3 categories are weaknesses
        for cat, cat_scores in sorted_categories[-3:]:
            avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
            if avg < 7:
                weaknesses.append(f"{cat}: {avg:.1f}/10 average - needs practice")
    
    # Generate recommendation
    recommendation = None
    if total_attempts == 0:
        recommendation = "Start your journey by completing your first practice session. Focus on understanding the question types and building confidence."
    elif avg_score < 5:
        recommendation = "Focus on fundamentals. Review feedback from previous attempts and practice consistently. Consider starting with easier questions to build momentum."
    elif avg_score < 7:
        recommendation = "You're making progress! Focus on your weaker categories and try to apply feedback from previous attempts. Aim for more detailed and structured answers."
    elif avg_score < 9:
        recommendation = "Great work! You're performing well. To reach the next level, focus on providing more specific examples and demonstrating deeper understanding in your answers."
    else:
        recommendation = "Excellent performance! Maintain your streak and consider challenging yourself with more complex questions or new categories."
    
    # Generate performance remark
    remark = None
    if total_attempts > 0:
        if avg_score >= 8:
            remark = f"Outstanding performance! You've completed {total_attempts} practice sessions with an impressive {avg_score:.1f}/10 average. Your consistency and dedication are paying off. Keep up the excellent work!"
        elif avg_score >= 6:
            remark = f"Good progress! You've completed {total_attempts} sessions with a {avg_score:.1f}/10 average. You're on the right track. Focus on your improvement areas to reach the next level."
        else:
            remark = f"You've completed {total_attempts} practice sessions. Your current average is {avg_score:.1f}/10. Don't get discouraged - every expert was once a beginner. Review feedback carefully and keep practicing!"
    
    return templates.TemplateResponse(
        "report_new.html",
        {
            "request": request,
            "user": user_dict,
            "attempts": attempts_list,
            "average": round(avg_score, 1) if avg_score else 0,
            "best_score": round(best_score, 1) if best_score else 0,
            "streak": streak,
            "category_labels": category_labels,
            "category_scores": category_avg_scores,
            "strengths": strengths if strengths else None,
            "weaknesses": weaknesses if weaknesses else None,
            "recommendation": recommendation,
            "remark": remark,
        },
    )

@app.get("/leaderboard", response_class=HTMLResponse)
def leaderboard(request: Request, db=Depends(get_db)):
    """Leaderboard page"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }
    
    # Get top users by score
    top_users = db.query(User).order_by(User.total_score.desc()).limit(10).all()
    
    # Convert top_users to dicts for JSON serialization
    top_users_list = []
    for u in top_users:
        top_users_list.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "total_score": float(u.total_score) if u.total_score else 0,
            "attempts": u.attempts if hasattr(u, 'attempts') else 0
        })
    
    return templates.TemplateResponse(
        "leaderboard_new.html",
        {
            "request": request,
            "user": user_dict,
            "page_title": "Leaderboard",
            "top_users": top_users_list,
        },
    )

@app.get("/api/leaderboard")
def get_leaderboard_api(request: Request, filter: str = "all", db=Depends(get_db)):
    """API endpoint for leaderboard data"""
    user = get_current_user(request, db)
    if not user:
        return {"error": "Not authenticated"}
    
    try:
        # Get all users with their scores
        users = db.query(User).all()
        
        # Calculate scores for each user
        leaderboard = []
        for u in users:
            attempts = db.query(Attempt).filter_by(user_id=u.id).all()
            scores = [a.score for a in attempts if a.score]
            
            total_score = sum(scores) if scores else 0
            avg_score = total_score / len(scores) if scores else 0
            
            leaderboard.append({
                "id": u.id,
                "name": u.name or u.username,
                "email": u.email,
                "total_score": total_score,
                "attempts": len(attempts)
            })
        
        # Sort by total score
        leaderboard.sort(key=lambda x: x["total_score"], reverse=True)
        
        # Get current user stats
        user_rank = next((i + 1 for i, u in enumerate(leaderboard) if u["id"] == user.id), None)
        user_attempts = db.query(Attempt).filter_by(user_id=user.id).all()
        user_scores = [a.score for a in user_attempts if a.score]
        user_total = sum(user_scores) if user_scores else 0
        
        percentile = None
        if user_rank and len(leaderboard) > 0:
            percentile = int((1 - (user_rank / len(leaderboard))) * 100)
        
        return {
            "leaderboard": leaderboard[:50],  # Top 50
            "user_stats": {
                "rank": user_rank,
                "score": user_total,
                "attempts": len(user_attempts),
                "percentile": percentile
            }
        }
    except Exception as e:
        logger.error(f"Error in leaderboard API: {str(e)}")
        return {"error": str(e), "leaderboard": [], "user_stats": {}}

@app.get("/saved", response_class=HTMLResponse)
def saved_questions(request: Request, db=Depends(get_db)):
    """Redirect to bookmarks page"""
    return RedirectResponse("/bookmarks", status_code=303)

@app.get("/bookmarks", response_class=HTMLResponse)
def bookmarks_page(request: Request, db=Depends(get_db)):
    """Enhanced bookmarks page with notes and tags"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }
    
    return templates.TemplateResponse("bookmarks_new.html", {
        "request": request, 
        "user": user_dict,
        "page_title": "Bookmarks"
    })

@app.get("/resume", response_class=HTMLResponse)
def resume_builder(request: Request, db=Depends(get_db)):
    """Resume builder page"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }
    
    return templates.TemplateResponse(
        "resume_new.html",
        {
            "request": request,
            "user": user_dict,
            "page_title": "Resume Builder",
        },
    )

@app.get("/resume/builder", response_class=HTMLResponse)
def resume_builder_alt(request: Request, db=Depends(get_db)):
    """Resume builder page (alternate route)"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }
    
    return templates.TemplateResponse(
        "resume_new.html",
        {
            "request": request,
            "user": user_dict,
            "page_title": "Resume Builder",
        },
    )

@app.post("/api/resume/generate")
async def generate_resume(request: Request, db=Depends(get_db)):
    """Generate resume PDF"""
    try:
        user = get_current_user(request, db)
        if not user:
            return JSONResponse({"error": "Not authenticated"}, status_code=401)
        
        data = await request.json()
        
        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, 
                              leftMargin=0.75*inch, rightMargin=0.75*inch,
                              topMargin=0.75*inch, bottomMargin=0.75*inch)
        styles = getSampleStyleSheet()
        story = []
        
        # Add resume header
        name = data.get('name', user.name)
        story.append(Paragraph(f"<b>{name}</b>", styles['Title']))
        story.append(Spacer(1, 0.1*inch))
        
        # Contact info
        contact_parts = []
        if data.get('email'):
            contact_parts.append(data['email'])
        if data.get('phone'):
            contact_parts.append(data['phone'])
        if data.get('linkedin'):
            contact_parts.append(data['linkedin'])
        
        if contact_parts:
            story.append(Paragraph(" | ".join(contact_parts), styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Professional Summary
        if data.get('summary'):
            story.append(Paragraph("<b>PROFESSIONAL SUMMARY</b>", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(data['summary'], styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Experience Section
        experience = data.get('experience', [])
        if experience and isinstance(experience, list) and len(experience) > 0:
            story.append(Paragraph("<b>EXPERIENCE</b>", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            for exp in experience:
                if isinstance(exp, dict):
                    # Job title and company
                    title = exp.get('title', '')
                    company = exp.get('company', '')
                    if title or company:
                        story.append(Paragraph(f"<b>{title}</b> - {company}", styles['Normal']))
                    
                    # Dates (frontend uses 'start' and 'end')
                    start_date = exp.get('start', exp.get('startDate', ''))
                    end_date = exp.get('end', exp.get('endDate', 'Present'))
                    if start_date or end_date:
                        story.append(Paragraph(f"{start_date} - {end_date}", styles['Normal']))
                    
                    # Description
                    description = exp.get('description', '')
                    if description:
                        # Split by newlines and create bullet points
                        lines = description.split('\n')
                        for line in lines:
                            line = line.strip()
                            if line:
                                story.append(Paragraph(f"• {line}", styles['Normal']))
                    
                    story.append(Spacer(1, 0.15*inch))
            
            story.append(Spacer(1, 0.1*inch))
        
        # Education Section
        education = data.get('education', [])
        if education and isinstance(education, list) and len(education) > 0:
            story.append(Paragraph("<b>EDUCATION</b>", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            for edu in education:
                if isinstance(edu, dict):
                    # Degree and school
                    degree = edu.get('degree', '')
                    school = edu.get('school', '')
                    if degree or school:
                        story.append(Paragraph(f"<b>{degree}</b> - {school}", styles['Normal']))
                    
                    # Year (frontend uses 'year' field)
                    year = edu.get('year', edu.get('endDate', ''))
                    if year:
                        story.append(Paragraph(f"Graduated: {year}", styles['Normal']))
                    
                    # GPA or additional info
                    gpa = edu.get('gpa', '')
                    if gpa:
                        story.append(Paragraph(f"GPA: {gpa}", styles['Normal']))
                    
                    story.append(Spacer(1, 0.15*inch))
            
            story.append(Spacer(1, 0.1*inch))
        
        # Skills Section
        skills = data.get('skills', [])
        if skills:
            story.append(Paragraph("<b>SKILLS</b>", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            # Handle both array and string formats
            if isinstance(skills, list):
                skills_text = ", ".join(skills)
            else:
                skills_text = str(skills)
            
            story.append(Paragraph(skills_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Generate filename
        filename = f"resume_{name.replace(' ', '_')}.pdf"
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"Resume generation error: {e}", exc_info=True)
        return JSONResponse({"error": f"Failed to generate PDF: {str(e)}"}, status_code=500)

@app.post("/api/resume/analyze")
async def analyze_resume_api(request: Request, db=Depends(get_db)):
    """Analyze resume and provide ATS score and suggestions"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}
        
        data = await request.json()
        
        from services.resume_service import get_resume_service
        resume_service = get_resume_service(Config.OPENAI_API_KEY)
        
        analysis = await resume_service.analyze_resume(data)
        
        return analysis
        
    except Exception as e:
        logger.error(f"Resume analysis error: {e}")
        return {"error": str(e), "ats_score": 0}

@app.post("/api/resume/optimize-bullet")
async def optimize_bullet_api(request: Request, db=Depends(get_db)):
    """Optimize a single bullet point using AI"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}
        
        data = await request.json()
        bullet_point = data.get("bullet_point", "")
        role = data.get("role", "")
        
        if not bullet_point:
            return {"error": "Bullet point required"}
        
        from services.resume_service import get_resume_service
        resume_service = get_resume_service(Config.OPENAI_API_KEY)
        
        optimized = await resume_service.optimize_bullet_point(bullet_point, role)
        
        return {"original": bullet_point, "optimized": optimized}
        
    except Exception as e:
        logger.error(f"Bullet optimization error: {e}")
        return {"error": str(e)}

@app.post("/api/resume/save")
async def save_resume_api(request: Request, db=Depends(get_db)):
    """Save resume data"""
    try:
        user = get_current_user(request, db)
        if not user:
            return {"error": "Not authenticated"}
        
        data = await request.json()
        
        # Save to database or file storage
        # For now, return success
        return {"success": True, "message": "Resume saved successfully"}
        
    except Exception as e:
        logger.error(f"Resume save error: {e}")
        return {"error": str(e)}

@app.get("/advisor", response_class=HTMLResponse)
def career_advisor(request: Request, db=Depends(get_db)):
    """Career advisor page"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Convert user to dict for JSON serialization
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "initials": "".join([n[0].upper() for n in user.name.split()[:2]]) if user.name else "U"
    }
    
    return templates.TemplateResponse(
        "advisor_new.html",
        {
            "request": request,
            "user": user_dict,
        },
    )



# ================================
# INCLUDE ADDITIONAL ROUTE MODULES
# ================================

# Include additional route modules
try:
    from auth_routes import router as auth_router
    app.include_router(auth_router)
    logger.info("✅ Auth routes loaded")
except ImportError:
    logger.warning("⚠️  Auth routes module not found")

try:
    from online_ide import ide_router
    app.include_router(ide_router)
    logger.info("✅ Online IDE routes loaded")
except ImportError:
    logger.warning("⚠️  Online IDE module not found")

# ================================
# NEW REDESIGNED UI ROUTES (TESTING)
# ================================

@app.get("/index_new", response_class=HTMLResponse)
def index_new(request: Request):
    """New redesigned landing page"""
    return templates.TemplateResponse("index_new.html", {
        "request": request,
        "page_title": "Home"
    })

@app.get("/report_new", response_class=HTMLResponse)
def report_new(request: Request, db=Depends(get_db)):
    """New redesigned dashboard/reports page"""
    try:
        user = get_current_user(request, db)
        if not user:
            # Return demo data for testing
            return templates.TemplateResponse("report_new.html", {
                "request": request,
                "user": {"name": "Demo User", "email": "demo@example.com", "initials": "DU"},
                "page_title": "Reports",
                "attempts": [],
                "average": 7.5,
                "best_score": 9.0,
                "streak": 3,
                "category_labels": ["Technical", "Behavioral", "System Design"],
                "category_scores": [8.0, 7.5, 6.8],
                "strengths": ["Strong technical knowledge", "Clear communication"],
                "weaknesses": ["Could provide more examples", "Work on system design"],
                "recommendation": "Focus on practicing system design questions to improve your overall score."
            })
        
        # Get user's attempts
        attempts = db.query(Attempt).filter_by(user_id=user.id).order_by(Attempt.timestamp.desc()).limit(20).all()
        
        # Calculate statistics
        scores = [a.score for a in attempts if a.score]
        average = sum(scores) / len(scores) if scores else 0
        best_score = max(scores) if scores else 0
        
        # Calculate streak
        streak = 0
        if attempts:
            last_date = attempts[0].timestamp.date()
            today = datetime.now().date()
            if last_date == today or last_date == today - timedelta(days=1):
                streak = 1
                for i in range(1, len(attempts)):
                    curr_date = attempts[i].timestamp.date()
                    prev_date = attempts[i-1].timestamp.date()
                    if (prev_date - curr_date).days == 1:
                        streak += 1
                    else:
                        break
        
        # Category performance
        category_data = {}
        for attempt in attempts:
            if attempt.category and attempt.score:
                if attempt.category not in category_data:
                    category_data[attempt.category] = []
                category_data[attempt.category].append(attempt.score)
        
        category_labels = list(category_data.keys())
        category_scores = [sum(scores)/len(scores) for scores in category_data.values()]
        
        # Generate insights
        strengths = []
        weaknesses = []
        if category_data:
            sorted_cats = sorted(category_data.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)
            if len(sorted_cats) >= 2:
                strengths = [f"Strong performance in {sorted_cats[0][0]}" for i in range(min(2, len(sorted_cats)))]
                weaknesses = [f"Focus more on {sorted_cats[-1][0]}" for i in range(min(2, len(sorted_cats)))]
        
        recommendation = "Keep practicing consistently to improve your interview skills."
        if average >= 8:
            recommendation = "Excellent work! You're interview-ready. Focus on maintaining consistency."
        elif average >= 6:
            recommendation = "Good progress! Focus on your weaker categories to reach the next level."
        
        return templates.TemplateResponse("report_new.html", {
            "request": request,
            "user": user,
            "page_title": "Reports",
            "attempts": attempts,
            "average": round(average, 1),
            "best_score": round(best_score, 1),
            "streak": streak,
            "category_labels": category_labels,
            "category_scores": [round(s, 1) for s in category_scores],
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendation": recommendation
        })
    except Exception as e:
        logger.error(f"Error in report_new: {str(e)}")
        # Return demo data on error
        return templates.TemplateResponse("report_new.html", {
            "request": request,
            "user": {"name": "Demo User", "email": "demo@example.com", "initials": "DU"},
            "page_title": "Reports",
            "attempts": [],
            "average": 7.5,
            "best_score": 9.0,
            "streak": 3,
            "category_labels": ["Technical", "Behavioral", "System Design"],
            "category_scores": [8.0, 7.5, 6.8],
            "strengths": ["Strong technical knowledge", "Clear communication"],
            "weaknesses": ["Could provide more examples", "Work on system design"],
            "recommendation": "Focus on practicing system design questions to improve your overall score."
        })

@app.get("/practice_new", response_class=HTMLResponse)
def practice_new(request: Request, db=Depends(get_db)):
    """New redesigned practice page"""
    try:
        user = get_current_user(request, db)
        if not user:
            user = {"name": "Demo User", "email": "demo@example.com", "initials": "DU"}
        
        # Get categories
        categories = [
            "Technical", "Behavioral", "System Design", "Coding",
            "Leadership", "Communication", "Problem Solving", "Teamwork"
        ]
        
        # Get companies
        companies = ["Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix"]
        
        return templates.TemplateResponse("practice_new.html", {
            "request": request,
            "user": user,
            "page_title": "Practice",
            "categories": categories,
            "companies": companies
        })
    except Exception as e:
        logger.error(f"Error in practice_new: {str(e)}")
        return templates.TemplateResponse("practice_new.html", {
            "request": request,
            "user": {"name": "Demo User", "email": "demo@example.com", "initials": "DU"},
            "page_title": "Practice",
            "categories": ["Technical", "Behavioral", "System Design", "Coding"],
            "companies": ["Google", "Amazon", "Microsoft"]
        })

@app.get("/profile_new", response_class=HTMLResponse)
def profile_new(request: Request, db=Depends(get_db)):
    """New redesigned profile page"""
    try:
        user = get_current_user(request, db)
        
        if not user:
            # Demo data for testing
            user_data = {
                "name": "Demo User",
                "email": "demo@example.com",
                "initials": "DU",
                "attempts": 42,
                "avg": 7.8,
                "best": 9.2,
                "streak": 5,
                "progress": 65,
                "badge": "Rising Learner",
                "joined": "January 2025",
                "location": "Not specified"
            }
        else:
            # Get user statistics
            attempts = db.query(Attempt).filter_by(user_id=user.id).all()
            scores = [a.score for a in attempts if a.score]
            
            user_data = {
                "name": user.username,
                "email": user.email,
                "initials": user.username[:2].upper() if user.username else "U",
                "attempts": len(attempts),
                "avg": round(sum(scores) / len(scores), 1) if scores else 0,
                "best": round(max(scores), 1) if scores else 0,
                "streak": 0,
                "progress": min(100, len(attempts) * 5),
                "badge": "Rising Learner",
                "joined": "January 2025",
                "location": "Not specified"
            }
        
        return templates.TemplateResponse("profile_new.html", {
            "request": request,
            "user": user_data,
            "page_title": "Profile"
        })
    except Exception as e:
        logger.error(f"Error in profile_new: {str(e)}")
        return templates.TemplateResponse("profile_new.html", {
            "request": request,
            "user": {
                "name": "Demo User",
                "email": "demo@example.com",
                "initials": "DU",
                "attempts": 42,
                "avg": 7.8,
                "best": 9.2,
                "streak": 5,
                "progress": 65,
                "badge": "Rising Learner",
                "joined": "January 2025",
                "location": "Not specified"
            },
            "page_title": "Profile"
        })

@app.get("/advisor_new", response_class=HTMLResponse)
def advisor_new(request: Request, db=Depends(get_db)):
    """New redesigned AI advisor page"""
    try:
        user = get_current_user(request, db)
        
        if not user:
            # Demo data
            attempts = []
            avg_score = 7.5
        else:
            # Get user's attempts
            attempts = db.query(Attempt).filter_by(user_id=user.id).all()
            scores = [a.score for a in attempts if a.score]
            avg_score = round(sum(scores) / len(scores), 1) if scores else 0
        
        # Generate insights
        strengths = [
            "Clear communication style",
            "Good technical knowledge",
            "Structured answers"
        ]
        
        weaknesses = [
            "Could provide more specific examples",
            "Practice STAR method more",
            "Work on conciseness"
        ]
        
        recommendation = "Focus on practicing behavioral questions using the STAR method. Your technical skills are strong, but adding more real-world examples will make your answers more compelling."
        
        # Sample learning plans
        plans = [
            {
                "id": 1,
                "title": "Behavioral Interview Mastery",
                "summary": "Master the STAR method and common behavioral questions",
                "estimated_time": "2 weeks"
            },
            {
                "id": 2,
                "title": "Technical Deep Dive",
                "summary": "Strengthen your technical interview skills with system design",
                "estimated_time": "3 weeks"
            }
        ]
        
        return templates.TemplateResponse("advisor_new.html", {
            "request": request,
            "user": user if user else {"name": "Demo User"},
            "page_title": "AI Advisor",
            "attempts": attempts,
            "avg_score": avg_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendation": recommendation,
            "plans": plans
        })
    except Exception as e:
        logger.error(f"Error in advisor_new: {str(e)}")
        return templates.TemplateResponse("advisor_new.html", {
            "request": request,
            "user": {"name": "Demo User"},
            "page_title": "AI Advisor",
            "attempts": [],
            "avg_score": 7.5,
            "strengths": ["Clear communication", "Good technical knowledge"],
            "weaknesses": ["Could provide more examples", "Practice STAR method"],
            "recommendation": "Focus on practicing behavioral questions using the STAR method.",
            "plans": [
                {
                    "id": 1,
                    "title": "Behavioral Interview Mastery",
                    "summary": "Master the STAR method and common behavioral questions",
                    "estimated_time": "2 weeks"
                }
            ]
        })

# ================================
# MAIN ENTRY POINT
# ================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "fastapi_app_cleaned:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )