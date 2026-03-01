"""
Bookmarking Service
Manages saved questions with notes, tags, and spaced repetition
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

logger = logging.getLogger(__name__)


class BookmarkingService:
    """Provides comprehensive question bookmarking with notes and organization"""
    
    @staticmethod
    def save_question(
        user_id: int,
        question: str,
        db: Session,
        company: str = None,
        category: str = None,
        notes: str = None,
        tags: List[str] = None,
        difficulty: str = None,
        priority: int = 0
    ) -> Dict:
        """
        Save a question with metadata
        
        Args:
            user_id: User ID
            question: Question text
            db: Database session
            company: Company name (optional)
            category: Category (optional)
            notes: User notes (optional)
            tags: List of tags (optional)
            difficulty: Difficulty level (optional)
            priority: Priority level 0-2 (optional)
            
        Returns:
            Dict with success status and saved question data
        """
        try:
            from fastapi_app_cleaned import SavedQuestion
            
            # Check if already saved
            existing = db.query(SavedQuestion).filter_by(
                user_id=user_id,
                question=question
            ).first()
            
            if existing:
                return {
                    "success": False,
                    "message": "Question already saved",
                    "question_id": existing.id
                }
            
            # Create new saved question
            tags_str = ",".join(tags) if tags else None
            
            saved_q = SavedQuestion(
                user_id=user_id,
                question=question,
                company=company,
                category=category,
                notes=notes,
                tags=tags_str,
                difficulty=difficulty,
                priority=priority
            )
            
            db.add(saved_q)
            db.commit()
            db.refresh(saved_q)
            
            return {
                "success": True,
                "message": "Question saved successfully",
                "question_id": saved_q.id,
                "question": {
                    "id": saved_q.id,
                    "question": saved_q.question,
                    "company": saved_q.company,
                    "category": saved_q.category,
                    "notes": saved_q.notes,
                    "tags": saved_q.tags.split(",") if saved_q.tags else [],
                    "difficulty": saved_q.difficulty,
                    "priority": saved_q.priority,
                    "timestamp": saved_q.timestamp.isoformat() if saved_q.timestamp else None
                }
            }
            
        except Exception as e:
            logger.error(f"Save question error: {e}")
            db.rollback()
            return {
                "success": False,
                "message": str(e)
            }
    
    @staticmethod
    def update_question(
        question_id: int,
        user_id: int,
        db: Session,
        notes: str = None,
        tags: List[str] = None,
        difficulty: str = None,
        priority: int = None,
        category: str = None,
        company: str = None
    ) -> Dict:
        """
        Update saved question metadata
        
        Args:
            question_id: Saved question ID
            user_id: User ID
            db: Database session
            notes: Updated notes (optional)
            tags: Updated tags (optional)
            difficulty: Updated difficulty (optional)
            priority: Updated priority (optional)
            category: Updated category (optional)
            company: Updated company (optional)
            
        Returns:
            Dict with success status
        """
        try:
            from fastapi_app_cleaned import SavedQuestion
            
            saved_q = db.query(SavedQuestion).filter_by(
                id=question_id,
                user_id=user_id
            ).first()
            
            if not saved_q:
                return {
                    "success": False,
                    "message": "Question not found"
                }
            
            # Update fields if provided
            if notes is not None:
                saved_q.notes = notes
            
            if tags is not None:
                saved_q.tags = ",".join(tags) if tags else None
            
            if difficulty is not None:
                saved_q.difficulty = difficulty
            
            if priority is not None:
                saved_q.priority = priority
            
            if category is not None:
                saved_q.category = category
            
            if company is not None:
                saved_q.company = company
            
            db.commit()
            
            return {
                "success": True,
                "message": "Question updated successfully",
                "question": {
                    "id": saved_q.id,
                    "question": saved_q.question,
                    "company": saved_q.company,
                    "category": saved_q.category,
                    "notes": saved_q.notes,
                    "tags": saved_q.tags.split(",") if saved_q.tags else [],
                    "difficulty": saved_q.difficulty,
                    "priority": saved_q.priority
                }
            }
            
        except Exception as e:
            logger.error(f"Update question error: {e}")
            db.rollback()
            return {
                "success": False,
                "message": str(e)
            }
    
    @staticmethod
    def delete_question(question_id: int, user_id: int, db: Session) -> Dict:
        """Delete a saved question"""
        try:
            from fastapi_app_cleaned import SavedQuestion
            
            saved_q = db.query(SavedQuestion).filter_by(
                id=question_id,
                user_id=user_id
            ).first()
            
            if not saved_q:
                return {
                    "success": False,
                    "message": "Question not found"
                }
            
            db.delete(saved_q)
            db.commit()
            
            return {
                "success": True,
                "message": "Question deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Delete question error: {e}")
            db.rollback()
            return {
                "success": False,
                "message": str(e)
            }
    
    @staticmethod
    def get_saved_questions(
        user_id: int,
        db: Session,
        category: str = None,
        company: str = None,
        tags: List[str] = None,
        difficulty: str = None,
        priority: int = None,
        search: str = None,
        sort_by: str = "timestamp",
        order: str = "desc"
    ) -> Dict:
        """
        Get saved questions with filtering and sorting
        
        Args:
            user_id: User ID
            db: Database session
            category: Filter by category (optional)
            company: Filter by company (optional)
            tags: Filter by tags (optional)
            difficulty: Filter by difficulty (optional)
            priority: Filter by priority (optional)
            search: Search in question text (optional)
            sort_by: Sort field (timestamp, priority, practice_count)
            order: Sort order (asc, desc)
            
        Returns:
            Dict with saved questions list
        """
        try:
            from fastapi_app_cleaned import SavedQuestion
            
            # Base query
            query = db.query(SavedQuestion).filter_by(user_id=user_id)
            
            # Apply filters
            if category:
                query = query.filter(SavedQuestion.category == category)
            
            if company:
                query = query.filter(SavedQuestion.company == company)
            
            if difficulty:
                query = query.filter(SavedQuestion.difficulty == difficulty)
            
            if priority is not None:
                query = query.filter(SavedQuestion.priority == priority)
            
            if tags:
                # Filter by any of the provided tags
                tag_filters = [SavedQuestion.tags.like(f"%{tag}%") for tag in tags]
                query = query.filter(or_(*tag_filters))
            
            if search:
                # Search in question text and notes
                search_filter = or_(
                    SavedQuestion.question.like(f"%{search}%"),
                    SavedQuestion.notes.like(f"%{search}%")
                )
                query = query.filter(search_filter)
            
            # Apply sorting
            sort_field = getattr(SavedQuestion, sort_by, SavedQuestion.timestamp)
            if order == "desc":
                query = query.order_by(sort_field.desc())
            else:
                query = query.order_by(sort_field.asc())
            
            # Execute query
            saved_questions = query.all()
            
            # Format results
            questions_list = []
            for sq in saved_questions:
                questions_list.append({
                    "id": sq.id,
                    "question": sq.question,
                    "company": sq.company,
                    "category": sq.category,
                    "notes": sq.notes,
                    "tags": sq.tags.split(",") if sq.tags else [],
                    "difficulty": sq.difficulty,
                    "priority": sq.priority,
                    "practice_count": sq.practice_count,
                    "last_practiced": sq.last_practiced.isoformat() if sq.last_practiced else None,
                    "timestamp": sq.timestamp.isoformat() if sq.timestamp else None
                })
            
            return {
                "success": True,
                "count": len(questions_list),
                "questions": questions_list
            }
            
        except Exception as e:
            logger.error(f"Get saved questions error: {e}")
            return {
                "success": False,
                "message": str(e),
                "questions": []
            }
    
    @staticmethod
    def get_question_by_id(question_id: int, user_id: int, db: Session) -> Dict:
        """Get a single saved question by ID"""
        try:
            from fastapi_app_cleaned import SavedQuestion
            
            saved_q = db.query(SavedQuestion).filter_by(
                id=question_id,
                user_id=user_id
            ).first()
            
            if not saved_q:
                return {
                    "success": False,
                    "message": "Question not found"
                }
            
            return {
                "success": True,
                "question": {
                    "id": saved_q.id,
                    "question": saved_q.question,
                    "company": saved_q.company,
                    "category": saved_q.category,
                    "notes": saved_q.notes,
                    "tags": saved_q.tags.split(",") if saved_q.tags else [],
                    "difficulty": saved_q.difficulty,
                    "priority": saved_q.priority,
                    "practice_count": saved_q.practice_count,
                    "last_practiced": saved_q.last_practiced.isoformat() if saved_q.last_practiced else None,
                    "timestamp": saved_q.timestamp.isoformat() if saved_q.timestamp else None
                }
            }
            
        except Exception as e:
            logger.error(f"Get question error: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    @staticmethod
    def mark_practiced(question_id: int, user_id: int, db: Session) -> Dict:
        """Mark a question as practiced (for spaced repetition)"""
        try:
            from fastapi_app_cleaned import SavedQuestion
            
            saved_q = db.query(SavedQuestion).filter_by(
                id=question_id,
                user_id=user_id
            ).first()
            
            if not saved_q:
                return {
                    "success": False,
                    "message": "Question not found"
                }
            
            saved_q.last_practiced = datetime.utcnow()
            saved_q.practice_count = (saved_q.practice_count or 0) + 1
            
            db.commit()
            
            return {
                "success": True,
                "message": "Question marked as practiced",
                "practice_count": saved_q.practice_count,
                "last_practiced": saved_q.last_practiced.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Mark practiced error: {e}")
            db.rollback()
            return {
                "success": False,
                "message": str(e)
            }
    
    @staticmethod
    def get_due_for_review(user_id: int, db: Session, days: int = 7) -> Dict:
        """
        Get questions due for review (spaced repetition)
        
        Args:
            user_id: User ID
            db: Database session
            days: Number of days since last practice
            
        Returns:
            Dict with questions due for review
        """
        try:
            from fastapi_app_cleaned import SavedQuestion
            
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Questions never practiced or not practiced in X days
            query = db.query(SavedQuestion).filter(
                SavedQuestion.user_id == user_id
            ).filter(
                or_(
                    SavedQuestion.last_practiced == None,
                    SavedQuestion.last_practiced < cutoff_date
                )
            ).order_by(SavedQuestion.priority.desc(), SavedQuestion.timestamp.asc())
            
            questions = query.all()
            
            questions_list = []
            for sq in questions:
                days_since = None
                if sq.last_practiced:
                    days_since = (datetime.utcnow() - sq.last_practiced).days
                
                questions_list.append({
                    "id": sq.id,
                    "question": sq.question,
                    "company": sq.company,
                    "category": sq.category,
                    "priority": sq.priority,
                    "practice_count": sq.practice_count,
                    "days_since_practice": days_since,
                    "last_practiced": sq.last_practiced.isoformat() if sq.last_practiced else None
                })
            
            return {
                "success": True,
                "count": len(questions_list),
                "questions": questions_list
            }
            
        except Exception as e:
            logger.error(f"Get due for review error: {e}")
            return {
                "success": False,
                "message": str(e),
                "questions": []
            }
    
    @staticmethod
    def get_statistics(user_id: int, db: Session) -> Dict:
        """Get statistics about saved questions"""
        try:
            from fastapi_app_cleaned import SavedQuestion
            from sqlalchemy import func
            
            # Total count
            total = db.query(func.count(SavedQuestion.id)).filter_by(user_id=user_id).scalar()
            
            # By category
            by_category = db.query(
                SavedQuestion.category,
                func.count(SavedQuestion.id)
            ).filter_by(user_id=user_id).group_by(SavedQuestion.category).all()
            
            # By difficulty
            by_difficulty = db.query(
                SavedQuestion.difficulty,
                func.count(SavedQuestion.id)
            ).filter_by(user_id=user_id).group_by(SavedQuestion.difficulty).all()
            
            # By priority
            by_priority = db.query(
                SavedQuestion.priority,
                func.count(SavedQuestion.id)
            ).filter_by(user_id=user_id).group_by(SavedQuestion.priority).all()
            
            # Most practiced
            most_practiced = db.query(SavedQuestion).filter_by(
                user_id=user_id
            ).order_by(SavedQuestion.practice_count.desc()).limit(5).all()
            
            # Never practiced
            never_practiced = db.query(func.count(SavedQuestion.id)).filter(
                SavedQuestion.user_id == user_id,
                SavedQuestion.practice_count == 0
            ).scalar()
            
            return {
                "success": True,
                "total": total,
                "by_category": {cat: count for cat, count in by_category if cat},
                "by_difficulty": {diff: count for diff, count in by_difficulty if diff},
                "by_priority": {pri: count for pri, count in by_priority},
                "most_practiced": [
                    {
                        "id": q.id,
                        "question": q.question[:100] + "..." if len(q.question) > 100 else q.question,
                        "practice_count": q.practice_count
                    }
                    for q in most_practiced
                ],
                "never_practiced": never_practiced
            }
            
        except Exception as e:
            logger.error(f"Get statistics error: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    @staticmethod
    def get_all_tags(user_id: int, db: Session) -> List[str]:
        """Get all unique tags used by user"""
        try:
            from fastapi_app_cleaned import SavedQuestion
            
            saved_questions = db.query(SavedQuestion).filter_by(user_id=user_id).all()
            
            all_tags = set()
            for sq in saved_questions:
                if sq.tags:
                    tags = sq.tags.split(",")
                    all_tags.update(tag.strip() for tag in tags if tag.strip())
            
            return sorted(list(all_tags))
            
        except Exception as e:
            logger.error(f"Get all tags error: {e}")
            return []


# Global instance
_bookmarking_service = None

def get_bookmarking_service() -> BookmarkingService:
    """Get or create global bookmarking service"""
    global _bookmarking_service
    if _bookmarking_service is None:
        _bookmarking_service = BookmarkingService()
    return _bookmarking_service
