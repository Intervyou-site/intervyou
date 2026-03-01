# resume_analyzer.py
"""
Resume/CV Analysis and Generation Module
Provides AI-powered resume analysis with feedback and MNC-standard resume generation
"""

import os
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import PyPDF2
import docx
from io import BytesIO

# Try to import AI utilities
try:
    from huggingface_utils import evaluate_answer_comprehensive
    HF_AVAILABLE = True
except:
    HF_AVAILABLE = False

# Resume analysis criteria based on MNC standards
RESUME_CRITERIA = {
    "format": {
        "weight": 0.15,
        "checks": [
            "clear_sections",
            "consistent_formatting",
            "professional_font",
            "appropriate_length",
            "proper_margins"
        ]
    },
    "content": {
        "weight": 0.35,
        "checks": [
            "quantifiable_achievements",
            "action_verbs",
            "relevant_keywords",
            "clear_impact",
            "no_jargon"
        ]
    },
    "structure": {
        "weight": 0.20,
        "checks": [
            "contact_info",
            "professional_summary",
            "work_experience",
            "education",
            "skills_section"
        ]
    },
    "language": {
        "weight": 0.15,
        "checks": [
            "grammar_correct",
            "concise_writing",
            "active_voice",
            "no_typos",
            "professional_tone"
        ]
    },
    "relevance": {
        "weight": 0.15,
        "checks": [
            "tailored_content",
            "recent_experience",
            "relevant_skills",
            "industry_alignment"
        ]
    }
}

# MNC-standard resume sections
MNC_RESUME_SECTIONS = [
    "Contact Information",
    "Professional Summary",
    "Core Competencies",
    "Professional Experience",
    "Education",
    "Certifications",
    "Technical Skills",
    "Projects (Optional)",
    "Awards & Recognition (Optional)"
]

# Action verbs for resume writing
ACTION_VERBS = [
    "Achieved", "Accelerated", "Accomplished", "Analyzed", "Architected",
    "Built", "Collaborated", "Created", "Delivered", "Designed",
    "Developed", "Drove", "Enhanced", "Established", "Executed",
    "Generated", "Implemented", "Improved", "Increased", "Initiated",
    "Launched", "Led", "Managed", "Optimized", "Orchestrated",
    "Pioneered", "Reduced", "Resolved", "Spearheaded", "Streamlined",
    "Transformed", "Upgraded"
]


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(BytesIO(file_bytes))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")


def extract_resume_text(file_bytes: bytes, filename: str) -> str:
    """Extract text from resume file (PDF or DOCX)"""
    ext = filename.lower().split('.')[-1]
    
    if ext == 'pdf':
        return extract_text_from_pdf(file_bytes)
    elif ext in ['docx', 'doc']:
        return extract_text_from_docx(file_bytes)
    elif ext == 'txt':
        return file_bytes.decode('utf-8')
    else:
        raise ValueError(f"Unsupported file format: {ext}. Please upload PDF, DOCX, or TXT.")


def analyze_resume_structure(text: str) -> Dict[str, Any]:
    """Analyze resume structure and identify sections"""
    sections_found = {}
    text_lower = text.lower()
    
    # Common section headers
    section_patterns = {
        "contact": r"(contact|email|phone|address)",
        "summary": r"(summary|objective|profile|about)",
        "experience": r"(experience|employment|work history)",
        "education": r"(education|academic|qualification)",
        "skills": r"(skills|competencies|expertise|technical)",
        "projects": r"(projects|portfolio)",
        "certifications": r"(certification|certificate|license)",
        "awards": r"(awards|achievement|recognition|honor)"
    }
    
    for section, pattern in section_patterns.items():
        if re.search(pattern, text_lower):
            sections_found[section] = True
        else:
            sections_found[section] = False
    
    return sections_found


def check_action_verbs(text: str) -> Dict[str, Any]:
    """Check for strong action verbs in resume"""
    found_verbs = []
    text_words = text.split()
    
    for verb in ACTION_VERBS:
        if verb.lower() in text.lower():
            found_verbs.append(verb)
    
    return {
        "count": len(found_verbs),
        "verbs": found_verbs[:10],  # Return first 10
        "score": min(len(found_verbs) / 10, 1.0)  # Max score at 10+ verbs
    }


