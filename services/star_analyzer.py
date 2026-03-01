"""
STAR Method Analyzer
Analyzes interview answers for STAR method components
"""
import json
import logging
import re
from typing import Dict, List, Optional
import httpx
import os

logger = logging.getLogger(__name__)


class STARAnalyzer:
    """Analyzes answers for STAR method components"""
    
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.openai_url = "https://api.openai.com/v1/chat/completions"
    
    async def analyze_answer(self, question: str, answer: str) -> Dict:
        """
        Analyze answer for STAR method components
        
        Returns:
            {
                "situation": {"present": bool, "excerpt": str, "score": int},
                "task": {"present": bool, "excerpt": str, "score": int},
                "action": {"present": bool, "excerpt": str, "score": int},
                "result": {"present": bool, "excerpt": str, "score": int},
                "star_score": int (0-100),
                "missing": List[str],
                "suggestions": List[str],
                "overall_feedback": str
            }
        """
        
        # Check if it's a behavioral question
        if not self._is_behavioral_question(question):
            return {
                "is_behavioral": False,
                "message": "STAR method is primarily for behavioral questions"
            }
        
        # If no API key, use heuristic analysis
        if not self.openai_api_key:
            return self._heuristic_analysis(answer)
        
        # Use AI for detailed analysis
        try:
            return await self._ai_analysis(question, answer)
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._heuristic_analysis(answer)
    
    def _is_behavioral_question(self, question: str) -> bool:
        """Check if question is behavioral"""
        behavioral_keywords = [
            "tell me about", "describe a time", "give an example",
            "how did you", "what would you do", "have you ever",
            "can you share", "walk me through", "tell us about",
            "describe your experience", "give me an example"
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in behavioral_keywords)
    
    def _heuristic_analysis(self, answer: str) -> Dict:
        """Simple heuristic-based STAR analysis"""
        
        answer_lower = answer.lower()
        words = answer.split()
        word_count = len(words)
        
        # Detect components using keywords
        situation_keywords = ["when", "where", "at", "during", "while", "context", "background"]
        task_keywords = ["responsible", "task", "challenge", "problem", "needed to", "had to"]
        action_keywords = ["i did", "i created", "i implemented", "i decided", "i worked", "i developed"]
        result_keywords = ["result", "outcome", "achieved", "improved", "increased", "decreased", "success"]
        
        situation = self._detect_component(answer_lower, situation_keywords)
        task = self._detect_component(answer_lower, task_keywords)
        action = self._detect_component(answer_lower, action_keywords)
        result = self._detect_component(answer_lower, result_keywords)
        
        # Calculate scores
        components_present = sum([situation["present"], task["present"], action["present"], result["present"]])
        star_score = int((components_present / 4) * 100)
        
        # Identify missing components
        missing = []
        if not situation["present"]:
            missing.append("Situation")
        if not task["present"]:
            missing.append("Task")
        if not action["present"]:
            missing.append("Action")
        if not result["present"]:
            missing.append("Result")
        
        # Generate suggestions
        suggestions = self._generate_suggestions(missing, word_count)
        
        return {
            "is_behavioral": True,
            "situation": situation,
            "task": task,
            "action": action,
            "result": result,
            "star_score": star_score,
            "missing": missing,
            "suggestions": suggestions,
            "overall_feedback": self._generate_overall_feedback(star_score, missing)
        }
    
    def _detect_component(self, text: str, keywords: List[str]) -> Dict:
        """Detect if a STAR component is present"""
        
        for keyword in keywords:
            if keyword in text:
                # Find excerpt around keyword
                start = max(0, text.find(keyword) - 50)
                end = min(len(text), text.find(keyword) + 100)
                excerpt = text[start:end].strip()
                
                return {
                    "present": True,
                    "excerpt": excerpt[:150] + "..." if len(excerpt) > 150 else excerpt,
                    "score": 25
                }
        
        return {
            "present": False,
            "excerpt": "",
            "score": 0
        }
    
    def _generate_suggestions(self, missing: List[str], word_count: int) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if "Situation" in missing:
            suggestions.append("Add context: When and where did this happen? What was the background?")
        
        if "Task" in missing:
            suggestions.append("Clarify your role: What were you responsible for? What was the challenge?")
        
        if "Action" in missing:
            suggestions.append("Describe your actions: What specific steps did you take? Use 'I' statements.")
        
        if "Result" in missing:
            suggestions.append("Share the outcome: What happened? Include metrics if possible (e.g., '30% improvement').")
        
        if word_count < 50:
            suggestions.append("Expand your answer: Aim for 100-200 words for a complete STAR response.")
        
        if word_count > 300:
            suggestions.append("Be more concise: Focus on the most important details of each STAR component.")
        
        return suggestions
    
    def _generate_overall_feedback(self, star_score: int, missing: List[str]) -> str:
        """Generate overall feedback message"""
        
        if star_score >= 90:
            return "Excellent! Your answer follows the STAR method very well."
        elif star_score >= 75:
            return "Good structure! Your answer includes most STAR components."
        elif star_score >= 50:
            return "Decent start, but missing some key STAR components."
        else:
            return "Try to structure your answer using all four STAR components."
    
    async def _ai_analysis(self, question: str, answer: str) -> Dict:
        """Use OpenAI for detailed STAR analysis"""
        
        prompt = f"""Analyze this interview answer for STAR method components.

Question: {question}

Answer: {answer}

Identify if the answer contains each STAR component:
1. Situation (S): Context, background, when/where it happened
2. Task (T): The person's responsibility, challenge, or goal
3. Action (A): Specific steps they took (should use "I" statements)
4. Result (R): Outcome, impact, metrics, what was learned

For each component, determine:
- Is it present? (true/false)
- Extract a brief excerpt (max 100 chars)
- Rate quality (0-25 points)

Calculate overall STAR score (0-100).

Return ONLY valid JSON in this exact format:
{{
    "is_behavioral": true,
    "situation": {{"present": true, "excerpt": "...", "score": 20}},
    "task": {{"present": true, "excerpt": "...", "score": 22}},
    "action": {{"present": true, "excerpt": "...", "score": 25}},
    "result": {{"present": false, "excerpt": "", "score": 0}},
    "star_score": 67,
    "missing": ["Result"],
    "suggestions": [
        "Add specific metrics to show the impact",
        "Describe what you learned from this experience"
    ],
    "overall_feedback": "Good structure but missing the result component."
}}"""

        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert interview coach specializing in the STAR method. Analyze answers objectively and provide constructive feedback. Always return valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 600
        }
        
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(self.openai_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            content = data["choices"][0]["message"]["content"]
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            return result


# Global instance
_star_analyzer = None

def get_star_analyzer() -> STARAnalyzer:
    """Get or create global STAR analyzer"""
    global _star_analyzer
    if _star_analyzer is None:
        _star_analyzer = STARAnalyzer()
    return _star_analyzer
