"""
XLNet-based Answer Evaluator for Interview Responses
Hybrid approach: XLNet for scoring, GPT for detailed feedback
"""

import torch
from transformers import XLNetTokenizer, XLNetForSequenceClassification
from sentence_transformers import SentenceTransformer, util
import numpy as np
from typing import Dict, List, Tuple
import os

class XLNetAnswerEvaluator:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"🔧 Using device: {self.device}")
        
        # Initialize models
        self.tokenizer = None
        self.xlnet_model = None
        self.sentence_model = None
        self.initialized = False
        
        # Try to load models
        try:
            self._load_models()
        except Exception as e:
            print(f"⚠️  XLNet models not loaded: {e}")
            print("💡 Will use fallback scoring method")
    
    def _load_models(self):
        """Load XLNet and sentence transformer models"""
        print("📦 Loading XLNet models...")
        
        # Load sentence transformer for semantic similarity
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.sentence_model.to(self.device)
        
        # For now, we'll use sentence similarity
        # You can fine-tune XLNet on interview data later
        self.initialized = True
        print("✅ Models loaded successfully!")
    
    def evaluate_answer(
        self, 
        question: str, 
        answer: str, 
        expected_keywords: List[str] = None,
        context: str = None
    ) -> Dict:
        """
        Evaluate interview answer using XLNet-based approach
        
        Args:
            question: The interview question
            answer: User's answer
            expected_keywords: Optional list of expected keywords
            context: Optional context (job role, category)
        
        Returns:
            Dict with score, confidence, and analysis
        """
        if not answer or len(answer.strip()) < 10:
            return {
                'score': 0,
                'confidence': 1.0,
                'semantic_score': 0,
                'keyword_score': 0,
                'length_score': 0,
                'coherence_score': 0,
                'analysis': 'Answer too short'
            }
        
        # Calculate multiple scoring dimensions
        semantic_score = self._calculate_semantic_similarity(question, answer)
        keyword_score = self._calculate_keyword_coverage(answer, expected_keywords)
        length_score = self._calculate_length_score(answer)
        coherence_score = self._calculate_coherence(answer)
        
        # Weighted combination
        weights = {
            'semantic': 0.40,
            'keyword': 0.25,
            'length': 0.15,
            'coherence': 0.20
        }
        
        final_score = (
            semantic_score * weights['semantic'] +
            keyword_score * weights['keyword'] +
            length_score * weights['length'] +
            coherence_score * weights['coherence']
        )
        
        # Calculate confidence based on answer quality
        confidence = self._calculate_confidence(answer, semantic_score)
        
        return {
            'score': round(final_score, 2),
            'confidence': round(confidence, 2),
            'semantic_score': round(semantic_score, 2),
            'keyword_score': round(keyword_score, 2),
            'length_score': round(length_score, 2),
            'coherence_score': round(coherence_score, 2),
            'analysis': self._generate_quick_analysis(
                final_score, semantic_score, keyword_score, length_score, coherence_score
            )
        }
    
    def _calculate_semantic_similarity(self, question: str, answer: str) -> float:
        """Calculate semantic similarity between question and answer"""
        if not self.initialized or not self.sentence_model:
            # Fallback: simple word overlap
            q_words = set(question.lower().split())
            a_words = set(answer.lower().split())
            overlap = len(q_words & a_words)
            return min(overlap / max(len(q_words), 1) * 100, 100)
        
        try:
            # Encode question and answer
            q_embedding = self.sentence_model.encode(question, convert_to_tensor=True)
            a_embedding = self.sentence_model.encode(answer, convert_to_tensor=True)
            
            # Calculate cosine similarity
            similarity = util.cos_sim(q_embedding, a_embedding).item()
            
            # Convert to 0-100 scale
            return max(0, min(100, similarity * 100))
        except Exception as e:
            print(f"Error in semantic similarity: {e}")
            return 50.0
    
    def _calculate_keyword_coverage(self, answer: str, keywords: List[str] = None) -> float:
        """Calculate how many expected keywords are covered"""
        if not keywords:
            return 75.0  # Neutral score if no keywords provided
        
        answer_lower = answer.lower()
        found_keywords = sum(1 for kw in keywords if kw.lower() in answer_lower)
        
        coverage = (found_keywords / len(keywords)) * 100
        return min(coverage, 100)
    
    def _calculate_length_score(self, answer: str) -> float:
        """Score based on answer length (optimal range: 50-300 words)"""
        words = answer.split()
        word_count = len(words)
        
        if word_count < 20:
            return (word_count / 20) * 50  # Too short
        elif word_count < 50:
            return 50 + ((word_count - 20) / 30) * 25  # Getting better
        elif word_count <= 300:
            return 75 + ((300 - abs(word_count - 150)) / 150) * 25  # Optimal
        else:
            return max(50, 100 - ((word_count - 300) / 10))  # Too long
    
    def _calculate_coherence(self, answer: str) -> float:
        """Calculate answer coherence based on structure"""
        sentences = [s.strip() for s in answer.split('.') if s.strip()]
        
        if len(sentences) < 2:
            return 50.0  # Single sentence
        
        # Check for transition words
        transition_words = [
            'however', 'therefore', 'moreover', 'furthermore', 'additionally',
            'consequently', 'thus', 'hence', 'because', 'since', 'although',
            'while', 'whereas', 'first', 'second', 'finally', 'also', 'for example'
        ]
        
        answer_lower = answer.lower()
        transitions_found = sum(1 for word in transition_words if word in answer_lower)
        
        # Score based on structure
        structure_score = min(len(sentences) / 5 * 50, 50)  # Up to 50 for good structure
        transition_score = min(transitions_found / 3 * 50, 50)  # Up to 50 for transitions
        
        return structure_score + transition_score
    
    def _calculate_confidence(self, answer: str, semantic_score: float) -> float:
        """Calculate confidence in the evaluation"""
        word_count = len(answer.split())
        
        # Higher confidence for longer, more relevant answers
        length_confidence = min(word_count / 100, 1.0)
        semantic_confidence = semantic_score / 100
        
        return (length_confidence * 0.4 + semantic_confidence * 0.6)
    
    def _generate_quick_analysis(
        self, 
        final_score: float, 
        semantic: float, 
        keyword: float, 
        length: float, 
        coherence: float
    ) -> str:
        """Generate quick analysis of the answer"""
        if final_score >= 80:
            return "Excellent answer with strong relevance and structure"
        elif final_score >= 60:
            return "Good answer, could be improved with more detail"
        elif final_score >= 40:
            return "Adequate answer, needs more relevant content"
        else:
            return "Answer needs significant improvement"
    
    def batch_evaluate(self, qa_pairs: List[Tuple[str, str]]) -> List[Dict]:
        """Evaluate multiple Q&A pairs efficiently"""
        results = []
        for question, answer in qa_pairs:
            result = self.evaluate_answer(question, answer)
            results.append(result)
        return results