def check_quantifiable_achievements(text: str) -> Dict[str, Any]:
    """Check for quantifiable achievements (numbers, percentages)"""
    # Patterns for numbers and percentages
    number_pattern = r'\d+[%$]?|\d+[.,]\d+[%$]?'
    matches = re.findall(number_pattern, text)
    
    # Look for achievement indicators
    achievement_keywords = [
        'increased', 'decreased', 'improved', 'reduced', 'generated',
        'saved', 'achieved', 'exceeded', 'delivered', 'grew'
    ]
    
    achievement_count = sum(1 for keyword in achievement_keywords if keyword in text.lower())
    
    return {
        "numbers_found": len(matches),
        "achievement_indicators": achievement_count,
        "score": min((len(matches) + achievement_count) / 15, 1.0)
    }


def analyze_resume_content(text: str) -> Dict[str, Any]:
    """Comprehensive resume content analysis"""
    
    # Structure analysis
    structure = analyze_resume_structure(text)
    structure_score = sum(structure.values()) / len(structure)
    
    # Action verbs analysis
    action_verbs = check_action_verbs(text)
    
    # Quantifiable achievements
    achievements = check_quantifiable_achievements(text)
    
    # Length analysis
    word_count = len(text.split())
    length_score = 1.0 if 300 <= word_count <= 800 else 0.7 if word_count < 300 else 0.8
    
    # Calculate overall scores
    format_score = structure_score * 0.7 + length_score * 0.3
    content_score = (action_verbs["score"] * 0.5 + achievements["score"] * 0.5)
    
    return {
        "structure": structure,
        "structure_score": structure_score,
        "action_verbs": action_verbs,
        "achievements": achievements,
        "word_count": word_count,
        "length_score": length_score,
        "format_score": format_score,
        "content_score": content_score,
        "overall_score": (format_score * 0.4 + content_score * 0.6)
    }


