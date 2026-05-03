"""
Enhanced Resume Builder Service with Advanced Analysis
Features: Multiple templates, detailed ATS scoring, AI suggestions, keyword optimization
"""
import os
import json
import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import httpx

logger = logging.getLogger(__name__)


class EnhancedResumeAnalyzer:
    """Comprehensive resume analysis with detailed scoring"""
    
    def __init__(self, openai_api_key: str = None):
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        
        # Industry-specific keywords database
        self.industry_keywords = {
            "software_engineering": {
                "technical": ["python", "java", "javascript", "react", "node.js", "sql", "aws", "docker", "kubernetes", "git"],
                "methodologies": ["agile", "scrum", "ci/cd", "devops", "tdd", "microservices"],
                "soft_skills": ["collaboration", "problem-solving", "leadership", "communication"]
            },
            "data_science": {
                "technical": ["python", "r", "sql", "machine learning", "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn"],
                "methodologies": ["statistical analysis", "data visualization", "predictive modeling", "a/b testing"],
                "soft_skills": ["analytical thinking", "communication", "business acumen"]
            },
            "product_management": {
                "technical": ["roadmap", "user stories", "wireframes", "analytics", "sql", "jira"],
                "methodologies": ["agile", "scrum", "lean", "design thinking", "user research"],
                "soft_skills": ["stakeholder management", "communication", "strategic thinking", "leadership"]
            }
        }
        
        # Action verbs categorized by impact
        self.action_verbs = {
            "leadership": ["led", "managed", "directed", "supervised", "coordinated", "mentored", "guided"],
            "achievement": ["achieved", "accomplished", "exceeded", "surpassed", "delivered", "completed"],
            "improvement": ["improved", "enhanced", "optimized", "streamlined", "increased", "reduced", "accelerated"],
            "creation": ["created", "developed", "designed", "built", "established", "launched", "implemented"],
            "analysis": ["analyzed", "evaluated", "assessed", "researched", "investigated", "identified"]
        }

    
    async def analyze_resume_comprehensive(self, resume_data: Dict) -> Dict[str, Any]:
        """
        Comprehensive resume analysis with detailed breakdown
        """
        try:
            analysis = {
                "overall_score": 0,
                "ats_score": 0,
                "breakdown": {
                    "contact_info": {"score": 0, "max": 15, "issues": []},
                    "summary": {"score": 0, "max": 15, "issues": []},
                    "experience": {"score": 0, "max": 30, "issues": []},
                    "education": {"score": 0, "max": 15, "issues": []},
                    "skills": {"score": 0, "max": 15, "issues": []},
                    "formatting": {"score": 0, "max": 10, "issues": []}
                },
                "keyword_analysis": {},
                "action_verb_analysis": {},
                "quantification_analysis": {},
                "strengths": [],
                "improvements": [],
                "ai_suggestions": None
            }
            
            # 1. Contact Information Analysis
            contact_score = self._analyze_contact_info(resume_data, analysis["breakdown"]["contact_info"])
            
            # 2. Summary Analysis
            summary_score = self._analyze_summary(resume_data, analysis["breakdown"]["summary"])
            
            # 3. Experience Analysis
            exp_score = self._analyze_experience(resume_data, analysis["breakdown"]["experience"])
            
            # 4. Education Analysis
            edu_score = self._analyze_education(resume_data, analysis["breakdown"]["education"])
            
            # 5. Skills Analysis
            skills_score = self._analyze_skills(resume_data, analysis["breakdown"]["skills"])
            
            # 6. Formatting Analysis
            format_score = self._analyze_formatting(resume_data, analysis["breakdown"]["formatting"])
            
            # Calculate overall scores
            total_score = contact_score + summary_score + exp_score + edu_score + skills_score + format_score
            analysis["overall_score"] = total_score
            analysis["ats_score"] = total_score
            
            # 7. Keyword Analysis
            analysis["keyword_analysis"] = self._analyze_keywords_detailed(resume_data)
            
            # 8. Action Verb Analysis
            analysis["action_verb_analysis"] = self._analyze_action_verbs(resume_data)
            
            # 9. Quantification Analysis
            analysis["quantification_analysis"] = self._analyze_quantification(resume_data)
            
            # 10. Generate strengths and improvements
            analysis["strengths"] = self._generate_strengths(analysis)
            analysis["improvements"] = self._generate_improvements(analysis)
            
            # 11. AI Suggestions (if API key available)
            if self.openai_api_key:
                analysis["ai_suggestions"] = await self._get_ai_suggestions(resume_data, analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Resume analysis error: {e}")
            return {"error": str(e), "overall_score": 0}

    
    def _analyze_contact_info(self, resume_data: Dict, breakdown: Dict) -> int:
        """Analyze contact information completeness"""
        score = 0
        max_score = 15
        
        if resume_data.get("name"):
            score += 4
        else:
            breakdown["issues"].append("Missing name")
        
        if resume_data.get("email"):
            score += 4
        else:
            breakdown["issues"].append("Missing email")
        
        if resume_data.get("phone"):
            score += 3
        else:
            breakdown["issues"].append("Missing phone number")
        
        if resume_data.get("linkedin"):
            score += 2
        else:
            breakdown["issues"].append("Consider adding LinkedIn profile")
        
        if resume_data.get("location"):
            score += 2
        
        breakdown["score"] = score
        return score
    
    def _analyze_summary(self, resume_data: Dict, breakdown: Dict) -> int:
        """Analyze professional summary quality"""
        score = 0
        max_score = 15
        summary = resume_data.get("summary", "")
        
        if not summary:
            breakdown["issues"].append("Missing professional summary")
            breakdown["score"] = 0
            return 0
        
        # Length check
        word_count = len(summary.split())
        if word_count >= 30:
            score += 5
        elif word_count >= 15:
            score += 3
        else:
            breakdown["issues"].append("Summary too short (aim for 30-50 words)")
        
        # Keyword presence
        if any(keyword in summary.lower() for keyword in ["experience", "skilled", "expertise", "professional"]):
            score += 5
        else:
            breakdown["issues"].append("Add professional keywords to summary")
        
        # Action-oriented language
        if any(verb in summary.lower() for verbs in self.action_verbs.values() for verb in verbs):
            score += 5
        else:
            breakdown["issues"].append("Use action verbs in summary")
        
        breakdown["score"] = score
        return score

    
    def _analyze_experience(self, resume_data: Dict, breakdown: Dict) -> int:
        """Analyze work experience quality"""
        score = 0
        max_score = 30
        experiences = resume_data.get("experience", [])
        
        if not experiences:
            breakdown["issues"].append("No work experience listed")
            breakdown["score"] = 0
            return 0
        
        # Number of positions
        if len(experiences) >= 3:
            score += 8
        elif len(experiences) >= 2:
            score += 6
        elif len(experiences) >= 1:
            score += 4
        
        # Check for quantifiable achievements
        has_numbers = sum(1 for exp in experiences if any(char.isdigit() for char in exp.get("description", "")))
        if has_numbers >= len(experiences):
            score += 10
        elif has_numbers > 0:
            score += 5
        else:
            breakdown["issues"].append("Add quantifiable achievements (numbers, percentages)")
        
        # Check for action verbs
        action_verb_count = 0
        for exp in experiences:
            desc = exp.get("description", "").lower()
            if any(verb in desc for verbs in self.action_verbs.values() for verb in verbs):
                action_verb_count += 1
        
        if action_verb_count >= len(experiences):
            score += 8
        elif action_verb_count > 0:
            score += 4
        else:
            breakdown["issues"].append("Use strong action verbs in experience descriptions")
        
        # Check for proper date formatting
        has_dates = sum(1 for exp in experiences if exp.get("start") and exp.get("end"))
        if has_dates >= len(experiences):
            score += 4
        else:
            breakdown["issues"].append("Add dates to all positions")
        
        breakdown["score"] = score
        return score
    
    def _analyze_education(self, resume_data: Dict, breakdown: Dict) -> int:
        """Analyze education section"""
        score = 0
        max_score = 15
        education = resume_data.get("education", [])
        
        if not education:
            breakdown["issues"].append("No education listed")
            breakdown["score"] = 0
            return 0
        
        # Has education entry
        score += 10
        
        # Check completeness
        for edu in education:
            if edu.get("degree") and edu.get("school") and edu.get("year"):
                score += 3
                break
        
        # GPA if strong
        for edu in education:
            gpa = edu.get("gpa", "")
            if gpa and any(char.isdigit() for char in gpa):
                score += 2
                break
        
        breakdown["score"] = min(score, max_score)
        return min(score, max_score)
    
    def _analyze_skills(self, resume_data: Dict, breakdown: Dict) -> int:
        """Analyze skills section"""
        score = 0
        max_score = 15
        skills = resume_data.get("skills", [])
        
        if not skills:
            breakdown["issues"].append("No skills listed")
            breakdown["score"] = 0
            return 0
        
        # Number of skills
        skill_count = len(skills)
        if skill_count >= 10:
            score += 10
        elif skill_count >= 5:
            score += 7
        elif skill_count >= 3:
            score += 4
        else:
            breakdown["issues"].append("Add more relevant skills (aim for 8-12)")
        
        # Check for technical keywords
        all_skills_text = " ".join(skills).lower()
        has_technical = any(keyword in all_skills_text 
                          for industry in self.industry_keywords.values() 
                          for keyword in industry.get("technical", []))
        if has_technical:
            score += 5
        else:
            breakdown["issues"].append("Add technical skills relevant to your field")
        
        breakdown["score"] = score
        return score
    
    def _analyze_formatting(self, resume_data: Dict, breakdown: Dict) -> int:
        """Analyze overall formatting and structure"""
        score = 10  # Start with full score
        
        # Check for proper structure
        required_sections = ["name", "email", "summary", "experience", "education", "skills"]
        missing = [s for s in required_sections if not resume_data.get(s)]
        
        if missing:
            score -= len(missing)
            breakdown["issues"].append(f"Missing sections: {', '.join(missing)}")
        
        breakdown["score"] = max(score, 0)
        return max(score, 0)
    
    def _analyze_keywords_detailed(self, resume_data: Dict) -> Dict:
        """Detailed keyword analysis"""
        all_text = " ".join([
            resume_data.get("summary", ""),
            " ".join([exp.get("description", "") for exp in resume_data.get("experience", [])]),
            " ".join(resume_data.get("skills", []))
        ]).lower()
        
        keyword_matches = {}
        total_matches = 0
        
        for industry, categories in self.industry_keywords.items():
            matches = {}
            for category, keywords in categories.items():
                found = [kw for kw in keywords if kw in all_text]
                if found:
                    matches[category] = found
                    total_matches += len(found)
            if matches:
                keyword_matches[industry] = matches
        
        return {
            "total_keywords_found": total_matches,
            "industry_matches": keyword_matches,
            "keyword_density": "good" if total_matches >= 10 else "needs_improvement"
        }
    
    def _analyze_action_verbs(self, resume_data: Dict) -> Dict:
        """Analyze action verb usage"""
        experiences = resume_data.get("experience", [])
        all_exp_text = " ".join([exp.get("description", "") for exp in experiences]).lower()
        
        verb_usage = {}
        total_verbs = 0
        
        for category, verbs in self.action_verbs.items():
            found = [v for v in verbs if v in all_exp_text]
            if found:
                verb_usage[category] = found
                total_verbs += len(found)
        
        return {
            "total_action_verbs": total_verbs,
            "by_category": verb_usage,
            "strength": "strong" if total_verbs >= 5 else "weak" if total_verbs >= 2 else "very_weak"
        }
    
    def _analyze_quantification(self, resume_data: Dict) -> Dict:
        """Analyze quantification of achievements"""
        experiences = resume_data.get("experience", [])
        
        total_bullets = len(experiences)
        quantified = sum(1 for exp in experiences if any(char.isdigit() for char in exp.get("description", "")))
        
        percentage = (quantified / total_bullets * 100) if total_bullets > 0 else 0
        
        return {
            "total_experience_items": total_bullets,
            "quantified_items": quantified,
            "quantification_rate": round(percentage, 1),
            "rating": "excellent" if percentage >= 70 else "good" if percentage >= 40 else "needs_improvement"
        }
    
    def _generate_strengths(self, analysis: Dict) -> List[str]:
        """Generate list of strengths"""
        strengths = []
        
        if analysis["overall_score"] >= 80:
            strengths.append("Excellent overall ATS score")
        
        breakdown = analysis["breakdown"]
        if breakdown["contact_info"]["score"] >= 12:
            strengths.append("Complete contact information")
        
        if breakdown["experience"]["score"] >= 20:
            strengths.append("Strong work experience section")
        
        if analysis["quantification_analysis"]["quantification_rate"] >= 50:
            strengths.append("Good use of quantifiable achievements")
        
        if analysis["action_verb_analysis"]["total_action_verbs"] >= 5:
            strengths.append("Strong action verbs throughout")
        
        if analysis["keyword_analysis"]["total_keywords_found"] >= 10:
            strengths.append("Good keyword optimization")
        
        return strengths if strengths else ["Resume has potential for improvement"]
    
    def _generate_improvements(self, analysis: Dict) -> List[str]:
        """Generate list of improvements"""
        improvements = []
        
        # Collect all issues from breakdown
        for section, data in analysis["breakdown"].items():
            improvements.extend(data.get("issues", []))
        
        # Add specific recommendations
        if analysis["quantification_analysis"]["quantification_rate"] < 40:
            improvements.append("Add numbers and metrics to quantify your achievements")
        
        if analysis["action_verb_analysis"]["strength"] == "weak":
            improvements.append("Use more strong action verbs (led, achieved, improved, etc.)")
        
        if analysis["keyword_analysis"]["total_keywords_found"] < 8:
            improvements.append("Include more industry-specific keywords")
        
        return improvements if improvements else ["Resume looks good! Minor tweaks can make it even better"]
    
    async def _get_ai_suggestions(self, resume_data: Dict, analysis: Dict) -> Optional[Dict]:
        """Get AI-powered suggestions"""
        if not self.openai_api_key:
            return None
        
        try:
            prompt = f"""Analyze this resume and provide 3-5 specific, actionable improvements.

Current ATS Score: {analysis['overall_score']}/100

Resume Summary: {resume_data.get('summary', 'Not provided')}
Experience Count: {len(resume_data.get('experience', []))}
Skills: {', '.join(resume_data.get('skills', [])[:5])}

Provide suggestions in JSON format:
{{
  "top_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"],
  "keyword_recommendations": ["keyword1", "keyword2", "keyword3"],
  "summary_rewrite": "improved summary text"
}}"""

            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are an expert resume writer and ATS optimization specialist."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7,
                "response_format": {"type": "json_object"}
            }
            
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(self.openai_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                return json.loads(content)
                
        except Exception as e:
            logger.error(f"AI suggestions error: {e}")
            return None


# Global instance
_enhanced_analyzer = None

def get_enhanced_analyzer(openai_api_key: str = None) -> EnhancedResumeAnalyzer:
    """Get or create global enhanced analyzer"""
    global _enhanced_analyzer
    if _enhanced_analyzer is None:
        _enhanced_analyzer = EnhancedResumeAnalyzer(openai_api_key)
    return _enhanced_analyzer
