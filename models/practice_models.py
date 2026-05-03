"""
Database Models for Enhanced Practice Features

New tables for:
- Aptitude questions and attempts
- MCQ attempts
- Coding challenge scores
- Daily practice streak
- Rapid fire scores
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

# Import Base from main app (will be imported in fastapi_app_cleaned.py)
# from fastapi_app_cleaned import Base

def create_practice_models(Base):
    """
    Factory function to create practice models with the given Base class
    This allows us to use the same Base as the main application
    """
    
    class AptitudeQuestion(Base):
        """Model for aptitude questions"""
        __tablename__ = "aptitude_question"
        
        id = Column(Integer, primary_key=True)
        category = Column(String(100), nullable=False)  # Quantitative, Logical, etc.
        question = Column(Text, nullable=False)
        options = Column(JSON, nullable=False)  # List of options
        correct_answer = Column(String(500), nullable=False)
        explanation = Column(Text, nullable=True)
        difficulty = Column(String(20), default="intermediate")  # beginner, intermediate, advanced
        created_at = Column(DateTime, default=datetime.utcnow)
        
        # Relationships
        attempts = relationship("AptitudeAttempt", back_populates="question", cascade="all, delete-orphan")
    
    class AptitudeAttempt(Base):
        """Model for user's aptitude question attempts"""
        __tablename__ = "aptitude_attempt"
        
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
        question_id = Column(Integer, ForeignKey("aptitude_question.id"), nullable=False)
        user_answer = Column(String(500), nullable=False)
        is_correct = Column(Boolean, nullable=False)
        time_taken = Column(Integer, nullable=True)  # Time in seconds
        timestamp = Column(DateTime, default=datetime.utcnow)
        
        # Relationships
        question = relationship("AptitudeQuestion", back_populates="attempts")
    
    class MCQAttempt(Base):
        """Model for MCQ mode attempts (for any category)"""
        __tablename__ = "mcq_attempt"
        
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
        category = Column(String(100), nullable=False)
        question = Column(Text, nullable=False)
        options = Column(JSON, nullable=False)
        user_answer = Column(String(500), nullable=False)
        correct_answer = Column(String(500), nullable=False)
        is_correct = Column(Boolean, nullable=False)
        difficulty = Column(String(20), default="intermediate")
        time_taken = Column(Integer, nullable=True)
        timestamp = Column(DateTime, default=datetime.utcnow)
    
    class CodingChallengeScore(Base):
        """Model for coding challenge attempts and scores"""
        __tablename__ = "coding_challenge_score"
        
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
        challenge_id = Column(String(100), nullable=False)
        challenge_title = Column(String(200), nullable=False)
        difficulty = Column(String(20), nullable=False)
        language = Column(String(50), default="python")
        code_submitted = Column(Text, nullable=False)
        test_cases_passed = Column(Integer, default=0)
        total_test_cases = Column(Integer, default=0)
        execution_time = Column(Float, nullable=True)  # Time in milliseconds
        memory_used = Column(Float, nullable=True)  # Memory in MB
        is_solved = Column(Boolean, default=False)
        timestamp = Column(DateTime, default=datetime.utcnow)
    
    class DailyStreak(Base):
        """Model for tracking daily practice streaks"""
        __tablename__ = "daily_streak"
        
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
        current_streak = Column(Integer, default=0)
        longest_streak = Column(Integer, default=0)
        last_practice_date = Column(DateTime, nullable=True)
        total_practice_days = Column(Integer, default=0)
        streak_data = Column(JSON, nullable=True)  # Store daily practice history
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    class RapidFireScore(Base):
        """Model for rapid fire round scores"""
        __tablename__ = "rapid_fire_score"
        
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
        category = Column(String(100), nullable=False)
        questions_attempted = Column(Integer, default=0)
        correct_answers = Column(Integer, default=0)
        total_time = Column(Integer, nullable=False)  # Total time in seconds
        average_time_per_question = Column(Float, nullable=True)
        accuracy = Column(Float, nullable=True)  # Percentage
        points_earned = Column(Integer, default=0)
        timestamp = Column(DateTime, default=datetime.utcnow)
    
    class PracticeRecommendation(Base):
        """Model for storing smart practice recommendations"""
        __tablename__ = "practice_recommendation"
        
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
        category = Column(String(100), nullable=False)
        subcategory = Column(String(100), nullable=True)
        reason = Column(Text, nullable=False)  # Why this is recommended
        priority = Column(Integer, default=0)  # Higher = more important
        is_active = Column(Boolean, default=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        completed_at = Column(DateTime, nullable=True)
    
    # Return all models as a dictionary
    return {
        "AptitudeQuestion": AptitudeQuestion,
        "AptitudeAttempt": AptitudeAttempt,
        "MCQAttempt": MCQAttempt,
        "CodingChallengeScore": CodingChallengeScore,
        "DailyStreak": DailyStreak,
        "RapidFireScore": RapidFireScore,
        "PracticeRecommendation": PracticeRecommendation
    }
