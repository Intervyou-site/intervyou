"""
Practice Session Manager
Tracks user progress, answered questions, and difficulty levels
"""
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class PracticeSession:
    """Manages a single practice session for a user"""
    
    def __init__(self, user_id: int, category: str, company: Optional[str] = None):
        self.user_id = user_id
        self.category = category
        self.company = company
        self.answered_questions: Set[str] = set()  # Track answered questions
        self.difficulty_level = "beginner"  # beginner, intermediate, advanced
        self.questions_at_level = 0
        self.total_score = 0.0
        self.scores_history: List[float] = []
        self.started_at = datetime.now()
        
    def mark_question_answered(self, question: str, score: float):
        """Mark a question as answered and update difficulty tracking"""
        # Add question to answered set (use hash to avoid exact duplicates)
        question_hash = hash(question.lower().strip())
        self.answered_questions.add(str(question_hash))
        
        # Track score
        self.scores_history.append(score)
        self.total_score += score
        self.questions_at_level += 1
        
        logger.info(f"Question answered: score={score}, level={self.difficulty_level}, count={self.questions_at_level}")
    
    def is_question_answered(self, question: str) -> bool:
        """Check if a question has already been answered"""
        question_hash = str(hash(question.lower().strip()))
        return question_hash in self.answered_questions
    
    def get_average_score(self) -> float:
        """Get average score for current difficulty level"""
        if self.questions_at_level == 0:
            return 0.0
        return self.total_score / self.questions_at_level
    
    def should_promote(self) -> bool:
        """Check if user should be promoted to next difficulty level"""
        if self.questions_at_level < 3:  # Need at least 3 questions
            return False
        
        avg_score = self.get_average_score()
        
        if self.difficulty_level == "beginner" and avg_score >= 7.0:
            return True
        elif self.difficulty_level == "intermediate" and avg_score >= 8.0:
            return True
        
        return False
    
    def should_demote(self) -> bool:
        """Check if user should be demoted to previous difficulty level"""
        if self.questions_at_level < 5:  # Need at least 5 questions to demote
            return False
        
        avg_score = self.get_average_score()
        
        # Demote if struggling (avg score < 4.0)
        if avg_score < 4.0:
            return self.difficulty_level in ["intermediate", "advanced"]
        
        return False
    
    def promote_level(self) -> str:
        """Promote to next difficulty level"""
        old_level = self.difficulty_level
        
        if self.difficulty_level == "beginner":
            self.difficulty_level = "intermediate"
        elif self.difficulty_level == "intermediate":
            self.difficulty_level = "advanced"
        
        # Reset counters for new level
        self.questions_at_level = 0
        self.total_score = 0.0
        
        logger.info(f"🎉 User {self.user_id} promoted: {old_level} → {self.difficulty_level}")
        return self.difficulty_level
    
    def demote_level(self) -> str:
        """Demote to previous difficulty level"""
        old_level = self.difficulty_level
        
        if self.difficulty_level == "advanced":
            self.difficulty_level = "intermediate"
        elif self.difficulty_level == "intermediate":
            self.difficulty_level = "beginner"
        
        # Reset counters for new level
        self.questions_at_level = 0
        self.total_score = 0.0
        
        logger.info(f"⚠️ User {self.user_id} demoted: {old_level} → {self.difficulty_level}")
        return self.difficulty_level
    
    def get_current_difficulty(self) -> str:
        """Get current difficulty level"""
        return self.difficulty_level
    
    def get_appropriate_questions(self, all_questions: List[str], category: str) -> List[str]:
        """Filter questions appropriate for current difficulty level"""
        try:
            from services.difficulty_classifier import get_difficulty_classifier
            classifier = get_difficulty_classifier()
            
            # Get difficulty-specific questions first
            difficulty_questions = classifier.get_questions_by_difficulty(
                category, 
                self.difficulty_level, 
                count=20
            )
            
            if difficulty_questions:
                # Filter out already answered
                unanswered = [q for q in difficulty_questions if not self.is_question_answered(q)]
                if unanswered:
                    logger.info(f"✅ Found {len(unanswered)} unanswered {self.difficulty_level} questions")
                    return unanswered
            
            # Fallback: classify existing questions
            classified = classifier.classify_batch(all_questions, category)
            appropriate_questions = classified.get(self.difficulty_level, [])
            
            # Filter out answered
            unanswered = [q for q in appropriate_questions if not self.is_question_answered(q)]
            
            logger.info(f"✅ Classified {len(appropriate_questions)} as {self.difficulty_level}, {len(unanswered)} unanswered")
            return unanswered
            
        except Exception as e:
            logger.error(f"Error getting appropriate questions: {e}")
            # Fallback: return all unanswered
            return [q for q in all_questions if not self.is_question_answered(q)]
    
    def get_stats(self) -> Dict:
        """Get session statistics"""
        return {
            "category": self.category,
            "company": self.company,
            "difficulty_level": self.difficulty_level,
            "questions_answered": len(self.answered_questions),
            "questions_at_level": self.questions_at_level,
            "average_score": round(self.get_average_score(), 2),
            "total_questions": len(self.scores_history),
            "session_duration": (datetime.now() - self.started_at).seconds
        }


