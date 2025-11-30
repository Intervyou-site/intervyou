"""
AI Model Integration - Currently Using TextBlob

NOTE: As of November 2024, Hugging Face has deprecated their free Inference API.
The system now uses TextBlob for sentiment analysis, which works great for interview evaluation.

TextBlob provides:
- Sentiment analysis (positive/negative/neutral)
- Polarity scores (-1 to +1)
- Subjectivity analysis
- No API key required
- Fast and reliable

For advanced AI features, you can integrate:
- OpenAI API (paid)
- Anthropic Claude (paid)
- Local models using transformers library (free but requires GPU)

The core validation and scoring improvements work independently of AI models.
"""

import requests
import json
from typing import Dict, List, Any, Optional
import time

# Hugging Face Inference API endpoints (free tier)
# Updated to new router endpoint as of Nov 2024
HF_API_BASE = "https://api-inference.huggingface.co/models"  # Deprecated
HF_API_ROUTER = "https://api-inference.huggingface.co"  # New router endpoint

# Free models available without authentication
FREE_MODELS = {
    "sentiment": "distilbert-base-uncased-finetuned-sst-2-english",
    "emotion": "j-hartmann/emotion-english-distilroberta-base",
    "text_quality": "textattack/roberta-base-CoLA",
    "grammar": "textattack/roberta-base-CoLA",
    "summarization": "facebook/bart-large-cnn",
    "question_answering": "deepset/roberta-base-squad2"
}


