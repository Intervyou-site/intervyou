"""
Daily Streak and Practice Recommendation Service

Handles:
- Daily practice streak tracking
- Streak maintenance and updates
- Smart practice recommendations based on user history
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class StreakService:
    """Service for managing daily practice streaks"""
    
    def __init__(self, db: Session, daily_streak_model, attempt_model):
        self.db = db
        self.DailyStreak = daily_streak_model
        self.Attempt = attempt_model
    
    def get_or_create_streak(self, user_id: int) -> Any:
        """Get or create streak record for user"""
        streak = self.db.query(self.DailyStreak).filter_by(user_id=user_id).first()
        
        if not streak:
            streak = self.DailyStreak(
                user_id=user_id,
                current_streak=0,
                longest_streak=0,
                total_practice_days=0,
                streak_data={}
            )
            self.db.add(streak)
            self.db.commit()
        
        return streak
    
    def update_streak(self, user_id: int) -> Dict[str, Any]:
        """
        Update user's practice streak
        
        Returns:
            Dictionary with streak info and whether it was updated
        """
        streak = self.get_or_create_streak(user_id)
        today = datetime.utcnow().date()
        
        # If already practiced today, no update needed
        if streak.last_practice_date and streak.last_practice_date.date() == today:
            return {
                "updated": False,
                "current_streak": streak.current_streak,
                "longest_streak": streak.longest_streak,
                "message": "Already practiced today!"
            }
        
        # Check if streak continues or breaks
        if streak.last_practice_date:
            last_date = streak.last_practice_date.date()
            days_diff = (today - last_date).days
            
            if days_diff == 1:
                # Streak continues
                streak.current_streak += 1
            elif days_diff > 1:
                # Streak broken
                streak.current_streak = 1
        else:
            # First practice
            streak.current_streak = 1
        
        # Update longest streak if current is higher
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
        
        # Update last practice date and total days
        streak.last_practice_date = datetime.utcnow()
        streak.total_practice_days += 1
        
        # Update streak data (calendar view)
        streak_data = streak.streak_data or {}
        date_key = today.isoformat()
        streak_data[date_key] = {
            "practiced": True,
            "streak_day": streak.current_streak
        }
        streak.streak_data = streak_data
        streak.updated_at = datetime.utcnow()
        
        self.db.commit()
        
        return {
            "updated": True,
            "current_streak": streak.current_streak,
            "longest_streak": streak.longest_streak,
            "total_days": streak.total_practice_days,
            "message": f"🔥 {streak.current_streak} day streak!"
        }
    
    def get_streak_info(self, user_id: int) -> Dict[str, Any]:
        """Get current streak information for user"""
        streak = self.get_or_create_streak(user_id)
        today = datetime.utcnow().date()
        
        # Check if streak is still active
        is_active = False
        if streak.last_practice_date:
            last_date = streak.last_practice_date.date()
            days_diff = (today - last_date).days
            is_active = days_diff <= 1
        
        # Get last 7 days for calendar widget
        calendar_days = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            date_key = date.isoformat()
            streak_data = streak.streak_data or {}
            
            calendar_days.append({
                "date": date.isoformat(),
                "day_name": date.strftime("%a"),
                "practiced": date_key in streak_data,
                "is_today": date == today
            })
        
        return {
            "current_streak": streak.current_streak if is_active else 0,
            "longest_streak": streak.longest_streak,
            "total_practice_days": streak.total_practice_days,
            "last_practice_date": streak.last_practice_date.isoformat() if streak.last_practice_date else None,
            "is_active": is_active,
            "calendar_days": calendar_days
        }
    
    def get_streak_calendar(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Get practice calendar for last N days"""
        streak = self.get_or_create_streak(user_id)
        today = datetime.utcnow().date()
        
        calendar = []
        streak_data = streak.streak_data or {}
        
        for i in range(days - 1, -1, -1):
            date = today - timedelta(days=i)
            date_key = date.isoformat()
            
            calendar.append({
                "date": date_key,
                "day": date.day,
                "month": date.strftime("%b"),
                "practiced": date_key in streak_data,
                "is_today": date == today
            })
        
        return calendar


