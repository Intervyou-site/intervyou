"""
Hugging Face Model Integration for IntervYou
Provides local AI models as alternatives to OpenAI API
"""

import os
from typing import List, Dict, Optional
from functools import lru_cache

# Lazy imports to avoid loading models unnecessarily
_MODELS = {}

def get_model(model_type: str):
    """
    Lazy load models on first use
    Caches models in memory to avoid reloading
    """
    if model_type in _MODELS:
        return _MODELS[model_type]
    
    from transformers import pipeline
    
    if model_type == "text_generation":
        # For question generation and feedback
        # Options: "gpt2", "distilgpt2" (fast), "mistralai/Mistral-7B-Instruct-v0.2" (better)
        model = pipeline("text-generation", model="distilgpt2", max_length=200)
        
    elif model_type == "sentiment":
        # For answer sentiment analysis
        model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        
    elif model_type == "question_answering":
        # For evaluating if answer addresses the question
        model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
        
    elif model_type == "summarization":
        # For summarizing long answers
        model = pipeline("summarization", model="facebook/bart-large-cnn")
        
    elif model_type == "speech_recognition":
        # For video interview transcription
        # Options: whisper-tiny (fast), whisper-base (balanced), whisper-small (better accuracy)
        model = pipeline("automatic-speech-recognition", model="openai/whisper-base")
        
    elif model_type == "embeddings":
        # For semantic similarity (already in use)
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    _MODELS[model_type] = model
    return model


@lru_cache(maxsize=100)
def generate_question_local(category: str, difficulty: str = "medium") -> str:
    """
    Generate interview question using local Hugging Face model
    Alternative to OpenAI API
    """
    model = get_model("text_generation")
    
    prompt = f"Generate a {difficulty} difficulty {category} interview question:\n"
    
    result = model(prompt, max_length=100, num_return_sequences=1, temperature=0.7)
    question = result[0]['generated_text'].replace(prompt, "").strip()
    
    # Clean up the output
    if "?" in question:
        question = question.split("?")[0] + "?"
    
    return question


def evaluate_answer_sentiment(answer: str) -> Dict[str, float]:
    """
    Analyze sentiment of user's answer
    Returns: {"label": "POSITIVE/NEGATIVE", "score": 0.0-1.0}
    """
    model = get_model("sentiment")
    result = model(answer[:512])  # Limit to 512 tokens
    return result[0]


def check_answer_relevance(question: str, answer: str) -> Dict[str, any]:
    """
    Check if answer is relevant to the question
    Uses question-answering model to extract key info
    """
    model = get_model("question_answering")
    
    try:
        result = model(question=question, context=answer)
        return {
            "relevant": result['score'] > 0.3,
            "confidence": result['score'],
            "extracted_answer": result['answer']
        }
    except Exception as e:
        return {"relevant": True, "confidence": 0.5, "error": str(e)}


def summarize_answer(answer: str, max_length: int = 50) -> str:
    """
    Summarize long answers for quick review
    """
    if len(answer.split()) < 30:
        return answer
    
    model = get_model("summarization")
    result = model(answer, max_length=max_length, min_length=10, do_sample=False)
    return result[0]['summary_text']


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio file to text using Whisper
    Alternative to paid transcription services
    
    Args:
        audio_path: Path to audio file (supports .wav, .mp3, .webm, .m4a)
    
    Returns:
        Transcribed text string
    """
    try:
        model = get_model("speech_recognition")
        result = model(audio_path)
        
        # Handle different return formats
        if isinstance(result, dict):
            return result.get('text', '')
        elif isinstance(result, list) and len(result) > 0:
            return result[0].get('text', '')
        else:
            return str(result)
    except Exception as e:
        print(f"Whisper transcription error: {e}")
        return ""


def get_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts
    Returns: 0.0 (different) to 1.0 (identical)
    """
    from sentence_transformers import util
    
    model = get_model("embeddings")
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)
    
    similarity = util.cos_sim(embeddings1, embeddings2)
    return float(similarity[0][0])


