"""
Answer Hints Service
Provides progressive hints for interview questions
"""
import logging
from typing import Dict, List, Optional
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class AnswerHintsService:
    """Provides progressive hints for interview questions"""
    
    def __init__(self):
        self.hints_database = self._load_hints()
        self.hint_penalty = 0.5  # Score reduction per hint used
    
    def _load_hints(self) -> Dict[str, Dict]:
        """Load all question hints"""
        return {
            # BEHAVIORAL QUESTIONS
            "tell_me_about_yourself": {
                "question": "Tell me about yourself",
                "hints": [
                    "💡 Hint 1: Start with your current role and what you do day-to-day",
                    "💡 Hint 2: Mention your background - education and years of experience",
                    "💡 Hint 3: End with why you're interested in THIS specific opportunity"
                ],
                "keywords": ["tell me about yourself", "introduce yourself", "walk me through your background"]
            },
            
            "challenging_project": {
                "question": "Describe a challenging project",
                "hints": [
                    "💡 Hint 1: Use the STAR method - Start with the Situation (what was the project?)",
                    "💡 Hint 2: Describe your Task (what was YOUR specific role and challenge?)",
                    "💡 Hint 3: Explain your Actions (what steps did you take? Be specific)",
                    "💡 Hint 4: Share the Results (what was the outcome? Include metrics if possible)"
                ],
                "keywords": ["challenging project", "difficult project", "complex project", "hardest project"]
            },
            
            "time_you_failed": {
                "question": "Tell me about a time you failed",
                "hints": [
                    "💡 Hint 1: Choose a real failure, but not a catastrophic one",
                    "💡 Hint 2: Explain what went wrong and why (take ownership)",
                    "💡 Hint 3: Focus heavily on what you LEARNED from the experience",
                    "💡 Hint 4: Show how you've improved since then with specific examples"
                ],
                "keywords": ["time you failed", "biggest failure", "mistake you made", "when things went wrong"]
            },
            
            "conflict_with_teammate": {
                "question": "Describe a conflict with a teammate",
                "hints": [
                    "💡 Hint 1: Describe the conflict objectively (avoid blaming the other person)",
                    "💡 Hint 2: Explain how you approached the situation (show emotional intelligence)",
                    "💡 Hint 3: Describe the resolution (focus on finding win-win solutions)",
                    "💡 Hint 4: Share the positive outcome (improved relationship, better results)"
                ],
                "keywords": ["conflict with teammate", "disagreement", "difficult coworker", "team conflict"]
            },
            
            "why_this_company": {
                "question": "Why do you want to work here?",
                "hints": [
                    "💡 Hint 1: Mention specific products, projects, or values that resonate with you",
                    "💡 Hint 2: Connect your skills and experience to their needs",
                    "💡 Hint 3: Show you've done research (mention recent news, blog posts, etc.)",
                    "💡 Hint 4: Explain how you can contribute and make an impact"
                ],
                "keywords": ["why this company", "why do you want to work here", "why us", "what interests you"]
            },
            
            # TECHNICAL QUESTIONS
            "explain_python_decorators": {
                "question": "What are Python decorators?",
                "hints": [
                    "💡 Hint 1: Think about functions that modify other functions",
                    "💡 Hint 2: Mention the @ symbol syntax",
                    "💡 Hint 3: Give common examples like @staticmethod, @property, @classmethod"
                ],
                "keywords": ["python decorators", "what are decorators", "explain decorators"]
            },
            
            "explain_rest_api": {
                "question": "What is a REST API?",
                "hints": [
                    "💡 Hint 1: REST stands for Representational State Transfer",
                    "💡 Hint 2: Mention HTTP methods (GET, POST, PUT, DELETE)",
                    "💡 Hint 3: Explain stateless communication and resource-based URLs",
                    "💡 Hint 4: Give a real-world example (like weather API)"
                ],
                "keywords": ["rest api", "what is rest", "explain rest", "restful"]
            },
            
            "explain_database_indexing": {
                "question": "What is database indexing?",
                "hints": [
                    "💡 Hint 1: Think of it like a book's index - helps find information faster",
                    "💡 Hint 2: Mention trade-offs (faster reads, slower writes)",
                    "💡 Hint 3: Explain when to use indexes (frequently queried columns)",
                    "💡 Hint 4: Give an example (indexing email column for user lookups)"
                ],
                "keywords": ["database indexing", "what is indexing", "explain indexes", "database index"]
            },
            
            "explain_async_programming": {
                "question": "What is asynchronous programming?",
                "hints": [
                    "💡 Hint 1: Compare to synchronous (blocking) vs asynchronous (non-blocking)",
                    "💡 Hint 2: Mention use cases (I/O operations, API calls, file reading)",
                    "💡 Hint 3: Explain benefits (better performance, resource utilization)",
                    "💡 Hint 4: Give a real example (async/await in JavaScript or Python)"
                ],
                "keywords": ["asynchronous programming", "async", "what is async", "explain async"]
            },
            
            # DATA STRUCTURES
            "explain_hash_table": {
                "question": "What is a hash table?",
                "hints": [
                    "💡 Hint 1: It's a data structure that maps keys to values",
                    "💡 Hint 2: Mention hash function (converts key to array index)",
                    "💡 Hint 3: Explain O(1) average time complexity for lookups",
                    "💡 Hint 4: Discuss collision handling (chaining or open addressing)"
                ],
                "keywords": ["hash table", "hash map", "dictionary", "what is hash"]
            },
            
            "explain_binary_tree": {
                "question": "What is a binary tree?",
                "hints": [
                    "💡 Hint 1: Each node has at most two children (left and right)",
                    "💡 Hint 2: Mention root node, leaf nodes, and parent-child relationships",
                    "💡 Hint 3: Explain common types (binary search tree, balanced tree)",
                    "💡 Hint 4: Give use cases (searching, sorting, hierarchical data)"
                ],
                "keywords": ["binary tree", "what is binary tree", "explain binary tree"]
            },
            
            # SYSTEM DESIGN
            "design_url_shortener": {
                "question": "How would you design a URL shortener?",
                "hints": [
                    "💡 Hint 1: Start with requirements (shorten URL, redirect, analytics)",
                    "💡 Hint 2: Discuss URL generation (base62 encoding, hash function)",
                    "💡 Hint 3: Mention database schema (original URL, short code, metadata)",
                    "💡 Hint 4: Consider scale (caching, load balancing, distributed system)"
                ],
                "keywords": ["design url shortener", "url shortener", "design bitly", "shorten url"]
            },
            
            "design_rate_limiter": {
                "question": "How would you design a rate limiter?",
                "hints": [
                    "💡 Hint 1: Define requirements (requests per time window, per user/IP)",
                    "💡 Hint 2: Discuss algorithms (token bucket, sliding window, fixed window)",
                    "💡 Hint 3: Mention storage (Redis for distributed rate limiting)",
                    "💡 Hint 4: Consider edge cases (burst traffic, multiple servers)"
                ],
                "keywords": ["design rate limiter", "rate limiting", "throttling", "api rate limit"]
            },
            
            # LEADERSHIP
            "leadership_example": {
                "question": "Give an example of leadership",
                "hints": [
                    "💡 Hint 1: Leadership isn't just about title - focus on initiative and influence",
                    "💡 Hint 2: Describe the situation that required leadership",
                    "💡 Hint 3: Explain how you motivated and guided others",
                    "💡 Hint 4: Share the team's results and what you learned"
                ],
                "keywords": ["leadership", "led a team", "took charge", "showed leadership"]
            },
            
            # STRENGTHS & WEAKNESSES
            "greatest_strength": {
                "question": "What is your greatest strength?",
                "hints": [
                    "💡 Hint 1: Choose a strength relevant to the job you're applying for",
                    "💡 Hint 2: Back it up with a specific example from your experience",
                    "💡 Hint 3: Show measurable impact (improved performance, saved time, etc.)",
                    "💡 Hint 4: Connect it to how you'll succeed in THIS role"
                ],
                "keywords": ["greatest strength", "what are you good at", "your strengths", "best quality"]
            },
            
            "greatest_weakness": {
                "question": "What is your greatest weakness?",
                "hints": [
                    "💡 Hint 1: Choose a REAL weakness (not 'I work too hard')",
                    "💡 Hint 2: Explain how it impacted you in the past",
                    "💡 Hint 3: Describe specific steps you're taking to improve",
                    "💡 Hint 4: Show actual progress you've made"
                ],
                "keywords": ["greatest weakness", "areas for improvement", "what do you struggle with", "weaknesses"]
            },
            
            # GENERAL TECHNICAL
            "explain_technical_concept": {
                "question": "Explain a technical concept",
                "hints": [
                    "💡 Hint 1: Start with a simple analogy or metaphor",
                    "💡 Hint 2: Explain the concept without using jargon",
                    "💡 Hint 3: Give a real-world example people can relate to",
                    "💡 Hint 4: Explain why it matters and where it's used"
                ],
                "keywords": ["explain", "what is", "describe", "technical concept"]
            }
        }
    
    def get_hints(self, question: str) -> Optional[Dict]:
        """
        Get hints for a question
        
        Args:
            question: The interview question
            
        Returns:
            Dict with hints or None if no match
        """
        question_lower = question.lower().strip()
        
        # Try exact keyword matching first
        for hint_id, hint_data in self.hints_database.items():
            for keyword in hint_data.get("keywords", []):
                if keyword in question_lower:
                    logger.info(f"✅ Hints match: {hint_id} (keyword: {keyword})")
                    return {
                        "question": hint_data["question"],
                        "hints": hint_data["hints"],
                        "total_hints": len(hint_data["hints"]),
                        "hint_penalty": self.hint_penalty
                    }
        
        # Try fuzzy matching
        best_match = None
        best_score = 0.0
        
        for hint_id, hint_data in self.hints_database.items():
            hint_question = hint_data["question"].lower()
            score = self._similarity(question_lower, hint_question)
            
            if score > best_score and score > 0.6:  # 60% similarity threshold
                best_score = score
                best_match = hint_data
        
        if best_match:
            logger.info(f"✅ Hints match: fuzzy match (score: {best_score:.2f})")
            return {
                "question": best_match["question"],
                "hints": best_match["hints"],
                "total_hints": len(best_match["hints"]),
                "hint_penalty": self.hint_penalty
            }
        
        logger.info(f"❌ No hints match for: {question}")
        return None
    
    def get_hint_by_level(self, question: str, hint_level: int) -> Optional[str]:
        """
        Get a specific hint level for a question
        
        Args:
            question: The interview question
            hint_level: Hint level (0-indexed)
            
        Returns:
            Hint text or None
        """
        hints_data = self.get_hints(question)
        
        if not hints_data:
            return None
        
        hints = hints_data["hints"]
        
        if 0 <= hint_level < len(hints):
            return hints[hint_level]
        
        return None
    
    def calculate_penalty(self, hints_used: int) -> float:
        """
        Calculate score penalty based on hints used
        
        Args:
            hints_used: Number of hints revealed
            
        Returns:
            Total penalty amount
        """
        return hints_used * self.hint_penalty
    
    def _similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    def get_all_hints_questions(self) -> List[str]:
        """Get list of all questions that have hints"""
        return [data["question"] for data in self.hints_database.values()]
    
    def search_hints(self, query: str) -> List[Dict]:
        """Search for hints by query"""
        query_lower = query.lower()
        results = []
        
        for hint_data in self.hints_database.values():
            # Search in question and keywords
            if (query_lower in hint_data["question"].lower() or
                any(query_lower in kw for kw in hint_data.get("keywords", []))):
                results.append({
                    "question": hint_data["question"],
                    "total_hints": len(hint_data["hints"]),
                    "hint_penalty": self.hint_penalty
                })
        
        return results


# Global instance
_hints_service = None

def get_hints_service() -> AnswerHintsService:
    """Get or create global hints service"""
    global _hints_service
    if _hints_service is None:
        _hints_service = AnswerHintsService()
    return _hints_service
