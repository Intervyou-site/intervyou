"""
Enhanced Industry-Level Company-Specific Aptitude Question Service

Combines static company questions with AI-generated questions and difficulty scaling:
- Hybrid static + AI question generation
- Dynamic difficulty scaling based on user performance
- Company-specific question templates
- OpenAI integration for unlimited question generation
- Adaptive question sets
"""

import json
import random
import logging
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime

# Import LLM utilities for AI question generation
try:
    from src.llm_utils import call_llm_chat
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

logger = logging.getLogger(__name__)

class EnhancedAptitudeService:
    """Enhanced service combining static and AI-generated aptitude questions"""
    
    # Company difficulty mapping
    COMPANY_DIFFICULTY = {
        "Google": "advanced",
        "Amazon": "intermediate", 
        "Microsoft": "advanced",
        "Meta": "advanced",
        "Apple": "advanced",
        "Netflix": "advanced",
        "Uber": "advanced",
        "Goldman Sachs": "intermediate",
        "JPMorgan": "intermediate",
        "McKinsey": "advanced",
        "Deloitte": "intermediate",
        "Accenture": "intermediate"
    }
    
    # AI Question Generation Templates
    AI_QUESTION_TEMPLATES = {
        "Quantitative Aptitude": {
            "beginner": "Generate a basic math problem involving {company} business context. Include percentage, ratio, or simple arithmetic. Provide 4 multiple choice options.",
            "intermediate": "Create a business math problem for {company} involving compound calculations, profit/loss, or data analysis. Include 4 options with detailed explanation.",
            "advanced": "Design a complex quantitative problem for {company} involving multiple steps, financial calculations, or optimization. Include 4 options."
        },
        "Logical Reasoning": {
            "beginner": "Create a simple logical reasoning question with {company} context. Include syllogisms, patterns, or basic deduction. Provide 4 options.",
            "intermediate": "Generate a logical puzzle involving {company} operations, coding/decoding, or analytical reasoning. Include 4 multiple choice options.",
            "advanced": "Design a complex logical reasoning problem for {company} involving multiple constraints, advanced patterns, or strategic thinking."
        },
        "Data Interpretation": {
            "beginner": "Create a simple data interpretation question about {company} with basic charts, percentages, or comparisons. Include 4 options.",
            "intermediate": "Generate a data analysis problem for {company} involving trends, growth rates, or multi-variable analysis. Provide 4 options.",
            "advanced": "Design a complex data interpretation scenario for {company} with multiple data sources, correlations, or predictive analysis."
        },
        "Probability": {
            "beginner": "Create a basic probability question in {company} context involving simple events or combinations. Include 4 options.",
            "intermediate": "Generate a probability problem for {company} involving conditional probability, combinations, or business scenarios.",
            "advanced": "Design a complex probability question for {company} involving multiple events, Bayes theorem, or statistical analysis."
        },
        "Puzzles": {
            "beginner": "Create a simple puzzle or brain teaser related to {company} operations. Make it engaging and logical. Include 4 options.",
            "intermediate": "Generate a moderately challenging puzzle involving {company} context, requiring creative thinking or problem-solving.",
            "advanced": "Design a complex puzzle for {company} that requires advanced logical thinking, multiple steps, or innovative solutions."
        }
    }
    
    def __init__(self):
        self.cache = {}
        # Import the original service for static questions
        try:
            from services.aptitude_service import AptitudeService
            self.static_service = AptitudeService()
        except ImportError:
            logger.warning("Could not import original AptitudeService")
            self.static_service = None
    
    async def generate_ai_question(
        self, 
        company: str, 
        category: str, 
        difficulty: str = "intermediate"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate AI-powered question using OpenAI
        
        Args:
            company: Target company name
            category: Question category
            difficulty: Question difficulty level
            
        Returns:
            Generated question dictionary or None if failed
        """
        if not LLM_AVAILABLE:
            logger.warning("LLM utilities not available for AI question generation")
            return None
            
        try:
            # Get template for category and difficulty
            template = self.AI_QUESTION_TEMPLATES.get(category, {}).get(
                difficulty, 
                "Generate a {difficulty} level {category} question for {company}. Include 4 multiple choice options with explanations."
            )
            
            # Format the prompt
            user_prompt = template.format(company=company, category=category, difficulty=difficulty)
            
            system_prompt = f"""You are an expert aptitude test creator specializing in company-specific interview questions.

Generate a single {difficulty} level {category} question for {company} interviews.

REQUIREMENTS:
1. Question must be relevant to {company}'s business context
2. Include exactly 4 multiple choice options (A, B, C, D)
3. Provide the correct answer
4. Include detailed explanation
5. Set appropriate difficulty level: {difficulty}

RESPONSE FORMAT (JSON):
{{
    "question": "Your question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option X",
    "explanation": "Detailed explanation of the solution",
    "difficulty": "{difficulty}",
    "company": "{company}",
    "category": "{category}",
    "source": "AI Generated"
}}

Generate only valid JSON response."""

            # Call OpenAI API
            response = await call_llm_chat(
                system_prompt=system_prompt,
                user_message=user_prompt,
                model="gpt-4o-mini",
                max_tokens=600,
                temperature=0.7
            )
            
            # Parse JSON response
            try:
                question_data = json.loads(response.strip())
                
                # Validate required fields
                required_fields = ["question", "options", "correct_answer", "explanation"]
                if all(field in question_data for field in required_fields):
                    # Add metadata
                    question_data.update({
                        "difficulty": difficulty,
                        "company": company,
                        "category": category,
                        "source": "AI Generated",
                        "generated_at": datetime.now().isoformat()
                    })
                    
                    logger.info(f"Successfully generated AI question for {company} - {category}")
                    return question_data
                else:
                    logger.error(f"Generated question missing required fields: {required_fields}")
                    return None
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating AI question: {e}")
            return None

    def get_static_questions(
        self,
        company: str,
        category: str,
        difficulty: Optional[str] = None,
        count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get static questions from the original service
        
        Args:
            company: Target company
            category: Question category
            difficulty: Filter by difficulty
            count: Number of questions
            
        Returns:
            List of static questions
        """
        if self.static_service:
            try:
                # Try to get company-specific questions
                questions = self.static_service.get_questions(category, difficulty, count)
                
                # Add company and source metadata
                for question in questions:
                    question["company"] = company
                    question["source"] = "Static"
                
                return questions
            except Exception as e:
                logger.error(f"Error getting static questions: {e}")
                return []
        
        return []

    async def get_hybrid_questions(
        self,
        company: str,
        category: str,
        difficulty: Optional[str] = None,
        count: int = 10,
        ai_ratio: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Get hybrid questions combining static and AI-generated questions
        
        Args:
            company: Target company
            category: Question category
            difficulty: Filter by difficulty
            count: Total number of questions
            ai_ratio: Ratio of AI-generated questions (0.0 to 1.0)
            
        Returns:
            List of mixed static and AI questions
        """
        questions = []
        
        # Calculate split
        ai_count = int(count * ai_ratio)
        static_count = count - ai_count
        
        # Get static questions first
        static_questions = self.get_static_questions(
            company=company,
            category=category,
            difficulty=difficulty,
            count=static_count
        )
        questions.extend(static_questions)
        
        # Generate AI questions if LLM is available
        if LLM_AVAILABLE and ai_count > 0:
            target_difficulty = difficulty or self.COMPANY_DIFFICULTY.get(company, "intermediate")
            
            for _ in range(ai_count):
                try:
                    ai_question = await self.generate_ai_question(
                        company=company,
                        category=category,
                        difficulty=target_difficulty
                    )
                    if ai_question:
                        questions.append(ai_question)
                except Exception as e:
                    logger.error(f"Failed to generate AI question: {e}")
                    continue
        
        # Fill remaining slots with static questions if AI generation failed
        if len(questions) < count:
            additional_static = self.get_static_questions(
                company=company,
                category=category,
                difficulty=difficulty,
                count=count - len(questions)
            )
            questions.extend(additional_static)
        
        # Shuffle to mix static and AI questions
        random.shuffle(questions)
        return questions[:count]

    def get_difficulty_scaled_questions(
        self,
        company: str,
        category: str,
        user_performance: Dict[str, Any],
        count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get difficulty-scaled questions based on user performance
        
        Args:
            company: Target company
            category: Question category
            user_performance: User's historical performance data
            count: Number of questions
            
        Returns:
            List of difficulty-appropriate questions
        """
        # Determine user's skill level based on performance
        accuracy = user_performance.get("accuracy", 50)
        
        if accuracy >= 80:
            target_difficulty = "advanced"
        elif accuracy >= 60:
            target_difficulty = "intermediate"
        else:
            target_difficulty = "beginner"
        
        # Adjust for company difficulty
        company_level = self.COMPANY_DIFFICULTY.get(company, "intermediate")
        
        # Scale difficulty based on company and performance
        if company_level == "advanced" and target_difficulty == "beginner":
            target_difficulty = "intermediate"  # Don't make it too easy for top companies
        elif company_level == "intermediate" and target_difficulty == "advanced":
            # Keep advanced if user is performing well
            pass
        
        logger.info(f"Scaling difficulty to {target_difficulty} for {company} based on {accuracy}% accuracy")
        
        # Get questions with scaled difficulty
        return self.get_static_questions(
            company=company,
            category=category,
            difficulty=target_difficulty,
            count=count
        )

    async def get_adaptive_question_set(
        self,
        company: str,
        categories: List[str],
        user_performance: Dict[str, Any],
        count: int = 20,
        ai_ratio: float = 0.4
    ) -> Dict[str, Any]:
        """
        Get adaptive question set with AI generation and difficulty scaling
        
        Args:
            company: Target company
            categories: List of categories to include
            user_performance: User's performance history
            count: Total questions
            ai_ratio: Ratio of AI-generated questions
            
        Returns:
            Dictionary with questions and metadata
        """
        question_set = {
            "company": company,
            "total_questions": count,
            "ai_generated_count": 0,
            "static_count": 0,
            "categories": categories,
            "questions": [],
            "difficulty_distribution": {},
            "generated_at": datetime.now().isoformat()
        }
        
        # Distribute questions across categories
        questions_per_category = count // len(categories)
        remaining_questions = count % len(categories)
        
        for i, category in enumerate(categories):
            category_count = questions_per_category
            if i < remaining_questions:
                category_count += 1
            
            # Get hybrid questions for this category
            category_questions = await self.get_hybrid_questions(
                company=company,
                category=category,
                difficulty=None,  # Let adaptive scaling handle this
                count=category_count,
                ai_ratio=ai_ratio
            )
            
            # Apply difficulty scaling
            scaled_questions = []
            for question in category_questions:
                if question.get("source") == "Static":
                    # Apply difficulty scaling to static questions
                    user_cat_performance = user_performance.get("categories", {}).get(category, {"accuracy": 50})
                    if user_cat_performance["accuracy"] >= 80 and question.get("difficulty") == "beginner":
                        continue  # Skip beginner questions for high performers
                    elif user_cat_performance["accuracy"] < 40 and question.get("difficulty") == "advanced":
                        continue  # Skip advanced questions for struggling users
                
                scaled_questions.append(question)
            
            question_set["questions"].extend(scaled_questions)
            
            # Update counters
            for question in scaled_questions:
                if question.get("source") == "AI Generated":
                    question_set["ai_generated_count"] += 1
                else:
                    question_set["static_count"] += 1
                
                # Track difficulty distribution
                difficulty = question.get("difficulty", "unknown")
                question_set["difficulty_distribution"][difficulty] = question_set["difficulty_distribution"].get(difficulty, 0) + 1
        
        # Shuffle final question set
        random.shuffle(question_set["questions"])
        
        logger.info(f"Generated adaptive question set: {question_set['static_count']} static, {question_set['ai_generated_count']} AI")
        
        return question_set

    async def generate_company_question_batch(
        self,
        company: str,
        categories: List[str],
        difficulty: str = "intermediate",
        questions_per_category: int = 5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate a batch of AI questions for a company across multiple categories
        
        Args:
            company: Target company
            categories: List of categories
            difficulty: Question difficulty
            questions_per_category: Number of questions per category
            
        Returns:
            Dictionary with category -> questions mapping
        """
        batch_results = {}
        
        for category in categories:
            category_questions = []
            
            for _ in range(questions_per_category):
                question = await self.generate_ai_question(
                    company=company,
                    category=category,
                    difficulty=difficulty
                )
                if question:
                    category_questions.append(question)
            
            batch_results[category] = category_questions
            logger.info(f"Generated {len(category_questions)} questions for {company} - {category}")
        
        return batch_results

    def validate_answer(self, question: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """
        Validate user's answer (compatible with original service)
        
        Returns:
            Dictionary with is_correct, correct_answer, explanation
        """
        correct_answer = question.get("correct_answer", "")
        is_correct = user_answer.strip() == correct_answer.strip()
        
        return {
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "explanation": question.get("explanation", ""),
            "user_answer": user_answer,
            "source": question.get("source", "Unknown"),
            "company": question.get("company", "Unknown")
        }

    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return list(self.AI_QUESTION_TEMPLATES.keys())

    def get_companies(self) -> List[str]:
        """Get all supported companies"""
        return list(self.COMPANY_DIFFICULTY.keys())

    def get_company_difficulty(self, company: str) -> str:
        """Get difficulty level for a company"""
        return self.COMPANY_DIFFICULTY.get(company, "intermediate")