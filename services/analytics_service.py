"""
Analytics Service
Calculates and provides user performance analytics
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Provides comprehensive user analytics"""
    
    @staticmethod
    def get_user_analytics(user_id: int, db: Session) -> Dict:
        """
        Generate comprehensive analytics for a user
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Dict with analytics data
        """
        try:
            # Import models here to avoid circular imports
            from fastapi_app_cleaned import User, Attempt
            
            # Get user
            user = db.query(User).filter_by(id=user_id).first()
            if not user:
                return {"error": "User not found"}
            
            # Get all attempts
            attempts = db.query(Attempt).filter_by(user_id=user_id).order_by(Attempt.timestamp).all()
            
            if not attempts:
                return {
                    "total_sessions": 0,
                    "average_score": 0,
                    "best_category": "-",
                    "best_category_score": 0,
                    "streak": 0,
                    "sessions_change": 0,
                    "score_change": 0,
                    "dates": [],
                    "scores": [],
                    "categories": [],
                    "category_counts": [],
                    "score_distribution": [0, 0, 0, 0, 0],
                    "recent_activity": []
                }
            
            # Basic stats
            total_sessions = len(attempts)
            scores = [float(a.score) for a in attempts if a.score]
            average_score = sum(scores) / len(scores) if scores else 0
            
            # Score distribution for chart (0-2, 2-4, 4-6, 6-8, 8-10)
            score_distribution = [0, 0, 0, 0, 0]
            for score in scores:
                if score < 2:
                    score_distribution[0] += 1
                elif score < 4:
                    score_distribution[1] += 1
                elif score < 6:
                    score_distribution[2] += 1
                elif score < 8:
                    score_distribution[3] += 1
                else:
                    score_distribution[4] += 1
            
            # Category analysis
            by_category = {}
            for attempt in attempts:
                category = attempt.category if hasattr(attempt, 'category') and attempt.category else AnalyticsService._extract_category(attempt.question)
                
                if category not in by_category:
                    by_category[category] = {
                        "count": 0,
                        "total_score": 0,
                        "scores": []
                    }
                
                by_category[category]["count"] += 1
                if attempt.score:
                    by_category[category]["total_score"] += attempt.score
                    by_category[category]["scores"].append(float(attempt.score))
            
            # Calculate category averages and find best
            best_category = "-"
            best_category_score = 0
            categories = []
            category_counts = []
            
            for category, data in by_category.items():
                avg = data["total_score"] / data["count"] if data["count"] > 0 else 0
                categories.append(category)
                category_counts.append(data["count"])
                
                if avg > best_category_score:
                    best_category = category
                    best_category_score = avg
            
            # Performance over time (dates and scores)
            dates = []
            perf_scores = []
            for attempt in attempts:
                if attempt.timestamp and attempt.score:
                    dates.append(attempt.timestamp.strftime("%m/%d"))
                    perf_scores.append(float(attempt.score))
            
            # Calculate streak
            streak = AnalyticsService._calculate_streak(attempts)
            
            # Calculate changes (compare last week to previous week)
            now = datetime.now()
            one_week_ago = now - timedelta(days=7)
            two_weeks_ago = now - timedelta(days=14)
            
            last_week_attempts = [a for a in attempts if a.timestamp and a.timestamp >= one_week_ago]
            prev_week_attempts = [a for a in attempts if a.timestamp and two_weeks_ago <= a.timestamp < one_week_ago]
            
            sessions_change = 0
            if len(prev_week_attempts) > 0:
                sessions_change = int(((len(last_week_attempts) - len(prev_week_attempts)) / len(prev_week_attempts)) * 100)
            elif len(last_week_attempts) > 0:
                sessions_change = 100
            
            score_change = 0
            if last_week_attempts and prev_week_attempts:
                last_week_avg = sum(a.score for a in last_week_attempts if a.score) / len(last_week_attempts)
                prev_week_avg = sum(a.score for a in prev_week_attempts if a.score) / len(prev_week_attempts)
                if prev_week_avg > 0:
                    score_change = int(((last_week_avg - prev_week_avg) / prev_week_avg) * 100)
            
            # Recent activity (last 10 attempts)
            recent_activity = []
            for attempt in attempts[-10:]:
                if attempt.timestamp and attempt.score:
                    category = attempt.category if hasattr(attempt, 'category') and attempt.category else AnalyticsService._extract_category(attempt.question)
                    recent_activity.append({
                        "category": category,
                        "score": float(attempt.score),
                        "date": attempt.timestamp.strftime("%b %d, %Y at %I:%M %p")
                    })
            recent_activity.reverse()  # Most recent first
            
            return {
                "total_sessions": total_sessions,
                "average_score": round(average_score, 1),
                "best_category": best_category,
                "best_category_score": round(best_category_score, 1),
                "streak": streak,
                "sessions_change": sessions_change,
                "score_change": score_change,
                "dates": dates,
                "scores": perf_scores,
                "categories": categories,
                "category_counts": category_counts,
                "score_distribution": score_distribution,
                "recent_activity": recent_activity
            }
            
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return {
                "total_sessions": 0,
                "average_score": 0,
                "best_category": "-",
                "best_category_score": 0,
                "streak": 0,
                "sessions_change": 0,
                "score_change": 0,
                "dates": [],
                "scores": [],
                "categories": [],
                "category_counts": [],
                "score_distribution": [0, 0, 0, 0, 0],
                "recent_activity": [],
                "error": str(e)
            }
    
    @staticmethod
    def _extract_category(question: str) -> str:
        """Extract category from question text (simplified)"""
        if not question:
            return "General"
        
        question_lower = question.lower()
        
        # Category keywords
        categories = {
            "Python": ["python", "decorator", "list comprehension", "generator"],
            "JavaScript": ["javascript", "js", "react", "node"],
            "Web Development": ["html", "css", "web", "frontend", "backend", "api", "rest"],
            "Data Structures": ["array", "linked list", "tree", "graph", "hash", "stack", "queue"],
            "Algorithms": ["algorithm", "sort", "search", "complexity", "big o"],
            "System Design": ["design", "architecture", "scale", "distributed", "microservice"],
            "Database": ["database", "sql", "query", "index", "transaction"],
            "Behavioral": ["tell me about", "describe a time", "give an example", "why do you"],
            "Leadership": ["leadership", "led a team", "managed", "mentor"],
            "Machine Learning": ["machine learning", "ml", "model", "training", "neural"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in question_lower for keyword in keywords):
                return category
        
        return "General"
    
    @staticmethod
    def _calculate_streak(attempts: List) -> int:
        """Calculate practice streak (consecutive days)"""
        if not attempts:
            return 0
        
        # Get unique practice dates
        dates = sorted(set(a.timestamp.date() for a in attempts if a.timestamp), reverse=True)
        
        if not dates:
            return 0
        
        # Check if practiced today
        today = datetime.now().date()
        if dates[0] != today:
            # Check if practiced yesterday (streak continues)
            if dates[0] != today - timedelta(days=1):
                return 0
        
        # Count consecutive days
        streak = 1
        for i in range(len(dates) - 1):
            diff = (dates[i] - dates[i + 1]).days
            if diff == 1:
                streak += 1
            else:
                break
        
        return streak
    
    @staticmethod
    def _analyze_time_patterns(attempts: List) -> Dict:
        """Analyze practice time patterns"""
        if not attempts:
            return {}
        
        # Practice by day of week
        by_day = {i: 0 for i in range(7)}  # 0=Monday, 6=Sunday
        
        # Practice by hour
        by_hour = {i: 0 for i in range(24)}
        
        for attempt in attempts:
            if attempt.timestamp:
                by_day[attempt.timestamp.weekday()] += 1
                by_hour[attempt.timestamp.hour] += 1
        
        # Find most active day
        most_active_day = max(by_day.items(), key=lambda x: x[1])
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Find most active hour
        most_active_hour = max(by_hour.items(), key=lambda x: x[1])
        
        return {
            "most_active_day": day_names[most_active_day[0]],
            "most_active_hour": f"{most_active_hour[0]:02d}:00",
            "by_day": by_day,
            "by_hour": by_hour
        }
    
    @staticmethod
    def _calculate_improvement(attempts: List) -> Dict:
        """Calculate improvement rate"""
        if len(attempts) < 2:
            return {"rate": 0, "trend": "neutral"}
        
        # Compare first 5 and last 5 attempts
        first_batch = attempts[:5] if len(attempts) >= 5 else attempts[:len(attempts)//2]
        last_batch = attempts[-5:] if len(attempts) >= 5 else attempts[len(attempts)//2:]
        
        first_avg = sum(a.score for a in first_batch if a.score) / len(first_batch)
        last_avg = sum(a.score for a in last_batch if a.score) / len(last_batch)
        
        improvement_rate = ((last_avg - first_avg) / first_avg * 100) if first_avg > 0 else 0
        
        if improvement_rate > 10:
            trend = "improving"
        elif improvement_rate < -10:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "rate": round(improvement_rate, 1),
            "trend": trend,
            "first_avg": round(first_avg, 2),
            "last_avg": round(last_avg, 2)
        }
    
    @staticmethod
    def _get_recent_activity(attempts: List, days: int = 7) -> List[Dict]:
        """Get recent activity summary"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent = [a for a in attempts if a.timestamp and a.timestamp >= cutoff_date]
        
        # Group by date
        by_date = {}
        for attempt in recent:
            date_str = attempt.timestamp.strftime("%Y-%m-%d")
            if date_str not in by_date:
                by_date[date_str] = {
                    "date": date_str,
                    "count": 0,
                    "avg_score": 0,
                    "total_score": 0
                }
            by_date[date_str]["count"] += 1
            if attempt.score:
                by_date[date_str]["total_score"] += attempt.score
        
        # Calculate averages
        for date_str in by_date:
            count = by_date[date_str]["count"]
            total = by_date[date_str]["total_score"]
            by_date[date_str]["avg_score"] = round(total / count, 2) if count > 0 else 0
        
        # Convert to list and sort
        activity = sorted(by_date.values(), key=lambda x: x["date"])
        
        return activity


# Global instance
_analytics_service = None

def get_analytics_service() -> AnalyticsService:
    """Get or create global analytics service"""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = AnalyticsService()
    return _analytics_service
