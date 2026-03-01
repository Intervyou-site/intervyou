"""
AI Interviewer Text-to-Speech Service
Provides voice synthesis for AI interviewer avatar
"""

import os
import requests
import base64
from typing import Optional, Dict
import hashlib


class AIInterviewerTTS:
    """Service for generating AI interviewer voice"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_tts_url = "https://api.openai.com/v1/audio/speech"
        self.cache_dir = "static/tts_cache"
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist"""
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_key(self, text: str, voice: str) -> str:
        """Generate cache key for text and voice combination"""
        content = f"{text}_{voice}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get full path for cached audio file"""
        return os.path.join(self.cache_dir, f"{cache_key}.mp3")
    
    async def generate_speech(
        self, 
        text: str, 
        voice: str = "alloy",
        use_cache: bool = True
    ) -> Dict:
        """
        Generate speech audio from text
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            use_cache: Whether to use cached audio if available
        
        Returns:
            Dict with audio_url, audio_base64, and duration
        """
        # Check cache first
        if use_cache:
            cache_key = self._get_cache_key(text, voice)
            cache_path = self._get_cache_path(cache_key)
            
            if os.path.exists(cache_path):
                # Return cached audio
                with open(cache_path, 'rb') as f:
                    audio_data = f.read()
                
                return {
                    "success": True,
                    "audio_url": f"/static/tts_cache/{cache_key}.mp3",
                    "audio_base64": base64.b64encode(audio_data).decode('utf-8'),
                    "cached": True,
                    "text": text
                }
        
        # Generate new audio
        if not self.openai_api_key:
            return self._fallback_response(text)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "tts-1",
                "input": text,
                "voice": voice,
                "response_format": "mp3"
            }
            
            response = requests.post(
                self.openai_tts_url, 
                headers=headers, 
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                audio_data = response.content
                
                # Cache the audio
                if use_cache:
                    cache_key = self._get_cache_key(text, voice)
                    cache_path = self._get_cache_path(cache_key)
                    
                    with open(cache_path, 'wb') as f:
                        f.write(audio_data)
                    
                    audio_url = f"/static/tts_cache/{cache_key}.mp3"
                else:
                    audio_url = None
                
                return {
                    "success": True,
                    "audio_url": audio_url,
                    "audio_base64": base64.b64encode(audio_data).decode('utf-8'),
                    "cached": False,
                    "text": text
                }
            else:
                error_msg = f"OpenAI TTS error: {response.status_code}"
                if response.status_code == 429:
                    error_msg += " (Rate limit exceeded - using browser TTS fallback)"
                elif response.status_code == 401:
                    error_msg += " (Invalid API key)"
                print(error_msg)
                return self._fallback_response(text, use_browser_tts=True)
                
        except Exception as e:
            print(f"TTS generation error: {e}")
            return self._fallback_response(text)
    
    def _fallback_response(self, text: str, use_browser_tts: bool = False) -> Dict:
        """Fallback response when TTS is not available"""
        return {
            "success": False,
            "audio_url": None,
            "audio_base64": None,
            "cached": False,
            "text": text,
            "use_browser_tts": use_browser_tts,
            "message": "Using browser text-to-speech" if use_browser_tts else "Text-to-speech not available. Please read the question."
        }
    
    def get_available_voices(self) -> Dict:
        """Get list of available voices with descriptions"""
        return {
            "alloy": {
                "name": "Alloy",
                "description": "Neutral, professional voice",
                "gender": "neutral",
                "recommended": True
            },
            "echo": {
                "name": "Echo",
                "description": "Male, clear voice",
                "gender": "male",
                "recommended": False
            },
            "fable": {
                "name": "Fable",
                "description": "British accent, expressive",
                "gender": "male",
                "recommended": False
            },
            "onyx": {
                "name": "Onyx",
                "description": "Deep, authoritative voice",
                "gender": "male",
                "recommended": False
            },
            "nova": {
                "name": "Nova",
                "description": "Warm, friendly female voice",
                "gender": "female",
                "recommended": True
            },
            "shimmer": {
                "name": "Shimmer",
                "description": "Soft, gentle female voice",
                "gender": "female",
                "recommended": False
            }
        }
    
    async def generate_question_audio(
        self,
        question: str,
        greeting: bool = False
    ) -> Dict:
        """
        Generate audio for interview question with optional greeting
        
        Args:
            question: The interview question
            greeting: Whether to add a greeting prefix
        
        Returns:
            Dict with audio data
        """
        if greeting:
            text = f"Hello! I'm Sarah, your AI interview assistant. Here's your question: {question}"
        else:
            text = question
        
        # Use Nova voice (warm, friendly female) for interviewer
        return await self.generate_speech(text, voice="nova")
    
    async def generate_followup_audio(self, followup_question: str) -> Dict:
        """Generate audio for follow-up question"""
        text = f"Interesting. Let me ask you this: {followup_question}"
        return await self.generate_speech(text, voice="nova")
    
    async def generate_encouragement(self, message: str = None) -> Dict:
        """Generate encouraging audio message"""
        if not message:
            messages = [
                "Great answer! Let's continue.",
                "Thank you for sharing that.",
                "That's insightful. Moving on.",
                "Excellent. Next question.",
                "I appreciate your detailed response."
            ]
            import random
            message = random.choice(messages)
        
        return await self.generate_speech(message, voice="nova")


# Singleton instance
_tts_service = None

def get_tts_service() -> AIInterviewerTTS:
    """Get or create the TTS service instance"""
    global _tts_service
    if _tts_service is None:
        _tts_service = AIInterviewerTTS()
    return _tts_service