def generate_feedback(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate actionable feedback based on analysis"""
    feedback = []
    
    # Structure feedback
    structure = analysis["structure"]
    if not structure.get("summary"):
        feedback.append({
            "type": "critical",
            "category": "Structure",
            "message": "Add a Professional Summary at the top highlighting your key strengths and career goals.",
            "priority": "high"
        })
    
    if not structure.get("experience"):
        feedback.append({
            "type": "critical",
            "category": "Structure",
            "message": "Include a Work Experience section with your professional history.",
            "priority": "high"
        })
    
    if not structure.get("skills"):
        feedback.append({
            "type": "warning",
            "category": "Structure",
            "message": "Add a Skills section to highlight your technical and soft skills.",
            "priority": "medium"
        })
    
    # Content feedback
    if analysis["action_verbs"]["count"] < 5:
        feedback.append({
            "type": "warning",
            "category": "Content",
            "message": f"Use more action verbs (found {analysis['action_verbs']['count']}). Examples: {', '.join(ACTION_VERBS[:5])}",
            "priority": "medium"
        })
    
    if analysis["achievements"]["numbers_found"] < 3:
        feedback.append({
            "type": "warning",
            "category": "Content",
            "message": "Add quantifiable achievements with numbers and percentages (e.g., 'Increased sales by 25%').",
            "priority": "high"
        })
    
    # Length feedback
    word_count = analysis["word_count"]
    if word_count < 300:
        feedback.append({
            "type": "info",
            "category": "Format",
            "message": f"Resume is too short ({word_count} words). Aim for 300-800 words with detailed achievements.",
            "priority": "medium"
        })
    elif word_count > 800:
        feedback.append({
            "type": "info",
            "category": "Format",
            "message": f"Resume is lengthy ({word_count} words). Consider condensing to 300-800 words for better readability.",
            "priority": "low"
        })
    
    # Positive feedback
    if analysis["overall_score"] > 0.7:
        feedback.append({
            "type": "success",
            "category": "Overall",
            "message": "Great job! Your resume follows many MNC standards.",
            "priority": "info"
        })
    
    return feedback


def generate_mnc_resume_template(user_data: Dict[str, Any]) -> str:
    """Generate MNC-standard resume template"""
    
    template = f"""
{user_data.get('name', '[Your Name]').upper()}
{user_data.get('email', '[email@example.com]')} | {user_data.get('phone', '[Phone]')} | {user_data.get('location', '[City, Country]')}
LinkedIn: {user_data.get('linkedin', '[linkedin.com/in/yourprofile]')} | Portfolio: {user_data.get('portfolio', '[yourportfolio.com]')}

PROFESSIONAL SUMMARY
{user_data.get('summary', '[3-4 lines highlighting your expertise, years of experience, key skills, and career objectives. Focus on value you bring to employers.]')}

CORE COMPETENCIES
{user_data.get('skills', '• [Skill 1] • [Skill 2] • [Skill 3] • [Skill 4] • [Skill 5]')}

PROFESSIONAL EXPERIENCE

{user_data.get('company1', '[Company Name]')} | {user_data.get('location1', '[City, Country]')}
{user_data.get('title1', '[Job Title]')} | {user_data.get('dates1', '[Month Year - Present]')}
• {user_data.get('achievement1_1', '[Action verb] + [what you did] + [quantifiable result]. Example: Increased team productivity by 30% through implementation of agile methodologies.')}
• {user_data.get('achievement1_2', '[Another achievement with numbers and impact]')}
• {user_data.get('achievement1_3', '[Third achievement demonstrating leadership or technical skills]')}

{user_data.get('company2', '[Previous Company]')} | {user_data.get('location2', '[City, Country]')}
{user_data.get('title2', '[Previous Job Title]')} | {user_data.get('dates2', '[Month Year - Month Year]')}
• {user_data.get('achievement2_1', '[Achievement with measurable impact]')}
• {user_data.get('achievement2_2', '[Another key accomplishment]')}

EDUCATION

{user_data.get('degree', '[Degree Name]')} in {user_data.get('major', '[Major]')}
{user_data.get('university', '[University Name]')}, {user_data.get('grad_year', '[Graduation Year]')}
{user_data.get('gpa', 'GPA: [X.XX/4.0]' if user_data.get('gpa') else '')}

CERTIFICATIONS
{user_data.get('certifications', '• [Certification Name] - [Issuing Organization], [Year]')}

TECHNICAL SKILLS
{user_data.get('technical_skills', '• Programming: [Languages]' + chr(10) + '• Frameworks: [Frameworks]' + chr(10) + '• Tools: [Tools]' + chr(10) + '• Databases: [Databases]')}

PROJECTS (Optional)
{user_data.get('project1', '[Project Name]')} | {user_data.get('project_tech1', '[Technologies Used]')}
• {user_data.get('project_desc1', '[Brief description of project and your role with quantifiable outcomes]')}

AWARDS & RECOGNITION (Optional)
{user_data.get('awards', '• [Award Name] - [Organization], [Year]')}
"""
    
    return template.strip()


def analyze_resume_with_ai(text: str) -> Dict[str, Any]:
    """Use AI to provide advanced resume analysis"""
    if not HF_AVAILABLE:
        return {"ai_available": False}
    
    try:
        # Create a prompt for AI analysis
        prompt = f"""Analyze this resume and provide professional feedback:

{text[:2000]}  # Limit text length

Evaluate:
1. Professional tone and language
2. Achievement clarity and impact
3. Industry relevance
4. Areas for improvement

Provide concise, actionable feedback."""
        
        # Use existing AI evaluation (if available)
        ai_feedback = evaluate_answer_comprehensive(
            question=prompt,
            answer=text[:1000],
            category="Professional"
        )
        
        return {
            "ai_available": True,
            "ai_feedback": ai_feedback
        }
    except Exception as e:
        return {"ai_available": False, "error": str(e)}


def analyze_resume_full(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Complete resume analysis pipeline"""
    try:
        # Extract text
        text = extract_resume_text(file_bytes, filename)
        
        if not text or len(text) < 50:
            raise ValueError("Resume text is too short or empty. Please upload a valid resume.")
        
        # Perform analysis
        analysis = analyze_resume_content(text)
        feedback = generate_feedback(analysis)
        
        # AI analysis (optional)
        ai_analysis = analyze_resume_with_ai(text)
        
        # Calculate grade
        score = analysis["overall_score"]
        if score >= 0.9:
            grade = "A+"
        elif score >= 0.8:
            grade = "A"
        elif score >= 0.7:
            grade = "B+"
        elif score >= 0.6:
            grade = "B"
        elif score >= 0.5:
            grade = "C"
        else:
            grade = "D"
        
        return {
            "success": True,
            "text_preview": text[:500],
            "word_count": analysis["word_count"],
            "overall_score": round(score * 100, 1),
            "grade": grade,
            "scores": {
                "format": round(analysis["format_score"] * 100, 1),
                "content": round(analysis["content_score"] * 100, 1),
                "structure": round(analysis["structure_score"] * 100, 1)
            },
            "structure": analysis["structure"],
            "action_verbs": analysis["action_verbs"],
            "achievements": analysis["achievements"],
            "feedback": feedback,
            "ai_analysis": ai_analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
