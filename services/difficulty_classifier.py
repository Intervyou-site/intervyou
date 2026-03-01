"""
Difficulty Classifier for Interview Questions
Intelligently classifies questions into beginner, intermediate, and advanced levels
"""
import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class DifficultyClassifier:
    """Classifies interview questions by difficulty level"""
    
    def __init__(self):
        # Keywords that indicate difficulty levels
        self.beginner_indicators = {
            # Basic concepts
            "what is", "define", "explain the difference between", "list", 
            "name", "basic", "simple", "introduction", "beginner",
            "fundamental", "overview", "describe",
            
            # Basic operations
            "how do you", "how to", "what are the types of",
            "give an example", "syntax", "declaration",
            
            # Common beginner topics
            "variable", "data type", "loop", "if statement", "function definition",
            "array", "string", "integer", "boolean"
        }
        
        self.intermediate_indicators = {
            # Practical application
            "implement", "create", "build", "design a simple",
            "how would you", "compare and contrast", "advantages and disadvantages",
            "when would you use", "best practices", "common use cases",
            
            # Intermediate concepts
            "class", "object", "inheritance", "polymorphism", "encapsulation",
            "exception handling", "file handling", "database connection",
            "api", "rest", "json", "xml", "testing",
            
            # Problem-solving
            "solve", "find", "calculate", "determine", "optimize",
            "debug", "fix", "improve", "refactor"
        }
        
        self.advanced_indicators = {
            # Complex concepts
            "architecture", "design pattern", "scalability", "performance",
            "distributed", "concurrent", "parallel", "asynchronous",
            "microservices", "system design", "trade-offs", "complexity analysis",
            
            # Advanced operations
            "optimize for", "scale to", "handle millions", "design for",
            "architect", "implement a production", "enterprise-level",
            
            # Deep technical
            "memory management", "garbage collection", "thread-safe",
            "race condition", "deadlock", "caching strategy",
            "load balancing", "sharding", "replication",
            
            # Advanced problem-solving
            "big o", "time complexity", "space complexity",
            "algorithm", "data structure design", "optimize performance"
        }
        
        # Category-specific difficulty mappings
        self.category_difficulty_map = {
            "Python": {
                "beginner": [
                    "What is Python?",
                    "What are Python data types?",
                    "How do you create a list in Python?",
                    "What is a variable in Python?",
                    "How do you write a for loop?",
                    "What is the difference between list and tuple?",
                    "How do you define a function?",
                    "What are Python comments?",
                    "How do you take user input?",
                    "What is string concatenation?"
                ],
                "intermediate": [
                    "What are Python decorators?",
                    "Explain list comprehensions.",
                    "How does exception handling work?",
                    "What are lambda functions?",
                    "Explain OOP concepts in Python.",
                    "What is the difference between @staticmethod and @classmethod?",
                    "How do you work with files in Python?",
                    "What are Python generators?",
                    "Explain the map, filter, and reduce functions.",
                    "How do you handle JSON data?"
                ],
                "advanced": [
                    "What is the Global Interpreter Lock (GIL)?",
                    "Explain Python's memory management and garbage collection.",
                    "What are metaclasses in Python?",
                    "How do you optimize Python code for performance?",
                    "Explain the difference between deep and shallow copy.",
                    "What are context managers and how do you create custom ones?",
                    "How does Python's asyncio work?",
                    "Explain Python's descriptor protocol.",
                    "What are Python's magic methods and dunder methods?",
                    "How do you implement a custom iterator?"
                ]
            },
            "Web Development": {
                "beginner": [
                    "What is HTML?",
                    "What is CSS?",
                    "What is JavaScript?",
                    "What is a web server?",
                    "What is HTTP?",
                    "What are HTML tags?",
                    "How do you create a link in HTML?",
                    "What is a CSS selector?",
                    "What is the DOM?",
                    "What is a variable in JavaScript?"
                ],
                "intermediate": [
                    "What is the difference between REST and GraphQL?",
                    "Explain how JWT authentication works.",
                    "What are the main differences between HTTP and HTTPS?",
                    "How does CORS work?",
                    "What is responsive web design?",
                    "Explain the MVC architecture pattern.",
                    "What are Progressive Web Apps?",
                    "How do you handle state management?",
                    "What is the difference between cookies and local storage?",
                    "How do you optimize website performance?"
                ],
                "advanced": [
                    "How would you design a scalable web application?",
                    "Explain microservices architecture.",
                    "How do you implement server-side rendering?",
                    "What are Web Workers and Service Workers?",
                    "How do you optimize for Core Web Vitals?",
                    "Explain the critical rendering path.",
                    "How do you implement real-time features with WebSockets?",
                    "What are the security best practices for web applications?",
                    "How do you handle millions of concurrent users?",
                    "Explain CDN and edge computing strategies."
                ]
            },
            "Data Structures": {
                "beginner": [
                    "What is an array?",
                    "What is a linked list?",
                    "What is a stack?",
                    "What is a queue?",
                    "What is the difference between array and linked list?",
                    "How do you implement a stack?",
                    "What is LIFO and FIFO?",
                    "What is a node in a linked list?",
                    "How do you access array elements?",
                    "What is array indexing?"
                ],
                "intermediate": [
                    "What is a hash table and how does it work?",
                    "Explain binary search tree.",
                    "What is the time complexity of common operations?",
                    "How do you detect a cycle in a linked list?",
                    "What is a heap data structure?",
                    "Explain BFS and DFS.",
                    "What is a trie?",
                    "How do you implement a queue using stacks?",
                    "What is a priority queue?",
                    "Explain the difference between tree and graph."
                ],
                "advanced": [
                    "How do you implement a LRU cache?",
                    "Explain self-balancing trees (AVL, Red-Black).",
                    "What is a B-tree and when would you use it?",
                    "How do you find the shortest path in a weighted graph?",
                    "Explain dynamic programming with examples.",
                    "What is amortized time complexity?",
                    "How do you implement a skip list?",
                    "Explain segment trees and their applications.",
                    "What is a Bloom filter?",
                    "How do you design a data structure for a specific problem?"
                ]
            },
            "System Design": {
                "beginner": [
                    "What is system design?",
                    "What is a client-server architecture?",
                    "What is a database?",
                    "What is an API?",
                    "What is a web server?",
                    "What is cloud computing?",
                    "What is scalability?",
                    "What is a load balancer?",
                    "What is caching?",
                    "What is a CDN?"
                ],
                "intermediate": [
                    "How would you design a URL shortener?",
                    "Explain load balancing strategies.",
                    "What is database sharding?",
                    "How would you design a rate limiter?",
                    "What is caching and what are common strategies?",
                    "How would you design a notification system?",
                    "Explain the CAP theorem.",
                    "What is database replication?",
                    "How do you handle session management?",
                    "What is horizontal vs vertical scaling?"
                ],
                "advanced": [
                    "How would you design Twitter/X?",
                    "How would you design Netflix?",
                    "How would you design Uber?",
                    "Explain distributed consensus algorithms.",
                    "How do you handle millions of concurrent users?",
                    "Design a global-scale messaging system.",
                    "How would you design a search engine?",
                    "Explain eventual consistency and strong consistency.",
                    "How do you design for fault tolerance?",
                    "Design a distributed file system like HDFS."
                ]
            },
            "Machine Learning": {
                "beginner": [
                    "What is machine learning?",
                    "What is supervised learning?",
                    "What is unsupervised learning?",
                    "What is a training set?",
                    "What is a test set?",
                    "What is a feature?",
                    "What is a label?",
                    "What is classification?",
                    "What is regression?",
                    "What is overfitting?"
                ],
                "intermediate": [
                    "Explain the bias-variance tradeoff.",
                    "What are ensemble methods?",
                    "How do you handle imbalanced datasets?",
                    "What is cross-validation?",
                    "Explain regularization techniques.",
                    "What is feature engineering?",
                    "How do you evaluate a classification model?",
                    "What is the difference between bagging and boosting?",
                    "Explain gradient descent.",
                    "What are hyperparameters?"
                ],
                "advanced": [
                    "Explain the mathematics behind neural networks.",
                    "How do you optimize deep learning models?",
                    "What is transfer learning and when would you use it?",
                    "Explain attention mechanisms in transformers.",
                    "How do you handle concept drift in production?",
                    "Design an ML system for real-time predictions.",
                    "Explain reinforcement learning algorithms.",
                    "How do you deploy ML models at scale?",
                    "What are the ethical considerations in ML?",
                    "How do you debug and interpret ML models?"
                ]
            },
            "Behavioral": {
                "beginner": [
                    "Tell me about yourself.",
                    "Why do you want this job?",
                    "What are your strengths?",
                    "What are your weaknesses?",
                    "Where do you see yourself in 5 years?",
                    "Why should we hire you?",
                    "What motivates you?",
                    "What is your greatest achievement?",
                    "How do you handle stress?",
                    "What are your hobbies?"
                ],
                "intermediate": [
                    "Describe a challenging project you worked on.",
                    "Tell me about a time you failed.",
                    "How do you handle conflicts in a team?",
                    "Describe a time you had to learn something quickly.",
                    "How do you prioritize tasks?",
                    "Tell me about a time you disagreed with your manager.",
                    "How do you handle feedback?",
                    "Describe a time you went above and beyond.",
                    "How do you stay updated with technology?",
                    "Tell me about a time you had to make a difficult decision."
                ],
                "advanced": [
                    "Describe a time you led a team through a crisis.",
                    "How would you handle a situation where your team is underperforming?",
                    "Tell me about a time you had to influence without authority.",
                    "Describe a complex technical decision you made and its impact.",
                    "How do you balance technical debt with feature development?",
                    "Tell me about a time you had to pivot a project mid-way.",
                    "How do you mentor junior developers?",
                    "Describe your approach to building team culture.",
                    "How do you handle stakeholder management?",
                    "Tell me about a time you had to make a trade-off decision."
                ]
            }
        }
    
    def classify_question(self, question: str, category: str = None) -> str:
        """
        Classify a question into beginner, intermediate, or advanced
        
        Args:
            question: The question text
            category: Optional category for context
        
        Returns:
            "beginner", "intermediate", or "advanced"
        """
        question_lower = question.lower()
        
        # Check category-specific mappings first
        if category and category in self.category_difficulty_map:
            for level, questions in self.category_difficulty_map[category].items():
                for q in questions:
                    if self._similarity(question_lower, q.lower()) > 0.7:
                        return level
        
        # Count indicators for each level
        beginner_score = sum(1 for indicator in self.beginner_indicators if indicator in question_lower)
        intermediate_score = sum(1 for indicator in self.intermediate_indicators if indicator in question_lower)
        advanced_score = sum(1 for indicator in self.advanced_indicators if indicator in question_lower)
        
        # Additional heuristics
        word_count = len(question.split())
        has_technical_terms = any(term in question_lower for term in [
            "algorithm", "complexity", "optimize", "scale", "architecture",
            "distributed", "concurrent", "performance"
        ])
        
        # Adjust scores based on heuristics
        if word_count > 20:
            advanced_score += 1
        if has_technical_terms:
            advanced_score += 2
        
        # Determine difficulty
        scores = {
            "beginner": beginner_score,
            "intermediate": intermediate_score,
            "advanced": advanced_score
        }
        
        max_score = max(scores.values())
        
        if max_score == 0:
            # Default to intermediate if no clear indicators
            return "intermediate"
        
        # Return the level with highest score
        for level, score in scores.items():
            if score == max_score:
                return level
        
        return "intermediate"
    
    def _similarity(self, str1: str, str2: str) -> float:
        """Calculate simple similarity between two strings"""
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def get_questions_by_difficulty(
        self, 
        category: str, 
        difficulty: str,
        count: int = 10
    ) -> List[str]:
        """Get questions for a specific difficulty level"""
        if category in self.category_difficulty_map:
            questions = self.category_difficulty_map[category].get(difficulty, [])
            return questions[:count]
        return []
    
    def classify_batch(
        self, 
        questions: List[str], 
        category: str = None
    ) -> Dict[str, List[str]]:
        """Classify a batch of questions"""
        classified = {
            "beginner": [],
            "intermediate": [],
            "advanced": []
        }
        
        for question in questions:
            difficulty = self.classify_question(question, category)
            classified[difficulty].append(question)
        
        return classified


# Global instance
_classifier = None

def get_difficulty_classifier() -> DifficultyClassifier:
    """Get or create the global difficulty classifier"""
    global _classifier
    if _classifier is None:
        _classifier = DifficultyClassifier()
    return _classifier
