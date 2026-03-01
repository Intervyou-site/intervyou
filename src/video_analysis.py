"""
Video Interview Analysis Module - Enhanced Virtual Bot System
Provides comprehensive analysis including:
- Emotion detection and micro-expressions
- Advanced eye tracking (gaze, blinks, attention)
- Voice analysis (pitch, pace, filler words)
- Body language and posture tracking
- Real-time feedback capabilities
- Sentiment analysis
"""

import os
import cv2
import numpy as np
import librosa
from textblob import TextBlob
from typing import Dict, List, Any, Optional, Tuple
import tempfile
import json
import re
from collections import Counter
from scipy import signal
from scipy.spatial import distance

# Try to import advanced analysis libraries
try:
    from fer import FER
    FER_AVAILABLE = True
except:
    FER_AVAILABLE = False
    print("⚠️  FER (Facial Emotion Recognition) not available - install with: pip install fer")

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except:
    DEEPFACE_AVAILABLE = False
    print("⚠️  DeepFace not available - install with: pip install deepface")

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️  MediaPipe not available - install with: pip install mediapipe")

# Speech recognition for transcription and filler word detection
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️  SpeechRecognition not available - install with: pip install SpeechRecognition")

# Filler words to detect
FILLER_WORDS = ['um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 'literally', 'kind of', 'sort of']


class VideoAnalyzer:
    """Comprehensive video interview analyzer with AI-powered insights and virtual bot tracking"""
    
    def __init__(self):
        self.emotion_detector = FER(mtcnn=True) if FER_AVAILABLE else None
        
        # Initialize MediaPipe components
        if MEDIAPIPE_AVAILABLE:
            self.mp_face_mesh = mp.solutions.face_mesh
            self.mp_pose = mp.solutions.pose
            self.face_mesh = mp.solutions.face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.pose = mp.solutions.pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        else:
            self.face_mesh = None
            self.pose = None
        
        # Eye tracking parameters
        self.EYE_AR_THRESH = 0.25  # Eye aspect ratio threshold for blink detection
        self.EYE_AR_CONSEC_FRAMES = 3  # Consecutive frames for blink
        
        # Speech recognizer
        self.recognizer = sr.Recognizer() if SPEECH_RECOGNITION_AVAILABLE else None
        
        # Validation thresholds
        self.MIN_VIDEO_DURATION = 10  # Minimum 10 seconds for meaningful analysis
        self.MIN_FACE_DETECTION_RATIO = 0.3  # At least 30% of frames should have face
        self.MIN_AUDIO_ENERGY = 0.01  # Minimum audio energy to consider speech present
        
    def analyze_video(self, video_path: str, transcription: str = "") -> Dict[str, Any]:
        """
        Comprehensive video analysis including:
        - Emotion detection and micro-expressions
        - Advanced eye tracking (gaze, blinks, attention)
        - Voice analysis (pitch, pace, filler words)
        - Body language and posture
        - Confidence metrics
        - Sentiment analysis
        - Real-time timeline data
        """
        results = {
            "emotions": {},
            "facial_analysis": {},
            "eye_tracking": {},
            "voice_analysis": {},
            "body_language": {},
            "micro_expressions": {},
            "attention_metrics": {},
            "confidence_score": 0.0,
            "professionalism_score": 0.0,
            "engagement_score": 0.0,
            "authenticity_score": 0.0,
            "recommendations": [],
            "timeline": [],
            "validation": {}
        }
        
        try:
            # STEP 1: Validate video quality and duration
            validation = self._validate_video_quality(video_path)
            results["validation"] = validation
            
            # If video is too short or has no content, return low scores with explanation
            if not validation["is_valid"]:
                results["confidence_score"] = validation["suggested_score"]
                results["professionalism_score"] = validation["suggested_score"]
                results["engagement_score"] = validation["suggested_score"]
                results["recommendations"] = validation["recommendations"]
                return results
            # Extract audio for voice analysis
            audio_path = self._extract_audio(video_path)
            
            # Analyze emotions from video frames
            emotions = self._analyze_emotions(video_path)
            results["emotions"] = emotions
            
            # Advanced eye tracking analysis
            eye_tracking = self._analyze_eye_tracking(video_path)
            results["eye_tracking"] = eye_tracking
            
            # Analyze facial features and expressions
            facial = self._analyze_facial_features(video_path)
            results["facial_analysis"] = facial
            
            # Detect micro-expressions
            micro = self._analyze_micro_expressions(video_path)
            results["micro_expressions"] = micro
            
            # Analyze body language and posture
            body = self._analyze_body_language(video_path)
            results["body_language"] = body
            
            # Analyze attention and focus
            attention = self._analyze_attention(video_path)
            results["attention_metrics"] = attention
            
            # Voice analysis (pitch, pace, filler words)
            if audio_path:
                voice = self._analyze_voice(audio_path, transcription)
                results["voice_analysis"] = voice
                
                # Get transcription if not provided
                if not transcription and voice.get("transcription"):
                    transcription = voice["transcription"]
            
            # Calculate overall scores
            results["confidence_score"] = self._calculate_confidence_score(emotions, facial, body, voice_analysis=results.get("voice_analysis"))
            results["professionalism_score"] = self._calculate_professionalism_score(facial, body, eye_tracking)
            results["engagement_score"] = self._calculate_engagement_score(emotions, facial, body, attention)
            results["authenticity_score"] = self._calculate_authenticity_score(micro, emotions, voice_analysis=results.get("voice_analysis"))
            
            # Analyze sentiment from transcription
            if transcription:
                sentiment = self._analyze_sentiment(transcription)
                results["sentiment"] = sentiment
            
            # Generate timeline data for visualization
            results["timeline"] = self._generate_timeline(video_path, emotions, eye_tracking, attention)
            
            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results)
            
            # Cleanup temp audio file
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except:
                    pass
            
        except Exception as e:
            print(f"Video analysis error: {e}")
            results["error"] = str(e)
        
        return results

    def _validate_video_quality(self, video_path: str) -> Dict[str, Any]:
        """
        Validate video quality before analysis
        Checks:
        - Video duration (minimum 10 seconds)
        - Face detection ratio (at least 30% of frames)
        - Audio presence and energy
        - Overall content quality
        """
        validation = {
            "is_valid": True,
            "duration": 0.0,
            "face_detection_ratio": 0.0,
            "has_audio": False,
            "audio_energy": 0.0,
            "issues": [],
            "recommendations": [],
            "suggested_score": 0.0
        }
        
        try:
            # Check video duration
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps
            validation["duration"] = round(duration, 2)
            
            # Check face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces_detected = 0
            frames_checked = 0
            sample_rate = max(1, int(fps))  # Check every second
            
            for i in range(0, frame_count, sample_rate):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if not ret:
                    break
                
                frames_checked += 1
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) > 0:
                    faces_detected += 1
            
            cap.release()
            
            if frames_checked > 0:
                validation["face_detection_ratio"] = round(faces_detected / frames_checked, 2)
            
            # Check audio presence
            try:
                import librosa
                y, sr = librosa.load(video_path, sr=None, duration=min(duration, 30))
                rms = librosa.feature.rms(y=y)[0]
                validation["audio_energy"] = round(float(np.mean(rms)), 4)
                validation["has_audio"] = validation["audio_energy"] > self.MIN_AUDIO_ENERGY
            except:
                validation["has_audio"] = False
                validation["audio_energy"] = 0.0
            
            # Validation checks
            if duration < self.MIN_VIDEO_DURATION:
                validation["is_valid"] = False
                validation["issues"].append(f"Video too short: {duration:.1f}s (minimum {self.MIN_VIDEO_DURATION}s required)")
                validation["recommendations"].append(f"🎥 Record a longer video - at least {self.MIN_VIDEO_DURATION} seconds needed for meaningful analysis")
                validation["recommendations"].append("💡 A good interview answer typically takes 30-90 seconds")
                validation["suggested_score"] = min(3.0, duration / self.MIN_VIDEO_DURATION * 3.0)
            
            if validation["face_detection_ratio"] < self.MIN_FACE_DETECTION_RATIO:
                validation["is_valid"] = False
                validation["issues"].append(f"Face not detected in most frames: {validation['face_detection_ratio']*100:.0f}%")
                validation["recommendations"].append("📹 Ensure your face is clearly visible in the camera frame")
                validation["recommendations"].append("💡 Position yourself in good lighting facing the camera")
                validation["suggested_score"] = max(validation["suggested_score"], 2.0)
            
            if not validation["has_audio"] or validation["audio_energy"] < self.MIN_AUDIO_ENERGY:
                validation["is_valid"] = False
                validation["issues"].append("No speech detected or audio too quiet")
                validation["recommendations"].append("🎤 Speak clearly and ensure your microphone is working")
                validation["recommendations"].append("💡 Check audio settings and speak at normal volume")
                validation["suggested_score"] = max(validation["suggested_score"], 2.0)
            
            # If multiple issues, lower the score
            if len(validation["issues"]) >= 2:
                validation["suggested_score"] = min(validation["suggested_score"], 2.5)
            
            # Add general recommendation if invalid
            if not validation["is_valid"]:
                validation["recommendations"].append("🔄 Please record again with proper setup for accurate analysis")
            
        except Exception as e:
            print(f"Validation error: {e}")
            validation["is_valid"] = False
            validation["issues"].append(f"Error validating video: {str(e)}")
            validation["suggested_score"] = 0.0
        
        return validation
    
    def _analyze_emotions(self, video_path: str) -> Dict[str, Any]:
        """Analyze emotions from video frames using FER"""
        emotions_timeline = []
        emotion_summary = {}
        
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            sample_rate = 30  # Analyze every 30th frame for performance
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % sample_rate == 0:
                    if self.emotion_detector:
                        result = self.emotion_detector.detect_emotions(frame)
                        if result:
                            emotions_timeline.append({
                                "frame": frame_count,
                                "timestamp": frame_count / 30.0,  # Assuming 30fps
                                "emotions": result[0]["emotions"]
                            })
                
                frame_count += 1
            
            cap.release()
            
            # Calculate emotion summary
            if emotions_timeline:
                emotion_keys = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
                for key in emotion_keys:
                    values = [e["emotions"].get(key, 0) for e in emotions_timeline]
                    emotion_summary[key] = {
                        "average": float(np.mean(values)),
                        "max": float(np.max(values)),
                        "min": float(np.min(values))
                    }
            
            return {
                "timeline": emotions_timeline[-10:],  # Last 10 samples
                "summary": emotion_summary,
                "dominant_emotion": max(emotion_summary.items(), key=lambda x: x[1]["average"])[0] if emotion_summary else "neutral"
            }
        
        except Exception as e:
            print(f"Emotion analysis error: {e}")
            return {"error": str(e), "dominant_emotion": "neutral"}
    
    def _extract_audio(self, video_path: str) -> Optional[str]:
        """Extract audio from video file for voice analysis"""
        try:
            import moviepy.editor as mp
            video = mp.VideoFileClip(video_path)
            if video.audio is None:
                return None
            
            audio_path = tempfile.mktemp(suffix=".wav")
            video.audio.write_audiofile(audio_path, logger=None)
            video.close()
            return audio_path
        except Exception as e:
            print(f"Audio extraction error: {e}")
            return None
    
    def _analyze_eye_tracking(self, video_path: str) -> Dict[str, Any]:
        """
        Advanced eye tracking analysis:
        - Gaze direction and stability
        - Blink rate and patterns
        - Eye contact percentage
        - Attention indicators
        """
        eye_data = {
            "gaze_direction": {"center": 0, "left": 0, "right": 0, "up": 0, "down": 0},
            "blink_rate": 0.0,
            "total_blinks": 0,
            "eye_contact_percentage": 0.0,
            "gaze_stability": 0.0,
            "attention_score": 0.0,
            "timeline": []
        }
        
        if not MEDIAPIPE_AVAILABLE or not self.face_mesh:
            return eye_data
        
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frame_count = 0
            blink_counter = 0
            ear_history = []
            gaze_positions = []
            eye_contact_frames = 0
            total_analyzed = 0
            
            # Eye landmark indices for MediaPipe Face Mesh
            LEFT_EYE = [362, 385, 387, 263, 373, 380]
            RIGHT_EYE = [33, 160, 158, 133, 153, 144]
            LEFT_IRIS = [474, 475, 476, 477]
            RIGHT_IRIS = [469, 470, 471, 472]
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                if frame_count % 5 != 0:  # Sample every 5th frame
                    continue
                
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_mesh.process(rgb_frame)
                
                if results.multi_face_landmarks:
                    total_analyzed += 1
                    landmarks = results.multi_face_landmarks[0]
                    h, w = frame.shape[:2]
                    
                    # Calculate Eye Aspect Ratio (EAR) for blink detection
                    left_ear = self._calculate_ear(landmarks, LEFT_EYE, w, h)
                    right_ear = self._calculate_ear(landmarks, RIGHT_EYE, w, h)
                    ear = (left_ear + right_ear) / 2.0
                    ear_history.append(ear)
                    
                    # Detect blink
                    if ear < self.EYE_AR_THRESH:
                        blink_counter += 1
                    
                    # Analyze gaze direction using iris position
                    gaze = self._calculate_gaze_direction(landmarks, LEFT_IRIS, RIGHT_IRIS, w, h)
                    gaze_positions.append(gaze)
                    
                    # Update gaze direction counts
                    if gaze["direction"] in eye_data["gaze_direction"]:
                        eye_data["gaze_direction"][gaze["direction"]] += 1
                    
                    # Check if looking at camera (center gaze)
                    if gaze["direction"] == "center":
                        eye_contact_frames += 1
                    
                    # Store timeline data
                    if frame_count % 30 == 0:  # Every second
                        eye_data["timeline"].append({
                            "timestamp": frame_count / fps,
                            "gaze": gaze["direction"],
                            "eye_contact": gaze["direction"] == "center",
                            "blink_detected": ear < self.EYE_AR_THRESH
                        })
            
            cap.release()
            
            # Calculate metrics
            if total_analyzed > 0:
                duration = frame_count / fps
                eye_data["blink_rate"] = (blink_counter / duration) * 60  # Blinks per minute
                eye_data["total_blinks"] = blink_counter
                eye_data["eye_contact_percentage"] = round((eye_contact_frames / total_analyzed) * 100, 2)
                
                # Calculate gaze stability (lower variance = more stable)
                if gaze_positions:
                    gaze_variance = np.var([g["x"] for g in gaze_positions] + [g["y"] for g in gaze_positions])
                    eye_data["gaze_stability"] = round(max(0, 1 - (gaze_variance / 0.1)), 2)
                
                # Attention score based on eye contact and stability
                eye_data["attention_score"] = round(
                    (eye_data["eye_contact_percentage"] / 100 * 0.7) + 
                    (eye_data["gaze_stability"] * 0.3), 2
                )
                
                # Normalize gaze direction percentages
                total_gaze = sum(eye_data["gaze_direction"].values())
                if total_gaze > 0:
                    for direction in eye_data["gaze_direction"]:
                        eye_data["gaze_direction"][direction] = round(
                            (eye_data["gaze_direction"][direction] / total_gaze) * 100, 2
                        )
        
        except Exception as e:
            print(f"Eye tracking error: {e}")
            eye_data["error"] = str(e)
        
        return eye_data
    
    def _calculate_ear(self, landmarks, eye_indices, w, h) -> float:
        """Calculate Eye Aspect Ratio for blink detection"""
        try:
            points = []
            for idx in eye_indices:
                landmark = landmarks.landmark[idx]
                points.append([landmark.x * w, landmark.y * h])
            
            points = np.array(points)
            
            # Compute vertical distances
            A = distance.euclidean(points[1], points[5])
            B = distance.euclidean(points[2], points[4])
            
            # Compute horizontal distance
            C = distance.euclidean(points[0], points[3])
            
            # Eye aspect ratio
            ear = (A + B) / (2.0 * C)
            return ear
        except:
            return 0.3  # Default value
    
    def _calculate_gaze_direction(self, landmarks, left_iris, right_iris, w, h) -> Dict[str, Any]:
        """Calculate gaze direction from iris position"""
        try:
            # Get iris center
            left_iris_points = [(landmarks.landmark[i].x * w, landmarks.landmark[i].y * h) for i in left_iris]
            right_iris_points = [(landmarks.landmark[i].x * w, landmarks.landmark[i].y * h) for i in right_iris]
            
            left_center = np.mean(left_iris_points, axis=0)
            right_center = np.mean(right_iris_points, axis=0)
            
            # Get eye corners for reference
            left_eye_left = landmarks.landmark[33]
            left_eye_right = landmarks.landmark[133]
            
            # Calculate relative position
            eye_width = abs(left_eye_right.x - left_eye_left.x) * w
            iris_x = (left_center[0] + right_center[0]) / 2
            eye_center_x = ((left_eye_left.x + left_eye_right.x) / 2) * w
            
            # Determine direction
            x_offset = (iris_x - eye_center_x) / eye_width
            y_offset = (left_center[1] - h/2) / h
            
            direction = "center"
            if abs(x_offset) > 0.15:
                direction = "right" if x_offset > 0 else "left"
            elif abs(y_offset) > 0.1:
                direction = "up" if y_offset < 0 else "down"
            
            return {
                "direction": direction,
                "x": round(x_offset, 3),
                "y": round(y_offset, 3)
            }
        except:
            return {"direction": "center", "x": 0, "y": 0}
    
    def _analyze_micro_expressions(self, video_path: str) -> Dict[str, Any]:
        """
        Detect micro-expressions (brief, involuntary facial expressions)
        These can indicate genuine emotions vs. controlled expressions
        """
        micro_data = {
            "detected_count": 0,
            "types": {},
            "authenticity_indicators": [],
            "timeline": []
        }
        
        if not DEEPFACE_AVAILABLE:
            return micro_data
        
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frame_count = 0
            prev_emotion = None
            emotion_changes = []
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                if frame_count % 10 != 0:  # Sample every 10th frame
                    continue
                
                try:
                    # Analyze with DeepFace
                    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, silent=True)
                    
                    if isinstance(result, list):
                        result = result[0]
                    
                    current_emotion = result.get('dominant_emotion')
                    
                    # Detect rapid emotion changes (micro-expressions)
                    if prev_emotion and current_emotion != prev_emotion:
                        emotion_changes.append({
                            "timestamp": frame_count / fps,
                            "from": prev_emotion,
                            "to": current_emotion
                        })
                        
                        # Count as micro-expression if change is rapid
                        if len(emotion_changes) > 1:
                            time_diff = emotion_changes[-1]["timestamp"] - emotion_changes[-2]["timestamp"]
                            if time_diff < 0.5:  # Less than 0.5 seconds
                                micro_data["detected_count"] += 1
                                micro_type = f"{prev_emotion}_to_{current_emotion}"
                                micro_data["types"][micro_type] = micro_data["types"].get(micro_type, 0) + 1
                    
                    prev_emotion = current_emotion
                
                except:
                    pass
            
            cap.release()
            
            # Analyze authenticity
            if micro_data["detected_count"] > 0:
                micro_data["authenticity_indicators"].append("Natural micro-expressions detected - indicates genuine emotions")
            
            if micro_data["detected_count"] > 20:
                micro_data["authenticity_indicators"].append("High micro-expression rate - may indicate nervousness or stress")
            elif micro_data["detected_count"] < 5:
                micro_data["authenticity_indicators"].append("Low micro-expression rate - expressions may be controlled")
        
        except Exception as e:
            print(f"Micro-expression analysis error: {e}")
            micro_data["error"] = str(e)
        
        return micro_data
    
    def _analyze_attention(self, video_path: str) -> Dict[str, Any]:
        """
        Analyze attention and focus indicators:
        - Looking away from camera
        - Head pose changes
        - Distraction indicators
        """
        attention_data = {
            "focus_percentage": 0.0,
            "distraction_count": 0,
            "head_pose_stability": 0.0,
            "looking_away_duration": 0.0,
            "attention_timeline": []
        }
        
        if not MEDIAPIPE_AVAILABLE or not self.face_mesh:
            return attention_data
        
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frame_count = 0
            focused_frames = 0
            total_frames = 0
            looking_away_frames = 0
            head_poses = []
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                if frame_count % 10 != 0:
                    continue
                
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.face_mesh.process(rgb_frame)
                
                if results.multi_face_landmarks:
                    total_frames += 1
                    landmarks = results.multi_face_landmarks[0]
                    
                    # Calculate head pose
                    head_pose = self._calculate_head_pose(landmarks, frame.shape)
                    head_poses.append(head_pose)
                    
                    # Check if focused (head facing forward)
                    is_focused = abs(head_pose["yaw"]) < 20 and abs(head_pose["pitch"]) < 15
                    
                    if is_focused:
                        focused_frames += 1
                    else:
                        looking_away_frames += 1
                    
                    # Record timeline
                    if frame_count % 30 == 0:
                        attention_data["attention_timeline"].append({
                            "timestamp": frame_count / fps,
                            "focused": is_focused,
                            "head_yaw": head_pose["yaw"],
                            "head_pitch": head_pose["pitch"]
                        })
                else:
                    # No face detected = distraction
                    attention_data["distraction_count"] += 1
                    looking_away_frames += 1
            
            cap.release()
            
            # Calculate metrics
            if total_frames > 0:
                attention_data["focus_percentage"] = round((focused_frames / total_frames) * 100, 2)
                attention_data["looking_away_duration"] = round((looking_away_frames / fps), 2)
                
                # Calculate head pose stability
                if head_poses:
                    yaw_variance = np.var([p["yaw"] for p in head_poses])
                    pitch_variance = np.var([p["pitch"] for p in head_poses])
                    stability = max(0, 1 - ((yaw_variance + pitch_variance) / 1000))
                    attention_data["head_pose_stability"] = round(stability, 2)
        
        except Exception as e:
            print(f"Attention analysis error: {e}")
            attention_data["error"] = str(e)
        
        return attention_data
    
    def _calculate_head_pose(self, landmarks, frame_shape) -> Dict[str, float]:
        """Calculate head pose angles (yaw, pitch, roll)"""
        try:
            h, w = frame_shape[:2]
            
            # Key facial landmarks for pose estimation
            nose_tip = landmarks.landmark[1]
            chin = landmarks.landmark[152]
            left_eye = landmarks.landmark[33]
            right_eye = landmarks.landmark[263]
            left_mouth = landmarks.landmark[61]
            right_mouth = landmarks.landmark[291]
            
            # Convert to pixel coordinates
            points_2d = np.array([
                [nose_tip.x * w, nose_tip.y * h],
                [chin.x * w, chin.y * h],
                [left_eye.x * w, left_eye.y * h],
                [right_eye.x * w, right_eye.y * h],
                [left_mouth.x * w, left_mouth.y * h],
                [right_mouth.x * w, right_mouth.y * h]
            ], dtype=np.float64)
            
            # 3D model points
            model_points = np.array([
                [0.0, 0.0, 0.0],           # Nose tip
                [0.0, -330.0, -65.0],      # Chin
                [-225.0, 170.0, -135.0],   # Left eye
                [225.0, 170.0, -135.0],    # Right eye
                [-150.0, -150.0, -125.0],  # Left mouth
                [150.0, -150.0, -125.0]    # Right mouth
            ])
            
            # Camera matrix
            focal_length = w
            center = (w / 2, h / 2)
            camera_matrix = np.array([
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ], dtype=np.float64)
            
            dist_coeffs = np.zeros((4, 1))
            
            # Solve PnP
            success, rotation_vector, translation_vector = cv2.solvePnP(
                model_points, points_2d, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
            )
            
            # Convert rotation vector to angles
            rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rotation_matrix)
            
            yaw = angles[1]
            pitch = angles[0]
            roll = angles[2]
            
            return {"yaw": round(yaw, 2), "pitch": round(pitch, 2), "roll": round(roll, 2)}
        
        except:
            return {"yaw": 0.0, "pitch": 0.0, "roll": 0.0}
    
    def _analyze_voice(self, audio_path: str, transcription: str = "") -> Dict[str, Any]:
        """
        Comprehensive voice analysis:
        - Pitch variation and range
        - Speech rate (words per minute)
        - Pause patterns
        - Volume consistency
        - Filler word detection
        - Clarity and articulation
        """
        voice_data = {
            "pitch": {"mean": 0, "std": 0, "range": 0},
            "speech_rate": 0,  # words per minute
            "pause_count": 0,
            "average_pause_duration": 0,
            "volume": {"mean": 0, "std": 0},
            "filler_words": {},
            "total_filler_count": 0,
            "clarity_score": 0.0,
            "energy_level": "moderate",
            "transcription": transcription
        }
        
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Pitch analysis
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_values = []
            
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if pitch_values:
                voice_data["pitch"]["mean"] = round(float(np.mean(pitch_values)), 2)
                voice_data["pitch"]["std"] = round(float(np.std(pitch_values)), 2)
                voice_data["pitch"]["range"] = round(float(np.max(pitch_values) - np.min(pitch_values)), 2)
            
            # Volume/Energy analysis
            rms = librosa.feature.rms(y=y)[0]
            voice_data["volume"]["mean"] = round(float(np.mean(rms)), 4)
            voice_data["volume"]["std"] = round(float(np.std(rms)), 4)
            
            # Energy level classification
            mean_energy = np.mean(rms)
            if mean_energy < 0.02:
                voice_data["energy_level"] = "low"
            elif mean_energy > 0.05:
                voice_data["energy_level"] = "high"
            else:
                voice_data["energy_level"] = "moderate"
            
            # Pause detection (silence detection)
            intervals = librosa.effects.split(y, top_db=30)
            pauses = []
            
            for i in range(len(intervals) - 1):
                pause_start = intervals[i][1] / sr
                pause_end = intervals[i + 1][0] / sr
                pause_duration = pause_end - pause_start
                if pause_duration > 0.3:  # Pauses longer than 0.3s
                    pauses.append(pause_duration)
            
            voice_data["pause_count"] = len(pauses)
            if pauses:
                voice_data["average_pause_duration"] = round(float(np.mean(pauses)), 2)
            
            # Transcription and filler word detection
            if not transcription and SPEECH_RECOGNITION_AVAILABLE and self.recognizer:
                try:
                    with sr.AudioFile(audio_path) as source:
                        audio = self.recognizer.record(source)
                        transcription = self.recognizer.recognize_google(audio)
                        voice_data["transcription"] = transcription
                except:
                    pass
            
            # Analyze filler words
            if transcription:
                transcription_lower = transcription.lower()
                words = transcription_lower.split()
                word_count = len(words)
                
                for filler in FILLER_WORDS:
                    count = transcription_lower.count(filler)
                    if count > 0:
                        voice_data["filler_words"][filler] = count
                        voice_data["total_filler_count"] += count
                
                # Calculate speech rate
                if duration > 0:
                    voice_data["speech_rate"] = round((word_count / duration) * 60, 2)
                
                # Clarity score (inverse of filler word ratio)
                if word_count > 0:
                    filler_ratio = voice_data["total_filler_count"] / word_count
                    voice_data["clarity_score"] = round(max(0, 1 - (filler_ratio * 2)), 2)
                else:
                    voice_data["clarity_score"] = 0.8
            
        except Exception as e:
            print(f"Voice analysis error: {e}")
            voice_data["error"] = str(e)
        
        return voice_data
    
    def _generate_timeline(self, video_path: str, emotions: Dict, eye_tracking: Dict, attention: Dict) -> List[Dict]:
        """Generate timeline data for visualization"""
        timeline = []
        
        try:
            # Combine data from different analyses
            emotion_timeline = emotions.get("timeline", [])
            eye_timeline = eye_tracking.get("timeline", [])
            attention_timeline = attention.get("attention_timeline", [])
            
            # Merge timelines
            all_timestamps = set()
            for item in emotion_timeline:
                all_timestamps.add(item.get("timestamp", 0))
            for item in eye_timeline:
                all_timestamps.add(item.get("timestamp", 0))
            for item in attention_timeline:
                all_timestamps.add(item.get("timestamp", 0))
            
            for ts in sorted(all_timestamps):
                timeline_entry = {"timestamp": ts}
                
                # Find matching data points
                for item in emotion_timeline:
                    if abs(item.get("timestamp", 0) - ts) < 0.5:
                        timeline_entry["emotions"] = item.get("emotions", {})
                
                for item in eye_timeline:
                    if abs(item.get("timestamp", 0) - ts) < 0.5:
                        timeline_entry["gaze"] = item.get("gaze")
                        timeline_entry["eye_contact"] = item.get("eye_contact")
                
                for item in attention_timeline:
                    if abs(item.get("timestamp", 0) - ts) < 0.5:
                        timeline_entry["focused"] = item.get("focused")
                
                timeline.append(timeline_entry)
        
        except Exception as e:
            print(f"Timeline generation error: {e}")
        
        return timeline[:50]  # Limit to 50 data points
    
    def _calculate_authenticity_score(self, micro: Dict, emotions: Dict, voice_analysis: Dict = None) -> float:
        """Calculate authenticity score based on micro-expressions and consistency"""
        score = 5.0
        
        try:
            # Micro-expressions indicate authenticity
            micro_count = micro.get("detected_count", 0)
            if 5 <= micro_count <= 20:
                score += 2  # Optimal range
            elif micro_count > 20:
                score += 1  # High but acceptable
            elif micro_count < 5:
                score -= 1  # Too controlled
            
            # Voice consistency
            if voice_analysis:
                pitch_std = voice_analysis.get("pitch", {}).get("std", 0)
                if 20 < pitch_std < 80:  # Natural variation
                    score += 1.5
                
                clarity = voice_analysis.get("clarity_score", 0)
                score += clarity * 1.5
            
            return round(max(0.0, min(10.0, score)), 2)
        except:
            return 5.0
    
    def _analyze_facial_features(self, video_path: str) -> Dict[str, Any]:
        """Analyze facial features including eye contact and expressions"""
        facial_data = {
            "eye_contact": 0.0,
            "smile_frequency": 0.0,
            "head_pose": [],
            "facial_symmetry": 0.0,
            "face_detected_ratio": 0.0
        }
        
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            sample_rate = 30
            eye_contact_frames = 0
            smile_frames = 0
            face_detected_frames = 0
            total_analyzed = 0
            
            # Load face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % sample_rate == 0:
                    total_analyzed += 1
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    
                    if len(faces) > 0:
                        face_detected_frames += 1
                        x, y, w, h = faces[0]
                        
                        # Estimate eye contact (face centered in frame)
                        frame_center_x = frame.shape[1] / 2
                        face_center_x = x + w / 2
                        if abs(face_center_x - frame_center_x) < frame.shape[1] * 0.2:
                            eye_contact_frames += 1
                        
                        # Detect smile
                        roi_gray = gray[y:y+h, x:x+w]
                        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
                        if len(smiles) > 0:
                            smile_frames += 1
                
                frame_count += 1
            
            cap.release()
            
            if total_analyzed > 0:
                facial_data["eye_contact"] = eye_contact_frames / total_analyzed
                facial_data["smile_frequency"] = smile_frames / total_analyzed
                facial_data["face_detected_ratio"] = face_detected_frames / total_analyzed
            
        except Exception as e:
            print(f"Facial analysis error: {e}")
            facial_data["error"] = str(e)
        
        return facial_data

    def _analyze_body_language(self, video_path: str) -> Dict[str, Any]:
        """Analyze body language and posture"""
        body_data = {
            "posture_score": 0.0,
            "movement_level": "moderate",
            "gestures_detected": 0,
            "stability": 0.0
        }
        
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            duration = frame_count / fps
            
            # Analyze frame differences for movement detection
            prev_frame = None
            movement_scores = []
            sample_rate = 30
            current_frame = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if current_frame % sample_rate == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    if prev_frame is not None:
                        diff = cv2.absdiff(prev_frame, gray)
                        movement = np.mean(diff)
                        movement_scores.append(movement)
                    prev_frame = gray
                
                current_frame += 1
            
            cap.release()
            
            # Calculate movement metrics
            if movement_scores:
                avg_movement = np.mean(movement_scores)
                movement_std = np.std(movement_scores)
                
                # Classify movement level
                if avg_movement < 5:
                    body_data["movement_level"] = "minimal"
                    body_data["posture_score"] = 0.9
                elif avg_movement < 15:
                    body_data["movement_level"] = "moderate"
                    body_data["posture_score"] = 0.85
                else:
                    body_data["movement_level"] = "active"
                    body_data["posture_score"] = 0.7
                
                body_data["stability"] = 1.0 - min(movement_std / 20, 1.0)
                body_data["gestures_detected"] = max(0, int(duration / 10))  # Estimate
            
        except Exception as e:
            print(f"Body language analysis error: {e}")
            body_data["error"] = str(e)
            body_data["posture_score"] = 0.75  # Default
        
        return body_data
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment from transcription using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            if polarity > 0.1:
                sentiment_label = "positive"
            elif polarity < -0.1:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            return {
                "polarity": round(polarity, 3),
                "subjectivity": round(subjectivity, 3),
                "label": sentiment_label,
                "confidence": round(abs(polarity), 3)
            }
        except Exception as e:
            return {"error": str(e), "label": "neutral"}
    
    def _calculate_confidence_score(self, emotions: Dict, facial: Dict, body: Dict, voice_analysis: Dict = None) -> float:
        """Calculate overall confidence score (0-10) with enhanced metrics"""
        score = 0.0  # Start from 0, build up based on actual data
        max_possible = 0.0  # Track maximum possible score
        
        try:
            # Emotion factors (max 3.5 points)
            if emotions.get("summary"):
                max_possible += 3.5
                happy = emotions["summary"].get("happy", {}).get("average", 0)
                neutral = emotions["summary"].get("neutral", {}).get("average", 0)
                fear = emotions["summary"].get("fear", {}).get("average", 0)
                sad = emotions["summary"].get("sad", {}).get("average", 0)
                
                emotion_score = (happy * 2 + neutral * 1) * 3.5
                emotion_score -= (fear * 2 + sad * 1.5) * 3.5
                score += max(0, emotion_score)
            
            # Facial factors (max 2.5 points)
            if facial.get("eye_contact") is not None:
                max_possible += 2.5
                score += facial["eye_contact"] * 2.5
            
            # Body language factors (max 2 points)
            if body.get("posture_score") is not None:
                max_possible += 1.5
                score += body["posture_score"] * 1.5
            
            if body.get("stability") is not None:
                max_possible += 0.5
                score += body["stability"] * 0.5
            
            # Voice factors (max 2 points)
            if voice_analysis and voice_analysis.get("clarity_score") is not None:
                max_possible += 1.5
                clarity = voice_analysis.get("clarity_score", 0)
                score += clarity * 1.5
                
                # Optimal speech rate (120-160 wpm)
                speech_rate = voice_analysis.get("speech_rate", 0)
                if speech_rate > 0:
                    max_possible += 0.5
                    if 120 <= speech_rate <= 160:
                        score += 0.5
                    elif 100 <= speech_rate <= 180:
                        score += 0.3
            
            # Normalize score to 0-10 scale based on available data
            if max_possible > 0:
                normalized_score = (score / max_possible) * 10
                return round(max(0.0, min(10.0, normalized_score)), 2)
            else:
                return 0.0
        except Exception as e:
            print(f"Confidence score calculation error: {e}")
            return 0.0
    
    def _calculate_professionalism_score(self, facial: Dict, body: Dict, eye_tracking: Dict = None) -> float:
        """Calculate professionalism score (0-10) with enhanced eye tracking"""
        score = 0.0
        max_possible = 0.0
        
        try:
            # Enhanced eye contact from eye tracking (max 4 points)
            if eye_tracking and eye_tracking.get("eye_contact_percentage") is not None:
                max_possible += 3.5
                eye_contact_pct = eye_tracking.get("eye_contact_percentage", 0)
                score += (eye_contact_pct / 100) * 3.5
                
                # Gaze stability (max 1.5 points)
                if eye_tracking.get("gaze_stability") is not None:
                    max_possible += 1.5
                    gaze_stability = eye_tracking.get("gaze_stability", 0)
                    score += gaze_stability * 1.5
            elif facial.get("eye_contact") is not None:
                # Fallback to basic eye contact
                max_possible += 3.5
                score += facial["eye_contact"] * 3.5
            
            # Face detection ratio (max 2 points)
            if facial.get("face_detected_ratio") is not None:
                max_possible += 2.0
                score += facial["face_detected_ratio"] * 2.0
            
            # Posture and stability (max 3 points)
            if body.get("posture_score") is not None:
                max_possible += 2.0
                score += body["posture_score"] * 2.0
            
            if body.get("stability") is not None:
                max_possible += 1.0
                score += body["stability"] * 1.0
            
            # Normalize to 0-10 scale
            if max_possible > 0:
                normalized_score = (score / max_possible) * 10
                return round(max(0.0, min(10.0, normalized_score)), 2)
            else:
                return 0.0
        except Exception as e:
            print(f"Professionalism score calculation error: {e}")
            return 0.0
    
    def _calculate_engagement_score(self, emotions: Dict, facial: Dict, body: Dict, attention: Dict = None) -> float:
        """Calculate engagement score (0-10) with attention metrics"""
        score = 0.0
        max_possible = 0.0
        
        try:
            # Positive emotions indicate engagement (max 3.5 points)
            if emotions.get("summary"):
                max_possible += 3.5
                happy = emotions["summary"].get("happy", {}).get("average", 0)
                surprise = emotions["summary"].get("surprise", {}).get("average", 0)
                score += (happy + surprise) * 3.5
            
            # Smiling shows engagement (max 2 points)
            if facial.get("smile_frequency") is not None:
                max_possible += 2.0
                score += facial["smile_frequency"] * 2.0
            
            # Attention and focus (max 2.5 points)
            if attention and attention.get("focus_percentage") is not None:
                max_possible += 2.0
                focus_pct = attention.get("focus_percentage", 0)
                score += (focus_pct / 100) * 2.0
                
                # Low distraction is good (max 0.5 points)
                max_possible += 0.5
                distraction_count = attention.get("distraction_count", 0)
                if distraction_count < 3:
                    score += 0.5
                elif distraction_count < 7:
                    score += 0.25
            
            # Movement and gestures (max 2 points)
            if body.get("movement_level"):
                max_possible += 1.0
                if body.get("movement_level") == "moderate":
                    score += 1.0
                elif body.get("movement_level") == "active":
                    score += 0.7
                elif body.get("movement_level") == "minimal":
                    score += 0.3
            
            if body.get("gestures_detected") is not None:
                max_possible += 1.0
                gesture_score = min(body["gestures_detected"] * 0.2, 1.0)
                score += gesture_score
            
            # Normalize to 0-10 scale
            if max_possible > 0:
                normalized_score = (score / max_possible) * 10
                return round(max(0.0, min(10.0, normalized_score)), 2)
            else:
                return 0.0
        except Exception as e:
            print(f"Engagement score calculation error: {e}")
            return 0.0

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate personalized recommendations based on comprehensive analysis"""
        recommendations = []
        
        try:
            # Eye tracking recommendations
            eye_tracking = results.get("eye_tracking", {})
            if eye_tracking.get("eye_contact_percentage", 0) < 60:
                recommendations.append("👁️ Improve eye contact - aim for 60-80% direct camera gaze")
            
            blink_rate = eye_tracking.get("blink_rate", 0)
            if blink_rate > 30:
                recommendations.append("� HMigh blink rate detected - try to relax and reduce nervousness")
            elif blink_rate < 10:
                recommendations.append("👀 Very low blink rate - remember to blink naturally to avoid appearing tense")
            
            gaze_stability = eye_tracking.get("gaze_stability", 0)
            if gaze_stability < 0.6:
                recommendations.append("🎯 Maintain steadier gaze - avoid darting eyes by focusing on the camera")
            
            # Voice analysis recommendations
            voice = results.get("voice_analysis", {})
            if voice:
                filler_count = voice.get("total_filler_count", 0)
                if filler_count > 10:
                    recommendations.append(f"🗣️ Reduce filler words (detected {filler_count}) - pause instead of using 'um', 'uh', 'like'")
                
                speech_rate = voice.get("speech_rate", 0)
                if speech_rate > 160:
                    recommendations.append("⏱️ Slow down your speech - aim for 120-160 words per minute")
                elif speech_rate < 100 and speech_rate > 0:
                    recommendations.append("⚡ Speak a bit faster - your pace is too slow, aim for 120-160 wpm")
                
                energy = voice.get("energy_level", "moderate")
                if energy == "low":
                    recommendations.append("🔊 Increase vocal energy and enthusiasm in your delivery")
                
                clarity = voice.get("clarity_score", 0)
                if clarity < 0.7:
                    recommendations.append("📢 Improve speech clarity - articulate words more clearly")
            
            # Attention and focus recommendations
            attention = results.get("attention_metrics", {})
            if attention.get("focus_percentage", 0) < 70:
                recommendations.append("🎯 Maintain better focus - you looked away frequently during the interview")
            
            if attention.get("distraction_count", 0) > 5:
                recommendations.append("📱 Minimize distractions - ensure a quiet, focused environment")
            
            # Micro-expression recommendations
            micro = results.get("micro_expressions", {})
            if micro.get("detected_count", 0) > 25:
                recommendations.append("😊 High micro-expression rate suggests nervousness - practice to feel more comfortable")
            
            # Confidence recommendations
            if results.get("confidence_score", 0) < 6:
                recommendations.append("💪 Build confidence through practice and positive self-talk")
            
            # Authenticity recommendations
            if results.get("authenticity_score", 0) < 6:
                recommendations.append("✨ Be more authentic - let your genuine personality show through")
            
            # Facial analysis
            facial = results.get("facial_analysis", {})
            if facial.get("smile_frequency", 0) < 0.2:
                recommendations.append("😊 Smile more naturally - it shows engagement and positivity")
            
            # Body language
            body = results.get("body_language", {})
            if body.get("movement_level") == "minimal":
                recommendations.append("🤲 Use natural hand gestures to emphasize key points")
            elif body.get("movement_level") == "active":
                recommendations.append("🧘 Reduce excessive movement - maintain a calm, steady presence")
            
            if body.get("posture_score", 0) < 0.7:
                recommendations.append("🪑 Improve posture - sit up straight and maintain good body alignment")
            
            # Engagement recommendations
            if results.get("engagement_score", 0) < 6:
                recommendations.append("🎯 Show more enthusiasm and engagement with your answers")
            
            # Professionalism
            if results.get("professionalism_score", 0) < 7:
                recommendations.append("👔 Enhance professionalism through better posture and eye contact")
            
            # Sentiment recommendations
            sentiment = results.get("sentiment", {})
            if sentiment.get("label") == "negative":
                recommendations.append("✨ Frame experiences more positively - focus on achievements and learning")
            
            # Positive feedback for excellent performance
            if (results.get("confidence_score", 0) >= 8 and 
                results.get("professionalism_score", 0) >= 8 and
                results.get("engagement_score", 0) >= 8):
                recommendations.insert(0, "🌟 Outstanding performance! You demonstrated excellent interview skills across all metrics")
            elif (results.get("confidence_score", 0) >= 7 and 
                  results.get("professionalism_score", 0) >= 7):
                recommendations.insert(0, "👏 Great job! You showed strong interview presence and communication skills")
            
        except Exception as e:
            print(f"Recommendation generation error: {e}")
            recommendations.append("Keep practicing to improve your interview skills")
        
        # Return top 8 most relevant recommendations
        return recommendations[:8]


def analyze_video_comprehensive(video_path: str, transcription: str = "") -> Dict[str, Any]:
    """
    Main function to perform comprehensive video analysis
    
    Args:
        video_path: Path to the video file
        transcription: Optional text transcription of the interview
    
    Returns:
        Dictionary containing all analysis results
    """
    analyzer = VideoAnalyzer()
    return analyzer.analyze_video(video_path, transcription)


def get_quick_feedback(video_path: str) -> str:
    """
    Get a quick text feedback summary
    
    Args:
        video_path: Path to the video file
    
    Returns:
        Human-readable feedback string
    """
    results = analyze_video_comprehensive(video_path)
    
    feedback_parts = []
    feedback_parts.append(f"📊 Confidence: {results.get('confidence_score', 0)}/10")
    feedback_parts.append(f"👔 Professionalism: {results.get('professionalism_score', 0)}/10")
    feedback_parts.append(f"🎯 Engagement: {results.get('engagement_score', 0)}/10")
    
    emotions = results.get("emotions", {})
    if emotions.get("dominant_emotion"):
        feedback_parts.append(f"\n😊 Dominant Emotion: {emotions['dominant_emotion'].title()}")
    
    recommendations = results.get("recommendations", [])
    if recommendations:
        feedback_parts.append("\n\n💡 Recommendations:")
        for rec in recommendations:
            feedback_parts.append(f"  • {rec}")
    
    return "\n".join(feedback_parts)
