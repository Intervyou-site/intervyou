"""
Hybrid Answer Evaluation System
Combines XLNet (fast scoring) with GPT (detailed feedback)
"""

import asyncio
from typing import Dict, Optional
from xlnet_evaluator import get_xlnet_evaluator
import os

# Import LLM utilities if available
try:
    from llm_utils import call_llm_chat
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("⚠️  LLM utilities not available")


class HybridAnswerEvaluator:
    """
    Hybrid evaluation system:
    1. XLNet provides fast, local scoring (0-100)
    2. GPT provides detailed feedback and suggestions
    """
    
    def __init__(self):
        self.xlnet_evaluator = get_xlnet_evaluator()
        self.use_gpt = LLM_AVAILABLE and os.getenv('OPENAI_API_KEY')
        
        if self.use_gpt:
            print("✅ Hybrid mode: XLNet + GPT")
        else:
            print("⚠️  XLNet-only mode (GPT not available)")
    
    async def evaluate_answer(
        self,
        question: str,
        answer: str,
        expected_keywords: list = None,
        category: str = None,
        use_detailed_feedback: bool = True
    ) -> Dict:
        """
        Evaluate answer using hybrid approach
        
        Args:
            question: Interview question
            answer: User's answer
            expected_keywords: Expected keywords in answer
            category: Question category (technical, behavioral, etc.)
            use_detailed_feedback: Whether to get GPT feedback
        
        Returns:
            Complete evaluation with score and feedback
        """
        
        # Step 1: Fast XLNet scoring (always runs, ~100ms)
        xlnet_result = self.xlnet_evaluator.evaluate_answer(
            question=question,
            answer=answer,
            expected_keywords=expected_keywords,
            context=category
        )
        
        # Step 2: Detailed GPT feedback (optional, ~2-3 seconds)
        detailed_feedback = None
        if use_detailed_feedback and self.use_gpt:
            try:
                detailed_feedback = await self._get_gpt_feedback(
                    question=question,
                    answer=answer,
                    xlnet_score=xlnet_result['score'],
                    category=category
                )
            except Exception as e:
                print(f"GPT feedback failed: {e}")
                detailed_feedback = self._generate_fallback_feedback(xlnet_result)
        else:
            detailed_feedback = self._generate_fallback_feedback(xlnet_result)
        
        # Combine results
        return {
            'score': xlnet_result['score'],
            'confidence': xlnet_result['confidence'],
            'breakdown': {
                'semantic': xlnet_result['semantic_score'],
                'keywords': xlnet_result['keyword_score'],
                'length': xlnet_result['length_score'],
                'coherence': xlnet_result['coherence_score']
            },
            'quick_analysis': xlnet_result['analysis'],
            'detailed_feedback': detailed_feedback,
            'evaluation_method': 'hybrid' if self.use_gpt else 'xlnet_only'
        }
    
    async def _get_gpt_feedback(
        self,
        question: str,
        answer: str,
        xlnet_score: float,
        category: str = None
    ) -> Dict:
        """Get detailed feedback from GPT"""
        
        prompt = f"""You are an expert interview coach. Evaluate this interview answer.

Question: {question}
Category: {category or 'General'}
Answer: {answer}

The answer received an initial score of {xlnet_score}/100 based on:
- Semantic relevance
- Keyword coverage
- Answer length
- Coherence

Provide detailed feedback in JSON format:
{{
    "strengths": ["strength 1", "strength 2"],
    "improvements": ["improvement 1", "improvement 2"],
    "suggestions": "Specific actionable advice",
    "example_answer": "Brief example of a better answer (2-3 sentences)"
}}

Keep it concise and actionable."""

        try:
            response = await call_llm_chat(
                system_prompt="You are a professional interview coach providing constructive feedback.",
                user_message=prompt,
                model="gpt-4o-mini",
                max_tokens=400
            )
            
            # Try to parse JSON
            import json
            feedback = json.loads(response)
            return feedback
            
        except json.JSONDecodeError:
            # If not JSON, structure the response
            return {
                'strengths': ['Answer provided'],
                'improvements': ['Could be more detailed'],
                'suggestions': response[:200],
                'example_answer': 'Focus on specific examples and achievements.'
            }
    
    def _generate_fallback_feedback(self, xlnet_result: Dict) -> Dict:
        """Generate feedback based on XLNet scores when GPT unavailable"""
        
        score = xlnet_result['score']
        semantic = xlnet_result['semantic_score']
        keyword = xlnet_result['keyword_score']
        length = xlnet_result['length_score']
        coherence = xlnet_result['coherence_score']
        
        strengths = []
        improvements = []
        
        # Analyze strengths
        if semantic >= 70:
            strengths.append("Answer is relevant to the question")
        if keyword >= 70:
            strengths.append("Good coverage of key concepts")
        if length >= 70:
            strengths.append("Appropriate answer length")
        if coherence >= 70:
            strengths.append("Well-structured response")
        
        # Analyze improvements
        if semantic < 60:
            improvements.append("Make your answer more relevant to the question")
        if keyword < 60:
            improvements.append("Include more specific keywords and concepts")
        if length < 60:
            improvements.append("Provide more detail and examples")
        if coherence < 60:
            improvements.append("Improve answer structure with clear transitions")
        
        # Default if no specific feedback
        if not strengths:
            strengths = ["You attempted the question"]
        if not improvements:
            improvements = ["Keep practicing to improve further"]
        
        # Generate suggestions based on score
        if score >= 80:
            suggestions = "Excellent answer! Minor refinements could make it even stronger."
        elif score >= 60:
            suggestions = "Good foundation. Add specific examples and use the STAR method (Situation, Task, Action, Result)."
        elif score >= 40:
            suggestions = "Focus on answering the question directly. Include relevant examples from your experience."
        else:
            suggestions = "Take time to understand the question. Structure your answer with clear points and examples."
        
        return {
            'strengths': strengths,
            'improvements': improvements,
            'suggestions': suggestions,
            'example_answer': 'Use specific examples and quantify your achievements when possible.'
        }
    
    def evaluate_answer_sync(self, question: str, answer: str, **kwargs) -> Dict:
        """Synchronous wrapper for evaluate_answer"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                self.evaluate_answer(question, answer, **kwargs)
            )
            return result
        finally:
            loop.close()


# Singleton instance
_hybrid_evaluator = None

def get_hybrid_evaluator() -> HybridAnswerEvaluator:
    """Get or create hybrid evaluator instance"""
    global _hybrid_evaluator
    if _hybrid_evaluator is None:
        _hybrid_evaluator = HybridAnswerEvaluator()
    return _hybrid_evaluator


# Quick test
async def test_hybrid():
    """Test hybrid evaluator"""
    evaluator = get_hybrid_evaluator()
    
    print("\n🧪 Testing Hybrid Evaluator\n")
    
    result = await evaluator.evaluate_answer(
        question="Tell me about a time you solved a difficult problem.",
        answer="In my previous role as a software engineer, I encountered a critical performance issue where our application was taking 30 seconds to load. I analyzed the code, identified inefficient database queries, implemented caching, and optimized the queries. This reduced load time to 3 seconds, improving user satisfaction by 85%.",
        expected_keywords=['problem', 'solution', 'result', 'impact'],
        category='behavioral'
    )
    
    print(f"📊 Score: {result['score']}/100")
    print(f"🎯 Confidence: {result['confidence']}")
    print(f"\n📈 Breakdown:")
    for key, value in result['breakdown'].items():
        print(f"  {key.capitalize()}: {value}")
    
    print(f"\n💡 Quick Analysis: {result['quick_analysis']}")
    
    if result['detailed_feedback']:
        print(f"\n✨ Detailed Feedback:")
        print(f"  Strengths: {', '.join(result['detailed_feedback']['strengths'])}")
        print(f"  Improvements: {', '.join(result['detailed_feedback']['improvements'])}")
        print(f"  Suggestions: {result['detailed_feedback']['suggestions']}")
    
    print(f"\n🔧 Method: {result['evaluation_method']}")


if __name__ == "__main__":
    asyncio.run(test_hybrid())