class FreeAIAnalyzer:
    """Free AI analysis using Hugging Face models"""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize analyzer
        
        Args:
            api_token: Optional HF API token for higher rate limits
                      If None, uses public inference (limited requests)
        """
        self.api_token = api_token
        self.headers = {}
        if api_token:
            self.headers["Authorization"] = f"Bearer {api_token}"
        
        self.request_delay = 1.0 if not api_token else 0.1  # Rate limiting
        self.last_request_time = 0
    
    def _make_request(self, model_name: str, payload: Dict) -> Optional[Dict]:
        """Make request to HF Inference API with rate limiting"""
        try:
            # Rate limiting
            elapsed = time.time() - self.last_request_time
            if elapsed < self.request_delay:
                time.sleep(self.request_delay - elapsed)
            
            # Use the router endpoint (new format)
            url = f"{HF_API_ROUTER}/models/{model_name}"
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            self.last_request_time = time.time()
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                # Model loading, wait and retry once
                print(f"⏳ Model {model_name} loading, waiting 20 seconds...")
                time.sleep(20)
                response = requests.post(url, headers=self.headers, json=payload, timeout=30)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"⚠️ Model still loading after retry")
            elif response.status_code == 401:
                print(f"⚠️ Authentication failed - check your HF token")
            elif response.status_code == 404:
                print(f"⚠️ Model not found: {model_name}")
            else:
                print(f"⚠️ API request failed: {response.status_code}")
            
            return None
        
        except Exception as e:
            print(f"⚠️ Request error: {e}")
            return None
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment using TextBlob (reliable and fast)
        
        Returns:
            {
                "label": "POSITIVE" | "NEGATIVE" | "NEUTRAL",
                "score": 0.0-1.0,
                "confidence": "high" | "medium" | "low"
            }
        """
        if not text or len(text.strip()) < 3:
            return {"label": "NEUTRAL", "score": 0.5, "confidence": "low"}
        
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to +1
            
            # Convert polarity to label
            if polarity > 0.1:
                label = "POSITIVE"
            elif polarity < -0.1:
                label = "NEGATIVE"
            else:
                label = "NEUTRAL"
            
            # Convert to 0-1 score
            score = (polarity + 1) / 2  # Convert -1 to +1 range to 0 to 1
            
            # Determine confidence based on absolute polarity
            abs_polarity = abs(polarity)
            if abs_polarity > 0.5:
                confidence = "high"
            elif abs_polarity > 0.2:
                confidence = "medium"
            else:
                confidence = "low"
            
            return {
                "label": label,
                "score": round(score, 3),
                "confidence": confidence,
                "polarity": round(polarity, 3)
            }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {"label": "NEUTRAL", "score": 0.5, "confidence": "low"}
    
    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """
        Analyze emotions using TextBlob sentiment as a proxy
        Maps sentiment to basic emotions
        
        Returns:
            {
                "dominant_emotion": str,
                "emotions": {emotion: score},
                "confidence": float
            }
        """
        if not text or len(text.strip()) < 3:
            return {"dominant_emotion": "neutral", "emotions": {}, "confidence": 0.0}
        
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Map sentiment to emotions
            emotions = {}
            if polarity > 0.3:
                emotions["joy"] = round(polarity, 3)
                emotions["confidence"] = round(polarity * 0.8, 3)
                dominant = "joy"
            elif polarity < -0.3:
                emotions["sadness"] = round(abs(polarity), 3)
                emotions["concern"] = round(abs(polarity) * 0.7, 3)
                dominant = "sadness"
            else:
                emotions["neutral"] = round(1 - abs(polarity), 3)
                emotions["calm"] = round((1 - subjectivity) * 0.8, 3)
                dominant = "neutral"
            
            confidence = abs(polarity) if abs(polarity) > 0.1 else 0.5
            
            return {
                "dominant_emotion": dominant,
                "emotions": emotions,
                "confidence": round(confidence, 3)
            }
        except Exception as e:
            print(f"Emotion analysis error: {e}")
            return {"dominant_emotion": "neutral", "emotions": {}, "confidence": 0.0}
    
    def analyze_text_quality(self, text: str) -> Dict[str, Any]:
        """
        Analyze text quality using basic heuristics
        
        Returns:
            {
                "is_acceptable": bool,
                "quality_score": 0.0-1.0,
                "issues": List[str]
            }
        """
        if not text or len(text.strip()) < 3:
            return {"is_acceptable": False, "quality_score": 0.0, "issues": ["Text too short"]}
        
        try:
            words = text.split()
            word_count = len(words)
            sentences = text.count('.') + text.count('!') + text.count('?')
            
            issues = []
            quality_score = 0.7  # Base score
            
            # Check length
            if word_count < 10:
                issues.append("Response too brief - provide more detail")
                quality_score -= 0.2
            elif word_count > 200:
                issues.append("Response very long - consider being more concise")
                quality_score -= 0.1
            else:
                quality_score += 0.1
            
            # Check sentence structure
            if sentences == 0:
                issues.append("No clear sentence structure")
                quality_score -= 0.2
            elif word_count / max(sentences, 1) > 40:
                issues.append("Sentences may be too long")
                quality_score -= 0.1
            
            # Check for filler words
            filler_words = ['um', 'uh', 'like', 'you know', 'basically', 'actually']
            filler_count = sum(text.lower().count(word) for word in filler_words)
            if filler_count > 3:
                issues.append(f"Too many filler words detected ({filler_count})")
                quality_score -= 0.15
            
            quality_score = max(0.0, min(1.0, quality_score))
            is_acceptable = quality_score >= 0.5
            
            return {
                "is_acceptable": is_acceptable,
                "quality_score": round(quality_score, 3),
                "issues": issues if issues else []
            }
        except Exception as e:
            print(f"Text quality analysis error: {e}")
            return {"is_acceptable": True, "quality_score": 0.7, "issues": []}
    
    def summarize_text(self, text: str, max_length: int = 130) -> str:
        """
        Summarize text using free BART model
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
        
        Returns:
            Summary string
        """
        if not text or len(text.strip()) < 50:
            return text
        
        try:
            result = self._make_request(
                FREE_MODELS["summarization"],
                {
                    "inputs": text[:1024],
                    "parameters": {
                        "max_length": max_length,
                        "min_length": 30,
                        "do_sample": False
                    }
                }
            )
            
            if result and isinstance(result, list) and len(result) > 0:
                return result[0].get("summary_text", text)
        except Exception as e:
            print(f"Summarization error: {e}")
        
        return text
    
    def analyze_interview_response(self, text: str, question: str = "") -> Dict[str, Any]:
        """
        Comprehensive interview response analysis
        
        Args:
            text: Interview response text
            question: Optional interview question for context
        
        Returns:
            Comprehensive analysis including sentiment, emotion, quality
        """
        analysis = {
            "sentiment": {},
            "emotion": {},
            "quality": {},
            "overall_score": 0.0,
            "strengths": [],
            "improvements": []
        }
        
        if not text or len(text.strip()) < 10:
            analysis["overall_score"] = 0.0
            analysis["improvements"] = ["Response too short - provide more detailed answers"]
            return analysis
        
        try:
            # Sentiment analysis
            sentiment = self.analyze_sentiment(text)
            analysis["sentiment"] = sentiment
            
            # Emotion analysis
            emotion = self.analyze_emotion(text)
            analysis["emotion"] = emotion
            
            # Text quality
            quality = self.analyze_text_quality(text)
            analysis["quality"] = quality
            
            # Calculate overall score
            sentiment_score = sentiment.get("score", 0.5)
            if sentiment.get("label") == "NEGATIVE":
                sentiment_score = 1 - sentiment_score
            
            emotion_score = emotion.get("confidence", 0.5)
            quality_score = quality.get("quality_score", 0.5)
            
            # Weighted average
            overall = (sentiment_score * 0.3 + emotion_score * 0.3 + quality_score * 0.4)
            analysis["overall_score"] = round(overall * 10, 2)  # Scale to 0-10
            
            # Generate strengths and improvements
            if sentiment.get("label") == "POSITIVE" and sentiment.get("score", 0) > 0.8:
                analysis["strengths"].append("Positive and confident tone")
            
            if quality.get("is_acceptable") and quality.get("quality_score", 0) > 0.8:
                analysis["strengths"].append("Clear and well-structured response")
            
            dominant_emotion = emotion.get("dominant_emotion", "").lower()
            if dominant_emotion in ["joy", "happiness", "confidence"]:
                analysis["strengths"].append("Enthusiastic and engaged delivery")
            
            # Improvements
            if sentiment.get("label") == "NEGATIVE":
                analysis["improvements"].append("Try to frame experiences more positively")
            
            if not quality.get("is_acceptable"):
                analysis["improvements"].append("Improve grammar and sentence structure")
            
            if dominant_emotion in ["fear", "sadness", "anger"]:
                analysis["improvements"].append("Work on projecting more confidence and positivity")
            
            if len(text.split()) < 30:
                analysis["improvements"].append("Provide more detailed and comprehensive answers")
            
        except Exception as e:
            print(f"Interview analysis error: {e}")
            analysis["overall_score"] = 5.0
        
        return analysis


