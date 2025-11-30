"""
Real-Time Video Interview Analysis
Provides live feedback during recording using WebSocket
"""

import asyncio
import cv2
import numpy as np
from typing import Dict, Any, Optional
import json
from datetime import datetime

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except:
    MEDIAPIPE_AVAILABLE = False

try:
    from fer import FER
    FER_AVAILABLE = True
except:
    FER_AVAILABLE = False


class RealtimeAnalyzer:
    """Real-time video analysis for live feedback during interviews"""
    
    def __init__(self):
        self.emotion_detector = FER(mtcnn=False) if FER_AVAILABLE else None  # Faster without MTCNN
        
        if MEDIAPIPE_AVAILABLE:
            self.face_mesh = mp.solutions.face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        else:
            self.face_mesh = None
        
        # Tracking state
        self.frame_count = 0
        self.metrics_history = {
            "eye_contact": [],
            "emotions": [],
            "posture": [],
            "attention": []
        }
        
        # Alert thresholds
        self.ALERT_THRESHOLDS = {
            "eye_contact_low": 0.4,
            "looking_away_duration": 5.0,  # seconds
            "poor_posture_duration": 10.0,
            "negative_emotion_duration": 8.0
        }
    
    def analyze_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Analyze a single frame and return real-time metrics
        
        Args:
            frame: BGR image from webcam
            
        Returns:
            Dictionary with current metrics and alerts
        """
        self.frame_count += 1
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "frame_number": self.frame_count,
            "metrics": {},
            "alerts": [],
            "feedback": {}
        }
        
        try:
            # Quick emotion detection
            emotions = self._detect_emotion_fast(frame)
            result["metrics"]["emotion"] = emotions
            
            # Eye contact and gaze
            if self.face_mesh:
                gaze_data = self._analyze_gaze_fast(frame)
                result["metrics"]["gaze"] = gaze_data
                
                # Check for alerts
                if gaze_data.get("eye_contact", False):
                    self.metrics_history["eye_contact"].append(1)
                else:
                    self.metrics_history["eye_contact"].append(0)
                
                # Alert if poor eye contact
                if len(self.metrics_history["eye_contact"]) > 30:
                    recent_eye_contact = np.mean(self.metrics_history["eye_contact"][-30:])
                    if recent_eye_contact < self.ALERT_THRESHOLDS["eye_contact_low"]:
                        result["alerts"].append({
                            "type": "eye_contact",
                            "severity": "warning",
                            "message": "Look at the camera more often"
                        })
                
                # Posture check
                posture = self._check_posture_fast(frame)
                result["metrics"]["posture"] = posture
            
            # Generate live feedback
            result["feedback"] = self._generate_live_feedback(result["metrics"])
            
            # Trim history to last 100 frames
            for key in self.metrics_history:
                if len(self.metrics_history[key]) > 100:
                    self.metrics_history[key] = self.metrics_history[key][-100:]
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _detect_emotion_fast(self, frame: np.ndarray) -> Dict[str, Any]:
        """Fast emotion detection for real-time use"""
        if not self.emotion_detector:
            return {"dominant": "neutral", "confidence": 0.0}
        
        try:
            # Resize for speed
            small_frame = cv2.resize(frame, (320, 240))
            emotions = self.emotion_detector.detect_emotions(small_frame)
            
            if emotions and len(emotions) > 0:
                emotion_scores = emotions[0]["emotions"]
                dominant = max(emotion_scores.items(), key=lambda x: x[1])
                
                return {
                    "dominant": dominant[0],
                    "confidence": round(dominant[1], 2),
                    "all_scores": {k: round(v, 2) for k, v in emotion_scores.items()}
                }
        except:
            pass
        
        return {"dominant": "neutral", "confidence": 0.0}
    
    def _analyze_gaze_fast(self, frame: np.ndarray) -> Dict[str, Any]:
        """Fast gaze analysis for real-time feedback"""
        gaze_data = {
            "eye_contact": False,
            "direction": "unknown",
            "confidence": 0.0
        }
        
        if not self.face_mesh:
            return gaze_data
        
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                h, w = frame.shape[:2]
                
                # Simple gaze estimation using nose and eye positions
                nose = landmarks.landmark[1]
                left_eye = landmarks.landmark[33]
                right_eye = landmarks.landmark[263]
                
                # Calculate if looking at camera (centered face)
                nose_x = nose.x
                eye_center_x = (left_eye.x + right_eye.x) / 2
                
                # Check if face is centered
                is_centered = abs(nose_x - 0.5) < 0.15
                eyes_level = abs(left_eye.y - right_eye.y) < 0.05
                
                gaze_data["eye_contact"] = is_centered and eyes_level
                gaze_data["confidence"] = 0.8 if gaze_data["eye_contact"] else 0.3
                
                # Determine direction
                if nose_x < 0.4:
                    gaze_data["direction"] = "left"
                elif nose_x > 0.6:
                    gaze_data["direction"] = "right"
                else:
                    gaze_data["direction"] = "center"
        
        except:
            pass
        
        return gaze_data
    
    def _check_posture_fast(self, frame: np.ndarray) -> Dict[str, Any]:
        """Quick posture check"""
        posture_data = {
            "good_posture": True,
            "face_visible": True,
            "centered": True
        }
        
        try:
            # Use face detection as proxy for posture
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                frame_center_x = frame.shape[1] / 2
                face_center_x = x + w / 2
                
                # Check if face is centered
                posture_data["centered"] = abs(face_center_x - frame_center_x) < frame.shape[1] * 0.2
                posture_data["face_visible"] = True
            else:
                posture_data["face_visible"] = False
                posture_data["good_posture"] = False
        
        except:
            pass
        
        return posture_data
    
    def _generate_live_feedback(self, metrics: Dict) -> Dict[str, str]:
        """Generate actionable live feedback"""
        feedback = {
            "primary": "Keep going!",
            "tips": []
        }
        
        try:
            # Emotion feedback
            emotion = metrics.get("emotion", {})
            dominant_emotion = emotion.get("dominant", "neutral")
            
            if dominant_emotion in ["sad", "fear", "angry"]:
                feedback["tips"].append("Try to relax and smile")
            elif dominant_emotion == "happy":
                feedback["primary"] = "Great energy!"
            
            # Gaze feedback
            gaze = metrics.get("gaze", {})
            if not gaze.get("eye_contact", False):
                feedback["tips"].append("Look at the camera")
            
            # Posture feedback
            posture = metrics.get("posture", {})
            if not posture.get("face_visible", True):
                feedback["tips"].append("Ensure your face is visible")
            elif not posture.get("centered", True):
                feedback["tips"].append("Center yourself in frame")
            
            # Limit tips to top 2
            feedback["tips"] = feedback["tips"][:2]
        
        except:
            pass
        
        return feedback
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of the recording session"""
        summary = {
            "total_frames": self.frame_count,
            "duration_seconds": self.frame_count / 30,  # Assuming 30fps
            "average_metrics": {}
        }
        
        try:
            if self.metrics_history["eye_contact"]:
                summary["average_metrics"]["eye_contact_percentage"] = round(
                    np.mean(self.metrics_history["eye_contact"]) * 100, 2
                )
        except:
            pass
        
        return summary
    
    def reset(self):
        """Reset analyzer state for new session"""
        self.frame_count = 0
        self.metrics_history = {
            "eye_contact": [],
            "emotions": [],
            "posture": [],
            "attention": []
        }


# Singleton instance
_realtime_analyzer = None

def get_realtime_analyzer() -> RealtimeAnalyzer:
    """Get or create singleton realtime analyzer"""
    global _realtime_analyzer
    if _realtime_analyzer is None:
        _realtime_analyzer = RealtimeAnalyzer()
    return _realtime_analyzer
