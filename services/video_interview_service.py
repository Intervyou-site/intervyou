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
                    "voice_analysis": voice_data or {},
                    "confidence_score": self._calculate_confidence_score(transcription, None, voice_data),
                    "professionalism_score": self._calculate_professionalism_score(transcription, voice_data),
                    "engagement_score": self._calculate_engagement_score(None, voice_data)
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
        """Calculate confidence score based on transcription and voice only (no emotion data)"""
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
        
        # No emotion-based adjustments - transcription only
        
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
        """Calculate engagement score based on voice data only (no emotion data)"""
        score = 7.0
        
        # No emotion-based scoring - transcription only
        
        # Voice energy if available
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
        """Provide basic analysis when OpenAI API is not available - TRANSCRIPTION ONLY"""
        
        # Check if this is a fallback transcription (when speech recognition failed)
        is_fallback = transcription.startswith("[Speech recorded")
        
        if is_fallback:
            # Estimate word count from duration
            duration = voice_data.get('duration', 10) if voice_data else 10
            word_count = voice_data.get('word_count', int(duration * 2.5)) if voice_data else int(duration * 2.5)
        else:
            word_count = len(transcription.split())
        
        # Validate minimum content - be strict for very short responses
        if not is_fallback and word_count <= 3:
            return {
                "success": True,
                "feedback": f"""VIDEO INTERVIEW ANALYSIS

CONTENT QUALITY: 1.5/10
Your response was extremely brief - only {word_count} word{'s' if word_count > 1 else ''}: "{transcription}"
A proper interview answer should be 50-150 words.

COMMUNICATION SKILLS: 2.0/10
Insufficient content to evaluate communication skills.

STRENGTHS:
- You attempted to respond

AREAS FOR IMPROVEMENT:
- Provide much more detailed answers
- Use the STAR method (Situation, Task, Action, Result)
- Aim for at least 50 words per answer
- Include specific examples from your experience

OVERALL SCORE: 1.8/10

RECOMMENDATIONS:
1. Practice answering questions with proper depth
2. Structure answers using STAR method
3. Speak for at least 30-60 seconds
4. Provide concrete examples

Note: Your response was too brief to demonstrate your qualifications.""",
                "score": 1.8,
                "detailed_analysis": {
                    "transcription": transcription,
                    "voice_analysis": voice_data or {},
                    "confidence_score": 2.0,
                    "professionalism_score": 1.5,
                    "engagement_score": 2.0
                }
            }
        
        # Calculate realistic scores based on transcription and voice data ONLY
        confidence_score = self._calculate_confidence_score(transcription, None, voice_data)
        professionalism_score = self._calculate_professionalism_score(transcription, voice_data)
        engagement_score = self._calculate_engagement_score(None, voice_data)
        
        # Adjust scores for fallback mode (slightly lower since we can't analyze text)
        if is_fallback:
            confidence_score = max(5.0, confidence_score - 1.0)
            professionalism_score = max(5.0, professionalism_score - 1.0)
        # Adjust scores based on word count - be strict
        elif word_count < 20:
            confidence_score = max(2.0, confidence_score - 3.0)
            professionalism_score = max(2.0, professionalism_score - 3.0)
            engagement_score = max(2.0, engagement_score - 2.0)
        elif word_count < 30:
            confidence_score = max(3.0, confidence_score - 2.0)
            professionalism_score = max(3.0, professionalism_score - 2.0)
        elif word_count > 200:
            # Too long might indicate rambling
            professionalism_score = max(5.0, professionalism_score - 1.0)
        
        overall_score = (confidence_score + professionalism_score + engagement_score) / 3
        
        # Generate feedback based on transcription only
        if is_fallback:
            feedback = f"""VIDEO INTERVIEW ANALYSIS

CONTENT QUALITY: {round(professionalism_score, 1)}/10
Your response was recorded for approximately {int(voice_data.get('duration', 10))} seconds.
Note: Detailed transcription was not available, so analysis is based on audio characteristics.

COMMUNICATION SKILLS: {round(confidence_score, 1)}/10
Based on audio analysis, your delivery shows {"good" if confidence_score > 6 else "moderate"} confidence.

STRENGTHS:
- Completed a response of reasonable length
- Maintained consistent audio throughout
- {"Good speaking pace" if voice_data and 120 <= voice_data.get('speech_rate', 150) <= 160 else "Attempted to answer the question"}

AREAS FOR IMPROVEMENT:
- Ensure clear audio quality for better analysis
- Practice speaking clearly and at a moderate pace
- Structure answers using STAR method (Situation, Task, Action, Result)

OVERALL SCORE: {round(overall_score, 1)}/10

RECOMMENDATIONS:
1. Improve microphone quality or speak closer to the microphone
2. Structure answers using STAR method
3. Speak at a moderate pace (120-150 words/min)
4. Use specific examples from your experience

Note: For more detailed feedback, ensure clear audio recording. Full AI analysis requires OpenAI API key configuration."""
        else:
            # Normal feedback with transcription
            content_quality_feedback = ""
            if word_count < 20:
                content_quality_feedback = f"Your response was extremely brief with only {word_count} words. This is insufficient for a proper interview answer. Aim for 50-150 words."
            elif word_count < 30:
                content_quality_feedback = f"Your response was very brief with {word_count} words. Aim for 50-150 words for better depth."
            elif word_count > 150:
                content_quality_feedback = f"Your response was detailed with {word_count} words. Good depth of information."
            else:
                content_quality_feedback = f"Your response had good length with {word_count} words."
            
            communication_feedback = ""
            if confidence_score > 7:
                communication_feedback = "Good clarity and confidence in delivery."
            elif confidence_score > 5:
                communication_feedback = "Moderate clarity. Work on reducing filler words and speaking more confidently."
            else:
                communication_feedback = "Work on clarity and confidence. Practice speaking more smoothly."
            
            # Determine strengths
            strengths = []
            if word_count >= 50:
                strengths.append("Provided adequate detail in response")
            elif word_count >= 20:
                strengths.append("Attempted to provide some detail")
            else:
                strengths.append("You attempted to respond")
                
            if professionalism_score > 7:
                strengths.append("Professional language used")
            if voice_data and voice_data.get('filler_count', 10) < 5:
                strengths.append("Minimal use of filler words")
            if voice_data and 120 <= voice_data.get('speech_rate', 0) <= 160:
                strengths.append("Good speaking pace")
            
            # Determine areas for improvement
            improvements = []
            if word_count < 20:
                improvements.append("Provide MUCH more detailed answers (aim for 50-150 words)")
                improvements.append("Your response was too brief to properly evaluate")
            elif word_count < 50:
                improvements.append("Provide more detailed answers (aim for 50-150 words)")
            if voice_data and voice_data.get('filler_count', 0) > 5:
                improvements.append(f"Reduce filler words (detected {voice_data.get('filler_count')} instances)")
            if voice_data and voice_data.get('speech_rate', 150) < 100:
                improvements.append("Speak at a slightly faster pace for better engagement")
            if voice_data and voice_data.get('speech_rate', 150) > 180:
                improvements.append("Slow down your speaking pace for better clarity")
            if professionalism_score < 7:
                improvements.append("Use more professional and specific language")
            improvements.append("Practice STAR method for behavioral questions")
            
            feedback = f"""VIDEO INTERVIEW ANALYSIS

CONTENT QUALITY: {round(professionalism_score, 1)}/10
{content_quality_feedback}

COMMUNICATION SKILLS: {round(confidence_score, 1)}/10
{communication_feedback}

STRENGTHS:
{chr(10).join(f'- {s}' for s in strengths)}

AREAS FOR IMPROVEMENT:
{chr(10).join(f'- {i}' for i in improvements)}

OVERALL SCORE: {round(overall_score, 1)}/10

RECOMMENDATIONS:
1. Structure answers using STAR method (Situation, Task, Action, Result)
2. Speak at a moderate pace (120-150 words/min)
3. Use specific examples from your experience
4. Aim for 50-150 words per answer

Note: Full AI analysis requires OpenAI API key configuration."""

        return {
            "success": True,
            "feedback": feedback,
            "score": round(overall_score, 1),
            "detailed_analysis": {
                "transcription": transcription,
                "voice_analysis": voice_data or {},
                "confidence_score": round(confidence_score, 1),
                "professionalism_score": round(professionalism_score, 1),
                "engagement_score": round(engagement_score, 1)
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
