"""
Example: How to protect your existing endpoints with API keys

Add these to your fastapi_app.py or create a new router file
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api_key_system import get_current_user_from_api_key
from fastapi_app import get_db, User

router = APIRouter(prefix="/api/v1", tags=["Protected API"])


# Example 1: Get user profile
@router.get("/profile")
async def get_profile(user: User = Depends(get_current_user_from_api_key)):
    """
    Get current user profile using API key
    
    Usage:
        curl -H "X-API-Key: your_key" http://localhost:8000/api/v1/profile
    """
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "total_score": user.total_score,
        "attempts": user.attempts,
        "badge": user.badge
    }


# Example 2: Get user's interview history
@router.get("/interview-history")
async def get_interview_history(
    user: User = Depends(get_current_user_from_api_key),
    db: Session = Depends(get_db)
):
    """
    Get user's interview attempt history
    
    Usage:
        curl -H "X-API-Key: your_key" http://localhost:8000/api/v1/interview-history
    """
    from fastapi_app import Attempt
    
    attempts = db.query(Attempt).filter(
        Attempt.user_id == user.id
    ).order_by(Attempt.timestamp.desc()).limit(10).all()
    
    return {
        "user": user.name,
        "total_attempts": len(attempts),
        "history": [
            {
                "question": a.question,
                "score": a.score,
                "feedback": a.feedback,
                "timestamp": a.timestamp.isoformat()
            }
            for a in attempts
        ]
    }


# Example 3: Submit interview answer via API
@router.post("/submit-answer")
async def submit_answer_api(
    question: str,
    answer: str,
    user: User = Depends(get_current_user_from_api_key),
    db: Session = Depends(get_db)
):
    """
    Submit an interview answer via API
    
    Usage:
        curl -X POST -H "X-API-Key: your_key" \
             -H "Content-Type: application/json" \
             -d '{"question":"What is Python?","answer":"Python is..."}' \
             http://localhost:8000/api/v1/submit-answer
    """
    from fastapi_app import Attempt
    
    # Simple scoring (you can use your existing evaluation logic)
    score = min(100, len(answer.split()) * 2)  # Simple word count scoring
    
    # Save attempt
    attempt = Attempt(
        user_id=user.id,
        question=question,
        score=score,
        feedback=f"Answer submitted via API. Score: {score}/100"
    )
    db.add(attempt)
    
    # Update user stats
    user.attempts += 1
    user.total_score += score
    
    db.commit()
    
    return {
        "success": True,
        "score": score,
        "total_attempts": user.attempts,
        "average_score": user.total_score / user.attempts
    }


# Example 4: Get saved questions
@router.get("/saved-questions")
async def get_saved_questions_api(
    user: User = Depends(get_current_user_from_api_key),
    db: Session = Depends(get_db)
):
    """
    Get user's saved questions
    
    Usage:
        curl -H "X-API-Key: your_key" http://localhost:8000/api/v1/saved-questions
    """
    from fastapi_app import SavedQuestion
    
    questions = db.query(SavedQuestion).filter(
        SavedQuestion.user_id == user.id
    ).all()
    
    return {
        "count": len(questions),
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "company": q.company,
                "saved_at": q.timestamp.isoformat()
            }
            for q in questions
        ]
    }


# Example 5: Generate interview question
@router.get("/generate-question")
async def generate_question_api(
    category: str = "Python",
    user: User = Depends(get_current_user_from_api_key)
):
    """
    Generate a new interview question
    
    Usage:
        curl -H "X-API-Key: your_key" \
             "http://localhost:8000/api/v1/generate-question?category=Python"
    """
    from fastapi_app import LOCAL_QUESTION_BANK
    import random
    
    questions = LOCAL_QUESTION_BANK.get(category, LOCAL_QUESTION_BANK["Python"])
    question = random.choice(questions)
    
    return {
        "category": category,
        "question": question,
        "user": user.name
    }


# To use this router, add to your fastapi_app.py:
# from example_protected_endpoints import router as protected_router
# app.include_router(protected_router)
