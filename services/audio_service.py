"""
Audio Processing Service

This service handles:
- Audio transcription using Whisper AI
- Voice analysis (pitch, energy, tone)
- Text-to-speech generation
- Audio file processing and validation
"""

import os
import logging
from typing import Dict, Optional, Tuple, Any
from io import BytesIO
import tempfile

import librosa
import numpy as np
from gtts import gTTS

logger = logging.getLogger(__name__)

class AudioService:
    """Service for audio processing and analysis"""
    
    def __init__(self, upload_folder: str, features):
        self.upload_folder = upload_folder
        self.features = features
        os.makedirs(upload_folder, exist_ok=True)
    
    async def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file to text using Whisper AI.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dictionary with transcription results
        """
        try:
            # Validate file exists
            if not os.path.exists(audio_file_path):
                return self._create_error_response("Audio file not found")
            
            # Get audio duration
            duration = self._get_audio_duration(audio_file_path)
            
            # Transcribe using available method
            transcription = await self._perform_transcription(audio_file_path)
            
            if not transcription:
                return self._create_error_response("No speech detected in audio")
            
            # Analyze transcription quality
            quality_metrics = self._analyze_transcription_quality(transcription)
            
            return {
                "success": True,
                "transcription": transcription,
                "duration": round(duration, 2),
                "word_count": len(transcription.split()),
                "quality_metrics": quality_metrics,
                "method": "whisper_ai" if self.features.huggingface_available else "fallback"
            }
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return self._create_error_response(f"Transcription failed: {str(e)}")
    
    async def analyze_voice(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Analyze voice characteristics from audio file.
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Dictionary with voice analysis results
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_file_path, sr=None)
            
            if len(y) == 0:
                return self._create_error_response("Empty audio file")
            
            # Perform various analyses
            energy_analysis = self._analyze_energy(y)
            pitch_analysis = self._analyze_pitch(y, sr)
            tone_analysis = self._analyze_tone(energy_analysis, pitch_analysis)
            speech_rate = self._analyze_speech_rate(y, sr)
            
            # Get transcription for additional analysis
            transcription_result = await self.transcribe_audio(audio_file_path)
            transcription = transcription_result.get("transcription", "")
            
            # Analyze speech patterns
            speech_patterns = self._analyze_speech_patterns(transcription)
            
            return {
                "success": True,
                "energy": energy_analysis,
                "pitch": pitch_analysis,
                "tone": tone_analysis,
                "speech_rate": speech_rate,
                "speech_patterns": speech_patterns,
                "transcription": transcription,
                "overall_assessment": self._generate_overall_assessment(
                    energy_analysis, pitch_analysis, tone_analysis, speech_patterns
                )
            }
            
        except Exception as e:
            logger.error(f"Voice analysis failed: {e}")
            return self._create_error_response(f"Voice analysis failed: {str(e)}")
    
    def generate_tts(self, text: str, filename: str, language: str = "en") -> bool:
        """
        Generate text-to-speech audio file.
        
        Args:
            text: Text to convert to speech
            filename: Output filename
            language: Language code (default: "en")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not text.strip():
                return False
            
            output_path = os.path.join(self.upload_folder, filename)
            
            # Generate TTS
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(output_path)
            
            logger.info(f"TTS generated successfully: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            return False
    
    async def _perform_transcription(self, audio_file_path: str) -> str:
        """Perform audio transcription using available methods"""
        # Method 1: Hugging Face Whisper (if available)
        if self.features.huggingface_available:
            try:
                from huggingface_utils import transcribe_audio as hf_transcribe_audio
                transcription = hf_transcribe_audio(audio_file_path)
                if transcription:
                    logger.info("Transcription completed using Hugging Face Whisper")
                    return transcription
            except Exception as e:
                logger.warning(f"Hugging Face transcription failed: {e}")
        
        # Method 2: OpenAI Whisper API (if API key available)
        # This would require OpenAI API integration
        
        # Method 3: Fallback - return placeholder
        logger.warning("No transcription method available, using fallback")
        return "[Transcription unavailable - please configure Whisper AI]"
    
    def _get_audio_duration(self, audio_file_path: str) -> float:
        """Get audio file duration in seconds"""
        try:
            y, sr = librosa.load(audio_file_path, sr=None)
            return len(y) / sr
        except Exception as e:
            logger.error(f"Failed to get audio duration: {e}")
            return 0.0
    
    def _analyze_energy(self, y: np.ndarray) -> Dict[str, float]:
        """Analyze audio energy levels"""
        try:
            # RMS energy
            rms = librosa.feature.rms(y=y)
            mean_energy = float(np.mean(rms))
            max_energy = float(np.max(rms))
            energy_variance = float(np.var(rms))
            
            # Classify energy level
            if mean_energy > 0.05:
                energy_level = "high"
            elif mean_energy > 0.02:
                energy_level = "medium"
            else:
                energy_level = "low"
            
            return {
                "mean_energy": round(mean_energy, 4),
                "max_energy": round(max_energy, 4),
                "energy_variance": round(energy_variance, 6),
                "energy_level": energy_level
            }
            
        except Exception as e:
            logger.error(f"Energy analysis failed: {e}")
            return {"mean_energy": 0.0, "energy_level": "unknown"}
    
    def _analyze_pitch(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Analyze pitch characteristics"""
        try:
            # Extract pitch using YIN algorithm
            pitches = librosa.yin(y, fmin=80, fmax=400)
            
            # Filter out invalid pitches (NaN or very low values)
            valid_pitches = pitches[~np.isnan(pitches)]
            valid_pitches = valid_pitches[valid_pitches > 50]
            
            if len(valid_pitches) == 0:
                return {"mean_pitch": 0.0, "pitch_variance": 0.0, "pitch_range": "unknown"}
            
            mean_pitch = float(np.mean(valid_pitches))
            pitch_variance = float(np.var(valid_pitches))
            min_pitch = float(np.min(valid_pitches))
            max_pitch = float(np.max(valid_pitches))
            
            # Classify pitch range
            if mean_pitch > 200:
                pitch_range = "high"
            elif mean_pitch > 120:
                pitch_range = "medium"
            else:
                pitch_range = "low"
            
            return {
                "mean_pitch": round(mean_pitch, 1),
                "pitch_variance": round(pitch_variance, 1),
                "min_pitch": round(min_pitch, 1),
                "max_pitch": round(max_pitch, 1),
                "pitch_range": pitch_range
            }
            
        except Exception as e:
            logger.error(f"Pitch analysis failed: {e}")
            return {"mean_pitch": 0.0, "pitch_range": "unknown"}
    
    def _analyze_tone(self, energy_analysis: Dict, pitch_analysis: Dict) -> Dict[str, str]:
        """Analyze overall tone based on energy and pitch"""
        try:
            energy_level = energy_analysis.get("energy_level", "unknown")
            pitch_range = pitch_analysis.get("pitch_range", "unknown")
            mean_energy = energy_analysis.get("mean_energy", 0)
            mean_pitch = pitch_analysis.get("mean_pitch", 0)
            
            # Determine tone based on energy and pitch combination
            if energy_level == "high" and pitch_range in ["medium", "high"]:
                tone = "Energetic / Confident"
                confidence = "high"
            elif energy_level == "low" and pitch_range == "low":
                tone = "Uncertain / Low Energy"
                confidence = "low"
            elif energy_level == "medium" and pitch_range == "medium":
                tone = "Calm / Neutral"
                confidence = "medium"
            elif energy_level == "high" and pitch_range == "low":
                tone = "Assertive / Serious"
                confidence = "medium-high"
            else:
                tone = "Varied / Dynamic"
                confidence = "medium"
            
            return {
                "tone_description": tone,
                "confidence_level": confidence,
                "energy_pitch_combination": f"{energy_level}_energy_{pitch_range}_pitch"
            }
            
        except Exception as e:
            logger.error(f"Tone analysis failed: {e}")
            return {"tone_description": "Unknown", "confidence_level": "unknown"}
    
    def _analyze_speech_rate(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze speech rate and rhythm"""
        try:
            # Estimate speech rate using onset detection
            onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
            onset_times = librosa.onset.onset_to_time(onset_frames, sr=sr)
            
            duration = len(y) / sr
            
            if len(onset_times) > 1:
                # Estimate words per minute based on onsets
                estimated_syllables = len(onset_times)
                estimated_words = estimated_syllables / 2  # Rough estimate
                words_per_minute = (estimated_words / duration) * 60
                
                # Classify speech rate
                if words_per_minute > 180:
                    rate_category = "fast"
                elif words_per_minute > 120:
                    rate_category = "normal"
                else:
                    rate_category = "slow"
            else:
                words_per_minute = 0
                rate_category = "unknown"
            
            return {
                "estimated_wpm": round(words_per_minute, 1),
                "rate_category": rate_category,
                "onset_count": len(onset_times),
                "duration": round(duration, 2)
            }
            
        except Exception as e:
            logger.error(f"Speech rate analysis failed: {e}")
            return {"estimated_wpm": 0, "rate_category": "unknown"}
    
    def _analyze_speech_patterns(self, transcription: str) -> Dict[str, Any]:
        """Analyze speech patterns from transcription"""
        try:
            if not transcription or transcription == "[Transcription unavailable - please configure Whisper AI]":
                return {"pattern_analysis": "unavailable"}
            
            words = transcription.lower().split()
            
            # Filler word detection
            filler_words = ["um", "uh", "like", "you know", "so", "well", "actually"]
            filler_count = sum(1 for word in words if word in filler_words)
            filler_percentage = (filler_count / len(words)) * 100 if words else 0
            
            # Sentence structure analysis
            sentences = [s.strip() for s in transcription.split('.') if s.strip()]
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
            
            # Vocabulary diversity (unique words / total words)
            unique_words = len(set(words))
            vocabulary_diversity = unique_words / len(words) if words else 0
            
            return {
                "filler_count": filler_count,
                "filler_percentage": round(filler_percentage, 1),
                "sentence_count": len(sentences),
                "avg_sentence_length": round(avg_sentence_length, 1),
                "vocabulary_diversity": round(vocabulary_diversity, 2),
                "total_words": len(words),
                "unique_words": unique_words
            }
            
        except Exception as e:
            logger.error(f"Speech pattern analysis failed: {e}")
            return {"pattern_analysis": "failed"}
    
    def _analyze_transcription_quality(self, transcription: str) -> Dict[str, Any]:
        """Analyze the quality of transcription"""
        try:
            # Basic quality metrics
            word_count = len(transcription.split())
            char_count = len(transcription)
            
            # Check for common transcription issues
            has_incomplete_words = "..." in transcription or "[" in transcription
            has_repeated_words = self._check_repeated_words(transcription)
            
            # Estimate confidence based on length and content
            if word_count > 10 and not has_incomplete_words:
                confidence = "high"
            elif word_count > 5:
                confidence = "medium"
            else:
                confidence = "low"
            
            return {
                "word_count": word_count,
                "character_count": char_count,
                "has_incomplete_words": has_incomplete_words,
                "has_repeated_words": has_repeated_words,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"Transcription quality analysis failed: {e}")
            return {"confidence": "unknown"}
    
    def _check_repeated_words(self, text: str) -> bool:
        """Check for repeated words that might indicate transcription errors"""
        words = text.lower().split()
        for i in range(len(words) - 1):
            if words[i] == words[i + 1] and len(words[i]) > 2:
                return True
        return False
    
    def _generate_overall_assessment(
        self, 
        energy_analysis: Dict, 
        pitch_analysis: Dict, 
        tone_analysis: Dict, 
        speech_patterns: Dict
    ) -> Dict[str, str]:
        """Generate overall voice assessment"""
        try:
            # Collect key metrics
            energy_level = energy_analysis.get("energy_level", "unknown")
            tone = tone_analysis.get("tone_description", "Unknown")
            confidence_level = tone_analysis.get("confidence_level", "unknown")
            filler_percentage = speech_patterns.get("filler_percentage", 0)
            
            # Generate assessment
            strengths = []
            improvements = []
            
            # Energy assessment
            if energy_level == "high":
                strengths.append("Good energy and enthusiasm")
            elif energy_level == "low":
                improvements.append("Increase energy and vocal presence")
            
            # Confidence assessment
            if confidence_level in ["high", "medium-high"]:
                strengths.append("Confident delivery")
            elif confidence_level == "low":
                improvements.append("Work on building confidence in delivery")
            
            # Filler words assessment
            if filler_percentage < 5:
                strengths.append("Minimal use of filler words")
            elif filler_percentage > 15:
                improvements.append("Reduce filler words (um, uh, like)")
            
            # Overall recommendation
            if len(strengths) >= 2:
                overall = "Strong vocal presentation"
            elif len(strengths) == 1:
                overall = "Good foundation with room for improvement"
            else:
                overall = "Focus on vocal confidence and clarity"
            
            return {
                "overall_rating": overall,
                "strengths": strengths,
                "improvements": improvements,
                "tone_summary": tone
            }
            
        except Exception as e:
            logger.error(f"Overall assessment generation failed: {e}")
            return {"overall_rating": "Assessment unavailable"}
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "success": False,
            "error": error_message,
            "transcription": "",
            "duration": 0.0,
            "word_count": 0
        }
    
    def validate_audio_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate audio file format and size.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if not os.path.exists(file_path):
                return False, "File does not exist"
            
            # Check file size (max 50MB)
            file_size = os.path.getsize(file_path)
            if file_size > 50 * 1024 * 1024:
                return False, "File too large (max 50MB)"
            
            # Try to load with librosa to validate format
            try:
                y, sr = librosa.load(file_path, duration=1.0)  # Load just 1 second for validation
                if len(y) == 0:
                    return False, "Empty audio file"
            except Exception:
                return False, "Invalid audio format"
            
            return True, "Valid audio file"
            
        except Exception as e:
            return False, f"Validation failed: {str(e)}"