def evaluate_answer_comprehensive(question: str, answer: str, expected_keywords: List[str] = None) -> Dict:
    """
    Comprehensive answer evaluation using multiple Hugging Face models
    Combines sentiment, relevance, keyword matching, and quality checks
    """
    # Quality checks first
    word_count = len(answer.split())
    char_count = len(answer.strip())
    
    # Immediate fail for very short answers
    if word_count < 3 or char_count < 10:
        return {
            "score": 1.0,
            "sentiment": {"label": "NEGATIVE", "score": 0.0},
            "relevance": {"relevant": False, "confidence": 0.0},
            "keyword_score": 0.0,
            "word_count": word_count,
            "quality_issues": ["Answer too short", "Minimum 3 words required"],
            "feedback": "Your answer is too short. Please provide a detailed response with at least 10-15 words explaining your understanding."
        }
    
    # Check for gibberish or single-word answers
    if word_count < 5:
        return {
            "score": 2.0,
            "sentiment": {"label": "NEGATIVE", "score": 0.0},
            "relevance": {"relevant": False, "confidence": 0.0},
            "keyword_score": 0.0,
            "word_count": word_count,
            "quality_issues": ["Answer lacks detail", "Needs more explanation"],
            "feedback": "Your answer is too brief. Please elaborate with specific details and examples to demonstrate your understanding."
        }
    
    # Sentiment analysis
    sentiment = evaluate_answer_sentiment(answer)
    
    # Relevance check
    relevance = check_answer_relevance(question, answer)
    
    # Semantic similarity check
    try:
        similarity = get_semantic_similarity(question, answer)
    except Exception:
        similarity = 0.0
    
    # Keyword matching (if provided)
    keyword_score = 0.0
    if expected_keywords:
        answer_lower = answer.lower()
        matched = sum(1 for kw in expected_keywords if kw.lower() in answer_lower)
        keyword_score = matched / len(expected_keywords) if expected_keywords else 0.0
    
    # Calculate overall score with stricter criteria
    base_score = 0.0  # Start from 0, not 5
    quality_issues = []
    
    # Length scoring (0-2 points)
    if word_count >= 50:
        base_score += 2.0
    elif word_count >= 30:
        base_score += 1.5
    elif word_count >= 15:
        base_score += 1.2
    elif word_count >= 10:
        base_score += 0.8
    else:
        quality_issues.append("Answer could be more detailed")
    
    # Semantic similarity (0-4 points) - CRITICAL
    if similarity >= 0.7:
        base_score += 4.0
    elif similarity >= 0.5:
        base_score += 2.5
    elif similarity >= 0.3:
        base_score += 1.0
    else:
        quality_issues.append("Answer doesn't address the question well")
    
    # Relevance scoring (0-2 points)
    if relevance.get('relevant', False):
        confidence = relevance.get('confidence', 0.0)
        if confidence >= 0.7:
            base_score += 2.0
        elif confidence >= 0.4:
            base_score += 1.2
        else:
            base_score += 0.5
    else:
        quality_issues.append("Answer lacks relevance to the question")
    
    # Sentiment bonus (0-1 point)
    if sentiment['label'] == 'POSITIVE' and sentiment['score'] > 0.7:
        base_score += 1.0
    elif sentiment['label'] == 'POSITIVE':
        base_score += 0.5
    
    # Keyword bonus (0-1 points)
    if keyword_score >= 0.8:
        base_score += 1.0
    elif keyword_score >= 0.5:
        base_score += 0.7
    elif keyword_score > 0:
        base_score += 0.3
    
    # Cap at 10
    final_score = min(base_score, 10.0)
    
    # Additional penalty for very low quality
    if word_count < 10 and similarity < 0.3:
        final_score = min(final_score, 3.0)
    
    return {
        "score": round(final_score, 1),
        "sentiment": sentiment,
        "relevance": relevance,
        "keyword_score": keyword_score,
        "semantic_similarity": round(similarity, 3),
        "word_count": word_count,
        "quality_issues": quality_issues,
        "feedback": generate_feedback(final_score, sentiment, relevance, word_count, similarity, quality_issues)
    }


def generate_feedback(score: float, sentiment: Dict, relevance: Dict, word_count: int = 0, similarity: float = 0.0, quality_issues: List[str] = None) -> str:
    """
    Generate human-readable feedback based on evaluation with specific guidance
    """
    feedback = []
    
    # Score-based feedback
    if score >= 9:
        feedback.append("🌟 Outstanding answer! Comprehensive, well-structured, and directly addresses the question.")
    elif score >= 7:
        feedback.append("✅ Good answer! You demonstrate understanding, but there's room for more detail.")
    elif score >= 5:
        feedback.append("⚠️ Adequate answer, but needs significant improvement in depth and relevance.")
    elif score >= 3:
        feedback.append("❌ Poor answer. Your response lacks detail and doesn't adequately address the question.")
    else:
        feedback.append("❌ Insufficient answer. Please provide a complete, detailed response.")
    
    # Length feedback
    if word_count < 10:
        feedback.append(f"Your answer is too short ({word_count} words). Aim for at least 15-20 words to properly explain your understanding.")
    elif word_count < 20:
        feedback.append(f"Your answer could be more detailed ({word_count} words). Try to elaborate with examples or additional context.")
    
    # Similarity feedback
    if similarity < 0.3:
        feedback.append("⚠️ Your answer doesn't seem to address the question. Make sure you understand what's being asked.")
    elif similarity < 0.5:
        feedback.append("Your answer is somewhat relevant but could be more focused on the specific question.")
    
    # Relevance feedback
    if not relevance.get('relevant', True):
        feedback.append("Make sure your answer directly addresses the question asked.")
    
    # Sentiment feedback
    if sentiment['label'] == 'NEGATIVE' and score < 7:
        feedback.append("Try to maintain a more positive and confident tone in your response.")
    
    # Quality issues
    if quality_issues:
        for issue in quality_issues[:2]:  # Limit to 2 issues
            feedback.append(f"• {issue}")
    
    # Constructive suggestions
    if score < 7:
        feedback.append("\n💡 Tips: Use specific examples, explain your reasoning, and ensure your answer is complete.")
    
    return " ".join(feedback)