class RecommendationService:
    """Service for generating smart practice recommendations"""
    
    def __init__(self, db: Session, attempt_model, mcq_attempt_model, aptitude_attempt_model):
        self.db = db
        self.Attempt = attempt_model
        self.MCQAttempt = mcq_attempt_model
        self.AptitudeAttempt = aptitude_attempt_model
    
    def get_recommendations(self, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Generate smart practice recommendations based on user history
        
        Args:
            user_id: User ID
            limit: Maximum number of recommendations
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Analyze interview question attempts
        interview_recs = self._analyze_interview_attempts(user_id)
        recommendations.extend(interview_recs)
        
        # Analyze MCQ attempts
        mcq_recs = self._analyze_mcq_attempts(user_id)
        recommendations.extend(mcq_recs)
        
        # Analyze aptitude attempts
        aptitude_recs = self._analyze_aptitude_attempts(user_id)
        recommendations.extend(aptitude_recs)
        
        # Sort by priority and return top N
        recommendations.sort(key=lambda x: x.get("priority", 0), reverse=True)
        return recommendations[:limit]
    
    def _analyze_interview_attempts(self, user_id: int) -> List[Dict[str, Any]]:
        """Analyze interview question attempts and generate recommendations"""
        try:
            # Get recent attempts
            recent_attempts = self.db.query(self.Attempt).filter_by(user_id=user_id).order_by(
                self.Attempt.timestamp.desc()
            ).limit(20).all()
            
            if not recent_attempts:
                # Don't recommend "General" - let other methods handle recommendations
                return []
            
            # Calculate average scores by category (if feedback contains scores)
            category_scores = {}
            for attempt in recent_attempts:
                # Try to extract category from question or use a default
                category = "Python"  # Default to Python instead of General
                
                if category not in category_scores:
                    category_scores[category] = []
                
                if attempt.score:
                    category_scores[category].append(attempt.score)
            
            # Find weak categories (average score < 6)
            recommendations = []
            for category, scores in category_scores.items():
                # Skip "General" and "Quantitative Aptitude" categories
                if category in ["General", "Quantitative Aptitude"]:
                    continue
                    
                if scores:
                    avg_score = sum(scores) / len(scores)
                    if avg_score < 6:
                        recommendations.append({
                            "category": category,
                            "type": "interview",
                            "reason": f"Average score: {avg_score:.1f}/10 - needs improvement",
                            "priority": 10 - int(avg_score)
                        })
            
            return recommendations
        except Exception as e:
            logger.error(f"Error analyzing interview attempts: {e}")
            return []
    
    def _analyze_mcq_attempts(self, user_id: int) -> List[Dict[str, Any]]:
        """Analyze MCQ attempts and generate recommendations"""
        try:
            # Get recent MCQ attempts
            recent_mcq = self.db.query(self.MCQAttempt).filter_by(user_id=user_id).order_by(
                self.MCQAttempt.timestamp.desc()
            ).limit(20).all()
            
            if not recent_mcq:
                return []
            
            # Calculate accuracy by category
            category_stats = {}
            for attempt in recent_mcq:
                category = attempt.category
                if category not in category_stats:
                    category_stats[category] = {"correct": 0, "total": 0}
                
                category_stats[category]["total"] += 1
                if attempt.is_correct:
                    category_stats[category]["correct"] += 1
            
            # Find categories with low accuracy (< 60%)
            recommendations = []
            for category, stats in category_stats.items():
                # Skip "Quantitative Aptitude" - it's handled by aptitude recommendations
                if category == "Quantitative Aptitude":
                    continue
                    
                accuracy = (stats["correct"] / stats["total"]) * 100
                if accuracy < 60:
                    recommendations.append({
                        "category": category,
                        "type": "mcq",
                        "reason": f"MCQ accuracy: {accuracy:.1f}% - practice more",
                        "priority": 8
                    })
            
            return recommendations
        except Exception as e:
            logger.error(f"Error analyzing MCQ attempts: {e}")
            return []
    
    def _analyze_aptitude_attempts(self, user_id: int) -> List[Dict[str, Any]]:
        """Analyze aptitude attempts and generate recommendations"""
        try:
            # Get recent aptitude attempts
            recent_aptitude = self.db.query(self.AptitudeAttempt).filter_by(user_id=user_id).order_by(
                self.AptitudeAttempt.timestamp.desc()
            ).limit(20).all()
            
            if not recent_aptitude:
                return [{
                    "category": "Aptitude",
                    "subcategory": "Quantitative Aptitude",
                    "type": "aptitude",
                    "reason": "Build your quantitative skills",
                    "priority": 6
                }]
            
            # Get question categories through relationship
            category_stats = {}
            for attempt in recent_aptitude:
                if attempt.question:
                    category = attempt.question.category
                    if category not in category_stats:
                        category_stats[category] = {"correct": 0, "total": 0}
                    
                    category_stats[category]["total"] += 1
                    if attempt.is_correct:
                        category_stats[category]["correct"] += 1
            
            # Find weak aptitude categories (< 50% accuracy)
            recommendations = []
            for category, stats in category_stats.items():
                accuracy = (stats["correct"] / stats["total"]) * 100
                if accuracy < 50:
                    recommendations.append({
                        "category": "Aptitude",
                        "subcategory": category,
                        "type": "aptitude",
                        "reason": f"{category} accuracy: {accuracy:.1f}% - needs focus",
                        "priority": 9
                    })
            
            return recommendations
        except Exception as e:
            logger.error(f"Error analyzing aptitude attempts: {e}")
            return []