# Singleton instance
_free_ai_analyzer = None

def get_free_ai_analyzer(api_token: Optional[str] = None) -> FreeAIAnalyzer:
    """Get or create singleton analyzer"""
    global _free_ai_analyzer
    if _free_ai_analyzer is None:
        _free_ai_analyzer = FreeAIAnalyzer(api_token)
    return _free_ai_analyzer


# Quick test function
if __name__ == "__main__":
    analyzer = FreeAIAnalyzer()
    
    # Test sentiment
    print("Testing sentiment analysis...")
    result = analyzer.analyze_sentiment("I am very excited about this opportunity and confident in my abilities!")
    print(f"Sentiment: {result}")
    
    # Test emotion
    print("\nTesting emotion analysis...")
    result = analyzer.analyze_emotion("I feel nervous but also excited about the interview")
    print(f"Emotion: {result}")
    
    # Test quality
    print("\nTesting text quality...")
    result = analyzer.analyze_text_quality("I have experience in Python and machine learning")
    print(f"Quality: {result}")
    
    # Test interview analysis
    print("\nTesting interview analysis...")
    result = analyzer.analyze_interview_response(
        "I have over 5 years of experience in software development, specializing in Python and web technologies. "
        "I'm passionate about creating efficient solutions and working in collaborative teams."
    )
    print(f"Interview Analysis: {json.dumps(result, indent=2)}")
