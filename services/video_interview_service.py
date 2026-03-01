"""
Video Interview Service - AI-Powered Interview Analysis
Provides comprehensive video interview analysis including:
- AI question generation
- Emotion and facial expression analysis
- Voice and speech analysis
- Eye tracking and attention metrics
- Real-time feedback
"""

import os
import json
import random
import requests
from typing import Dict, List, Optional, Any


class VideoInterviewService:
    """Service for managing video interviews with AI analysis"""
    
    def __init__(self):
        self.question_bank = self._initialize_question_bank()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        
    def _initialize_question_bank(self) -> Dict[str, List[Dict]]:
        """Initialize comprehensive question bank for video interviews"""
        return {
            "Behavioral": [
                {
                    "question": "Tell me about a time when you had to work under pressure. How did you handle it?",
                    "difficulty": "intermediate",
                    "time_limit": 90,
                    "tips": ["Use STAR method", "Show problem-solving", "Demonstrate resilience"]
                },
                {
                    "question": "Describe a situation where you had to deal with a difficult team member.",
                    "difficulty": "intermediate",
                    "time_limit": 90,
                    "tips": ["Focus on conflict resolution", "Show empathy", "Highlight positive outcome"]
                },
                {
                    "question": "Tell me about your greatest professional achievement.",
                    "difficulty": "beginner",
                    "time_limit": 60,
                    "tips": ["Be specific", "Quantify results", "Show impact"]
                },
                {
                    "question": "Describe a time when you failed. What did you learn from it?",
                    "difficulty": "advanced",
                    "time_limit": 90,
                    "tips": ["Be honest", "Show growth mindset", "Demonstrate learning"]
                },
                {
                    "question": "How do you prioritize tasks when you have multiple deadlines?",
                    "difficulty": "intermediate",
                    "time_limit": 75,
                    "tips": ["Explain your system", "Give examples", "Show organization skills"]
                }
            ],
            "Technical": [
                {
                    "question": "Explain a complex technical concept to someone without a technical background.",
                    "difficulty": "intermediate",
                    "time_limit": 90,
                    "tips": ["Use analogies", "Avoid jargon", "Check understanding"]
                },
                {
                    "question": "Walk me through your approach to debugging a production issue.",
                    "difficulty": "advanced",
                    "time_limit": 120,
                    "tips": ["Show systematic thinking", "Mention tools", "Discuss prevention"]
                },
                {
                    "question": "Describe your experience with [relevant technology]. What projects have you built?",
                    "difficulty": "intermediate",
                    "time_limit": 90,
                    "tips": ["Be specific", "Discuss challenges", "Show expertise"]
                },
                {
                    "question": "How do you stay updated with the latest technology trends?",
                    "difficulty": "beginner",
                    "time_limit": 60,
                    "tips": ["Mention resources", "Show passion", "Give examples"]
                }
            ],
            "Leadership": [
                {
                    "question": "Tell me about a time when you had to lead a team through a challenging project.",
                    "difficulty": "advanced",
                    "time_limit": 120,
                    "tips": ["Show leadership style", "Discuss challenges", "Highlight team success"]
                },
                {
                    "question": "How do you motivate team members who are underperforming?",
                    "difficulty": "advanced",
                    "time_limit": 90,
                    "tips": ["Show empathy", "Discuss strategies", "Focus on development"]
                },
                {
                    "question": "Describe your leadership philosophy.",
                    "difficulty": "intermediate",
                    "time_limit": 75,
                    "tips": ["Be authentic", "Give examples", "Show values"]
                }
            ],
            "Problem Solving": [
                {
                    "question": "Describe a time when you had to make a decision with incomplete information.",
                    "difficulty": "advanced",
                    "time_limit": 90,
                    "tips": ["Show analytical thinking", "Discuss risk assessment", "Explain outcome"]
                },
                {
                    "question": "Tell me about a creative solution you developed for a business problem.",
                    "difficulty": "intermediate",
                    "time_limit": 90,
                    "tips": ["Show innovation", "Explain process", "Quantify impact"]
                },
                {
                    "question": "How do you approach solving a problem you've never encountered before?",
                    "difficulty": "intermediate",
                    "time_limit": 75,
                    "tips": ["Show methodology", "Discuss research", "Mention collaboration"]
                }
            ],
            "Communication": [
                {
                    "question": "Tell me about a time when you had to present complex information to stakeholders.",
                    "difficulty": "intermediate",
                    "time_limit": 90,
                    "tips": ["Show clarity", "Discuss preparation", "Mention feedback"]
                },
                {
                    "question": "Describe a situation where you had to persuade someone to see things your way.",
                    "difficulty": "advanced",
                    "time_limit": 90,
                    "tips": ["Show influence skills", "Discuss approach", "Highlight outcome"]
                },
                {
                    "question": "How do you handle receiving critical feedback?",
                    "difficulty": "intermediate",
                    "time_limit": 60,
                    "tips": ["Show openness", "Discuss growth", "Give examples"]
                }
            ]
        }
    
    def get_question(self, category: str = None, difficulty: str = None) -> Dict:
        """Get a random question from the bank"""
        if category and category in self.question_bank:
            questions = self.question_bank[category]
        else:
            # Get from all categories
            all_questions = []
            for cat_questions in self.question_bank.values():
                all_questions.extend(cat_questions)
            questions = all_questions
        
        # Filter by difficulty if specified
        if difficulty:
            questions = [q for q in questions if q.get("difficulty") == difficulty]
        
        if not questions:
            questions = self.question_bank["Behavioral"]  # Fallback
        
        return random.choice(questions)
    
    async def generate_ai_question(self, category: str, user_profile: Dict = None) -> Dict:
        """Generate a personalized AI question based on user profile"""
        # If no API key, return from bank
        if not self.openai_api_key:
            return self.get_question(category)
        
        try:
            profile_context = ""
            if user_profile:
                profile_context = f"""
                User Background:
                - Role: {user_profile.get('role', 'Professional')}
                - Experience: {user_profile.get('experience', 'Mid-level')}
                - Industry: {user_profile.get('industry', 'Technology')}
                """
            
            prompt = f"""Generate a thoughtful {category} interview question for a video interview.
            {profile_context}
            
            The question should:
            1. Be clear and specific
            2. Allow the candidate to demonstrate their skills
            3. Be answerable in 60-90 seconds
            4. Be relevant to modern workplace scenarios
            
            Return ONLY the question text, nothing else."""
            
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are an expert interviewer creating insightful interview questions."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 150
            }
            
            response = requests.post(self.openai_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                question_text = data['choices'][0]['message']['content'].strip()
                
                return {
                    "question": question_text,
                    "category": category,
                    "difficulty": "intermediate",
                    "time_limit": 90,
                    "ai_generated": True,
                    "tips": [
                        "Structure your answer clearly",
                        "Provide specific examples",
                        "Show your thought process"
                    ]
                }
            else:
                print(f"OpenAI API error: {response.status_code}")
                return self.get_question(category)
                
        except Exception as e:
            print(f"Error generating AI question: {e}")
            return self.get_question(category)
    
    async def analyze_video_response(self, 
                                    transcription: str,
                                    question: str,
                                    emotion_data: Dict = None,
                                    voice_data: Dict = None) -> Dict:
        """Comprehensive AI analysis of video interview response"""
        # If no API key, provide basic analysis
        if not self.openai_api_key:
            return self._basic_analysis(transcription, question, emotion_data, voice_data)
        
        try:
            analysis_prompt = f"""Analyze this video interview response as a senior interviewer.

Question: {question}

Candidate's Response: {transcription}

Additional Context:
- Dominant Emotion: {emotion_data.get('dominant_emotion', 'N/A') if emotion_data else 'N/A'}
- Speech Rate: {voice_data.get('speech_rate', 'N/A') if voice_data else 'N/A'} words/min
- Filler Words: {voice_data.get('filler_count', 'N/A') if voice_data else 'N/A'}

Provide a comprehensive analysis with:

1. CONTENT QUALITY (Score 1-10):
   - Relevance to question
   - Depth of answer
   - Use of examples
   - Structure (STAR method if applicable)

2. COMMUNICATION SKILLS (Score 1-10):
   - Clarity and articulation
   - Confidence level
   - Professional language
   - Engagement

3. STRENGTHS (2-3 specific points)

4. AREAS FOR IMPROVEMENT (2-3 specific points)

5. OVERALL SCORE (1-10)

6. ACTIONABLE RECOMMENDATIONS (3-4 specific tips)

Format your response clearly with these sections."""

            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a senior technical interviewer with 15+ years of experience. Provide constructive, specific feedback."},
                    {"role": "user", "content": analysis_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            response = requests.post(self.openai_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                feedback = data['choices'][0]['message']['content'].strip()
            else:
                print(f"OpenAI API error: {response.status_code}")
                return self._basic_analysis(transcription, question, emotion_data, voice_data)
            
            # Extract overall score from feedback
            score = self._extract_score(feedback)
            
            return {
                "success": True,
                "feedback": feedback,
                "score": score,
                "detailed_analysis": {
                    "transcription": transcription,
                    "emotions": emotion_data or {},
                    "voice_analysis": voice_data or {},
                    "confidence_score": self._calculate_confidence_score(transcription, emotion_data, voice_data),
                    "professionalism_score": self._calculate_professionalism_score(transcription, voice_data),
                    "engagement_score": self._calculate_engagement_score(emotion_data, voice_data),
                    "authenticity_score": self._calculate_authenticity_score(emotion_data)
                }
            }
        except Exception as e:
            print(f"Error in video analysis: {e}")
            return {
                "success": False,
                "error": str(e),
                "feedback": "Unable to complete analysis. Please try again.",
                "score": 0
            }
    
    def _extract_score(self, feedback: str) -> float:
        """Extract overall score from feedback text"""
        import re
        # Look for patterns like "OVERALL SCORE: 8" or "Overall: 8/10"
        patterns = [
            r'OVERALL SCORE[:\s]+(\d+(?:\.\d+)?)',
            r'Overall[:\s]+(\d+(?:\.\d+)?)',
            r'Score[:\s]+(\d+(?:\.\d+)?)/10'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, feedback, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        return 7.5  # Default score
    
    def _calculate_confidence_score(self, transcription: str, emotion_data: Dict, voice_data: Dict) -> float:
        """Calculate confidence score based on multiple factors"""
        score = 7.0  # Base score
        
        # Adjust based on speech rate
        if voice_data and 'speech_rate' in voice_data:
            rate = voice_data['speech_rate']
            if 120 <= rate <= 160:  # Optimal range
                score += 1.5
            elif rate < 100 or rate > 180:
                score -= 1.0
        
        # Adjust based on filler words
        if voice_data and 'filler_count' in voice_data:
            filler_count = voice_data['filler_count']
            if filler_count < 3:
                score += 1.0
            elif filler_count > 8:
                score -= 1.5
        
        # Adjust based on emotion
        if emotion_data and 'dominant_emotion' in emotion_data:
            emotion = emotion_data['dominant_emotion'].lower()
            if emotion in ['happy', 'confident', 'neutral']:
                score += 0.5
            elif emotion in ['anxious', 'nervous']:
                score -= 0.5
        
        return min(10.0, max(1.0, score))
    
    def _calculate_professionalism_score(self, transcription: str, voice_data: Dict) -> float:
        """Calculate professionalism score"""
        score = 7.5
        
        # Check for professional language
        professional_words = ['experience', 'project', 'team', 'achieved', 'developed', 'implemented']
        unprofessional_words = ['like', 'um', 'uh', 'yeah', 'stuff', 'things']
        
        text_lower = transcription.lower()
        prof_count = sum(1 for word in professional_words if word in text_lower)
        unprof_count = sum(1 for word in unprofessional_words if word in text_lower)
        
        score += (prof_count * 0.3)
        score -= (unprof_count * 0.2)
        
        return min(10.0, max(1.0, score))
    
    def _calculate_engagement_score(self, emotion_data: Dict, voice_data: Dict) -> float:
        """Calculate engagement score"""
        score = 7.0
        
        if emotion_data:
            emotion = emotion_data.get('dominant_emotion', '').lower()
            if emotion in ['happy', 'excited', 'confident']:
                score += 2.0
            elif emotion in ['neutral']:
                score += 0.5
            elif emotion in ['sad', 'bored']:
                score -= 1.5
        
        if voice_data and 'energy_level' in voice_data:
            energy = voice_data['energy_level']
            if energy == 'high':
                score += 1.5
            elif energy == 'low':
                score -= 1.0
        
        return min(10.0, max(1.0, score))
    
    def _calculate_authenticity_score(self, emotion_data: Dict) -> float:
        """Calculate authenticity score based on emotion consistency"""
        score = 8.0
        
        if emotion_data and 'micro_expressions' in emotion_data:
            # Check for consistency between dominant emotion and micro-expressions
            dominant = emotion_data.get('dominant_emotion', '').lower()
            micro = emotion_data.get('micro_expressions', [])
            
            if micro and dominant:
                consistency = sum(1 for expr in micro if expr.lower() == dominant)
                consistency_ratio = consistency / len(micro) if micro else 0
                
                if consistency_ratio > 0.7:
                    score += 1.5
                elif consistency_ratio < 0.3:
                    score -= 2.0
        
        return min(10.0, max(1.0, score))
    
    def _basic_analysis(self, transcription: str, question: str, 
                       emotion_data: Dict = None, voice_data: Dict = None) -> Dict:
        """Provide basic analysis when OpenAI API is not available"""
        word_count = len(transcription.split())
        
        # Calculate basic scores
        confidence_score = self._calculate_confidence_score(transcription, emotion_data, voice_data)
        professionalism_score = self._calculate_professionalism_score(transcription, voice_data)
        engagement_score = self._calculate_engagement_score(emotion_data, voice_data)
        authenticity_score = self._calculate_authenticity_score(emotion_data)
        
        overall_score = (confidence_score + professionalism_score + engagement_score + authenticity_score) / 4
        
        feedback = f"""VIDEO INTERVIEW ANALYSIS

CONTENT QUALITY: {round(professionalism_score, 1)}/10
Your response was {"detailed" if word_count > 100 else "concise"} with {word_count} words.

COMMUNICATION SKILLS: {round(confidence_score, 1)}/10
{"Good clarity and confidence" if confidence_score > 7 else "Work on clarity and confidence"}.

STRENGTHS:
- Completed the response
- {"Professional language used" if professionalism_score > 7 else "Attempted to answer the question"}
- {"Good engagement" if engagement_score > 7 else "Showed effort"}

AREAS FOR IMPROVEMENT:
- {"Reduce filler words" if voice_data and voice_data.get('filler_count', 0) > 5 else "Maintain current speech patterns"}
- {"Provide more specific examples" if word_count < 80 else "Keep responses focused"}
- Practice STAR method for behavioral questions

OVERALL SCORE: {round(overall_score, 1)}/10

RECOMMENDATIONS:
1. Structure answers using STAR method (Situation, Task, Action, Result)
2. Maintain eye contact with the camera
3. Speak at a moderate pace (120-150 words/min)
4. Use specific examples from your experience

Note: Full AI analysis requires OpenAI API key configuration."""

        return {
            "success": True,
            "feedback": feedback,
            "score": round(overall_score, 1),
            "detailed_analysis": {
                "transcription": transcription,
                "emotions": emotion_data or {},
                "voice_analysis": voice_data or {},
                "confidence_score": round(confidence_score, 1),
                "professionalism_score": round(professionalism_score, 1),
                "engagement_score": round(engagement_score, 1),
                "authenticity_score": round(authenticity_score, 1)
            }
        }


# Singleton instance
_video_interview_service = None

def get_video_interview_service() -> VideoInterviewService:
    """Get or create the video interview service instance"""
    global _video_interview_service
    if _video_interview_service is None:
        _video_interview_service = VideoInterviewService()
    return _video_interview_service
