"""
Question Generation and Management Service

This service handles:
- AI-powered question generation
- Question caching and retrieval
- Category-based question management
- Company-specific question filtering
"""

import json
import random
import asyncio
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class QuestionService:
    """Service for managing interview questions and generation"""
    
    def __init__(self, app_state, llm_client, config):
        self.app_state = app_state
        self.llm_client = llm_client
        self.config = config
        self.generation_cache = {}
    
    async def generate_questions_for_category(
        self, 
        category: str, 
        count: int = 10,
        difficulty: str = "medium",
        company: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate questions for a specific category with optional company focus.
        
        Args:
            category: Interview category (e.g., "Python", "System Design")
            count: Number of questions to generate
            difficulty: Difficulty level ("easy", "medium", "hard")
            company: Optional company to focus questions on
            
        Returns:
            List of question dictionaries with id and prompt
        """
        cache_key = f"{category}_{difficulty}_{company or 'general'}_{count}"
        
        # Check cache first
        if cache_key in self.generation_cache:
            cached_result = self.generation_cache[cache_key]
            if self._is_cache_valid(cached_result):
                logger.info(f"Using cached questions for {category}")
                return cached_result["questions"]
        
        generated_questions = []
        
        # Try different generation methods in order of preference
        try:
            # Method 1: Smart AI Generator (if available)
            if hasattr(self, '_generate_with_smart_ai'):
                questions = await self._generate_with_smart_ai(category, count, difficulty, company)
                if questions:
                    generated_questions.extend(questions)
            
            # Method 2: OpenAI/LLM Generation
            if len(generated_questions) < count:
                needed = count - len(generated_questions)
                llm_questions = await self._generate_with_llm(category, needed, difficulty, company)
                generated_questions.extend(llm_questions)
            
            # Method 3: Fallback to local question bank
            if len(generated_questions) < count:
                needed = count - len(generated_questions)
                local_questions = self._get_local_questions(category, needed)
                generated_questions.extend(local_questions)
            
            # Cache the results
            self.generation_cache[cache_key] = {
                "questions": generated_questions,
                "timestamp": datetime.utcnow(),
                "category": category,
                "difficulty": difficulty,
                "company": company
            }
            
            logger.info(f"Generated {len(generated_questions)} questions for {category}")
            return generated_questions
            
        except Exception as e:
            logger.error(f"Question generation failed for {category}: {e}")
            # Return local questions as ultimate fallback
            return self._get_local_questions(category, count)
    
    async def _generate_with_llm(
        self, 
        category: str, 
        count: int, 
        difficulty: str,
        company: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate questions using LLM (OpenAI/compatible API)"""
        try:
            # Build context-aware prompt
            company_context = f" for {company}" if company else ""
            difficulty_context = self._get_difficulty_context(difficulty)
            
            system_prompt = (
                "You are an expert interview question generator. "
                "Generate high-quality, realistic interview questions that test "
                "practical knowledge and problem-solving skills."
            )
            
            user_prompt = (
                f"Generate {count} distinct interview questions for {category}{company_context}. "
                f"{difficulty_context} "
                f"Return a JSON array of strings. Each question should be concise "
                f"(under 120 characters) and test practical knowledge. "
                f"Focus on real-world scenarios and problem-solving."
            )
            
            response = await self.llm_client.call_llm_chat(
                system_prompt, 
                user_prompt, 
                temperature=0.7, 
                max_tokens=800
            )
            
            # Parse the response
            questions = self._parse_llm_response(response)
            
            # Convert to standard format
            return [
                {"id": f"llm-{i+1}", "prompt": q} 
                for i, q in enumerate(questions[:count])
            ]
            
        except Exception as e:
            logger.error(f"LLM question generation failed: {e}")
            return []
    
    def _parse_llm_response(self, response: str) -> List[str]:
        """Parse LLM response and extract questions"""
        try:
            # Try to parse as JSON first
            if response.strip().startswith('['):
                questions = json.loads(response)
                if isinstance(questions, list):
                    return [str(q).strip() for q in questions if str(q).strip()]
            
            # Extract from code blocks
            import re
            if "```" in response:
                match = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL | re.IGNORECASE)
                if match:
                    try:
                        questions = json.loads(match.group(1))
                        if isinstance(questions, list):
                            return [str(q).strip() for q in questions if str(q).strip()]
                    except json.JSONDecodeError:
                        pass
            
            # Extract quoted strings
            quoted_questions = re.findall(r'"([^"]{10,})"', response)
            if quoted_questions:
                return [q.strip() for q in quoted_questions]
            
            # Split by lines and clean up
            lines = response.strip().split('\n')
            questions = []
            for line in lines:
                line = line.strip()
                # Remove numbering and bullet points
                line = re.sub(r'^\d+[\.\)]\s*', '', line)
                line = re.sub(r'^[-•*]\s*', '', line)
                if len(line) > 10 and '?' in line:
                    questions.append(line)
            
            return questions
            
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return []
    
    def _get_local_questions(self, category: str, count: int) -> List[Dict[str, Any]]:
        """Get questions from local question bank"""
        local_bank = self.config.LOCAL_QUESTION_BANK
        questions = local_bank.get(category, [])
        
        if not questions:
            # If category not found, get from all categories
            all_questions = []
            for cat_questions in local_bank.values():
                all_questions.extend(cat_questions)
            questions = all_questions
        
        # Shuffle and take requested count
        random.shuffle(questions)
        selected = questions[:count]
        
        return [
            {"id": f"local-{i+1}", "prompt": q} 
            for i, q in enumerate(selected)
        ]
    
    def _get_difficulty_context(self, difficulty: str) -> str:
        """Get context string for difficulty level"""
        contexts = {
            "easy": "Focus on basic concepts and fundamental knowledge. Suitable for beginners.",
            "medium": "Include practical scenarios and moderate complexity. Suitable for intermediate level.",
            "hard": "Include complex scenarios, system design, and advanced concepts. Suitable for senior level."
        }
        return contexts.get(difficulty, contexts["medium"])
    
    def _is_cache_valid(self, cached_result: Dict) -> bool:
        """Check if cached result is still valid (not expired)"""
        if not cached_result or "timestamp" not in cached_result:
            return False
        
        # Cache expires after 1 hour
        cache_age = datetime.utcnow() - cached_result["timestamp"]
        return cache_age.total_seconds() < 3600
    
    def get_categories(self) -> List[str]:
        """Get list of available question categories"""
        return list(self.config.LOCAL_QUESTION_BANK.keys())
    
    def get_random_question(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Get a random question from specified category or any category"""
        if category and category in self.app_state.question_bank:
            questions = self.app_state.question_bank[category]
        else:
            # Get from all categories
            all_questions = []
            for cat_questions in self.app_state.question_bank.values():
                all_questions.extend(cat_questions)
            questions = all_questions
        
        if not questions:
            return {
                "q": "Tell me about your experience and background.",
                "keywords": []
            }
        
        selected_question = random.choice(questions)
        return {
            "q": selected_question,
            "keywords": []
        }
    
    def save_generated_questions(self, questions: List[Dict[str, Any]], metadata: Dict[str, Any]):
        """Save generated questions to application state"""
        for question in questions:
            question_id = question.get("id") or f"gen-{len(self.app_state.generated_questions) + 1}"
            self.app_state.generated_questions[question_id] = {
                "prompt": question.get("prompt", ""),
                "category": metadata.get("category", "General"),
                "difficulty": metadata.get("difficulty", "medium"),
                "company": metadata.get("company"),
                "created_at": datetime.utcnow(),
                "source": "ai_generated"
            }
    
    def clear_cache(self):
        """Clear the question generation cache"""
        self.generation_cache.clear()
        logger.info("Question generation cache cleared")

class QuestionBank:
    """Manages the dynamic question bank with caching and updates"""
    
    def __init__(self, initial_bank: Dict[str, List[str]]):
        self.bank = {k: list(v) for k, v in initial_bank.items()}
        self.last_updated = datetime.utcnow()
    
    def add_questions(self, category: str, questions: List[str]):
        """Add questions to a category"""
        if category not in self.bank:
            self.bank[category] = []
        
        # Avoid duplicates
        existing = set(self.bank[category])
        new_questions = [q for q in questions if q not in existing]
        
        self.bank[category].extend(new_questions)
        self.last_updated = datetime.utcnow()
        
        return len(new_questions)
    
    def get_questions(self, category: str, count: Optional[int] = None) -> List[str]:
        """Get questions from a category"""
        questions = self.bank.get(category, [])
        if count:
            return random.sample(questions, min(count, len(questions)))
        return questions.copy()
    
    def get_all_categories(self) -> List[str]:
        """Get all available categories"""
        return list(self.bank.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the question bank"""
        return {
            "categories": len(self.bank),
            "total_questions": sum(len(questions) for questions in self.bank.values()),
            "questions_per_category": {cat: len(questions) for cat, questions in self.bank.items()},
            "last_updated": self.last_updated
        }