# ============================================
# Hybrid Mode: Use OpenAI if available, fallback to Hugging Face
# ============================================

def generate_question_hybrid(category: str, use_openai: bool = True) -> str:
    """
    Try OpenAI first, fallback to Hugging Face if API key missing or fails
    """
    if use_openai and os.getenv("OPENAI_API_KEY"):
        try:
            from llm_utils import call_llm_chat
            import asyncio
            
            prompt = f"Generate one concise {category} interview question. Return only the question."
            result = asyncio.run(call_llm_chat("You are an interview coach.", prompt))
            return result.strip()
        except Exception as e:
            print(f"OpenAI failed, using local model: {e}")
    
    # Fallback to local Hugging Face model
    return generate_question_local(category)


def evaluate_answer_hybrid(question: str, answer: str, use_openai: bool = True) -> Dict:
    """
    Try OpenAI first, fallback to Hugging Face if API key missing or fails
    Uses strict evaluation criteria to prevent inflated scores
    """
    # Quick quality check first - applies to both OpenAI and HF
    word_count = len(answer.split())
    char_count = len(answer.strip())
    
    # Immediate fail for very short answers
    if word_count < 3 or char_count < 10:
        return {
            "score": 1.0,
            "feedback": f"Answer too short ({word_count} words). Please provide a detailed response with at least 10-15 words.",
            "source": "quality_check",
            "word_count": word_count,
            "quality_issues": ["Answer too short"]
        }
    
    if use_openai and os.getenv("OPENAI_API_KEY"):
        try:
            from llm_utils import call_llm_chat
            import asyncio
            
            # More detailed prompt for better evaluation
            prompt = f"""Question: {question}
Answer: {answer}

Evaluate this answer strictly on a scale of 1-10 considering:
1. Relevance to the question (does it actually answer what was asked?)
2. Completeness (is it detailed enough?)
3. Accuracy (is the information correct?)
4. Clarity (is it well-explained?)

Word count: {word_count} words
Minimum expected: 15-20 words for a good answer

Provide:
- Score (1-10, be strict - short or irrelevant answers should get 1-3)
- Brief feedback explaining the score

Format: Score: X/10
Feedback: ..."""
            
            result = asyncio.run(call_llm_chat("You are a strict interview evaluator. Grade answers honestly - don't be lenient with poor answers.", prompt))
            
            # Parse OpenAI response
            import re
            score_match = re.search(r'(?:Score:?\s*)?(\d+(?:\.\d+)?)\s*/\s*10', result, re.IGNORECASE)
            score = float(score_match.group(1)) if score_match else None
            
            # If no score found or answer is too short, use HF evaluation
            if score is None or word_count < 5:
                raise Exception("Invalid OpenAI response or answer too short")
            
            # Apply additional penalty for very short answers
            if word_count < 10:
                score = min(score, 3.0)
            elif word_count < 15:
                score = min(score, 5.0)
            
            return {
                "score": round(score, 1),
                "feedback": result,
                "source": "openai",
                "word_count": word_count
            }
        except Exception as e:
            print(f"OpenAI failed, using local model: {e}")
    
    # Fallback to local Hugging Face evaluation (already strict)
    result = evaluate_answer_comprehensive(question, answer)
    result["source"] = "huggingface"
    return result


# ============================================
# Model Management
# ============================================

def preload_models():
    """
    Preload commonly used models at startup to reduce first-request latency
    Call this in your FastAPI startup event
    """
    print("🤗 Preloading Hugging Face models...")
    try:
        get_model("embeddings")
        print("   ✅ Embeddings model loaded")
        get_model("sentiment")
        print("   ✅ Sentiment model loaded")
        print("🤗 Hugging Face models ready!")
    except Exception as e:
        print(f"   ⚠️  Model preload failed: {e}")


def clear_model_cache():
    """
    Clear loaded models from memory
    Useful for memory management
    """
    global _MODELS
    _MODELS.clear()
    print("🗑️  Model cache cleared")


def get_model_info() -> Dict:
    """
    Get information about loaded models
    """
    return {
        "loaded_models": list(_MODELS.keys()),
        "model_count": len(_MODELS),
        "available_types": [
            "text_generation",
            "sentiment",
            "question_answering",
            "summarization",
            "speech_recognition",
            "embeddings"
        ]
    }


# ============================================
# Example Usage
# ============================================

if __name__ == "__main__":
    # Test the models
    print("Testing Hugging Face integration...\n")
    
    # 1. Generate question
    question = generate_question_local("Python", "medium")
    print(f"Generated Question: {question}\n")
    
    # 2. Evaluate answer
    answer = "Python is a high-level programming language known for its simplicity and readability."
    evaluation = evaluate_answer_comprehensive(question, answer)
    print(f"Evaluation: {evaluation}\n")
    
    # 3. Semantic similarity
    similarity = get_semantic_similarity(
        "What is Python?",
        "Python is a programming language"
    )
    print(f"Similarity: {similarity}\n")
    
    # 4. Model info
    info = get_model_info()
    print(f"Model Info: {info}")