class PracticeSessionManager:
    """Manages practice sessions for all users"""
    
    def __init__(self):
        self.sessions: Dict[int, PracticeSession] = {}
        logger.info("✅ Practice Session Manager initialized")
    
    def get_or_create_session(
        self, 
        user_id: int, 
        category: str, 
        company: Optional[str] = None
    ) -> PracticeSession:
        """Get existing session or create new one"""
        
        # Check if session exists and matches category/company
        if user_id in self.sessions:
            session = self.sessions[user_id]
            
            # If category or company changed, create new session
            if session.category != category or session.company != company:
                logger.info(f"Creating new session for user {user_id}: {category} + {company}")
                session = PracticeSession(user_id, category, company)
                self.sessions[user_id] = session
            
            return session
        
        # Create new session
        logger.info(f"Creating first session for user {user_id}: {category} + {company}")
        session = PracticeSession(user_id, category, company)
        self.sessions[user_id] = session
        return session
    
    def get_session(self, user_id: int) -> Optional[PracticeSession]:
        """Get existing session"""
        return self.sessions.get(user_id)
    
    def clear_session(self, user_id: int):
        """Clear user's session"""
        if user_id in self.sessions:
            del self.sessions[user_id]
            logger.info(f"Session cleared for user {user_id}")
    
    def record_answer(
        self, 
        user_id: int, 
        question: str, 
        score: float
    ) -> Dict:
        """Record an answer and return updated session info"""
        session = self.sessions.get(user_id)
        
        if not session:
            logger.warning(f"No session found for user {user_id}")
            return {
                "difficulty_level": "beginner",
                "questions_at_level": 0,
                "promoted": False,
                "demoted": False
            }
        
        # Mark question as answered
        session.mark_question_answered(question, score)
        
        # Check for level changes
        promoted = False
        demoted = False
        
        if session.should_promote():
            session.promote_level()
            promoted = True
        elif session.should_demote():
            session.demote_level()
            demoted = True
        
        return {
            "difficulty_level": session.difficulty_level,
            "questions_at_level": session.questions_at_level,
            "average_score": session.get_average_score(),
            "total_answered": len(session.answered_questions),
            "promoted": promoted,
            "demoted": demoted,
            "stats": session.get_stats()
        }
    
    def is_question_answered(self, user_id: int, question: str) -> bool:
        """Check if user has already answered this question"""
        session = self.sessions.get(user_id)
        if not session:
            return False
        return session.is_question_answered(question)
    
    def get_unanswered_questions(
        self, 
        user_id: int, 
        questions: List[str]
    ) -> List[str]:
        """Filter out already answered questions"""
        session = self.sessions.get(user_id)
        if not session:
            return questions
        
        unanswered = [
            q for q in questions 
            if not session.is_question_answered(q)
        ]
        
        logger.info(f"Filtered questions: {len(questions)} → {len(unanswered)} unanswered")
        return unanswered
    
    def get_session_stats(self, user_id: int) -> Optional[Dict]:
        """Get session statistics"""
        session = self.sessions.get(user_id)
        if not session:
            return None
        return session.get_stats()


# Global instance
_session_manager = None

def get_session_manager() -> PracticeSessionManager:
    """Get or create the global session manager"""
    global _session_manager
    if _session_manager is None:
        _session_manager = PracticeSessionManager()
    return _session_manager
