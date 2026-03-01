"""
Web Question Fetcher Service - Fetches real interview questions from web sources
"""
import os
import logging
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json
import re

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

logger = logging.getLogger(__name__)


class WebQuestionFetcher:
    """Fetch interview questions from web sources"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=24)
        self.serpapi_key = os.environ.get("SERPAPI_KEY")
        self.openai_key = os.environ.get("OPENAI_API_KEY")
    
    async def fetch_questions(
        self, 
        category: str, 
        company: Optional[str] = None,
        count: int = 10,
        difficulty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fetch interview questions from web sources"""
        cache_key = f"{category}_{company}_{difficulty}_{count}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if datetime.now() - cached_data['timestamp'] < self.cache_duration:
                logger.info(f"✅ Returning cached questions for {cache_key}")
                return cached_data['questions']
        
        questions = []
        
        try:
            # Try SerpAPI for real-time web search
            if self.serpapi_key and HTTPX_AVAILABLE:
                serpapi_questions = await self._fetch_from_serpapi(category, company, count)
                questions.extend(serpapi_questions)
            
            # Try OpenAI to generate questions
            if self.openai_key and HTTPX_AVAILABLE and len(questions) < count:
                openai_questions = await self._fetch_from_openai(category, company, count - len(questions))
                questions.extend(openai_questions)
            
            # Fallback to curated question bank
            if len(questions) < count:
                fallback_questions = self._get_fallback_questions(category, company, count - len(questions))
                questions.extend(fallback_questions)
            
            # Cache the results
            self.cache[cache_key] = {
                'questions': questions[:count],
                'timestamp': datetime.now()
            }
            
            logger.info(f"✅ Fetched {len(questions)} questions for {category}")
            return questions[:count]
            
        except Exception as e:
            logger.error(f"❌ Error fetching questions: {e}")
            return self._get_fallback_questions(category, company, count)
    
    async def _fetch_from_serpapi(self, category: str, company: Optional[str] = None, count: int = 10) -> List[Dict[str, Any]]:
        """Fetch questions using SerpAPI"""
        if not HTTPX_AVAILABLE:
            return []
        
        try:
            company_part = f"{company} " if company else ""
            query = f"{company_part}{category} interview questions 2024"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    "https://serpapi.com/search",
                    params={"q": query, "api_key": self.serpapi_key, "num": min(count, 10)}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    questions = self._parse_serpapi_results(data, category, company)
                    logger.info(f"✅ SerpAPI returned {len(questions)} questions")
                    return questions
                else:
                    logger.warning(f"⚠️ SerpAPI returned status {response.status_code}")
                    return []
        except Exception as e:
            logger.error(f"❌ SerpAPI error: {e}")
            return []
    
    def _parse_serpapi_results(self, data: Dict, category: str, company: Optional[str]) -> List[Dict[str, Any]]:
        """Parse SerpAPI results"""
        questions = []
        
        # Extract from organic results
        for result in data.get("organic_results", [])[:5]:
            snippet = result.get("snippet", "")
            title = result.get("title", "")
            extracted = self._extract_questions_from_text(snippet + " " + title)
            
            for q in extracted:
                questions.append({
                    "question": q,
                    "category": category,
                    "company": company,
                    "source": "web_search",
                    "url": result.get("link"),
                    "difficulty": "medium",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Extract from related questions
        for rq in data.get("related_questions", []):
            question_text = rq.get("question", "")
            if question_text and len(question_text) > 10:
                questions.append({
                    "question": question_text,
                    "category": category,
                    "company": company,
                    "source": "related_search",
                    "difficulty": "medium",
                    "timestamp": datetime.now().isoformat()
                })
        
        return questions
    
    async def _fetch_from_openai(self, category: str, company: Optional[str] = None, count: int = 10) -> List[Dict[str, Any]]:
        """Generate questions using OpenAI"""
        if not HTTPX_AVAILABLE:
            return []
        
        try:
            company_context = f" for {company}" if company else ""
            prompt = f"Generate {count} {category} interview questions{company_context}. Return only questions, numbered 1-{count}."
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.openai_key}", "Content-Type": "application/json"},
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.8,
                        "max_tokens": 1000
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    extracted = self._extract_questions_from_text(content)
                    
                    questions = []
                    for q in extracted:
                        questions.append({
                            "question": q,
                            "category": category,
                            "company": company,
                            "source": "ai_generated",
                            "difficulty": "medium",
                            "timestamp": datetime.now().isoformat()
                        })
                    
                    logger.info(f"✅ OpenAI generated {len(questions)} questions")
                    return questions
                else:
                    return []
        except Exception as e:
            logger.error(f"❌ OpenAI error: {e}")
            return []
    
    def _extract_questions_from_text(self, text: str) -> List[str]:
        """Extract questions from text"""
        questions = []
        
        # Pattern: Numbered questions
        pattern = r'\d+[\.\)]\s*([^?\n]+\?)'
        matches = re.findall(pattern, text)
        questions.extend([m.strip() for m in matches])
        
        # Pattern: Question starters
        starters = ["What", "How", "Why", "When", "Where", "Which", "Explain", "Describe"]
        for sentence in text.split('.'):
            sentence = sentence.strip()
            if any(sentence.startswith(s) for s in starters):
                if '?' in sentence:
                    questions.append(sentence.split('?')[0] + '?')
                elif 20 < len(sentence) < 200:
                    questions.append(sentence + '?')
        
        return list(set(questions))[:10]
    
    def _get_fallback_questions(self, category: str, company: Optional[str] = None, count: int = 10) -> List[Dict[str, Any]]:
        """Get questions from curated fallback bank"""
        fallback_bank = {
            "Python": [
                "What are Python decorators and how do you use them?",
                "Explain the difference between list, tuple, and set in Python.",
                "What is the Global Interpreter Lock (GIL) in Python?",
                "How does Python's garbage collection work?",
                "Explain list comprehensions and generator expressions.",
                "What are Python's magic methods?",
                "How do you handle exceptions in Python?",
                "What is the difference between @staticmethod and @classmethod?",
                "Explain Python's context managers.",
                "What are Python generators?"
            ],
            "Web Development": [
                "What is the difference between REST and GraphQL?",
                "Explain how JWT authentication works.",
                "What are the main differences between HTTP and HTTPS?",
                "How does CORS work?",
                "Explain responsive web design.",
                "What is the difference between cookies and local storage?",
                "How do you optimize website performance?",
                "Explain the MVC architecture pattern.",
                "What are Progressive Web Apps?",
                "How do you handle state management?"
            ],
            "Data Structures": [
                "Explain the difference between an array and a linked list.",
                "What is a hash table?",
                "Describe tree data structures.",
                "What is time complexity?",
                "Explain stack vs queue.",
                "What is a heap?",
                "Describe graph data structures.",
                "What is BFS vs DFS?",
                "Explain trie data structure.",
                "Hash map vs array?"
            ],
            "System Design": [
                "How would you design a URL shortener?",
                "Explain load balancing.",
                "What is database sharding?",
                "How would you design a rate limiter?",
                "Explain the CAP theorem.",
                "How would you design a notification system?",
                "What is caching?",
                "How would you design a chat app?",
                "Explain microservices architecture.",
                "How to handle millions of users?"
            ],
            "Machine Learning": [
                "What is supervised vs unsupervised learning?",
                "Explain overfitting.",
                "What is bias-variance tradeoff?",
                "How do you evaluate ML models?",
                "Classification vs regression?",
                "What are ensemble methods?",
                "How to handle imbalanced datasets?",
                "Explain feature engineering.",
                "What is cross-validation?",
                "Bagging vs boosting?"
            ],
            "Behavioral": [
                "Tell me about yourself.",
                "Why do you want to work here?",
                "Describe a challenging project.",
                "How do you handle conflicts?",
                "Tell me about a failure.",
                "How do you prioritize tasks?",
                "Describe your ideal work environment.",
                "How do you stay updated?",
                "Tell me about learning something quickly.",
                "Where do you see yourself in 5 years?"
            ]
        }
        
        questions_list = fallback_bank.get(category, fallback_bank["Python"])
        questions = []
        
        for q in questions_list[:count]:
            questions.append({
                "question": q,
                "category": category,
                "company": company,
                "source": "curated_bank",
                "difficulty": "medium",
                "timestamp": datetime.now().isoformat()
            })
        
        return questions
    
    def clear_cache(self):
        """Clear the question cache"""
        self.cache.clear()
        logger.info("🗑️ Question cache cleared")
    
    async def search_questions(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for specific interview questions"""
        try:
            if self.serpapi_key and HTTPX_AVAILABLE:
                return await self._fetch_from_serpapi(query, None, limit)
            elif self.openai_key and HTTPX_AVAILABLE:
                return await self._fetch_from_openai(query, None, limit)
            else:
                all_questions = []
                for cat in ["Python", "Web Development", "Data Structures"]:
                    all_questions.extend(self._get_fallback_questions(cat, None, 10))
                
                query_lower = query.lower()
                matching = [q for q in all_questions if query_lower in q["question"].lower()]
                return matching[:limit]
        except Exception as e:
            logger.error(f"❌ Search error: {e}")
            return []


# Global instance
_fetcher_instance = None

def get_question_fetcher() -> WebQuestionFetcher:
    """Get or create the global question fetcher instance"""
    global _fetcher_instance
    if _fetcher_instance is None:
        _fetcher_instance = WebQuestionFetcher()
    return _fetcher_instance