# Singleton instance
_evaluator = None

def get_xlnet_evaluator() -> XLNetAnswerEvaluator:
    """Get or create XLNet evaluator instance"""
    global _evaluator
    if _evaluator is None:
        _evaluator = XLNetAnswerEvaluator()
    return _evaluator


# Quick test function
def test_evaluator():
    """Test the evaluator with sample data"""
    evaluator = get_xlnet_evaluator()
    
    test_cases = [
        {
            'question': 'What is your greatest strength?',
            'answer': 'My greatest strength is problem-solving. I excel at analyzing complex issues, breaking them down into manageable parts, and developing effective solutions. For example, in my previous role, I identified a bottleneck in our workflow and implemented a new system that improved efficiency by 40%.',
            'keywords': ['problem-solving', 'analytical', 'solutions', 'example']
        },
        {
            'question': 'Why do you want this job?',
            'answer': 'I want money.',
            'keywords': ['passion', 'growth', 'company', 'skills']
        }
    ]
    
    print("\n🧪 Testing XLNet Evaluator\n")
    for i, test in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"Q: {test['question']}")
        print(f"A: {test['answer'][:100]}...")
        
        result = evaluator.evaluate_answer(
            test['question'], 
            test['answer'], 
            test['keywords']
        )
        
        print(f"\n📊 Results:")
        print(f"  Final Score: {result['score']}/100")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Semantic: {result['semantic_score']}")
        print(f"  Keywords: {result['keyword_score']}")
        print(f"  Length: {result['length_score']}")
        print(f"  Coherence: {result['coherence_score']}")
        print(f"  Analysis: {result['analysis']}")
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    test_evaluator()
