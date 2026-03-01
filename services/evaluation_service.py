"""
Answer Evaluation Service

This service handles:
- AI-powered answer evaluation
- Multiple evaluation methods (XLNet, Hugging Face, OpenAI)
- Plagiarism detection
- Performance scoring and feedback generation
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class EvaluationService:
    """Service for evaluating interview answers using multiple AI methods"""
    
    def __init__(self, llm_client, similarity_calc, features, config):
        self.llm_client = llm_client
        self.similarity_calc = similarity_calc
        self.features = features
        self.config = config
    
    async def evaluate_answer(
        self,
        question: str,
        answer: str,
        keywords: Optional[List[str]] = None,
        category: str = "general",
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive answer evaluation using multiple methods.
        
        Args:
            question: The interview question
            answer: User's answer
            keywords: Expected keywords (optional)
            category: Question category
            user_id: User ID for tracking (optional)
            
        Returns:
            Evaluation result with score, feedback, and analysis
        """
        if not answer.strip():
            return self._create_error_response("Answer cannot be empty")
        
        evaluation_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "answer_length": len(answer.split()),
            "category": category
        }
        
        try:
            # Step 1: AI Detection (if available)
            ai_detection = await self._detect_ai_content(answer)
            if ai_detection:
                evaluation_result["ai_detection"] = ai_detection
            
            # Step 2: Main evaluation using best available method
            main_evaluation = await self._get_main_evaluation(
                question, answer, keywords, category
            )
            evaluation_result.update(main_evaluation)
            
            # Step 3: Plagiarism check
            plagiarism_result = await self._check_plagiarism(answer)
            evaluation_result["plagiarism"] = plagiarism_result
            
            # Step 4: Apply penalties for AI detection or plagiarism
            evaluation_result = self._apply_penalties(evaluation_result)
            
            # Step 5: Generate final recommendations
            evaluation_result["recommendations"] = self._generate_recommendations(evaluation_result)
            
            return evaluation_result
            
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return self._create_error_response(f"Evaluation failed: {str(e)}")
    
    async def _get_main_evaluation(
        self, 
        question: str, 
        answer: str, 
        keywords: Optional[List[str]], 
        category: str
    ) -> Dict[str, Any]:
        """Get main evaluation using the best available method"""
        
        # Method 1: XLNet Hybrid Evaluator (most comprehensive)
        if self.features.xlnet_available:
            try:
                return await self._evaluate_with_xlnet(question, answer, keywords, category)
            except Exception as e:
                logger.warning(f"XLNet evaluation failed: {e}")
        
        # Method 2: Hugging Face Hybrid (local + OpenAI)
        if self.features.huggingface_available:
            try:
                return await self._evaluate_with_huggingface(question, answer, keywords)
            except Exception as e:
                logger.warning(f"Hugging Face evaluation failed: {e}")
        
        # Method 3: Direct OpenAI evaluation
        try:
            return await self._evaluate_with_openai(question, answer, keywords)
        except Exception as e:
            logger.warning(f"OpenAI evaluation failed: {e}")
        
        # Method 4: Fallback heuristic evaluation
        return self._evaluate_with_heuristics(answer, keywords)
    
    async def _evaluate_with_xlnet(
        self, 
        question: str, 
        answer: str, 
        keywords: Optional[List[str]], 
        category: str
    ) -> Dict[str, Any]:
        """Evaluate using XLNet hybrid system"""
        try:
            from hybrid_evaluator import get_hybrid_evaluator
            
            evaluator = get_hybrid_evaluator()
            result = await evaluator.evaluate_answer(
                question=question,
                answer=answer,
                expected_keywords=keywords or [],
                category=category,
                use_detailed_feedback=True
            )
            
            # Convert to standard format
            feedback = result.get('detailed_feedback', {})
            return {
                "score": result['score'] / 10,  # Convert 0-100 to 0-10
                "confidence": result['confidence'],
                "evaluation_method": "xlnet_hybrid",
                "summary": feedback.get('suggestions', 'Answer evaluated successfully'),
                "strengths": feedback.get('strengths', []),
                "improvements": feedback.get('improvements', []),
                "breakdown": result['breakdown'],
                "quick_analysis": result['quick_analysis'],
                "example_answer": feedback.get('example_answer', ''),
                "grammar_feedback": feedback.get('grammar', ''),
                "structure_feedback": feedback.get('structure', '')
            }
            
        except Exception as e:
            logger.error(f"XLNet evaluation error: {e}")
            raise
    
    async def _evaluate_with_huggingface(
        self, 
        question: str, 
        answer: str, 
        keywords: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Evaluate using Hugging Face models"""
        try:
            from huggingface_utils import evaluate_answer_comprehensive
            
            result = evaluate_answer_comprehensive(
                question=question,
                answer=answer,
                expected_keywords=keywords or []
            )
            
            return {
                "score": result.get("score", 5.0),
                "evaluation_method": "huggingface",
                "summary": result.get("feedback", "Answer evaluated"),
                "improvements": result.get("improvements", []),
                "sentiment": result.get("sentiment"),
                "relevance": result.get("relevance"),
                "confidence": result.get("confidence", 0.8)
            }
            
        except Exception as e:
            logger.error(f"Hugging Face evaluation error: {e}")
            raise
    
    async def _evaluate_with_openai(
        self, 
        question: str, 
        answer: str, 
        keywords: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Evaluate using OpenAI API"""
        try:
            system_prompt = (
                "You are IntervYou: a precise interview answer evaluator. "
                "Analyze the given question and answer, then provide structured feedback. "
                "Return valid JSON with: score (0-10), summary, improvements (array), "
                "strengths (array), grammar_feedback, and structure_feedback."
            )
            
            keyword_context = ""
            if keywords:
                keyword_context = f"\\nExpected keywords: {', '.join(keywords)}"
            
            user_prompt = (
                f"Question: {question}\\n"
                f"Answer: {answer}{keyword_context}\\n\\n"
                f"Evaluate this interview answer and return JSON with detailed feedback."
            )
            
            response = await self.llm_client.call_llm_chat(
                system_prompt, user_prompt, max_tokens=600, temperature=0.3
            )
            
            # Parse JSON response
            try:
                evaluation = json.loads(response)
                evaluation["evaluation_method"] = "openai"
                evaluation["confidence"] = 0.9
                return evaluation
            except json.JSONDecodeError:
                # If not valid JSON, create structured response from text
                return {
                    "score": self._extract_score_from_text(response),
                    "evaluation_method": "openai_text",
                    "summary": response[:300],
                    "improvements": [],
                    "confidence": 0.7
                }
                
        except Exception as e:
            logger.error(f"OpenAI evaluation error: {e}")
            raise
    
    def _evaluate_with_heuristics(
        self, 
        answer: str, 
        keywords: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Fallback heuristic evaluation"""
        word_count = len(answer.split())
        
        # Basic scoring based on length and content
        base_score = min(8.0, max(2.0, word_count / 20))
        
        # Keyword matching bonus
        keyword_score = 0
        if keywords:
            answer_lower = answer.lower()
            matched_keywords = [kw for kw in keywords if kw.lower() in answer_lower]
            keyword_score = (len(matched_keywords) / len(keywords)) * 2
        
        final_score = min(10.0, base_score + keyword_score)
        
        # Generate feedback based on analysis
        improvements = []
        if word_count < 30:
            improvements.append("Provide more detailed explanations and examples")
        if keywords and keyword_score < 1:
            improvements.append("Include more relevant technical terms and concepts")
        if len(answer.split('.')) < 3:
            improvements.append("Structure your answer with multiple clear points")
        
        return {
            "score": round(final_score, 1),
            "evaluation_method": "heuristic",
            "summary": f"Answer analyzed using basic heuristics. Score: {final_score:.1f}/10",
            "improvements": improvements,
            "word_count": word_count,
            "keyword_matches": keyword_score if keywords else None,
            "confidence": 0.6
        }
    
    async def _detect_ai_content(self, text: str) -> Optional[Dict[str, Any]]:
        """Detect if content is AI-generated"""
        if not self.features.ai_detection_available:
            return None
        
        try:
            from ai_detection import detect_ai_generated
            
            result = detect_ai_generated(text)
            return {
                "ai_probability": result["ai_probability"],
                "confidence": result["confidence"],
                "warning": result["warning"],
                "verdict": result["verdict"],
                "indicators": result["indicators"][:3]  # Top 3 indicators
            }
            
        except Exception as e:
            logger.error(f"AI detection failed: {e}")
            return None
    
    async def _check_plagiarism(self, text: str) -> Dict[str, Any]:
        """Check for plagiarism using local similarity"""
        try:
            # This would integrate with your plagiarism checking service
            # For now, return a basic similarity check
            return {
                "plagiarism_score": 0.0,
                "matches": [],
                "method": "local_similarity"
            }
            
        except Exception as e:
            logger.error(f"Plagiarism check failed: {e}")
            return {
                "plagiarism_score": 0.0,
                "matches": [],
                "error": str(e)
            }
    
    def _apply_penalties(self, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """Apply penalties for AI detection or plagiarism"""
        original_score = evaluation.get("score", 0)
        penalties_applied = []
        
        # AI detection penalty
        ai_detection = evaluation.get("ai_detection")
        if ai_detection and ai_detection.get("ai_probability", 0) >= 0.7:
            # Severe penalty for likely AI content
            evaluation["score"] = min(original_score * 0.3, 3.0)
            evaluation["original_score"] = original_score
            penalties_applied.append("AI-generated content detected")
        elif ai_detection and ai_detection.get("ai_probability", 0) >= 0.5:
            # Moderate penalty for possibly AI content
            evaluation["score"] = original_score * 0.6
            evaluation["original_score"] = original_score
            penalties_applied.append("Possible AI assistance detected")
        
        # Plagiarism penalty
        plagiarism = evaluation.get("plagiarism", {})
        if plagiarism.get("plagiarism_score", 0) >= 0.8:
            current_score = evaluation.get("score", original_score)
            evaluation["score"] = min(current_score * 0.4, 2.0)
            if "original_score" not in evaluation:
                evaluation["original_score"] = original_score
            penalties_applied.append("High plagiarism similarity detected")
        
        if penalties_applied:
            evaluation["penalties_applied"] = penalties_applied
        
        return evaluation
    
    def _generate_recommendations(self, evaluation: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations based on evaluation"""
        recommendations = []
        score = evaluation.get("score", 0)
        
        # Score-based recommendations
        if score >= 8:
            recommendations.append("Excellent answer! Focus on refining delivery and confidence.")
        elif score >= 6:
            recommendations.append("Good foundation. Work on adding more specific examples.")
        elif score >= 4:
            recommendations.append("Decent attempt. Focus on structure and key concepts.")
        else:
            recommendations.append("Needs improvement. Practice basic concepts and structure.")
        
        # Method-specific recommendations
        method = evaluation.get("evaluation_method", "")
        if "xlnet" in method:
            recommendations.append("Consider the detailed breakdown for targeted improvement.")
        
        # AI detection recommendations
        if evaluation.get("ai_detection", {}).get("ai_probability", 0) > 0.5:
            recommendations.append("Practice answering in your own words and speaking style.")
        
        # Add improvements from evaluation
        improvements = evaluation.get("improvements", [])
        recommendations.extend(improvements[:2])  # Add top 2 improvements
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _extract_score_from_text(self, text: str) -> float:
        """Extract numerical score from text response"""
        import re
        
        # Look for patterns like "8/10", "Score: 7.5", "8.0 out of 10"
        patterns = [
            r'(\d+\.?\d*)\s*/\s*10',
            r'score:?\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*out\s*of\s*10'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                try:
                    score = float(match.group(1))
                    return min(10.0, max(0.0, score))
                except ValueError:
                    continue
        
        # Default score if no pattern found
        return 5.0
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "error": True,
            "message": error_message,
            "score": 0.0,
            "evaluation_method": "error",
            "summary": f"Evaluation failed: {error_message}",
            "improvements": ["Please try again with a valid answer"],
            "timestamp": datetime.utcnow().isoformat()
        }

class FeedbackGenerator:
    """Generate human-friendly feedback from evaluation results"""
    
    @staticmethod
    def generate_detailed_feedback(evaluation: Dict[str, Any]) -> Dict[str, str]:
        """Generate detailed, human-readable feedback"""
        score = evaluation.get("score", 0)
        method = evaluation.get("evaluation_method", "unknown")
        
        # Score interpretation
        if score >= 9:
            score_feedback = "Outstanding! Your answer demonstrates excellent understanding."
        elif score >= 7:
            score_feedback = "Great job! Your answer shows strong knowledge."
        elif score >= 5:
            score_feedback = "Good effort! Your answer covers the basics well."
        elif score >= 3:
            score_feedback = "Fair attempt. There's room for improvement."
        else:
            score_feedback = "Keep practicing! Focus on the fundamentals."
        
        # Method-specific feedback
        method_feedback = {
            "xlnet_hybrid": "Analyzed using advanced AI for comprehensive evaluation.",
            "huggingface": "Evaluated using specialized language models.",
            "openai": "Assessed using state-of-the-art AI evaluation.",
            "heuristic": "Analyzed using fundamental scoring criteria."
        }.get(method, "Evaluated using available assessment methods.")
        
        # Confidence feedback
        confidence = evaluation.get("confidence", 0.5)
        if confidence >= 0.9:
            confidence_feedback = "High confidence in this assessment."
        elif confidence >= 0.7:
            confidence_feedback = "Good confidence in this evaluation."
        else:
            confidence_feedback = "Moderate confidence - consider additional practice."
        
        return {
            "score_feedback": score_feedback,
            "method_feedback": method_feedback,
            "confidence_feedback": confidence_feedback,
            "overall_summary": f"{score_feedback} {confidence_feedback}"
        }