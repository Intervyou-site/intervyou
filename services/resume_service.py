"""
Industry-Grade Resume Builder Service
Features: ATS optimization, AI suggestions, keyword analysis, PDF generation
"""
import os
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx

logger = logging.getLogger(__name__)


class ResumeService:
    """Comprehensive resume building and optimization service"""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        
        # ATS keywords database by industry
        self.ats_keywords = {
            "software_engineering": [
                "agile", "scrum", "ci/cd", "git", "docker", "kubernetes",
                "microservices", "rest api", "database", "cloud", "aws", "azure"
            ],
            "data_science": [
                "machine learning", "python", "tensorflow", "pytorch", "sql",
                "data analysis", "statistics", "visualization", "pandas", "numpy"
            ],
            "product_management": [
                "roadmap", "stakeholder", "user stories", "agile", "metrics",
                "kpi", "product strategy", "market research", "a/b testing"
            ],
            "marketing": [
                "seo", "sem", "content strategy", "analytics", "social media",
                "campaign", "roi", "conversion", "engagement", "brand"
            ]
        }
    
    async def analyze_resume(self, resume_data: Dict) -> Dict[str, Any]:
        """
        Comprehensive resume analysis with ATS scoring
        """
        try:
            analysis = {
                "ats_score": 0,
                "strengths": [],
                "weaknesses": [],
                "suggestions": [],
                "keyword_analysis": {},
                "formatting_score": 0,
                "content_score": 0,
                "impact_score": 0
            }
            
            # 1. ATS Score Calculation
            ats_score = self._calculate_ats_score(resume_data)
            analysis["ats_score"] = ats_score
            
            # 2. Keyword Analysis
            keyword_analysis = self._analyze_keywords(resume_data)
            analysis["keyword_analysis"] = keyword_analysis
            
            # 3. Formatting Check
            formatting_score = self._check_formatting(resume_data)
            analysis["formatting_score"] = formatting_score
            
            # 4. Content Quality
            content_score = self._analyze_content_quality(resume_data)
            analysis["content_score"] = content_score
            
            # 5. Impact Analysis
            impact_score = self._analyze_impact(resume_data)
            analysis["impact_score"] = impact_score
            
            # 6. Generate AI-powered suggestions
            if self.openai_api_key:
                ai_suggestions = await self._get_ai_suggestions(resume_data)
                if ai_suggestions:
                    analysis["ai_suggestions"] = ai_suggestions
            
            # 7. Identify strengths and weaknesses
            analysis["strengths"] = self._identify_strengths(resume_data, ats_score)
            analysis["weaknesses"] = self._identify_weaknesses(resume_data, ats_score)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Resume analysis error: {e}")
            return {"error": str(e), "ats_score": 0}

    
    def _calculate_ats_score(self, resume_data: Dict) -> int:
        """Calculate ATS compatibility score (0-100)"""
        score = 0
        max_score = 100
        
        # Contact information (20 points)
        if resume_data.get("email"):
            score += 5
        if resume_data.get("phone"):
            score += 5
        if resume_data.get("linkedin"):
            score += 5
        if resume_data.get("location"):
            score += 5
        
        # Professional summary (15 points)
        summary = resume_data.get("summary", "")
        if len(summary) > 50:
            score += 10
        if len(summary) > 150:
            score += 5
        
        # Experience section (30 points)
        experiences = resume_data.get("experience", [])
        if len(experiences) > 0:
            score += 10
        if len(experiences) >= 2:
            score += 10
        # Check for quantifiable achievements
        has_numbers = any(any(char.isdigit() for char in exp.get("description", "")) 
                         for exp in experiences)
        if has_numbers:
            score += 10
        
        # Education (15 points)
        education = resume_data.get("education", [])
        if len(education) > 0:
            score += 15
        
        # Skills (20 points)
        skills = resume_data.get("skills", [])
        if len(skills) >= 5:
            score += 10
        if len(skills) >= 10:
            score += 10
        
        return min(score, max_score)
    
    def _analyze_keywords(self, resume_data: Dict) -> Dict:
        """Analyze keyword density and relevance"""
        # Combine all text from resume
        all_text = " ".join([
            resume_data.get("summary", ""),
            " ".join([exp.get("description", "") for exp in resume_data.get("experience", [])]),
            " ".join([edu.get("description", "") for edu in resume_data.get("education", [])]),
            " ".join(resume_data.get("skills", []))
        ]).lower()
        
        # Check for industry keywords
        found_keywords = {}
        for industry, keywords in self.ats_keywords.items():
            found = [kw for kw in keywords if kw in all_text]
            if found:
                found_keywords[industry] = found
        
        return {
            "total_keywords": len(all_text.split()),
            "industry_matches": found_keywords,
            "keyword_density": "optimal" if 50 < len(all_text.split()) < 500 else "needs_improvement"
        }
    
    def _check_formatting(self, resume_data: Dict) -> int:
        """Check formatting best practices (0-100)"""
        score = 0
        
        # Check for proper structure
        if resume_data.get("name"):
            score += 20
        if resume_data.get("summary"):
            score += 20
        if resume_data.get("experience"):
            score += 30
        if resume_data.get("education"):
            score += 15
        if resume_data.get("skills"):
            score += 15
        
        return score
    
    def _analyze_content_quality(self, resume_data: Dict) -> int:
        """Analyze content quality (0-100)"""
        score = 0
        
        # Check experience descriptions
        experiences = resume_data.get("experience", [])
        for exp in experiences:
            desc = exp.get("description", "")
            # Check for action verbs
            action_verbs = ["led", "managed", "developed", "created", "implemented", 
                           "designed", "improved", "increased", "reduced", "achieved"]
            if any(verb in desc.lower() for verb in action_verbs):
                score += 10
            # Check for quantifiable results
            if any(char.isdigit() for char in desc):
                score += 10
        
        return min(score, 100)
    
    def _analyze_impact(self, resume_data: Dict) -> int:
        """Analyze impact and achievements (0-100)"""
        score = 0
        
        experiences = resume_data.get("experience", [])
        for exp in experiences:
            desc = exp.get("description", "")
            # Look for impact indicators
            impact_words = ["increased", "decreased", "improved", "reduced", 
                           "saved", "generated", "grew", "optimized"]
            if any(word in desc.lower() for word in impact_words):
                score += 15
            # Look for percentages or numbers
            if "%" in desc or any(char.isdigit() for char in desc):
                score += 10
        
        return min(score, 100)

    
    def _identify_strengths(self, resume_data: Dict, ats_score: int) -> List[str]:
        """Identify resume strengths"""
        strengths = []
        
        if ats_score >= 80:
            strengths.append("Excellent ATS compatibility")
        
        experiences = resume_data.get("experience", [])
        if len(experiences) >= 3:
            strengths.append("Strong work history with multiple positions")
        
        # Check for quantifiable achievements
        has_metrics = any(any(char.isdigit() for char in exp.get("description", "")) 
                         for exp in experiences)
        if has_metrics:
            strengths.append("Includes quantifiable achievements")
        
        skills = resume_data.get("skills", [])
        if len(skills) >= 10:
            strengths.append("Comprehensive skills section")
        
        if resume_data.get("linkedin"):
            strengths.append("Professional online presence included")
        
        return strengths
    
    def _identify_weaknesses(self, resume_data: Dict, ats_score: int) -> List[str]:
        """Identify areas for improvement"""
        weaknesses = []
        
        if ats_score < 70:
            weaknesses.append("ATS score could be improved")
        
        if not resume_data.get("summary"):
            weaknesses.append("Missing professional summary")
        
        experiences = resume_data.get("experience", [])
        if len(experiences) == 0:
            weaknesses.append("No work experience listed")
        
        # Check for lack of quantifiable results
        has_metrics = any(any(char.isdigit() for char in exp.get("description", "")) 
                         for exp in experiences)
        if not has_metrics and len(experiences) > 0:
            weaknesses.append("Add quantifiable achievements (numbers, percentages)")
        
        skills = resume_data.get("skills", [])
        if len(skills) < 5:
            weaknesses.append("Add more relevant skills")
        
        if not resume_data.get("linkedin"):
            weaknesses.append("Consider adding LinkedIn profile")
        
        return weaknesses
    
    async def _get_ai_suggestions(self, resume_data: Dict) -> Optional[Dict]:
        """Get AI-powered resume improvement suggestions"""
        if not self.openai_api_key:
            return None
        
        try:
            prompt = f"""Analyze this resume and provide specific, actionable improvement suggestions.

Resume Data:
{json.dumps(resume_data, indent=2)}

Provide suggestions in JSON format:
{{
  "summary_improvements": ["specific suggestion 1", "specific suggestion 2"],
  "experience_improvements": ["specific suggestion 1", "specific suggestion 2"],
  "skills_to_add": ["skill 1", "skill 2", "skill 3"],
  "formatting_tips": ["tip 1", "tip 2"],
  "ats_optimization": ["optimization 1", "optimization 2"]
}}

Focus on:
1. Making achievements more quantifiable
2. Using strong action verbs
3. ATS keyword optimization
4. Industry-specific improvements
5. Formatting best practices"""

            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are an expert resume writer and career coach with 15+ years of experience."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 800,
                "temperature": 0.7,
                "response_format": {"type": "json_object"}
            }
            
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(self.openai_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
                
        except Exception as e:
            logger.error(f"AI suggestions error: {e}")
            return None
    
    async def optimize_bullet_point(self, bullet_point: str, role: str = "") -> str:
        """Optimize a single bullet point using AI"""
        if not self.openai_api_key:
            return bullet_point
        
        try:
            prompt = f"""Improve this resume bullet point to be more impactful and ATS-friendly.

Original: {bullet_point}
Role: {role}

Requirements:
1. Start with a strong action verb
2. Include quantifiable results if possible
3. Be specific and concise
4. Use industry keywords
5. Keep it under 150 characters

Return only the improved bullet point, nothing else."""

            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are an expert resume writer. Improve bullet points to be impactful and ATS-optimized."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 100,
                "temperature": 0.7
            }
            
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(self.openai_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
                
        except Exception as e:
            logger.error(f"Bullet point optimization error: {e}")
            return bullet_point


# Global instance
_resume_service = None

def get_resume_service(openai_api_key: str = None) -> ResumeService:
    """Get or create global resume service"""
    global _resume_service
    if _resume_service is None:
        _resume_service = ResumeService(openai_api_key)
    return _resume_service
